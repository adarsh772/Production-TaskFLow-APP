from pydantic import BaseModel, EmailStr, ConfigDict, field_validator


class UserSchema(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def password_min_length(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return value


class UserResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    username: str
    email: EmailStr


class LoginSchema(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    token: str
    token_type: str = "bearer"
