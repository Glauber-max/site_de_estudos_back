from pydantic import BaseModel, ConfigDict, EmailStr



class CreateUser(BaseModel):
    nome: str
    email: EmailStr
    senha: str

class UserResponse(BaseModel):
    nome: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    senha: str

class ChangePassword(BaseModel):
    email: EmailStr

class ChangePasswordValidation(BaseModel):
    email: EmailStr
    token: str
    senha: str

class RefreshToken(BaseModel):
    refresh_token: str