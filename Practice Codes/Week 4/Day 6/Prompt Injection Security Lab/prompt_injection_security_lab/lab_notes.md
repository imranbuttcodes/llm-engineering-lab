# What to investigate

Do not just run the lab. For each experiment answer:

## Experiment 1
- Did DeepSeek follow the system instruction?
- Did different jailbreak/injection wording produce different results?
- Why is putting a real secret in an LLM context dangerous?

## Experiment 2
- Does the malicious document influence the model?
- Does wrapping the document in "UNTRUSTED DATA" reliably solve the problem?
- What happens if the malicious instruction is paraphrased?

## Experiment 3
- Can the model request a sensitive tool?
- What is the actual security boundary?
- Why should the application authorize tool calls instead of trusting the model?

## Experiment 4
- Which defense is enforced by the application?
- Which defense is only a model instruction?
- What happens when an attacker changes wording?

## Key principle

Prompt-level defenses are useful, but authorization and capability controls
must be enforced outside the model.

A model should be treated as an untrusted decision-maker, not as the final
security authority.
