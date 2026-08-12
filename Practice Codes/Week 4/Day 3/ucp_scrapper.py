import os
import re
import json
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

class UCPPortalScraper:
    """
    A robust, stateful API wrapper for the UCP Student Portal.
    
    This class automatically handles session management, Microsoft Single Sign-On (SSO) authentication 
    via Playwright, and fast data extraction using Python `requests` and `BeautifulSoup`.
    
    Attributes:
        BASE_URL (str): The root URL of the UCP portal.
        STATE_FILE (Path): The local file path where session cookies are cached.
        session (requests.Session): The active, authenticated HTTP session.
    """
    
    BASE_URL = "https://horizon.ucp.edu.pk"
    STATE_FILE = Path("portal_session.json")
    
    def __init__(self, headless: bool = True):
        """
        Initializes the scraper and ensures an active, authenticated session exists.
        
        Args:
            headless (bool): If True, Playwright runs in the background. Note that Microsoft SSO 
                             often blocks headless logins, so False is recommended for the initial login.
        """
        self.headless = headless
        self.session = requests.Session()
        self._initialize_session()

    def _login_and_save_session(self):
        """
        Uses Playwright to physically launch a browser, navigate the Microsoft login flow, 
        and save the authenticated cookies to the STATE_FILE.
        """
        #print("[Auth] Logging in via Playwright Microsoft SSO...")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            context = browser.new_context()
            page = context.new_page()

            page.goto(self.BASE_URL)
            page.wait_for_load_state('networkidle')
            
            
            page.locator('text="login With Microsoft"').click()
            page.fill('input[type="email"]', os.environ["UCP_EMAIL"], timeout=60000)
            page.click('input[type="submit"]')
            
            page.fill('input[type="password"]', os.environ["UCP_PASSWORD"], timeout=60000)
            page.click('input[type="submit"]')
            
            # Handle "Stay signed in?" prompt
            try:
                page.locator('text="No"').click(timeout=3000)
            except Exception:
                pass
                
            page.wait_for_load_state('networkidle')
            page.wait_for_timeout(2000)  # Ensure Odoo backend cookies finalize

            context.storage_state(path=str(self.STATE_FILE))
            #print("[Auth] Successfully logged in and saved session.")
            browser.close()

    def _initialize_session(self):
        """
        Loads the cached session from disk and injects it into the requests Session.
        If no cache exists, it triggers a Playwright login.
        """
        if not self.STATE_FILE.exists():
            self._login_and_save_session()
            if not self.STATE_FILE.exists():
                raise Exception("Critical: Failed to generate session state file.")

        with open(self.STATE_FILE, 'r') as f:
            state = json.load(f)

        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        })
        
        for cookie in state.get('cookies', []):
            self.session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])

    def _request(self, endpoint: str, stream: bool = False, _is_retry: bool = False) -> requests.Response:
        """
        A robust wrapper around requests.get() that automatically detects expired sessions,
        silently re-authenticates, and retries the exact request.
        
        Args:
            endpoint (str): The URL endpoint (e.g., '/student/dashboard')
            stream (bool): Set to True for downloading files.
            _is_retry (bool): Internal flag to prevent infinite authentication loops.
            
        Returns:
            requests.Response: The HTTP response object.
        """
        url = f"{self.BASE_URL}{endpoint}" if endpoint.startswith('/') else endpoint
        response = self.session.get(url, stream=stream)
        
        # Odoo redirects unauthenticated users to the login page
        if "login" in response.url.lower():
            if _is_retry:
                raise Exception(f"Authentication loop detected. Failed to access {url}")
                
            print(f"[Auth] Session expired while accessing {endpoint}. Re-authenticating...")
            if self.STATE_FILE.exists():
                self.STATE_FILE.unlink()
                
            self._initialize_session()
            return self._request(endpoint, stream=stream, _is_retry=True)
            
        return response

    # ==========================================
    # PUBLIC API METHODS
    # ==========================================

    def get_dashboard(self) -> dict:
        """
        Scrapes the main student dashboard.
        
        Returns:
            dict: {
                "name": str,
                "roll_no": str,
                "department": str,
                "cgpa": str,
                "earned_cr": str,
                "total_cr": str,
                "inprogress_cr": str,
                "scholarships": list[str],
                "today_classes": list[str],
                "courses": list[dict(name, url)]
            }
        """
      #  print("[API] Fetching Dashboard...")
        response = self._request("/student/dashboard")
        soup = BeautifulSoup(response.text, 'html.parser')
        raw = soup.get_text(separator='\n', strip=True)
        
        profile = {}
        
        name_match = re.search(r'([A-Z][a-z]+(?: [A-Z][a-z]+){1,4})\s*\n\s*(L\d[A-Z]\d{2}[A-Z]+\d+)', raw)
        if name_match:
            profile["name"]    = name_match.group(1).strip()
            profile["roll_no"] = name_match.group(2).strip()

        dept_match = re.search(r'(Faculty of [A-Za-z ]+(?:and [A-Za-z ]+)?)', raw)
        if dept_match:
            profile["department"] = dept_match.group(1).strip()

        cgpa_match = re.search(r'CGPA\s*[:\-]?\s*([\d.]+)', raw)
        if cgpa_match: profile["cgpa"] = cgpa_match.group(1)

        earned_match     = re.search(r'Earned Cr\s*[:\-]?\s*([\d.]+)', raw)
        total_match      = re.search(r'Total Cr\s*[:\-]?\s*([\d.]+)', raw)
        inprogress_match = re.search(r'Inprogress Cr\s*[:\-]?\s*([\d.]+)', raw)
        
        if earned_match:     profile["earned_cr"]     = earned_match.group(1)
        if total_match:      profile["total_cr"]      = total_match.group(1)
        if inprogress_match: profile["inprogress_cr"] = inprogress_match.group(1)

        badges = []
        for badge in soup.select('.uk-badge, .uk-label, .badge, .label, span.label-success, span.label-info, span.bg-success'):
            text = badge.get_text(strip=True)
            if text and 2 < len(text) < 40 and not text.isdigit():
                badges.append(text)
        profile["scholarships"] = list(set(badges))

        today_classes = []
        today_section = re.search(r"Today Classes\s*:(.*?)(?:\n\n|\Z)", raw, re.DOTALL)
        if today_section:
            today_raw = today_section.group(1).strip()
            if "No class" not in today_raw and today_raw:
                today_classes = [line.strip() for line in today_raw.splitlines() if line.strip()]
        profile["today_classes"] = today_classes

        courses = []
        for link in soup.select('a[href^="/student/course/info/"]'):
            name_span = link.select_one('.card-header span')
            if name_span:
                courses.append({
                    "name": name_span.get_text(strip=True),
                    "url": f"{self.BASE_URL}{link.get('href')}"
                })

        return {"profile": profile, "courses": courses}

    def get_profile(self) -> dict:
        """
        Scrapes the detailed /student/profile page (ABOUT and BIO DATA tabs).
        
        Returns:
            dict: Demographic data like dob, gender, blood_group, nationality, religion, 
                  contact information, and family details (father/guardian names and CNICs).
        """
       # print("[API] Fetching Detailed Profile...")
        response = self._request("/student/profile")
        soup = BeautifulSoup(response.text, 'html.parser')
        p_raw = soup.get_text(separator='\n', strip=True)
        
        profile = {}

        # Fallback regex for standard text fields
        email_match = re.search(r'([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})', p_raw)
        if email_match: profile["email"] = email_match.group(1)

        phone_match = re.search(r'\b(03\d{9})\b', p_raw)
        if phone_match: profile["phone"] = phone_match.group(1)

        lines = [line.strip() for line in p_raw.splitlines() if line.strip()]
        for i, line in enumerate(lines):
            if i == 0: continue
            val = lines[i-1]
            if "Career" in line: profile["career"] = val
            elif "Program" in line and len(line) < 15: profile["program"] = val
            elif "Current Semester" in line: profile["current_semester"] = val

        # Robust DOM extraction for all UIKit list properties
        for content in soup.find_all('div', class_='md-list-content'):
            label_span = content.find('span', class_='uk-text-muted')
            if not label_span: continue
                
            raw_label = label_span.get_text(separator=' ', strip=True)
            label = ' '.join(raw_label.split()).lower()
            
            label_span.extract()
            for inp in content.find_all('input'):
                inp.extract()
                
            value = content.get_text(separator=', ', strip=True).strip(', ')
            if not value or value == '-': 
                continue
                
            if "email" in label: profile["email"] = value
            elif "phone" in label: profile["phone"] = value
            elif "emergency contact" in label: profile["emergency_contact"] = value
            elif "present address" in label: profile["present_address"] = value
            elif "permanent address" in label: profile["permanent_address"] = value
            elif "date of birth" in label: profile["dob"] = value
            elif "gender" in label: profile["gender"] = value
            elif "cnic" in label and "father" not in label and "guardian" not in label: 
                if "cnic" not in profile: profile["cnic"] = value
            elif "domicile" in label: profile["domicile"] = value
            elif "nationlity" in label or "nationality" in label: profile["nationality"] = value
            elif "religion" in label: profile["religion"] = value
            elif "blood group" in label: profile["blood_group"] = value
            elif "father name" in label: profile["father_name"] = value
            elif "father cnic" in label: profile["father_cnic"] = value
            elif "guardian name" in label: profile["guardian_name"] = value
            elif "guardian cnic" in label: profile["guardian_cnic"] = value
            elif "marital status" in label: profile["marital_status"] = value

        return profile

    def get_grades(self) -> list:
        """
        Scrapes the student's result/grade history.
        
        Returns:
            list[dict]: A list of semesters, each containing SGPA, CGPA, earned_ch, 
                        and a list of specific courses with their credit hours and grades.
        """
        print("[API] Fetching Grades...")
        response = self._request("/student/results")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        current_term = None
        
        for row in soup.select('tr.table-parent-row, tr.table-child-row'):
            row_classes = row.get('class', [])
            cells = row.find_all('td')
            
            if 'table-parent-row' in row_classes and len(cells) >= 8:
                current_term = {
                    "term": cells[0].get_text(strip=True),
                    "grade_points": cells[1].get_text(strip=True),
                    "cumulative_gp": cells[2].get_text(strip=True),
                    "attempted_ch": cells[3].get_text(strip=True),
                    "earned_ch": cells[4].get_text(strip=True),
                    "cumulative_ch": cells[5].get_text(strip=True),
                    "sgpa": cells[6].get_text(strip=True),
                    "cgpa": cells[7].get_text(strip=True),
                    "courses": [],
                }
                results.append(current_term)

            elif 'table-child-row' in row_classes and current_term is not None and len(cells) >= 4:
                current_term["courses"].append({
                    "course": cells[0].get_text(strip=True),
                    "credit_hours": cells[1].get_text(strip=True),
                    "grade_pts": cells[2].get_text(strip=True),
                    "final_grade": cells[3].get_text(strip=True),
                })
                
        return results

    def get_timetable(self) -> dict:
        """
        Scrapes the student's weekly timetable.
        
        Returns:
            dict: Keys are days of the week (e.g., 'Monday'). Values are lists of class dicts 
                  containing start, end, teacher, subject, course_code, and room.
        """
       # print("[API] Fetching Timetable...")
        response = self._request("/student/class/schedule")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        schedule = {}
        for group in soup.select('li.cd-schedule__group'):
            day_span = group.select_one('.cd-schedule__top-info span')
            if not day_span: continue
            day_name = day_span.get_text(strip=True)
            
            day_classes = []
            for event in group.select('li.cd-schedule__event'):
                link = event.select_one('a')
                if not link: continue
                    
                spans = [s.get_text(strip=True) for s in link.select('span')]
                em_tag = link.select_one('em')
                
                day_classes.append({
                    "start": link.get('data-start', ''),
                    "end": link.get('data-end', ''),
                    "teacher": em_tag.get_text(strip=True) if em_tag else "",
                    "subject": spans[0] if len(spans) > 0 else "",
                    "course_code": spans[1] if len(spans) > 1 else "",
                    "room": spans[2] if len(spans) > 2 else "",
                })
            schedule[day_name] = day_classes
            
        return schedule

    def get_notifications(self) -> list:
        """
        Scrapes the student's notifications.
        
        Returns:
            list[dict]: A list of notifications, or an empty list if there are none.
        """
       # print("[API] Fetching Notifications...")
        response = self._request("/student/notifications")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        notifications = []
        
        # Try to find standard list items or notification cards
        alerts = soup.select('.alert, .notification, .md-list-item, ul.md-list > li')
        if alerts:
            for alert in alerts:
                text = alert.get_text(separator=' ', strip=True)
                if text and "No notifications" not in text:
                    notifications.append({"message": text})
            return notifications
            
        # Fallback: Check the main page content block
        content = soup.select_one('#page_content_inner')
        if content:
            text = content.get_text(separator=' ', strip=True)
            if "No notifications" in text:
                return []
            if text:
                return [{"message": text}]
                
        return notifications

    def get_invoices(self) -> list:
        """
        Scrapes the student's invoice and challan history.
        
        Returns:
            list[dict]: A list of invoices containing details like Due Date, 
                        Payable Amount, Status, Challan ID, and Paid Date.
        """
        print("[API] Fetching Invoices...")
        response = self._request("/student/invoices")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # The invoices are displayed in a standard table
        table = soup.select_one('table')
        if table:
            return self._parse_table(table)
        return []

    def get_datesheet(self) -> list:
        """
        Scrapes the student's exam datesheet.
        
        Returns:
            list[dict]: A list of scheduled exams (Class, Teacher, Date, Time, Venue).
        """
        print("[API] Fetching Exam Datesheet...")
        response = self._request("/student/exam/datesheet")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        table = soup.select_one('table')
        if table:
            return self._parse_table(table)
        return []

    def _parse_table(self, table_soup) -> list:
        """Helper method to parse standard UIkit tables."""
        if not table_soup: return []
        headers = [th.get_text(strip=True) for th in table_soup.select('thead th')]
        rows = []
        for tr in table_soup.select('tbody tr'):
            cells = tr.find_all('td')
            if not cells or 'No ' in tr.get_text(strip=True) or len(cells) == 1:
                continue
            row = {}
            for i, header in enumerate(headers):
                if i < len(cells):
                    a_tag = cells[i].find('a', href=True)
                    if a_tag and '/download/' in a_tag.get('href', ''):
                        row[f"{header}_download_url"] = f"{self.BASE_URL}{a_tag['href']}"
                    row[header] = cells[i].get_text(strip=True)
            rows.append(row)
        return rows

    def get_course_details(self, course_url: str) -> dict:
        """
        Scrapes detailed information for a specific course across all its tabs.
        
        Args:
            course_url (str): The absolute URL to the course page.
            
        Returns:
            dict: Contains announcements, outline, materials, assessments, 
                  submissions, gradebook, attendance, and parsed course info.
        """
        course_id = course_url.rstrip('/').split('/')[-1]
        print(f"[API] Fetching Course Details for ID: {course_id}")
        
        result = {}
        
        # Attendance & Course Info extraction
        soup = BeautifulSoup(self._request(f"/student/course/attendance/{course_id}").text, 'html.parser')
        content = soup.select_one('#page_content_inner')
        attendance = {"stats": {}, "records": self._parse_table(soup.select_one('table'))}
        
        if content:
            raw = content.get_text(separator='\n', strip=True)
            code_match = re.search(r'([A-Z]{2,6}\d{2,4}(?:-[A-Z0-9]+){3,5})', raw)
            if code_match: attendance["stats"]["Course Code"] = code_match.group(1)
            
            patterns = {
                "Course": r'Course\s*:\s*\n\s*(.+)',
                "Number of classes Conducted": r'Number of classes Conducted\s*:\s*\n\s*(\d+)',
                "Number of classes Attended": r'Number of classes Attended\s*:\s*\n\s*(\d+)',
                "Academic Term": r'Academic Term\s*:\s*\n\s*(.+)',
                "Attendance Percentage": r'Attendance Percentage\s*[:\s]*\n\s*([\d.]+)',
            }
            for key, pattern in patterns.items():
                m = re.search(pattern, raw)
                if m: attendance["stats"][key] = m.group(1).strip()
                
        result["attendance"] = attendance

        raw_code = attendance.get("stats", {}).get("Course Code", "")
        if raw_code:
            parts = raw_code.strip().split('-')
            info = {"full_code": raw_code}
            if len(parts) >= 1: info["subject_code"] = parts[0]
            if len(parts) >= 2: info["revision"] = parts[1]
            if len(parts) >= 3: info["program"] = parts[2]
            if len(parts) >= 4: info["department"] = parts[3]
            if len(parts) >= 5: info["semester"] = parts[4]
            if len(parts) >= 6: info["section"] = parts[5]
            result["course_info"] = info
        else:
            result["course_info"] = {}

        # Other standard tabs
        tabs = {
            "announcements": f"/student/course/info/{course_id}",
            "assessments": f"/student/course/assessment/{course_id}",
            "submissions": f"/student/course/submission/{course_id}",
        }
        for key, ep in tabs.items():
            soup = BeautifulSoup(self._request(ep).text, 'html.parser')
            result[key] = self._parse_table(soup.select_one('table'))

        # Gradebook
        soup = BeautifulSoup(self._request(f"/student/course/gradebook/{course_id}").text, 'html.parser')
        gradebook = {"summary": [], "details": []}
        tables = soup.select('table')
        if len(tables) >= 1: gradebook["summary"] = self._parse_table(tables[0])
        if len(tables) >= 2: gradebook["details"] = self._parse_table(tables[1])
        result["gradebook"] = gradebook

        # Materials
        soup = BeautifulSoup(self._request(f"/student/course/material/{course_id}").text, 'html.parser')
        materials = []
        for tr in soup.select('tbody tr.table-child-row'):
            cells = tr.find_all('td')
            a_tag = tr.find('a', href=lambda h: h and '/download/' in h)
            if len(cells) >= 2:
                materials.append({
                    "filename": cells[1].get_text(strip=True),
                    "description": cells[2].get_text(strip=True) if len(cells) > 2 else "",
                    "download_url": f"{self.BASE_URL}{a_tag['href']}" if a_tag else None,
                })
        result["materials"] = materials

        # Outline
        soup = BeautifulSoup(self._request(f"/student/course/outline/{course_id}").text, 'html.parser')
        content = soup.select_one('#page_content_inner')
        outline = {"text_books": [], "reference_books": [], "web_resources": [], "assessment_weights": [], "raw_text": ""}
        if content:
            tables = content.select('table')
            if len(tables) >= 1: outline["text_books"] = self._parse_table(tables[0])
            if len(tables) >= 2: outline["reference_books"] = self._parse_table(tables[1])
            if len(tables) >= 3: outline["web_resources"] = self._parse_table(tables[2])
            if len(tables) >= 4: outline["assessment_weights"] = self._parse_table(tables[3])
            outline["raw_text"] = content.get_text(separator='\n', strip=True)
        result["outline"] = outline

        return result

    def download_specific_file(self, download_url: str, filename: str, download_dir: str = "downloads") -> str:
        """
        Downloads a single specific file using its direct download URL.
        
        Args:
            download_url (str): The direct URL to the file (e.g. extracted from get_course_details).
            filename (str): The name to save the file as.
            download_dir (str): The folder to save the file in.
            
        Returns:
            str: The absolute path to the saved file, or None if it failed.
        """
        os.makedirs(download_dir, exist_ok=True)
        safe_filename = filename.replace('/', '_').replace('\\', '_').replace(':', '_')
        filepath = os.path.abspath(os.path.join(download_dir, safe_filename))
        
        print(f"[Download] Fetching specific file: {safe_filename}")
        file_res = self._request(download_url, stream=True)
        
        if file_res.status_code == 200:
            try:
                with open(filepath, 'wb') as f:
                    for chunk in file_res.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"[Download] ✅ Saved: {filepath}")
                return filepath
            except Exception as e:
                print(f"[Download] ❌ Error writing '{safe_filename}': {e}")
                return None
        else:
            print(f"[Download] ❌ Failed to fetch (HTTP {file_res.status_code})")
            return None

    def download_course_files(self, course_url: str, download_dir: str = "downloads", target_filenames: list = None) -> list:
        """
        Scans a course's Material and Submission tabs and downloads attachments.
        
        Args:
            course_url (str): The absolute URL to the course page.
            download_dir (str): Path to the folder where files should be saved.
            target_filenames (list, optional): If provided, only downloads files matching these names.
            
        Returns:
            list[str]: A list of absolute filepaths for successfully downloaded files.
        """
        course_id = course_url.rstrip('/').split('/')[-1]
        os.makedirs(download_dir, exist_ok=True)
        downloaded_paths = []
        
        endpoints = [
            f"/student/course/material/{course_id}",
            f"/student/course/submission/{course_id}"
        ]
        
        for ep in endpoints:
            soup = BeautifulSoup(self._request(ep).text, 'html.parser')
            for link in soup.select('a[href*="/download/"]'):
                href = link.get('href')
                
                # Try to extract a clean filename from the neighboring table cell
                filename = "unknown_file"
                row = link.find_parent('tr')
                if row:
                    for cell in row.find_all('td'):
                        text = cell.get_text(strip=True)
                        if text and '.' in text and not text.isdigit():
                            filename = text
                            break
                            
                # If the user requested specific files, skip if not a match
                if target_filenames and filename not in target_filenames:
                    continue
                    
                safe_filename = filename.replace('/', '_').replace('\\', '_').replace(':', '_')
                filepath = os.path.abspath(os.path.join(download_dir, safe_filename))
                
                print(f"[Download] Fetching: {safe_filename}")
                file_res = self._request(href, stream=True)
                
                if file_res.status_code == 200:
                    try:
                        with open(filepath, 'wb') as f:
                            for chunk in file_res.iter_content(chunk_size=8192):
                                f.write(chunk)
                        downloaded_paths.append(filepath)
                        print(f"[Download] ✅ Saved: {filepath}")
                    except PermissionError:
                        print(f"[Download] ⚠️ Permission denied for '{safe_filename}'.")
                    except Exception as e:
                        print(f"[Download] ❌ Error writing '{safe_filename}': {e}")
                else:
                    print(f"[Download] ❌ Failed to fetch (HTTP {file_res.status_code})")
                    
        return downloaded_paths


if __name__ == "__main__":
    import pprint
    print("=======================================")
    print("    UCP Portal Scraper Initialization  ")
    print("=======================================")
    
    scraper = UCPPortalScraper(headless=False)
    
    print("\n[1] Fetching Dashboard...")
    dash = scraper.get_dashboard()
    
    print("\n[2] Fetching Detailed Profile...")
    prof = scraper.get_profile()
    
    # Merge them for display
    full_profile = dash["profile"].copy()
    full_profile.update(prof)
    
    print("\n--- COMBINED STUDENT PROFILE ---")
    pprint.pprint(full_profile, sort_dicts=False)
    
    print("\n[3] Fetching Timetable...")
    timetable = scraper.get_timetable()
    print(f"Found classes for {len(timetable)} days.")
    
    print("\n[4] Fetching Grades...")
    grades = scraper.get_grades()
    print(f"Found grade records for {len(grades)} semesters.")
    
    print("\n[5] Fetching Invoices...")
    invoices = scraper.get_invoices()
    print(f"Found {len(invoices)} invoices!")
    if invoices:
        pprint.pprint(invoices[0], sort_dicts=False)
    
    print("\n[6] Fetching Notifications...")
    notifications = scraper.get_notifications()
    if notifications:
        print(f"Found {len(notifications)} notifications:")
        for n in notifications:
            print(f"  - {n['message']}")
    else:
        print("No notifications at this time.")

    print("\n[7] Fetching Exam Datesheet...")
    datesheet = scraper.get_datesheet()
    if datesheet:
        print(f"Found {len(datesheet)} scheduled exams:")
        pprint.pprint(datesheet[0], sort_dicts=False)
    else:
        print("No exams scheduled.")
    
    courses = dash.get("courses", [])
    if courses:
        first_course = courses[0]
        print(f"\n[5] Fetching Detailed Data for Course: {first_course['name']}...")
        details = scraper.get_course_details(first_course['url'])
        
        print("\n--- COURSE DETAILS (Attendance, Gradebook, Assessments, Materials) ---")
        # Pretty print the dictionary so you can see exactly what the AI agent will receive
        pprint.pprint(details, sort_dicts=False, depth=3)
        
        print(f"\n[6] Testing Download Function for {first_course['name']}...")
        dl_folder = f"{first_course['name']}_files".replace(" ", "_").replace("/", "_")
        downloaded = scraper.download_course_files(first_course['url'], download_dir=dl_folder)
        if downloaded:
            print(f"Successfully downloaded {len(downloaded)} files to the '{dl_folder}' directory!")
        else:
            print(f"No files were available to download for this course.")
            
    print("\n=======================================")
    print("  ALL API ENDPOINTS TESTED SUCCESSFULLY! ")
    print("=======================================")
