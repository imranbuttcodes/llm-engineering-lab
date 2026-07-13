Awesome. 🔥 Now we're moving from **basic schemas** to the **industry standard**.

If `TypedDict` is a blueprint, then **Pydantic is a blueprint with a quality inspector**.

---

# What is Pydantic?

**Pydantic** is a Python library used to create **data models** with **type checking and validation**.

It not only defines **what fields should exist**, but also checks whether the data is **correct**.

---

## Real-Life Analogy

Imagine a university admission form.

### TypedDict

The form only says:

```text
Name: ______

Age: ______

CGPA: ______
```

You could enter:

```text
Name: Imran
Age: Apple
CGPA: Elephant
```

The form doesn't verify anything.

---

### Pydantic

Now imagine an online admission portal.

You enter:

```text
Name: Imran
Age: Apple
```

Immediately it says:

❌ Age must be an integer.

Or

```text
CGPA = 5.7
```

It says

❌ CGPA must be between 0 and 4.

Pydantic validates everything automatically.

---

# Creating a Pydantic Model

Instead of `TypedDict`, we inherit from `BaseModel`.

```python
from pydantic import BaseModel

class Student(BaseModel):
    name: str
    age: int
    cgpa: float
```

Looks almost identical.

But it's much more powerful.

---

# Creating an Object

```python
student = Student(
    name="Imran",
    age=20,
    cgpa=3.8
)

print(student)
```

Output

```text
name='Imran'
age=20
cgpa=3.8
```

---

# Automatic Validation

Suppose someone writes

```python
student = Student(
    name="Imran",
    age="Twenty",
    cgpa=3.8
)
```

Output

```text
ValidationError

age
Input should be a valid integer
```

Pydantic refuses invalid data.

---

# Another Example

```python
from pydantic import BaseModel

class Book(BaseModel):
    title: str
    author: str
    price: float
```

```python
book = Book(
    title="Python",
    author="Guido",
    price=45.99
)
```

---

# Why LangChain Loves Pydantic

Suppose you ask

> Explain Machine Learning.

Instead of getting paragraphs, you want

```python
{
    "topic": "...",
    "difficulty": "...",
    "summary": "...",
    "example": "..."
}
```

Define

```python
from pydantic import BaseModel

class Lesson(BaseModel):
    topic: str
    difficulty: str
    summary: str
    example: str
```

Then

```python
structured_model = model.with_structured_output(Lesson)
```

The model now knows exactly what fields to produce, and LangChain can validate the returned data against the `Lesson` model.

---

# Adding Descriptions

This is one of the coolest features.

```python
from pydantic import BaseModel, Field

class Student(BaseModel):
    name: str = Field(description="Student's full name")
    age: int = Field(description="Student age")
```

These descriptions aren't just for humans.

LangChain passes them to the LLM as part of the schema, helping the model understand what each field represents.

---

# Default Values

```python
from pydantic import BaseModel

class Student(BaseModel):
    name: str
    age: int = 18
```

If age isn't provided

```python
Student(name="Imran")
```

Output

```text
name='Imran'
age=18
```

---

# Validation Rules

You can enforce constraints.

```python
from pydantic import BaseModel, Field

class Student(BaseModel):
    age: int = Field(gt=0, lt=100)
```

Valid

```python
age=20
```

Invalid

```python
age=-5
```

Output

```text
ValidationError
```

---

# More Constraints

```python
price: float = Field(gt=0)

rating: float = Field(ge=0, le=5)

username: str = Field(min_length=3, max_length=20)
```

These are incredibly useful when building production applications.

---

# TypedDict vs Pydantic

| Feature            | TypedDict | Pydantic    |
| ------------------ | --------- | ----------- |
| Defines fields     | ✅         | ✅           |
| Type hints         | ✅         | ✅           |
| Runtime validation | ❌         | ✅           |
| Default values     | ❌         | ✅           |
| Field descriptions | ❌         | ✅           |
| Constraints        | ❌         | ✅           |
| Error messages     | ❌         | ✅           |
| Best for AI apps   | Good      | Excellent ⭐ |

---

# Why Pydantic is the Industry Standard

Most production AI systems use **Pydantic** because it ensures the data you receive is reliable before your application uses it. If an LLM returns something unexpected, Pydantic can catch the problem immediately instead of letting bad data flow through your app.

---

# Key Takeaways

* **Pydantic** builds structured data models using `BaseModel`.
* It defines both the **shape** and the **rules** for your data.
* It automatically validates input types and values.
* `Field()` lets you add descriptions, defaults, and constraints.
* In LangChain, Pydantic is the **most common choice** for `with_structured_output()` because it combines clear schemas with robust validation.

---

## One thing to notice

`TypedDict` and `Pydantic` look very similar:

```python
# TypedDict
class Student(TypedDict):
    name: str
    age: int
```

```python
# Pydantic
class Student(BaseModel):
    name: str
    age: int
```

The syntax is almost the same, but the behavior is very different. `TypedDict` simply describes the expected structure, while `Pydantic` creates a real model that can validate, document, and manage data. That's why Pydantic is the go-to choice for modern AI applications.
