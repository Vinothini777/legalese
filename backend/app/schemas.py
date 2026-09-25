from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AnalysisCreate(BaseModel):
    title: str = Field(default="Legal Analysis", max_length=200)
    issue: str = Field(min_length=5, max_length=10000)
    category: str = Field(default="General", max_length=80)


class AnalysisResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    issue: str
    category: str
    response: str
    created_at: datetime


class DocumentCreate(BaseModel):
    title: str = Field(default="Untitled Document", max_length=200)
    content: str = Field(default="", max_length=50000)


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
