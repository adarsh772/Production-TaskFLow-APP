from src.user.dtos import UserSchema
from sqlalchemy.orm import Session

def registration(db:Session,body:UserSchema):
    print(body)
    return{"Registred sucessfully ."}
