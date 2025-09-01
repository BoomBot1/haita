import pytest
from httpx import Client


class TestAnswersAPI:
    def test_create_answer(self, test_client: Client, test_question):
        answer_data = {
            "text": "This is a test answer",
            "user_id": "test-user-456",
        }

        response = test_client.post(f"/api/v1/questions/{test_question.id}/answers/", json=answer_data)
        data = response.json()
        print(data)

        assert response.status_code == 201

    def test_get_answer(self, test_client: Client, test_answer):
        response = test_client.get(f"/api/v1/answers/{test_answer.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_answer.id
        assert data["text"] == test_answer.text
        assert data["user_id"] == test_answer.user_id

    def test_get_nonexistent_answer(self, test_client: Client):
        response = test_client.get("/api/v1/answers/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Answer not found"

    def test_delete_answer(self, test_client: Client, test_answer):
        response = test_client.delete(f"/api/v1/answers/{test_answer.id}")

        assert response.status_code == 204

        # Verify the answer was deleted
        response = test_client.get(f"/api/v1/answers/{test_answer.id}")
        assert response.status_code == 404

    def test_delete_nonexistent_answer(self, test_client: Client):
        response = test_client.delete("/api/v1/answers/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Answer not found"

    def test_create_answer_validation_error(self, test_client: Client, test_question):
        invalid_data = {
            "text": "",  # Empty text
            "user_id": "test-user",
        }

        response = test_client.post(f"/api/v1/questions/{test_question.id}/answers/", json=invalid_data)

        assert response.status_code == 422

    def test_create_answer_to_nonexistent_question(self, test_client: Client):
        data = {
            "text": "This is a test answer",
            "user_id": "test-user",
        }

        response = test_client.post(f"/api/v1/questions/999/answers/", json=data)

        assert response.status_code == 404