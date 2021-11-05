from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    id: int
    name: str


class UserCreation(BaseModel):
    name: str


users: Dict[int, str] = dict()

not_found_response: Dict[int, Dict[str, str]] = {
    404: {"description": "User not found"}}

duplicated_response: Dict[int, Dict[str, str]] = {
    409: {"description": "User already exists"}}


@app.get("/users", response_model=List[User])
def read_users(filter_name: Optional[str] = None):
    u_list: List[User] = list()
    for user_id, name in users.items():
        if filter_name:
            if filter_name in name:
                u_list.append(User(id=user_id, name=name))
        else:
            u_list.append(User(id=user_id, name=name))

    return u_list


@app.get("/users/{user_id}", response_model=User, responses=not_found_response)
def read_user(user_id: int):
    try:
        user = User(id=user_id, name=users[user_id])
    except Exception:
        error_code = 404
        raise HTTPException(status_code=error_code,
                            detail=not_found_response[error_code]["description"])
    return user


@app.post("/users", response_model=User, responses=duplicated_response)
def create_user(user: UserCreation):
    if user.name in users.values():
        error_code = 409
        raise HTTPException(status_code=error_code,
                            detail=duplicated_response[error_code]["description"])
    try:
        user_id = max(users.keys())
    except ValueError:
        user_id = 0
    user_id += 1
    users[user_id] = user.name
    user = User(id=user_id, name=user.name)
    return user


@app.delete("/users/{user_id}", response_model=User, responses=not_found_response)
def delete_user(user_id: int):
    try:
        user_name = users.pop(user_id)
    except Exception:
        error_code = 404
        raise HTTPException(status_code=error_code,
                            detail=not_found_response[error_code]["description"])
    return User(id=user_id, name=user_name)
