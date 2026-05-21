from pydantic import BaseModel, HttpUrl, Field, field_validator
from fastapi import HTTPException

class SchemaCreateSummaryFromYoutube(BaseModel):
    url: HttpUrl
    @field_validator('url')
    @classmethod
    def url_validator(cls, v: HttpUrl) -> HttpUrl:
        url_str = str(v)
        if "youtube.com" not in url_str and "youtu.be" not in url_str:
            raise HTTPException(status_code=400, detail="Invalid URL")
        return v

class SummaryCreate(BaseModel):
    subject: str = Field(description="Um título ou assunto curto, claro e direto para o resumo.")
    content: str = Field(description="O resumo detalhado e estruturado do conteúdo fornecido seguindo as regras do prompt.")