import os
import resend
from dotenv import load_dotenv
from abc import ABC, abstractmethod


load_dotenv()

class SendService(ABC):
    @abstractmethod
    def send_email(self, email_end: str, code: str):
        pass

class GmailSendService(SendService):
    def send_email(self, email_end: str, code: str):
        pass
