# Real Prompt Injection Security Lab — DeepSeek

This is a practical, real-LLM security lab for learning prompt injection.

## What it teaches

1. Direct prompt injection against a real DeepSeek API.
2. System/developer instruction vs user-controlled content.
3. Secret-extraction attempts.
4. Indirect prompt injection using retrieved/untrusted text.
5. Tool-call injection in a real agent-like workflow.
6. A deliberately vulnerable architecture.
7. Layered defenses: authorization, context separation, output validation, and tool policy.
8. Adversarial regression tests.

## Setup

Create a virtual environment if you want:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install:

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and put your DeepSeek API key there.

```bash
cp .env.example .env
```

Run:

```bash
python lab.py
```

## Important

All "secrets" and tools in this lab are fake/local training data. Do not put real credentials in the lab.

The vulnerable modes are intentionally vulnerable so you can attack them.

## Suggested sequence

Start with:
1. `1` — direct injection
2. `2` — indirect injection
3. `3` — tool injection
4. `4` — defenses
5. `5` — automated attack suite

Then inspect the code and explain why each defense exists.
