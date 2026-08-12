import tiktoken

# This is OpenAI's tokenizer, but it's close enough to give you the FEEL
# of tokenization across most models (Gemini/Groq split similarly)
encoding = tiktoken.get_encoding("cl100k_base")

samples = [
    "the",
    "unbelievable",
    "ChatGPT",
    "I am learning LLM engineering this summer.",
]

for text in samples:
    tokens = encoding.encode(text)
    print(f"'{text}'")
    print()
    print('tokens')
    print(f'{tokens}')
    print(f"  -> {len(tokens)} tokens: {[encoding.decode([t]) for t in tokens]}")
    print()


print()
samples = [
    "flibbertigibbet",     # real but obscure word
    "asdkjqwe",             # pure random gibberish
    "unbelievablyyyyy",     # typo/extended real word
    "xXx_ProGamer_2026",    # made-up gamertag style
]

for text in samples:
    tokens = encoding.encode(text)
    pieces = [encoding.decode([t]) for t in tokens]
    print(f"'{text}' -> {len(tokens)} tokens: {pieces}")