import re

import pydantic
from errors import HttpError


class BaseValidator(pydantic.BaseModel):
    pass


class UserValidator(BaseValidator):
    username: str
    password: str
    email: str

    @pydantic.field_validator('password')
    @classmethod
    def validate_password(cls, value):
        if not re.fullmatch(r'(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}', value):
            raise ValueError("Password must include at least one uppercase "
                             "English letter, at least one lowercase English "
                             "letter, at least one digit and be at least 8 "
                             "characters long.")
        return value

    @pydantic.field_validator('email')
    @classmethod
    def validate_email(cls, value):
        if not re.fullmatch(r'\S+@\S+\.\S+', value):
            raise ValueError("Not a valid email address.")
        return value


class UserLoginValidator(BaseValidator):
    username: str | None = None
    email: str | None = None
    password: str


class UserUpdateValidator(UserValidator):
    username: str | None = None
    password: str | None = None
    email: str | None = None


class AdvertisementValidator(BaseValidator):
    title: str
    description: str


class AdvertisementUpdateValidator(AdvertisementValidator):
    title: str | None = None
    description: str | None = None


def validate_data(data: dict, schema_class: type[BaseValidator]) -> dict:
    try:
        model = schema_class(**data)
        return model.model_dump(exclude_unset=True)
    except pydantic.ValidationError as e:
        errors = e.errors()
        for error in errors:
            error.pop('ctx', None)
        raise HttpError(400, errors)
