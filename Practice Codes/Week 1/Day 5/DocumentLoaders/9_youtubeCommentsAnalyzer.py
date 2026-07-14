import requests
import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
import streamlit as st
from urllib.parse import urlparse, parse_qs
from langchain_core.output_parsers import StrOutputParser


st.set_page_config(
    page_title="InsightTube",
)

st.title("📊 InsightTube")
st.caption("AI-Powered YouTube Comment Intelligence")




def extract_video_id(url: str) -> str:
    """
    Supported formats:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/shorts/VIDEO_ID
    """

    parsed = urlparse(url)

    if parsed.netloc in ("www.youtube.com", "youtube.com"):

        # Normal YouTube video
        if parsed.path == "/watch":

            video_id = parse_qs(parsed.query).get("v")

            if not video_id:
                raise ValueError("Video ID not found.")

            return video_id[0]

        # YouTube Shorts
        elif parsed.path.startswith("/shorts/"):

            video_id = parsed.path.split("/")[2]

            if not video_id:
                raise ValueError("Video ID not found.")

            return video_id

        else:
            raise ValueError("Invalid YouTube URL.")

    elif parsed.netloc == "youtu.be":

        video_id = parsed.path.strip("/")

        if not video_id:
            raise ValueError("Video ID not found.")

        return video_id

    raise ValueError("Invalid YouTube URL.")





load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")



video_url = st.text_input('Enter Video Url')

if video_url:
    try:
        VIDEO_ID = extract_video_id(video_url)


    except ValueError as e:
        st.error(e)

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

model = ChatGroq(model = 'llama-3.3-70b-versatile',
                        groq_api_key = os.getenv('GROQ_API_KEY'))


parser = StrOutputParser()

chain = analysis_prompt | model | parser

if st.button('Analyze'):
    with st.spinner('analyzing'):

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
            st.error(f'Failed to fetch comments! {response.status_code}')

            st.stop()

        data = response.json()


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

        comments = ""

        for doc in documents:
            comments += f"""
                Author: {doc.metadata['author']}
                Likes: {doc.metadata['likes']}
                Comment: {doc.page_content}
            """


     
        response = chain.invoke(
            {'comments': comments}
        )

        st.write(response)
