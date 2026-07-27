from fastmcp import FastMCP
import sqlite3
import os




DB_Path = os.path.join(os.path.dirname(__file__),'expenses.db')

CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")


mcp = FastMCP(name = "Expense-Tracker")

def init_db():
    """
    this function creates table if not exist
    """

    with sqlite3.connect(database=DB_Path) as c:
        c.execute(
            """
        CREATE TABLE IF NOT EXISTS expenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        subcategory TEXT DEFAULT '',
        note TEXT DEFAULT ''
        )            
"""
        )

init_db()


@mcp.tool()
def add_expenses(date, amount, category, subcategory= "", note=""):
    """
        this function adds a new expense entry to the database
    """

    with sqlite3.connect(DB_Path) as c:
        curr = c.execute(
            "INSERT INTO expenses (date, amount, category, subcategory, note) VALUES (?,?,?,?,?)",
            (date, amount, category, subcategory, note)
        )

        c.commit()

        return {"status": "OK", "id": curr.lastrowid}


@mcp.tool()
def list_expenses(start_date, end_date):

    """
    This Function returns dict of expenses in a given date
    """
    with sqlite3.connect(DB_Path) as c:
            curr = c.execute(
                """SELECT id, date, amount, category, subcategory, note FROM expenses 
                 WHERE date BETWEEN ? AND ?
                 ORDER BY id ASC""",
                 (start_date, end_date)
            )

            cols = [d[0] for d in curr.description]
            return [dict(zip(cols, r)) for r in curr.fetchall()]


@mcp.tool()
def summarize(start_date, end_date, category=None):
    '''Summarize expenses by category within an inclusive date range.'''
    with sqlite3.connect(DB_Path) as c:
        query = (
            """
            SELECT category, SUM(amount) AS total_amount
            FROM expenses
            WHERE date BETWEEN ? AND ?
            """
        )
        params = [start_date, end_date]

        if category:
            query += " AND category = ?"
            params.append(category)

        query += " GROUP BY category ORDER BY category ASC"

        cur = c.execute(query, params)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]



@mcp.tool()
def get_expense(expense_id: int):
    """
    Return a single expense by its ID.
    """

    with sqlite3.connect(DB_Path) as c:
        cur = c.execute(
            """
            SELECT id, date, amount, category, subcategory, note
            FROM expenses
            WHERE id = ?
            """,
            (expense_id,)
        )

        row = cur.fetchone()

        if row is None:
            return {"status": "ERROR", "message": "Expense not found"}

        cols = [d[0] for d in cur.description]

        return dict(zip(cols, row))



@mcp.tool()
def delete_expense(expense_id: int):
    """
    Delete an expense by its ID.
    """

    with sqlite3.connect(DB_Path) as c:
        cur = c.execute(
            """
            DELETE FROM expenses
            WHERE id = ?
            """,
            (expense_id,)
        )

        c.commit()

        if cur.rowcount == 0:
            return {"status": "ERROR", "message": "Expense not found"}

        return {"status": "OK", "deleted_id": expense_id}




@mcp.tool()
def update_expense(
    expense_id: int,
    date: str = None,
    amount: float = None,
    category: str = None,
    subcategory: str = None,
    note: str = None
):
    """
    Update any fields of an existing expense.
    """

    updates = []
    values = []

    if date is not None:
        updates.append("date = ?")
        values.append(date)

    if amount is not None:
        updates.append("amount = ?")
        values.append(amount)

    if category is not None:
        updates.append("category = ?")
        values.append(category)

    if subcategory is not None:
        updates.append("subcategory = ?")
        values.append(subcategory)

    if note is not None:
        updates.append("note = ?")
        values.append(note)

    if not updates:
        return {"status": "ERROR", "message": "Nothing to update"}

    values.append(expense_id)

    with sqlite3.connect(DB_Path) as c:

        cur = c.execute(
            f"""
            UPDATE expenses
            SET {', '.join(updates)}
            WHERE id = ?
            """,
            values
        )

        c.commit()

        if cur.rowcount == 0:
            return {"status": "ERROR", "message": "Expense not found"}

        return {"status": "OK", "updated_id": expense_id}



@mcp.tool()
def search_by_category(category: str):
    """
    Return all expenses for a category.
    """

    with sqlite3.connect(DB_Path) as c:

        cur = c.execute(
            """
            SELECT id, date, amount, category, subcategory, note
            FROM expenses
            WHERE category = ?
            ORDER BY date ASC
            """,
            (category,)
        )

        cols = [d[0] for d in cur.description]

        return [dict(zip(cols, r)) for r in cur.fetchall()]


@mcp.tool()
def search_note(keyword: str):
    """
    Search expenses whose notes contain a keyword.
    """

    with sqlite3.connect(DB_Path) as c:

        cur = c.execute(
            """
            SELECT id, date, amount, category, subcategory, note
            FROM expenses
            WHERE note LIKE ?
            ORDER BY date ASC
            """,
            (f"%{keyword}%",)
        )

        cols = [d[0] for d in cur.description]

        return [dict(zip(cols, r)) for r in cur.fetchall()]


@mcp.tool()
def total_spending(start_date: str, end_date: str):
    """
    Return total spending within a date range.
    """

    with sqlite3.connect(DB_Path) as c:

        cur = c.execute(
            """
            SELECT SUM(amount)
            FROM expenses
            WHERE date BETWEEN ? AND ?
            """,
            (start_date, end_date)
        )

        total = cur.fetchone()[0] or 0

        return {
            "start_date": start_date,
            "end_date": end_date,
            "total_spending": total
        }


@mcp.tool()
def largest_expense():
    """
    Return the largest recorded expense.
    """

    with sqlite3.connect(DB_Path) as c:

        cur = c.execute(
            """
            SELECT id, date, amount, category, subcategory, note
            FROM expenses
            ORDER BY amount DESC
            LIMIT 1
            """
        )

        row = cur.fetchone()

        if row is None:
            return {"status": "ERROR", "message": "No expenses found"}

        cols = [d[0] for d in cur.description]

        return dict(zip(cols, row))


@mcp.tool()
def average_expense():
    """
    Return average expense amount.
    """

    with sqlite3.connect(DB_Path) as c:

        cur = c.execute(
            """
            SELECT AVG(amount)
            FROM expenses
            """
        )

        avg = cur.fetchone()[0] or 0

        return {"average_expense": round(avg, 2)}

@mcp.tool()
def expense_count():
    """
    Return total number of expenses.
    """

    with sqlite3.connect(DB_Path) as c:

        cur = c.execute(
            """
            SELECT COUNT(*)
            FROM expenses
            """
        )

        return {"count": cur.fetchone()[0]}


@mcp.tool()
def recent_expenses(limit: int = 5):
    """
    Return the most recently added expenses.
    """

    with sqlite3.connect(DB_Path) as c:

        cur = c.execute(
            """
            SELECT id, date, amount, category, subcategory, note
            FROM expenses
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        )

        cols = [d[0] for d in cur.description]

        return [dict(zip(cols, r)) for r in cur.fetchall()]

@mcp.resource("expense://categories", mime_type="application/json")
def categories():
    # Read fresh each time so you can edit the file without restarting
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        return f.read()
    
if __name__ == '__main__':
    mcp.run()