import os
import resend
from dotenv import load_dotenv
from abc import ABC, abstractmethod
from src.services.email.html_gerator_ import create_html
from src.services.email.code_gerator import create_token
from src.services.email.create_redis import saved_redis
load_dotenv()
resend.api_key = os.getenv("RESEND.API_KEY")

class SendService(ABC):
    @abstractmethod
    def send_emails(self, email_end: str, nome: str):
        pass

#it method call function for create token, store in redis, and call the function for render template,
# and finally send email
class GmailSendService(SendService):
    def send_emails(self, email_end: str, nome: str):
        token = create_token()
        saved_redis(email_end=email_end, code=token)
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

def send_service():
    return GmailSendService()