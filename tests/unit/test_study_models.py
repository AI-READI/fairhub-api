"""Tests for the Study model"""
from model.study import Study
import uuid


def test_new_study():
    """
    GIVEN a Study model
    WHEN a new Study is created
    THEN check the name, description, and owner fields are defined correctly
    """
    study = Study.from_data(
        {
            "title": "Study1",
            "image": "https://api.dicebear.com/6.x/adventurer/svg",
            "last_updated": "2021-01-01",
        }
    )

    assert study.title == "Study1"
    assert uuid.UUID(study.id)
    assert study.image == "https://api.dicebear.com/6.x/adventurer/svg"

    # assert study.owner.affiliations == "affiliations1"
