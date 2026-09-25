from pydantic import BaseModel


class TaskSchema(BaseModel):   
     title:str
     discription:str
     is_completed:bool=False