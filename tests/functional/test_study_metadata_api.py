"""Tests for the Study Metadata API endpoints"""
import json
import pytest

def test_get_arm_metadata(test_client):
  """
  GIVEN a Flask application configured for testing and a study ID
  WHEN the '/study/{study_id}/arm/metadata' endpoint is requested (GET)
  THEN check that the response is valid and retrieves the arm metadata
  """
  study_id = pytest.global_study_id["id"]
  response = test_client.get(f"/study/{study_id}/metadata/arm")
  response_data = json.loads(response.data)
  assert response.status_code == 200
  print(response_data)

def test_post_arm_metadata(test_client):
  """
  Given a Flask application configured for testing and a study ID
  WHEN the '/study/{study_id}/metadata/arm' endpoint is requested (POST)
  THEN check that the response is vaild and create a new arm
  """
  study_id = pytest.global_study_id["id"]