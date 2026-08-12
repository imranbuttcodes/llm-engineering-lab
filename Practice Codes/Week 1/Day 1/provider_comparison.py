import os
import time
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

load_dotenv()

PROMPT = "Explain what a REST API is, in 2-3 sentences, for a beginner programmer."

def test_provider(name, llm_factory):
    """Runs the prompt against one provider, times it, catches errors cleanly."""
    print(f"\n{'='*50}")
    print(f"Provider: {name}")
    print('='*50)
    try:
        llm = llm_factory()
        start = time.time()
        response = llm.invoke([HumanMessage(content=PROMPT)])
        elapsed = time.time() - start

        print(f"Response: {response.content}")
        print(f"\nLatency: {elapsed:.2f}s")

        # Token usage lives in different spots depending on provider/wrapper
        usage = response.response_metadata.get("token_usage") or response.usage_metadata
        if usage:
            print(f"Token usage: {usage}")
        else:
            print("Token usage: not returned by this provider")

    except Exception as e:
        print(f"FAILED: {e}")


# ---- Groq ----
def groq_llm():
    from langchain_groq import ChatGroq
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0,
    )

# ---- Gemini ----
def gemini_llm():
    from langchain_google_genai import ChatGoogleGenerativeAI
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0,
    )

# ---- OpenRouter (OpenAI-compatible SDK, different base_url) ----
def openrouter_llm():
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(
        model="openrouter/free",
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=0,
    )

# ---- Cerebras (also OpenAI-compatible SDK, different base_url) ----
def cerebras_llm():
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(
        model="gpt-oss-120b",
        openai_api_key=os.getenv("CEREBRAS_API_KEY"),
        openai_api_base="https://api.cerebras.ai/v1",
        temperature=0,
    )


if __name__ == "__main__":
    test_provider("Groq", groq_llm)
  #  test_provider("Gemini", gemini_llm)
    test_provider("OpenRouter", openrouter_llm)
    test_provider("Cerebras", cerebras_llm)