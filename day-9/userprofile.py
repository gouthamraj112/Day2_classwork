from typing import List, Optional,TypedDict

class UserProfile(TypedDict):
    id: int
    name: str
    email: str
    bio:Optional[str]
def format_user_profile(users:List[UserProfile])->List:
    return [f"{u['name']}({u['email']})" for u in users]

users=[
    {
        "id":1,
        "name":"Alice",
        "email":"alice@example.com",
        "bio":None
    },
    {
        "id":2,
        "name":"Bob",
        "email":"bob@example.com",
        "bio":"junior developer"
    }
]
print(format_user_profile(users))
#print(format_user_profile([1,"xyz","xyz@gmail.com"]))