from src.services.email.send_email import GmailSendServiceCreateAccount, GmailSendChangedPasswordService
from src.services.summary_IA.whisper_transcription import WhisperTranscription
class FactoryMessage:
    _types_of_messages = {
        "create_account": GmailSendServiceCreateAccount(),
        "change_password": GmailSendChangedPasswordService(),
    }
    @classmethod
    def factory_method(cls, tipo: str):
        return cls._types_of_messages.get(tipo)

class FactoryTranscription:
    _types_of_transcriptions = {
        "whisper": WhisperTranscription(),
    }
    @classmethod
    def factory_method(cls, tipo: str):
        return cls._types_of_transcriptions.get(tipo)
