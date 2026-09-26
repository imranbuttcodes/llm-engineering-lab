from laya import Router

router = Router()

state = "YOUR INPUT / DATA"

questions = {
    "YOUR_DECISION_NAME": {

        "type": "choice",

        "instructions": "YOUR QUESTION",

        "criteria": {
            "OPTION_1": "What OPTION_1 means",
            "OPTION_2": "What OPTION_2 means",
            "OPTION_3": "What OPTION_3 means"
        }
    }
}

result = router.predict(state, questions)

print(result)

So we can define multiple questoins for the same state

state = "My payment failed and I want to cancel my subscription."

questions = {

    "is_support": {
        "type": "choice",
        "instructions": "Is this a customer support request?",
        "criteria": {
            "support": "The user needs help with a problem",
            "not_support": "The user does not need help"
        }
    },

    "wants_cancellation": {
        "type": "noul",
        "instructions": "Does the user want to cancel their subscription?"
    },

    "urgency": {
        "type": "choice",
        "instructions": "How urgent is the request?",
        "criteria": {
            "low": "The issue is not urgent",
            "medium": "The issue needs attention soon",
            "high": "The issue requires immediate attention"
        }
    }
}

