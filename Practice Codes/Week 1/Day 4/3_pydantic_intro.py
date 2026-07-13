from pydantic import BaseModel, Field, EmailStr
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()

# class Person(BaseModel):
#     name: str


# new_person = {'name': 'Imran Butt'}

# person = Person(**new_person)

# class Student(BaseModel):
#     name: str
#     age: int
#     CGPA: float


# student = Student(
#     name="Imran Butt",
#     age= 12,
#     CGPA=9.3
# )
# print(student)

# student = Student(
#     name="Imran Butt",
#     age= "Yoah",
#     CGPA=9.3
# )

# print(student)

# also let's add descriptions(helping the model understand what each field represents.)
# class Lesson(BaseModel):
#     topic: str = Field(description="Name of the TOPIC")
#     difficulty: int = Field(description="Return Difficuly Level in INTEGER NOT STRING")
#     summery: str = Field(description="That's the Summery of the topic")
#     example: str = Field(description="Include One Example")


# # Let's now add some Validation Rules 
# # 
# class Lesson2(BaseModel):
#     topic: str = Field(description="Name of the TOPIC")
#     difficulty: int = Field(gt=0, lt=10, default = 5) # validation
#     summery: str = Field(description="That's the Summery of the topic")
#     example: str =  Field(min_length=3, max_length=200, description="Wirte the Short Summery of MiximumLength (200)") # Validation Rule
#     auther: str = "Imran Butt" # With Default Value
#     compony: Optional[int] = 32

# model = ChatGroq(model = 'llama-3.3-70b-versatile',
#                  groq_api_key = os.getenv('GROQ_API_KEY'))  # llama-3.3-70b-versatile


# structured_model = model.with_structured_output(Lesson2)

# result = structured_model.invoke('What is AI? And What Impacts does it has on FUTURE JOBS?')

# print(result)

# print()
# print()

# print("TOPIC:", result.topic)
# print()
# print("Difficulty:", result.difficulty)
# print()
# print("Summery:", result.summery)
# print()
# print("Example:", result.example)
# print()
# print("Auther:", result.auther)

# print()
# print("Compony:", result.compony)



class Student(BaseModel):
    name: str
    email: EmailStr

new_student = {'name': "imran butt", 'email': 'imran@gmail.com'}

student = Student(**new_student)
print(student)

# new_student1 = {'name': "imran butt", 'email': 'imran@gmailcom'}


# student = Student(**new_student1)

# Using through DIct
student_dic = dict(student)
print()
print("Dictionary",student_dic)
print()
print(student_dic['name'])

print()

# Converting to JSON

student_json = student.model_dump_json()
print("IN JSON FOrmat")
print(student_json)


