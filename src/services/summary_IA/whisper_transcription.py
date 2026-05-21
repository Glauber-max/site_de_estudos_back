from faster_whisper import WhisperModel
from abc import ABC, abstractmethod
import os
class Transcription(ABC):
    @abstractmethod
    def transcribe(self, transcription: WhisperModel):
        pass

class WhisperTranscription(Transcription):
    def __init__(self):
        self.model = WhisperModel("base", device="cpu", compute_type="int8")

    def transcribe(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError("path invalid or not found")
        segments, info = self.model.transcribe(file_path, beam_size=5)
        text_final: str = ""
        for segment in segments:
            text_final += segment.text + " "
        return text_final


