from pydantic import BaseModel,EmailStr




class UserSchema(BaseModel):
    name:str
    username:str
    email:EmailStr
    password:str
    

class UserResponseModel(BaseModel):   
    name:str
    username:str
    email:EmailStr 

class LoginSchema(BaseModel):
     
    username:str
       
    password:str   