import os

DB_Path = os.path.join(os.path.dirname(__file__),'expenses.db')

print(DB_Path)
print(os.path.exists(DB_Path))