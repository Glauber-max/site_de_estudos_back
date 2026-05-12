#now here I will write filters code
from pydantic import BaseModel, ConfigDict

#basic filter for create user
class CreateUser(BaseModel):
    nome: str
    email: str
    senha: str

class UserResponse(BaseModel):
    nome: str
    email: str
    senha: str
    model_config = ConfigDict(from_attributes=True)