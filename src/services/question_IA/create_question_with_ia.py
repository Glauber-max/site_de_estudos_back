from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
from abc import abstractmethod, ABC

api_key_genai = os.getenv("GEMINI_API_KEY")
load_dotenv()
from src.schemas.question_filter import CreateQuestionForIa

class MakeQuestion(ABC):
    def __init__(self):
        self.client = genai.Client()
        self.prompt = """
        I want you to act as a professor and high-level exam creator, inspired by a methodology of deep and conceptual teaching (focusing on breaking away from ready-made formulas and developing intellectual maturity). Your task is to analyze the content of the provided summary and produce exactly the number of original questions requested by the student based on it.

The questions must follow the guidelines below:

1. High Difficulty Level
- The main focus should be on questions with Medium to High difficulty. Avoid literal questions that require mere memorization.
- For Humanities/Biological subjects: Focus on critical analysis, dense text interpretation, concept correlation, and complex inferences about what was discussed in the video.
- For Exact Sciences: Focus on problems that require advanced logical reasoning, application of principles in unconventional scenarios, or challenging conceptual manipulations.
- Objective Prompts: Get straight to the technical or conceptual point. Eliminate long or empty contextual texts that do not serve the resolution of the problem.

2. The Anatomy of the Problem (For each question)
Right after the question's prompt, you must provide an answer key and fundamentals structure divided exactly like this:

- A) Correct Answer: Indicate the correct alternative (if multiple choice) or the final answer (if open-ended).
- B) Step-by-Step Resolution: The complete and logical development to reach the result. If math/physics is involved, demonstrate the algebraic or geometric step-by-step.
- C) Fundamentals to Master (The Necessary Base): What are the underlying fundamental concepts the student needs to master to even start thinking about this question? (E.g., "Conservation of energy", "Wave-particle duality", "Contractualism in Philosophy"). Explain how these fundamentals apply here.
- D) The Reasoning Insight: What is the "turning point" (the intellectual breakthrough) that solves the problem? Explain the thought pattern the student needs to develop to see this way out in future problems, instead of just memorizing this specific solution.

 The ultimate goal is not just to test if the student watched the video, but to elevate their reasoning capacity and make them evolve intellectually through the deep analysis of the problem.
        """
    @abstractmethod
    def make_question(self, summary: str, number_of_questions: int):
        pass

class QuestionMakeForIAThreeDotFive(MakeQuestion):
    def make_question(self, summary: str, number_of_questions: int):
        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=CreateQuestionForIa,
        )
        response = self.client.models.generate_content(
            model="gemini-3.5-flash",
            contents=[self.prompt, summary, str(number_of_questions)],
            config=config
        )
        return response.text

class QuestionMakeForIATwoDotFive(MakeQuestion):
    def make_question(self, summary: str, number_of_questions: int):
        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=CreateQuestionForIa,
        )
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[self.prompt, summary, str(number_of_questions)],
            config=config
        )
        return response.text
