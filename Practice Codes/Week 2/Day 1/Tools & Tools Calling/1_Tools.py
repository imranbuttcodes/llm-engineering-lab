# Creating Custom Tools

from langchain_core.tools import tool


@tool

def add(a: int, b: int) -> int:
    """
    This Function Adds Two Numbers and return them
    """
    return a + b



print(add)
print()
print(type(add))
print(add.args)
print("Yoah")
print(add.name)

print(add.description)

print(add.args)

print(add.args_schema)
print("Actual JSON Schema that sent to LLMs")
print(add.args_schema.model_json_schema())

print("Using Tool")
print(add.invoke(
    {
        'a': 10,
        'b': 20
    }
))

# IT sugest that tools are also RUNNABLES