from langchain_groq import ChatGroq
from typing import TypedDict, Annotated, Optional, Literal
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field


load_dotenv()


model = ChatGroq(model = 'llama-3.3-70b-versatile',
                 groq_api_key = os.getenv('GROQ_API_KEY'))



#Schema
# class Review(TypedDict):
#     Summery: str
#     Sentiment: str 


# Schema with Annotated

class Review(BaseModel):

    key_themes: list[str] = Field(description='Write down all the key themes discussed int the review in list')


    Summery: str =  Field(description='A Brief Summery of the review')
    Sentiment: Literal['pos', 'neg'] = Field(description='Return Sentiment Bro Either Negative , positive')
    pros: Optional[list[str]] = Field(description= 'Write down all the pros discussed in the review in list')
    cons: Optional[list[str]] = Field(description= 'Write down all the cons discussed in the review in list')


structured_model = model.with_structured_output(Review) # here behind the scene it generates the system prompt to encourage model to return structured output!

# response = structured_model.invoke("""
#     I recently upgraded to the Samsung Galaxy S24 Ultra, and I must say, it’s an absolute powerhouse! The Snapdragon 8 Gen 3 processor makes everything lightning fast—whether I’m gaming, multitasking, or editing photos. The 5000mAh battery easily lasts a full day even with heavy use, and the 45W fast charging is a lifesaver.                                   
# """)


response = structured_model.invoke(
    """"I recently upgraded to the Samsung Galaxy S24 Ultra, and I must say, it’s an absolute powerhouse! The Snapdragon 8 Gen 3 processor makes everything lightning fast—whether I’m gaming, multitasking, or editing photos. The 5000mAh battery easily lasts a full day even with heavy use, and the 45W fast charging is a lifesaver.

The S-Pen integration is a great touch for note-taking and quick sketches, though I don't use it often. What really blew me away is the 200MP camera—the night mode is stunning, capturing crisp, vibrant images even in low light. Zooming up to 100x actually works well for distant objects, but anything beyond 30x loses quality.

However, the weight and size make it a bit uncomfortable for one-handed use. Also, Samsung’s One UI still comes with bloatware—why do I need five different Samsung apps for things Google already provides? The $1,300 price tag is also a hard pill to swallow.

Pros:
Insanely powerful processor (great for gaming and productivity)
Stunning 200MP camera with incredible zoom capabilities
Long battery life with fast charging
S-Pen support is unique and useful
                                 
Review by Imran Butt"""
)


print(type(response))
print()
print(response)
print()
print()
response = dict(response)
print(response['Summery'])
print()
print(response['Sentiment'])
print()
print(response['key_themes'])
print()
print(response['pros'])
print()
print(response['cons'])
