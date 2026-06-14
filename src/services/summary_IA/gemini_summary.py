
import os
from abc import abstractmethod, ABC
from src.schemas.summary_filter import SummaryCreate
from  google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()
api_key_genai = os.getenv("GEMINI_API_KEY")



class SummaryWthIA(ABC):
    def __init__(self):
        self.cliente = genai.Client()
        self.prompt = """I want you to act as an objective and efficient video summarizer. Your task is to analyze the video's content and produce a clear, short, and structured summary. The summary must contain:

- Quickly explain the main subject of the video.
- Identify the author's proposal or objective.
- List the most relevant topics presented.
- Explain each point briefly, without dragging on.
- If there are important examples or data, mention them briefly.
- If the video is educational, describe what it teaches in a few sentences.
- Summarize instructions or lessons in a practical and direct way.

Conclusion or Final Message:
- Show how the video ends: conclusion, recommendation, or call to action.
- If there is a summary provided by the author, include it in a condensed form.

Guidelines:
- Be faithful to the content, without inserting personal opinions.
- Use short and objective sentences.
- The summary should be quick to read, but comprehensive enough to understand the video without needing to watch it.
- The summary must not be extremely long: maintain objectivity, save time, and focus strictly on the essential points."""
    @abstractmethod
    def summarize(self, roteiro: str):
        pass

class GeminiSummarythreeDotFive(SummaryWthIA):

    def summarize(self, roteiro: str):
        audio = self.cliente.files.upload(file=roteiro, config={"mime_type": "audio/mp3" })
        configs = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=SummaryCreate,
        )
        response  = self.cliente.models.generate_content(
            model="gemini-3.5-flash",
            contents=[self.prompt, audio],
            config=configs
        )
        return response.text

class GeminiSummaryTwoDotFive(SummaryWthIA):
    def summarize(self, roteiro: str):
        audio = self.cliente.files.upload(file=roteiro, config={"mime_type": "audio/mp3"})
        configs = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=SummaryCreate,
        )
        response = self.cliente.models.generate_content(
            model="gemini-2.5-flash",
            contents=[self.prompt, audio],
            config=configs
        )
        return response.text