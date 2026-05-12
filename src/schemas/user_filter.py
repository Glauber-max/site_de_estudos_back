#now here I will write filters code
from pydantic import BaseModel, ConfigDict, EmailStr


#basic filter for create user
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