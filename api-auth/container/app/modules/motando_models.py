#
# auth/container/app/modules/motando_models.py
#

import re

from pydantic import BaseModel, EmailStr, validator


class LoginModel(BaseModel):
    email: EmailStr
    senha: str

    @validator('senha')
    def senha_validator(cls, value):
        if not re.match('^[A-Za-z0-9_!@#$%^&(*&) ]{10,}$', value):
            raise ValueError('A senha inserida está incorreta.')
        return value