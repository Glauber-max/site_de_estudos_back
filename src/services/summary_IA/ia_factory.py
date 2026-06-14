from src.services.summary_IA.whisper_transcription import WhisperTranscription
from src.services.summary_IA.gemini_summary import GeminiSummarythreeDotFive, GeminiSummaryTwoDotFive
class FactoryTranscription:
    _types_of_transcriptions = {
        "whisper": WhisperTranscription(),
    }
    @classmethod
    def factory_method(cls, tipo: str) -> WhisperTranscription | None: return cls._types_of_transcriptions.get(tipo)

class FactorySummary:
    _types_of_summary = {
        "3.5": GeminiSummarythreeDotFive(),
        "2.5": GeminiSummaryTwoDotFive(),

    }
    @classmethod
    def factory_method(cls, tipo: str):  return cls._types_of_summary.get(tipo)