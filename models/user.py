"""User models for API requests and responses."""

from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from typing import Optional
from enum import Enum


class UserTitle(str, Enum):
    """User title enum."""
    MR = "Mr"
    MRS = "Mrs"
    MISS = "Miss"


class UserLogin(BaseModel):
    """User login model for POST /api/verifyLogin endpoint."""
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    email: EmailStr
    password: str


class UserRegister(BaseModel):
    """User registration model for POST /api/createAccount endpoint."""
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    name: str
    email: EmailStr
    password: str
    title: UserTitle
    birth_date: int
    birth_month: int
    birth_year: int
    firstname: str
    lastname: str
    address1: str
    country: str
    zipcode: str
    state: str
    city: str
    mobile_number: str
    company: Optional[str] = None
    address2: Optional[str] = None
    
    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        """Validate email has @ and domain."""
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("Invalid email format")
        return v
    
    @field_validator("password")
    @classmethod
    def validate_password_not_empty(cls, v: str) -> str:
        """Validate password is not empty."""
        if not v or len(v) == 0:
            raise ValueError("Password cannot be empty")
        return v
    
    @field_validator("birth_date")
    @classmethod
    def validate_birth_date(cls, v: int) -> int:
        """Validate birth date is between 1 and 31."""
        if not 1 <= v <= 31:
            raise ValueError("Birth date must be between 1 and 31")
        return v
    
    @field_validator("birth_month")
    @classmethod
    def validate_birth_month(cls, v: int) -> int:
        """Validate birth month is between 1 and 12."""
        if not 1 <= v <= 12:
            raise ValueError("Birth month must be between 1 and 12")
        return v
    
    @field_validator("birth_year")
    @classmethod
    def validate_birth_year(cls, v: int) -> int:
        """Validate birth year is reasonable."""
        if not 1900 <= v <= 2023:
            raise ValueError("Birth year must be between 1900 and 2023")
        return v


class UserResponse(BaseModel):
    """User response model from API."""
    
    model_config = ConfigDict(populate_by_name=True)
    
    response_code: int
    message: str
    data: Optional[dict] = None
