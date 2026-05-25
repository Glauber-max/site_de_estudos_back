import os
import uuid
from abc import ABC, abstractmethod
from pytubefix import YouTube
from pytubefix.cli import on_progress
from src.services.summary_IA.ia_factory import FactoryTranscription

class CreateSummary(ABC):
    @abstractmethod
    def get_audio_from_youtube(self, url: str) -> str:
        pass

    @abstractmethod
    def get_transcription_from_archive(self, filepath: str) -> str:
        pass

class CreateSummaryFromYoutube(CreateSummary):
    def get_audio_from_youtube(self, url: str) -> str:
        id_aleatorio = str(uuid.uuid7())
        yt = YouTube(url, on_progress_callback=on_progress)
        yt_audio = yt.streams.get_audio_only(subtype='mp3')
        if yt_audio is None:
            raise Exception('No audio found')
        yt_audio.download(output_path="downloads_audio", filename= id_aleatorio)
        return f"downloads_audio/{id_aleatorio}"

    def get_transcription_from_archive(self, filepath: str) -> str:
        transcription = FactoryTranscription.factory_method("whisper")
        if transcription is None:
            raise Exception('get out transcription from archive')
        text = transcription.transcribe(filepath)
        os.remove(filepath)
        return text
