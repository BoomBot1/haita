import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from src.models.base import Base
from sqlalchemy.orm import sessionmaker, Session
from src.main import app
from src.api.deps import get_db

TEST_DATABASE_URI = 'sqlite:///test.db'


@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine(
        TEST_DATABASE_URI,
        connect_args={"check_same_thread": False},
        echo=False,
    )

    Base.metadata.create_all(bind=engine)

    yield engine

    engine.dispose()


@pytest.fixture
def db_session(test_engine):
    connection = test_engine.connect()
    transaction = connection.begin()

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=connection,
    )

    session = TestingSessionLocal()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def override_get_db(db_session):
    """Override the get_db dependency."""

    def _override_get_db():
        try:
            yield db_session
        finally:
            pass

    return _override_get_db


@pytest.fixture
def test_client(override_get_db):
    """Create test client."""
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def test_question(db_session):
    """Create a test question."""
    from src.models.question import Question

    question = Question(text="Test question")
    db_session.add(question)
    db_session.commit()
    db_session.refresh(question)

    return question


@pytest.fixture
def test_answer(db_session, test_question):
    """Create a test answer."""
    from src.models.answer import Answer

    answer = Answer(
        text="Test answer",
        user_id="test-user-123",
        question_id=test_question.id
    )
    db_session.add(answer)
    db_session.commit()
    db_session.refresh(answer)

    return answer