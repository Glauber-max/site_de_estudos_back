from src.services.question_IA.create_question_with_ia import QuestionMakeForIATwoDotFive, QuestionMakeForIAThreeDotFive


class FactoryQuestionIA:
    _dict_question = {
            "2.5": QuestionMakeForIATwoDotFive(),
            "3.5": QuestionMakeForIAThreeDotFive(),
        }
    @classmethod
    def make_question(cls, ia: str):
        return cls._dict_question.get(ia)