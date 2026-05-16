
from pytubefix import YouTube
from pytubefix.cli import on_progress
from src.services.factory.factory_method_ import FactoryTranscription


class CreateSummaryFromYoutube:
    def __init__(self, file_name: str):
        self.file_name = file_name
    def get_audio_from_youtube(self, url: str) -> str:
        yt = YouTube(url, on_progress_callback=on_progress)
        yt_audio = yt.streams.get_audio_only(subtype='mp4')
        if yt_audio is None:
            raise Exception('No audio found')
        yt_audio.download(output_path="downloads_audio", filename=self.file_name)
        return "downloads_audio/audio.mp4"

    def get_transcription_from_archive(self, filepath: str) -> None:
        pass
