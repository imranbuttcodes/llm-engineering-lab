#Dynamic and resuable Prompts

from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

prompt = PromptTemplate.from_template('Summerize {topic} in {emotion} tone')

print(prompt.format(topic='Cricket', emotion = 'fun'))



# Role based Prompt

chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "hi you are an experienced {profession}"),
        ("human", "tell me about {topic}")
    ]
)

print(chat_prompt.format_messages(profession='doctor', topic = 'diabetes'))


# few shot prompt

from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate

examples = [
    {"input": "happy", "output": "sad"},
    {"input": "hot", "output": "cold"},
    {"input": "fast", "output": "slow"},
]

example_prompt = PromptTemplate(
    input_variables=["input", "output"],
    template="Input: {input}\nOutput: {output}"
)

few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="Give the opposite of the word below.",
    suffix="Input: {word}\nOutput:",
    input_variables=["word"],
)

print(few_shot_prompt.format(word="big"))