"""User factory for generating dummy test data."""

from uuid import uuid4
from faker import Faker
from models.user import UserRegister, UserLogin, UserTitle
from typing import Optional


fake = Faker("en_US")

# Constants
DEFAULT_PASSWORD = "Test@1234"
YOPMAIL_DOMAIN = "yopmail.com"


def make_register_user(**overrides) -> UserRegister:
    """
    Generate a valid user registration object.
    
    Each call creates a new user with unique email (qa_<uuid>@yopmail.com).
    Password is fixed to "Test@1234" for test predictability.
    
    Args:
        **overrides: Optional field overrides (e.g., email="custom@mail.com")
    
    Returns:
        UserRegister: Valid user object for registration tests.
    
    Example:
        >>> user = make_register_user()
        >>> user.email
        'qa_a1b2c3d4@yopmail.com'
        >>> user.password
        'Test@1234'
        
        >>> user = make_register_user(name="John Doe")
        >>> user.name
        'John Doe'
    """
    unique_id = uuid4().hex[:8]
    
    default_data = {
        "name": fake.name(),
        "email": f"qa_{unique_id}@{YOPMAIL_DOMAIN}",
        "password": DEFAULT_PASSWORD,
        "title": UserTitle.MR,
        "birth_date": fake.random_int(min=1, max=28),
        "birth_month": fake.random_int(min=1, max=12),
        "birth_year": fake.random_int(min=1980, max=2000),
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "address1": fake.street_address(),
        "address2": fake.secondary_address(),
        "country": "United States",
        "zipcode": fake.zipcode(),
        "state": fake.state(),
        "city": fake.city(),
        "mobile_number": fake.phone_number(),
        "company": fake.company(),
    }
    
    # Apply overrides
    default_data.update(overrides)
    
    return UserRegister(**default_data)


def make_login_user(**overrides) -> UserLogin:
    """
    Generate a valid user login object.
    
    Email is unique (qa_<uuid>@yopmail.com) and password is "Test@1234".
    Use overrides to simulate invalid credentials for negative tests.
    
    Args:
        **overrides: Optional field overrides (e.g., email="invalid@mail.com")
    
    Returns:
        UserLogin: Valid login credentials object.
    
    Example:
        >>> login = make_login_user()
        >>> login.email
        'qa_a1b2c3d4@yopmail.com'
        
        >>> login = make_login_user(email="nonexistent@mail.com", password="wrong")
        >>> login.email
        'nonexistent@mail.com'
        >>> login.password
        'wrong'
    """
    unique_id = uuid4().hex[:8]
    
    default_data = {
        "email": f"qa_{unique_id}@{YOPMAIL_DOMAIN}",
        "password": DEFAULT_PASSWORD,
    }
    
    # Apply overrides
    default_data.update(overrides)
    
    return UserLogin(**default_data)


def make_invalid_users() -> list[dict]:
    """
    Generate a list of invalid user credentials for negative testing.
    
    Returns a hardcoded list of common invalid scenarios to test
    error handling and validation.
    
    Returns:
        list[dict]: List of invalid user dicts with 'email', 'password', 'reason'.
    
    Example:
        >>> invalid_users = make_invalid_users()
        >>> len(invalid_users)
        6
        >>> invalid_users[0]
        {'email': 'invalidemail.com', 'password': 'Test@1234', 'reason': 'email without @'}
    """
    return [
        {
            "email": "invalidemail.com",
            "password": DEFAULT_PASSWORD,
            "reason": "email without @",
        },
        {
            "email": "",
            "password": DEFAULT_PASSWORD,
            "reason": "empty email",
        },
        {
            "email": f"qa_{uuid4().hex[:8]}@{YOPMAIL_DOMAIN}",
            "password": "",
            "reason": "empty password",
        },
        {
            "email": "test@",
            "password": DEFAULT_PASSWORD,
            "reason": "email with incomplete domain",
        },
        {
            "email": "test @mail.com",
            "password": DEFAULT_PASSWORD,
            "reason": "email with spaces",
        },
        {
            "email": f"qa_{uuid4().hex[:8]}@{YOPMAIL_DOMAIN}",
            "password": "aB1",
            "reason": "password too short",
        },
    ]
