Excellent. Now we're entering the actual implementation of Long-Term Memory in LangGraph.

---

# What is `BaseStore`?

`BaseStore` is simply an **abstract interface (or blueprint)** for any memory store.

Think of it like this:

```text
            BaseStore
               ▲
               │
      --------------------
      │        │         │
 InMemory   SQLite   Postgres
   Store      Store      Store
```

It doesn't actually store anything.

It only defines:

> "Every memory store must support these operations."

---

# Real-life Analogy

Imagine an Animal class.

```python
class Animal:

    def eat(self):
        ...

    def sleep(self):
        ...
```

Animal isn't a dog.

Animal isn't a cat.

It's just a blueprint.

Then

```python
Dog(Animal)

Cat(Animal)

Lion(Animal)
```

Same thing.

---

For LangGraph

```text
BaseStore

↓

Memory Stores
```

---

# Why does LangGraph need BaseStore?

Because LangGraph doesn't care

whether your memories are stored in

* SQLite
* Postgres
* Redis
* Chroma
* Pinecone
* MongoDB

It only wants to call

```python
store.put(...)

store.get(...)

store.search(...)
```

No matter which database you're using.

---

# Internally

Imagine

```python
class BaseStore:

    def put(...):
        pass

    def get(...):
        pass

    def search(...):
        pass

    def delete(...):
        pass
```

Notice

There is **no implementation.**

Only the function signatures.

---

Then

## InMemoryStore

inherits

```python
BaseStore
```

and implements

```python
put()

get()

search()

delete()
```

using a Python dictionary.

---

SQLiteStore

implements

```python
put()

get()

search()

delete()
```

using SQL.

---

PostgresStore

implements the same methods

using PostgreSQL.

---

# Why is this useful?

Suppose your code says

```python
memory = SomeStore()

memory.put(...)
```

Tomorrow you change

```python
SomeStore
```

to

```python
PostgresStore
```

Nothing else changes.

Because every store follows the **BaseStore contract**.

---

# Stores that inherit from `BaseStore`

The exact available stores depend on the LangGraph version you're using, but conceptually you'll encounter stores such as:

```text
BaseStore
│
├── InMemoryStore
│
├── SQLite Store
│
├── Postgres Store
│
└── Any custom store you build yourself
```

You can even create your own.

```python
class MyCompanyStore(BaseStore):

    def put(...):
        ...

    def get(...):
        ...

    def search(...):
        ...

    def delete(...):
        ...
```

LangGraph will use it exactly like the built-in ones.

---

# Big Picture

```text
                LangGraph

                    │

        store.put(memory)

                    │

             BaseStore API

                    │

     ┌──────────────┼──────────────┐
     │              │              │
InMemoryStore   SQLiteStore   PostgresStore
```

LangGraph talks only to **BaseStore**.

The actual storage implementation is hidden behind it.

---

## In one sentence

> **`BaseStore` is the common interface that defines how LangGraph reads, writes, searches, and deletes long-term memories, while concrete stores (like `InMemoryStore`, SQLite-backed stores, or Postgres-backed stores) provide the actual implementation.**

This abstraction is what lets you swap storage backends without changing your LangGraph logic.
