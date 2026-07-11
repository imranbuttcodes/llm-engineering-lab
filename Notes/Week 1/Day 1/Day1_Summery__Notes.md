# Week 1, Day 1 — LLM API Fundamentals

**Goal for today:** Understand what's actually happening when you call an LLM API — no framework magic, just the real mechanics — and prove every concept hands-on with real code against real providers (Groq, OpenRouter, Cerebras, Gemini).

---

## 1. What an LLM Actually Is

Strip away the "AI" branding. At its core, an LLM does exactly one thing, repeatedly:

> **Given the text so far, predict the most likely next token. Append it. Repeat until it decides to stop.**

That's the entire mechanism. Every capability you've seen — chatting, writing code, answering questions — is this one loop running over and over. Nothing "understands" your question the way a human does; the model generates the statistically most fitting continuation of your input, based on patterns learned from massive training data.

**Why this matters:** when a model "hallucinates" or gives a wrong answer, it's not confused — it generated a continuation that *seemed* statistically reasonable, even if it was factually wrong. This mental model matters for debugging weird outputs later.

---

## 2. Tokens — The Real Unit of Everything

Models don't read words. They read **tokens** — chunks of text that can be a whole word, part of a word, or punctuation.

### Encoding vs Decoding

- **Encoding** = text → numeric IDs. The tokenizer has a fixed vocabulary (a giant lookup table, ~100K entries for `cl100k_base`). Each entry maps a text chunk to a number.
- **Decoding** = numeric IDs → text. Reverse lookup — take the IDs the model generated, look each one up in the same vocab table, glue the strings back together.

### Why words split unevenly (BPE)

Tokenizers use **Byte Pair Encoding (BPE)** — during training, they learn which chunks of characters appear together most often. Common chunks earn their own single token. Rare/unusual combinations get broken into smaller familiar pieces.

### Hands-on results (using `tiktoken`, `cl100k_base` encoding)

| Text | Token Count | Breakdown |
|---|---|---|
| `"the"` | 1 | `['the']` — common word, earned its own token |
| `"unbelievable"` | 3 | `['un', 'belie', 'vable']` — less common as a whole unit |
| `"ChatGPT"` | 3 | `['Chat', 'G', 'PT']` — rare/newer term, no single-token slot |
| `"I am learning LLM engineering this summer."` | 9 | `['I', ' am', ' learning', ' L', 'LM', ' engineering', ' this', ' summer', '.']` |

**Key observation:** tokens include leading spaces baked in (`" am"` not `"am"`) — spaces are meaningful boundaries to the tokenizer, not separate characters.

### BPE on unfamiliar text

The more "normal English" your text is, the fewer tokens per character. The weirder/rarer the text (gibberish, typos, gamertags, random IDs), the closer token count gets to character count — worst case, nearly one token per character.

**Why this matters practically:**
- Pricing and rate limits are token-based, not word-based
- Context windows are measured in tokens
- Messy/unusual text (code, IDs, non-English text, typos) burns more tokens than clean prose — this matters a lot once you're stuffing real documents into RAG prompts (Week 1, Days 5–7)

---

## 3. Roles — System / User / Assistant

Every LLM API call sends a **list of messages**, each tagged with a role:

- **system** — behavioral instructions, set once, treated as higher-priority rules by the model
- **user** — what the human actually asked
- **assistant** — the model's reply (also used to feed back conversation history)

**Why this exists:** the model was specifically trained to treat `system`-role text as behavior-shaping instructions, distinct from the `user`-role actual request. This lets you control *how* the model responds without that instruction looking like part of the user's message.

### Hands-on proof

Same question (`"What's 15 * 12?"`), same model (`llama-3.3-70b-versatile` via Groq):

**No system role:**
```
15 * 12 = 180.
```

**With system role** (`"You are a strict math tutor. NEVER give the final answer directly. Only give a hint."`):
```
To solve this multiplication problem, you can try breaking it down into
smaller parts. For example, you could think of 15 * 12 as (10 * 12) + (5 * 12).
Does that help you get started?
```

Same exact user question — completely different behavior, purely because of the system message. This is the foundation for building any persona, agent, or structured-output extractor later in the roadmap.

**Note:** smaller/weaker models sometimes respect system instructions less strictly under pressure from the user prompt — worth testing per-model if behavior consistency matters.

---

## 4. Temperature — The Randomness Dial

At every generation step, the model calculates a probability for every possible next token. Temperature controls **how the model samples from that probability distribution**.

- **temperature = 0** → always pick the single highest-probability token. Deterministic, repeatable.
- **temperature = 1** → sample naturally according to real probabilities — lower-probability tokens get a real, but proportional, chance.
- **temperature = 1.5–2** → flattens the distribution, even unlikely tokens get picked often. Output can become incoherent.

### Hands-on proof

Prompt: `"Describe the color blue in one sentence."` — run 3x at each setting.

**Temperature = 0** (3 runs — identical every time):
```
The color blue is a cool and calming hue that can range in shade from the
pale, serene tones of a clear sky to the deep, rich tones of a still ocean,
evoking feelings of tranquility and trust.
```
*(All 3 runs were word-for-word identical.)*

**Temperature = 1.5** (3 runs — same idea, different wording each time):
```
[1] Blue is a cool, calming, and versatile color that ranges in shade from
    the palest sky blue to the deepest navy...
[2] Blue is a cool and calming color that can range in shade from pale,
    gentle hues like sky blue or light azure, to deeper, richer tones...
[3] The color blue is a cool and calming hue that encompasses a wide range
    of shades, from the pale sky tones and soft pastels...
```

**When to use which:**
- Structured extraction, classification, code, JSON output → **temperature 0–0.3**
- Creative writing, brainstorming, chatbot personality → **temperature 0.7–1.0**
- Agent decision-making / tool calling → usually kept low for predictability

---

## 5. top_p — Nucleus Sampling

Where temperature changes *how sharply* the model favors top tokens, **top_p controls how many candidate tokens are even eligible** to be picked.

**Mechanism:** sort all possible next tokens by probability, highest to lowest. Add them up until the cumulative probability hits `top_p` (e.g. 0.9 = 90%). Only tokens within that cumulative slice are eligible — everything past that cutoff is discarded entirely, regardless of temperature.

**Practical rule of thumb:** tune **one knob at a time** — usually temperature, leaving top_p at its default (1.0). Aggressively tuning both simultaneously makes behavior unpredictable and hard to debug.

### Hands-on observation

Tested at temp=1.3 with top_p=1.0 vs top_p=0.1 on a short factual prompt — outputs were nearly identical in both cases. **Honest finding:** top_p's effect is much more visible on genuinely open-ended prompts (creative writing, storytelling) where the model has many legitimately different paths to take. Short, narrow-answer prompts naturally converge to similar phrasing regardless of top_p, because there isn't much real uncertainty to restrict in the first place.

---

## 6. max_tokens — The Output Length Ceiling

Caps how many tokens the model is **allowed to generate** in its response. No effect on quality or randomness — it's a hard, dumb cutoff.

**Critical detail:** the model doesn't know it's about to hit the limit. Generation just stops mid-token-stream the instant the cap is reached — even mid-word or mid-JSON-object.

### Hands-on proof

Prompt: `"Explain how airplanes fly, in detail, covering lift, thrust, drag, and weight."`

**max_tokens = 20:**
```
The miracle of flight! Airplanes are able to fly by harnessing the
principles of aerodynamics,
[Finish reason: length]
```
Cut off mid-sentence, trailing comma, no period.

**max_tokens = 300:**
```
[Full explanation of lift, and started on thrust...]
...Thrust: The Forward Force
Thrust is
[Finish reason: length]
```
**Even at 300 tokens, it was STILL truncated** — never reached drag or weight, which the prompt explicitly asked for.

**The real lesson:** never assume a token limit is "high enough." Always check the `finish_reason` field programmatically:
- `finish_reason == "length"` → response was truncated, incomplete
- `finish_reason == "stop"` → model finished naturally

This matters enormously for structured JSON extraction (Day 3) — a truncated JSON response will fail to parse, and without checking `finish_reason`, the root cause is invisible.

---

## 7. Context Window

The **context window** is the maximum total size, in tokens, that a model can hold in view at once — input (system + user + prior conversation history) **and** output, combined.

Think of it as the model's short-term memory span for the *current* request — not what it knows from training, but how much of the live conversation/document it can actually process at once.

**Reference sizes encountered today:**
- Llama 3.3 70B (Groq) → 128K tokens
- Gemini 2.0 Flash → 1M tokens

**Why it matters:**
- **Multi-turn chat (Day 4):** every prior message fed back in eats into this budget — long conversations eventually need older messages dropped or summarized
- **RAG (Days 5–7):** document chunks + question + system prompt must all fit within the window, or the request fails or gets silently truncated
- Directly tied to tokens (Concept 2) — a 128K window is roughly ~90–100K words, not 128K words, since tokens ≈ ¾ word on average

---

## 8. Multi-Provider Capstone: Real-World Lessons

Built `provider_comparison.py` — same prompt sent to Groq, OpenRouter, and Cerebras (Gemini blocked by a provider-side quota issue, tracked separately), logging response, latency, and token usage per provider.

### Results snapshot

| Provider | Latency | Total Tokens | Reasoning Tokens |
|---|---|---|---|
| Groq | 1.23s | 150 | 0 |
| OpenRouter | 8.12s | 626 | 480 |
| Cerebras | 1.23s | 224 | 28 |

### Key lessons learned the hard way

**1. Model names on free/hosted tiers rotate constantly — don't trust them long-term.**
Hit a `404` on Cerebras (`llama-3.3-70b` was deprecated Feb 16, 2026) and OpenRouter (a guessed free model ID no longer existed). Real production lesson: build in fallback model lists, or use auto-routing (`"openrouter/free"`) instead of hardcoding one specific free-tier model ID.

**2. `queue_time` is a real, separate cost from generation time.**
Groq's response metadata splits `queue_time` (waiting for server availability) from `prompt_time` and `completion_time` (actual work). On free tiers, queue congestion can be a meaningful chunk of total latency — this explains why identical requests feel faster or slower run-to-run.

**3. Reasoning models cost hidden tokens and latency, even on simple questions.**
OpenRouter's auto-router picked a reasoning-capable model, which burned 480 invisible "thinking" tokens before producing a 3-sentence answer — explaining both the high token count and the 8.12s latency versus Groq/Cerebras's ~1.2s. Lesson: match model choice to task complexity. A simple factual question doesn't need a model that reasons at length first — that's wasted latency and token budget.

**4. `429` errors aren't always "you did something wrong."**
OpenRouter's free-tier models are shared across all users — a `429 RESOURCE_EXHAUSTED` or rate-limit error can simply mean upstream congestion, not a bug in your code or a personal limit being hit.

### Open issue

**Gemini quota (`limit: 0`)** — this is a distinct problem from the model-rotation issues above. A `limit: 0` response (as opposed to a normal rate-limit-exceeded message) suggests the linked Google Cloud project has zero quota configured for the free tier, rather than a standard usage cap. Needs investigation directly in Google Cloud Console / AI Studio — flagged for follow-up, not blocking the rest of the roadmap since Groq is the active primary provider.

---

## Summary — What Actually Clicked Today

1. LLMs are next-token predictors — nothing more mystical than that
2. Tokens (not words) are the real unit — encoding/decoding is just vocabulary lookup, BPE splits unfamiliar text into familiar pieces
3. System role shapes behavior; user role is the actual ask — proven with a strict-tutor example
4. Temperature controls *how much* randomness; top_p controls *how many* tokens are eligible for randomness — tune one at a time
5. max_tokens is a hard, dumb cutoff — always verify `finish_reason`, never assume a number is "high enough"
6. Context window = total token budget per request (input + output combined)
7. Real APIs are messy — model names rotate, free tiers queue and rate-limit, and different providers/models trade off speed vs depth of reasoning

**Next up: Day 2 — LangChain LCEL basics, rebuilding today's comparison logic with proper chains instead of raw provider calls.**