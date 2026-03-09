"""
Tests for the Mergington High School Activities API
Uses the AAA (Arrange-Act-Assert) pattern.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to a clean state before each test."""
    original_data = {name: dict(details, participants=list(details["participants"]))
                     for name, details in activities.items()}
    yield
    activities.clear()
    activities.update(original_data)


@pytest.fixture
def client():
    return TestClient(app)


class TestGetActivities:
    def test_get_activities_returns_all_activities(self, client):
        # Arrange - client is ready

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 4

    def test_get_activities_includes_chess_club(self, client):
        # Arrange - client is ready

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "Chess Club" in data

    def test_get_activities_have_required_fields(self, client):
        # Arrange - client is ready

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        for activity in data.values():
            assert "description" in activity
            assert "schedule" in activity
            assert "max_participants" in activity
            assert "participants" in activity


class TestSignupForActivity:
    def test_signup_adds_student_to_activity(self, client):
        # Arrange
        email = "newstudent@mergington.edu"
        activity_name = "Chess Club"

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 200
        assert email in activities[activity_name]["participants"]

    def test_signup_returns_success_message(self, client):
        # Arrange
        email = "newstudent@mergington.edu"
        activity_name = "Chess Club"

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 200
        assert "message" in response.json()

    def test_signup_for_nonexistent_activity_returns_404(self, client):
        # Arrange
        email = "student@mergington.edu"
        activity_name = "Nonexistent Activity"

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 404

    def test_signup_duplicate_returns_400(self, client):
        # Arrange
        email = "michael@mergington.edu"
        activity_name = "Chess Club"

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"].lower()


class TestUnregisterFromActivity:
    def test_unregister_removes_student_from_activity(self, client):
        # Arrange
        email = "michael@mergington.edu"
        activity_name = "Chess Club"

        # Act
        response = client.delete(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 200
        assert email not in activities[activity_name]["participants"]

    def test_unregister_returns_success_message(self, client):
        # Arrange
        email = "michael@mergington.edu"
        activity_name = "Chess Club"

        # Act
        response = client.delete(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 200
        assert "message" in response.json()

    def test_unregister_from_nonexistent_activity_returns_404(self, client):
        # Arrange
        email = "student@mergington.edu"
        activity_name = "Nonexistent Activity"

        # Act
        response = client.delete(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 404

    def test_unregister_student_not_in_activity_returns_404(self, client):
        # Arrange
        email = "notregistered@mergington.edu"
        activity_name = "Chess Club"

        # Act
        response = client.delete(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 404
