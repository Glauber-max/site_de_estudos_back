from src.services.summary_IA.whisper_transcription import WhisperTranscription
from src.services.summary_IA.gemini_summary import GeminiSummaryFlash, GeminiSummaryGemma
class FactoryTranscription:
    _types_of_transcriptions = {
        "whisper": WhisperTranscription(),
    }
    @classmethod
    def factory_method(cls, tipo: str) -> WhisperTranscription | None: return cls._types_of_transcriptions.get(tipo)

class FactorySummary:
    _types_of_summary = {
        "flash": GeminiSummaryFlash(),
        "gemma": GeminiSummaryGemma(),

    }
    @classmethod
    def factory_method(cls, tipo: str) -> GeminiSummaryFlash | GeminiSummaryGemma:  return cls._types_of_summary.get(tipo)