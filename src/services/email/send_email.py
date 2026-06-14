import os
import resend
from dotenv import load_dotenv
from abc import ABC, abstractmethod
from fastapi import HTTPException
from pydantic import EmailStr
from src.services.email.html_gerator_ import create_html, create_html_changed_password
import logging
logger = logging.getLogger(__name__)
load_dotenv()
resend.api_key = os.getenv("RESEND.API_KEY")

class SendService(ABC):
    @abstractmethod
    def send_emails(self, email_end: str, nome: str, token: str):
        pass

class GmailSendServiceCreateAccount(SendService):
    def send_emails(self, email_end: EmailStr, nome: str, token: str) -> dict[str, str] | None:
        html = create_html(name=nome, code=token,  email=email_end)
        try:
            resend.Emails.send({
                "from": "onboarding@resend.dev",
                "to": email_end,
                "subject": "send code for activing account",
                "html": html
            })
            return {"menssage": "code sent successfully"}
        except Exception as e:
            logger.error(f"error in sending email, {e}")
            raise HTTPException(status_code=500, detail="error in sending email")

class GmailSendChangedPasswordService(SendService):
    def send_emails(self, email_end: EmailStr, nome: str, token: str) -> dict[str, str] | None:
        html = create_html_changed_password(name=nome, code=token)
        try:
            resend.Emails.send({
                "from": "onboarding@resend.dev",
                "to": email_end,
                "subject": "send code for activing account",
                "html": html
            })
            return {"menssage": "code sent successfully"}
        except Exception as e:
            logger.error(f"error in sending email, {e}")
            raise HTTPException(status_code=500, detail="error in sending email")
def send_service():
    return GmailSendServiceCreateAccount()