# import requests
# import os
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# API_KEY = os.getenv("YOUTUBE_API_KEY")

# # Video ID
# VIDEO_ID = "bL92ALSZ2Cg"   

# # YouTube Data API Endpoint
# URL = "https://www.googleapis.com/youtube/v3/videos"

# # Query Parameters
# params = {
#     "part": "snippet,statistics",
#     "id": VIDEO_ID,
#     "key": API_KEY
# }

# # Send Request
# response = requests.get(URL, params=params)

# # Check request status
# if response.status_code != 200:
#     print("Request Failed!")
#     print(response.status_code)
#     print(response.text)
#     exit()

# # Convert JSON to Python Dictionary
# data = response.json()

# # Get first video
# video = data["items"][0]

# # Extract Information
# title = video["snippet"]["title"]
# channel = video["snippet"]["channelTitle"]
# description = video["snippet"]["description"]
# published = video["snippet"]["publishedAt"]

# views = video["statistics"]["viewCount"]
# likes = video["statistics"].get("likeCount", "Hidden")
# comments = video["statistics"].get("commentCount", "Disabled")

# thumbnail = video["snippet"]["thumbnails"]["high"]["url"]

# # Print Results
# print("=" * 60)

# print("Title       :", title)
# print("Channel     :", channel)
# print("Published   :", published)

# print()
# print("Views       :", views)
# print("Likes       :", likes)
# print("Comments    :", comments)

# print()
# print("Thumbnail   :", thumbnail)

# print()
# print("Description:")
# print(description)

# print("=" * 60)


import requests
import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq



load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

VIDEO_ID = "bL92ALSZ2Cg"

URL = "https://www.googleapis.com/youtube/v3/commentThreads"

params = {
    "part": "snippet",
    "videoId": VIDEO_ID,
    "maxResults": 100,      # maximum comments to fetch
    "textFormat": "plainText",
    "key": API_KEY
}

response = requests.get(URL, params=params)

if response.status_code != 200:
    print(response.status_code)
    print(response.text)
    exit()

data = response.json()

for i, item in enumerate(data["items"], start=1):

    comment = item["snippet"]["topLevelComment"]["snippet"]

    print("="*60)
    print(f"Comment #{i}")
    print("Author :", comment["authorDisplayName"])
    print("Likes  :", comment["likeCount"])
    print("Date   :", comment["publishedAt"])
    print("Comment:", comment["textDisplay"])
    print()

documents = []

for item in data["items"]:

    comment = item["snippet"]["topLevelComment"]["snippet"]

    doc = Document(
        page_content=comment["textDisplay"],
        metadata={
            "author": comment["authorDisplayName"],
            "likes": comment["likeCount"],
            "published_at": comment["publishedAt"],
            "video_id": VIDEO_ID
        }
    )

    documents.append(doc)





analysis_prompt = PromptTemplate(
    template="""
You are an expert Customer Feedback Analyst and Business Consultant.

You have been given comments collected from a YouTube video.

Your task is to analyze all comments and generate a professional report.

Comments:
{comments}

Generate the report in the following format.

# 1. Overall Sentiment
- Percentage of Positive comments
- Percentage of Negative comments
- Percentage of Neutral comments

# 2. Main Discussion Topics
List the most common topics people are discussing.

# 3. What People Liked
Summarize the most appreciated aspects mentioned by viewers.

# 4. What People Disliked
Summarize the most common complaints.

# 5. Negative Comments
List every strongly negative comment in this format:

Author:
Comment:
Reason why it is negative:

# 6. Business Recommendations
If this were a business or YouTube channel, what actions should be taken?

Include:
- Content improvements
- Product improvements
- Customer experience improvements
- Community engagement suggestions

# 7. Urgent Issues
Mention anything that requires immediate attention.

# 8. Frequently Requested Features
Mention things users repeatedly requested.

# 9. Hidden Opportunities
Mention any opportunities or ideas suggested by users.

# 10. Final Summary
Provide an executive summary in less than 200 words suitable for a business owner.

Be objective.
Use evidence from the comments.
Do not invent information.
""",
    input_variables=["comments"]
)


comments = ""

for doc in documents:
    comments += f"""
        Author: {doc.metadata['author']}
        Likes: {doc.metadata['likes']}
        Comment: {doc.page_content}
    """


model = ChatGroq(model = 'llama-3.3-70b-versatile',
                 groq_api_key = os.getenv('GROQ_API_KEY'))


from langchain_core.output_parsers import StrOutputParser



parser = StrOutputParser()

chain = analysis_prompt | model | parser

response = chain.invoke(
    {'comments': comments}
)

print(response)


