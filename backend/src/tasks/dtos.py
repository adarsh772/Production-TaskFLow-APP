from pydantic import BaseModel, ConfigDict


class TaskSchema(BaseModel):
    title: str
    description: str
    is_completed: bool = False


class TaskResponseSchema(TaskSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
