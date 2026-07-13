from typing import TypedDict

class Person(TypedDict):
    name: str
    age: int

new_dict: Person = {'name': "Imran", 'age': 12}

print(new_dict['age'])