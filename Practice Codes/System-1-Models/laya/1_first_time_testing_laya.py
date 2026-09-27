# from laya import Router

# router = Router()

# state = "Hey, my payment failed."

# questions = {
#     "is_support": {
#         "type": "choice",
#         "instructions": "Is this a customer support request?",
#         "criteria": {
#             "support": "The message is asking for help with a problem",
#             "not_support": "The message is not asking for help"
#         }
#     }
# }

# result = router.predict(state, questions)

# #print("BRO WHAT?",result['answers']['is_support']['choice'])






from laya import Router

router = Router()

state = "Hey, my payment failed."

questions = {
    "is_support": {
        "type": "choice",
        "instructions": "Is this a customer support request?",
        "criteria": {
            "support": "The message is asking for help with a problem",
            "not_support": "The message is not asking for help"
        }
    }
}

result = router.predict(state, questions)

print()
print()
print("Laya Response:\n",result)

print()
print()

print("Clearning Response\n")
answer = result["answers"]["is_support"]
routing = result["routing"]
usage = result["usage"]

print("\n" + "=" * 50)
print("                 LAYA PREDICTION")
print("=" * 50)

print(f"\nModel:")
print(f"  {result['model']}")

print(f"\nQuestion:")
print(f"  is_support")

print(f"\nDecision Type:")
print(f"  {answer['type']}")

print("\n" + "-" * 50)
print("                    RESULT")
print("-" * 50)

print(f"\nSelected Choice:")
print(f"  {answer['choice']}")

print("\nProbabilities:")
for choice, probability in answer["probabilities"].items():
    print(f"  {choice:<12} → {probability:.2%}")

print(f"\nAnswer Confidence:")
print(f"  {answer['answer_confidence']:.2%}")

print(f"\nAction Probability:")
print(f"  {answer['action']['act_probability']:.2%}")

print("\n" + "-" * 50)
print("                   ROUTING")
print("-" * 50)

print(f"\nModel:")
print(f"  {routing['model']}")

print(f"\nRepository:")
print(f"  {routing['repo']}")

print(f"\nReason:")
print(f"  {routing['reason']}")

print("\n" + "-" * 50)
print("                    USAGE")
print("-" * 50)

print(f"\nInput Tokens:")
print(f"  {usage['input_tokens']}")

print(f"\nOutput Tokens:")
print(f"  {usage['output_tokens']}")

print("\n" + "=" * 50)