from langgraph.graph import StateGraph,START, END
from typing import TypedDict, Literal, Annotated
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import os
import operator

load_dotenv()

generator_llm = ChatGroq(
    model = 'llama-3.3-70b-versatile',
    api_key = os.getenv("GROQ_API_KEY")
)

evaluation_llm = ChatGroq(
    model = 'llama-3.3-70b-versatile',
    api_key = os.getenv("GROQ_API_KEY")
)

optimizer_llm = ChatGroq(
    model = 'llama-3.3-70b-versatile',
    api_key = os.getenv("GROQ_API_KEY")
)


class TweetState(TypedDict):
    topic: str
    tweet: str
    evaluation: Literal['approved', 'needs_improvement']
    feedback: str
    iteration: int 
    max_iteration: int

    tweet_history: Annotated[list[str], operator.add]
    feedback_history: Annotated[list[str], operator.add]



# evaluation schema for evaluation_model

class evaluate_tweet_schema(BaseModel):
    evaluation: Literal['approved', 'needs_improvement'] = Field(description="Final evaluation result.")
    feedback: str = Field(description="feedback for the tweet.")

structured_evaluation_model = evaluation_llm.with_structured_output(evaluate_tweet_schema)



# Generate Tweet
def generate_tweet(state: TweetState):
    topic = state['topic']
    messages = [
        SystemMessage(content='Bro You are a funny tweet influencer who post stuff in the saddest possible way yet incredibly funniest'),
        HumanMessage(content = f"""Generate a short and Saddest yet funniest Tweet on the following Topic:\n\n Topic: {topic}
    Rules:
- Do NOT use question-answer format.
- Max 280 characters.
- Use observational humor, irony, sarcasm, or cultural references.
- Think in meme logic, punchlines, or relatable takes.
- Use simple, day to day english
"""),
    ]
    
    response = generator_llm.invoke(messages).content

    return {
        'tweet': response,
        'tweet_history': [response]
    }


def evaluate_tweet(state: TweetState):
    
    messages = [
    SystemMessage(content="You are a ruthless, no-laugh-given Twitter critic. You evaluate tweets based on humor, originality, virality, and tweet format."),
    HumanMessage(content=f"""
Evaluate the following tweet:

Tweet: "{state['tweet']}"

Use the criteria below to evaluate the tweet:

1. Originality - Is this fresh, or have you seen it a hundred times before?  
2. Humor - Did it genuinely make you smile, laugh, or chuckle?  
3. Punchiness - Is it short, sharp, and scroll-stopping?  
4. Virality Potential - Would people retweet or share it?  
5. Format - Is it a well-formed tweet (not a setup-punchline joke, not a Q&A joke, and under 280 characters)?

Auto-reject if:
- It's written in question-answer format (e.g., "Why did..." or "What happens when...")
- It exceeds 280 characters
- It reads like a traditional setup-punchline joke
- Dont end with generic, throwaway, or deflating lines that weaken the humor (e.g., “Masterpieces of the auntie-uncle universe” or vague summaries)

### Respond ONLY in structured format:
- evaluation: "approved" or "needs_improvement"  
- feedback: One paragraph explaining the strengths and weaknesses 
""")
]
    response = structured_evaluation_model.invoke(messages)

    return {
        'evaluation': response.evaluation, 
        'feedback_history': [response.feedback],
        'feedback': response.feedback
    }


def evaluation_router(state: TweetState):

    if state['evaluation'] == 'approved' or state['iteration'] >= state['max_iteration']:
        return 'approved'
    else:
        return 'needs_improvement'


def optimize_tweet(state: TweetState):

    messages = [
        SystemMessage(content="You punch up tweets for virality and humor based on given feedback."),
        HumanMessage(content=f"""
Improve the tweet based on this feedback:
"{state['feedback']}"

Topic: "{state['topic']}"
Original Tweet:
{state['tweet']}

Re-write it as a short, viral-worthy tweet. Avoid Q&A style and stay under 280 characters.
""")
    ]

    response = optimizer_llm.invoke(messages).content
    iteration = state['iteration'] + 1

    return {'tweet': response, 'iteration': iteration, 'tweet_history': [response]}




graph = StateGraph(TweetState)

graph.add_node('generate_tweet', generate_tweet)
graph.add_node('evaluate_tweet', evaluate_tweet)
graph.add_node('optimize_tweet', optimize_tweet)



graph.add_edge(START, 'generate_tweet')
graph.add_edge('generate_tweet', 'evaluate_tweet')

graph.add_conditional_edges('evaluate_tweet', 
                            evaluation_router,
                            {
                                'approved': END,
                                'needs_improvement': 'optimize_tweet'
                            }
                            )
graph.add_edge('optimize_tweet', 'evaluate_tweet')

workflow = graph.compile()

initial_state = {
    "topic": "Why the hell is AI replacing Humans",
    "iteration": 1,
    "max_iteration": 5
}
result = workflow.invoke(initial_state)

print(result)
