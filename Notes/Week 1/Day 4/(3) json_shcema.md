# JSON Schema in LangChain

## What is JSON Schema?

A **JSON Schema** is a set of rules that defines the structure of a JSON object.

Think of it as a **blueprint** or **contract** that tells the LLM:

- Which fields should be generated.
- What data type each field should have.
- Which fields are required.
- What validation rules should be followed.

It **does not contain the data itself**. Instead, it describes **how the data should look**.

---

## Why do we use JSON Schema?

Without a schema, an LLM can return responses in many different formats.

Example Prompt:

```
Explain Artificial Intelligence.
```

Possible Response #1

```text
Artificial Intelligence is...
```

Possible Response #2

```json
{
    "topic":"AI",
    "summary":"..."
}
```

Possible Response #3

```text
Topic: AI

Difficulty: Medium

Summary...
```

The output is inconsistent.

With a JSON Schema, we force the model to generate a predictable structure.

Example Output

```json
{
    "topic": "Artificial Intelligence",
    "difficulty": 5,
    "summary": "AI enables machines to perform tasks requiring human intelligence.",
    "example": "ChatGPT"
}
```

Now every response follows the same structure.

---

# JSON Schema Structure

Example Schema

```json
{
    "title": "Lesson",
    "type": "object",

    "properties": {

        "topic": {
            "type": "string"
        },

        "difficulty": {
            "type": "integer"
        },

        "summary": {
            "type": "string"
        },

        "example": {
            "type": "string"
        }

    },

    "required": [
        "topic",
        "difficulty",
        "summary",
        "example"
    ]
}
```

---

# Important Keywords

## title

Gives a name to the schema.

```json
"title": "Lesson"
```

---

## type

Specifies the type of data.

Possible values:

- string
- integer
- number
- boolean
- object
- array
- null

Example

```json
"type":"object"
```

---

## properties

Defines every field inside the object.

Example

```json
"properties":{

    "topic":{
        "type":"string"
    },

    "difficulty":{
        "type":"integer"
    }

}
```

---

## required

Specifies which fields must exist.

```json
"required":[
    "topic",
    "difficulty"
]
```

---

## description

Provides extra information to the LLM.

```json
"topic":{

    "type":"string",

    "description":"Topic name"

}
```

Descriptions help the model generate better outputs.

---

## minimum & maximum

Validation for numbers.

```json
"age":{

    "type":"integer",

    "minimum":18,

    "maximum":60

}
```

---

## minLength & maxLength

Validation for strings.

```json
"name":{

    "type":"string",

    "minLength":3,

    "maxLength":30

}
```

---

## enum

Restricts values.

```json
"difficulty":{

    "type":"string",

    "enum":[
        "Easy",
        "Medium",
        "Hard"
    ]

}
```

Only these values are allowed.

---

## items

Used for arrays.

```json
"subjects":{

    "type":"array",

    "items":{
        "type":"string"
    }

}
```

Output

```json
[
    "Python",
    "Machine Learning",
    "AI"
]
```

---

# Creating a Schema in Python

Instead of creating a separate JSON file, we can define it as a Python dictionary.

```python
schema = {

    "title":"Lesson",

    "type":"object",

    "properties":{

        "topic":{
            "type":"string"
        },

        "difficulty":{
            "type":"integer"
        },

        "summary":{
            "type":"string"
        }

    },

    "required":[
        "topic",
        "difficulty",
        "summary"
    ]

}
```

---

# Using JSON Schema with LangChain

```python
structured_model = model.with_structured_output(schema)
```

This tells the model:

> "Always generate output that follows this JSON Schema."

Now invoke it normally.

```python
result = structured_model.invoke(
    "Explain Artificial Intelligence."
)

print(result)
```

Output

```python
{
    "topic":"Artificial Intelligence",
    "difficulty":5,
    "summary":"AI is..."
}
```

Notice that JSON Schema returns a **Python Dictionary**.

---

# Storing the Schema in a JSON File

Real-world projects usually store schemas separately.

Project Structure

```
Project/

│── app.py

│── lesson_schema.json

│── .env
```

Example

**lesson_schema.json**

```json
{
    "title":"Lesson",
    "type":"object",

    "properties":{

        "topic":{
            "type":"string"
        },

        "difficulty":{
            "type":"integer"
        }

    },

    "required":[
        "topic",
        "difficulty"
    ]
}
```

---

# Loading the JSON Schema

Python provides the built-in **json** module.

```python
import json

with open("lesson_schema.json","r") as file:

    schema = json.load(file)
```

The variable `schema` is now a Python dictionary.

You can use it directly.

```python
structured_model = model.with_structured_output(schema)
```

---

# json.load() vs json.loads()

## json.load()

Reads JSON from a file.

```python
import json

with open("lesson_schema.json") as file:

    schema = json.load(file)
```

---

## json.loads()

Reads JSON from a string.

```python
import json

json_string = '''

{

    "name":"Imran",

    "age":20

}

'''

data = json.loads(json_string)
```

---

### Easy Trick to Remember

```
json.load(file)

↓

File
```

```
json.loads(string)

↓

String
```

The extra **"s"** stands for **String**.

---

# TypedDict vs Pydantic vs JSON Schema

| Feature | TypedDict | Pydantic | JSON Schema |
|----------|-----------|-----------|-------------|
| Written In | Python | Python | JSON |
| Returns | Dictionary | Pydantic Object | Dictionary |
| Validation | ❌ | ✅ | ✅ |
| Descriptions | ❌ | ✅ | ✅ |
| Type Checking | ✅ | ✅ | ✅ |
| Best For | Simple Structures | Python Applications | APIs, LLMs, Cross-Language Systems |

---

# Summary

- JSON Schema is a blueprint that describes JSON data.
- It defines the fields, types, validation rules, and required properties.
- LangChain can use a JSON Schema through `with_structured_output()`.
- Schemas are commonly stored in separate `.json` files.
- Use `json.load()` to load a schema from a file.
- JSON Schema returns a standard Python dictionary.
- It is language-independent and widely used in APIs, OpenAPI, and LLM structured outputs.