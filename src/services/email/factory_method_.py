from src.services.email.send_email import GmailSendServiceCreateAccount, GmailSendChangedPasswordService
class FactoryMessage:
    _types_of_messages = {
        "create_account": GmailSendServiceCreateAccount(),
        "change_password": GmailSendChangedPasswordService(),
    }
    @classmethod
    def factory_method(cls, tipo: str):
        return cls._types_of_messages.get(tipo)
