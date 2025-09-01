import factory
from datetime import datetime
from src.models.question import Question as QuestionModel
from src.models.answer import Answer as AnswerModel


class QuestionFactory(factory.Factory):
    class Meta:
        model = QuestionModel

    id = factory.Sequence(lambda n: n+1)
    text = factory.Faker('sentence')
    created_at = factory.LazyFunction(datetime.now)


class AnswerFactory(factory.Factory):
    class Meta:
        model = AnswerModel

    id = factory.Sequence(lambda n: n+1)
    text = factory.Faker('sentence')
    user_id = factory.Faker('uuid4')
    question_id = factory.Sequence(lambda n: n + 1)
    created_at = factory.LazyFunction(datetime.utcnow)