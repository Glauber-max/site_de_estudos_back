import os
import resend
from dotenv import load_dotenv
from abc import ABC, abstractmethod
from pydantic import EmailStr
from src.services.email.html_gerator_ import create_html, create_html_changed_password
from src.services.email.code_gerator import create_token
from src.services.email.create_redis import saved_redis
load_dotenv()
resend.api_key = os.getenv("RESEND.API_KEY")

class SendService(ABC):
    @abstractmethod
    def send_emails(self, email_end: str, nome: str, token: str):
        pass

#it method call function for create token, store in redis, and call the function for render template,
# and finally send email
class GmailSendServiceCreateAccount(SendService):
    def send_emails(self, email_end: str, nome: str, token: str):
        saved_redis(nome=nome, code=token)
        html = create_html(name=nome, code=token, emails=email_end)
        try:
            resend.Emails.send({
                "from": "onboarding@resend.dev",
                "to": email_end,
                "subject": "send code for activing account",
                "html": html
            })
            return {"menssage": "code sent successfully"}
        except Exception as e:
            print(e)

class GmailSendChangedPasswordService(SendService):
    def send_emails(self, email_end: EmailStr, nome: str, token: str):
        saved_redis(key=email_end, code=token)
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
            print(e)
def send_service():
    return GmailSendServiceCreateAccount()