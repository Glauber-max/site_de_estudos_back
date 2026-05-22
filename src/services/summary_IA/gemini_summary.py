
import os
from abc import abstractmethod, ABC
from src.schemas.summary_filter import SummaryCreate
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()
api_key_genai = os.getenv("GEMINI_API_KEY")



class SummaryWthIA(ABC):
    def __init__(self):
        self.cliente = genai.Client()
        self.prompt = """Quero que você atue como um resumidor de vídeos de forma objetiva e eficiente. Sua tarefa é analisar o conteúdo do vídeo e produzir um resumo claro, curto e estruturado. O resumo deve conter
        Explique rapidamente qual é o assunto principal do vídeo.  
        Identifique a proposta ou objetivo do autor.
        Liste os tópicos mais relevantes apresentados.  
        Explique cada ponto de forma breve, sem se alongar.  
        Se houver exemplos ou dados importantes, mencione de forma resumida.
        Caso o vídeo seja educativo, descreva o que ele ensina em poucas frases.  
        Resuma instruções ou lições de forma prática e direta.
        Conclusão ou mensagem final
        Mostre como o vídeo termina: conclusão, recomendação ou chamada para ação.  
        Se houver resumo do próprio autor, inclua-o de forma condensada.
        Seja fiel ao conteúdo, sem opiniões pessoais.  
        Use frases curtas e objetivas.  
        O resumo deve ser rápido de ler, mas suficiente para entender o vídeo sem precisar assisti-lo.
        O resumo não deve ser extremamente longo: mantenha a objetividade, economize tempo e foque apenas nos pontos essenciais."""
    @abstractmethod
    def summarize(self, roteiro: str):
        pass

class GeminiSummaryFlash(SummaryWthIA):

    def summarize(self, roteiro: str):
        audio = self.cliente.files.upload(file=roteiro, config={"mime_type": "audio/mp3" })
        configs = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=SummaryCreate,
        )
        response  = self.cliente.models.generate_content(
            model="gemini-2.5-flash",
            contents=[self.prompt, audio],
            config=configs
        )
        return response.text

class GeminiSummaryGemma(SummaryWthIA):
    def summarize(self, roteiro: str):
        configs = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=SummaryCreate,
        )
        response = self.cliente.models.generate_content(
            model="gemma4-31b",
            contents=[self.prompt, f"Aqui está o roteiro do vídeo para resumir:{roteiro}"],
            config=configs
        )
        return response.text