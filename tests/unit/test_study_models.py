"""Tests for the Study model"""
from model.study import Study


def test_new_study():
    """
    GIVEN a Study model
    WHEN a new Study is created
    THEN check the name, description, and owner fields are defined correctly
    """
    study = Study.from_data(
        {
            "title": "Study1",
            "description": "This is a test study",
            "image": "https://api.dicebear.com/6.x/adventurer/svg",
            "size": "100 GB",
            "keywords": ["test", "study"],
            "last_updated": "2021-01-01",
            "owner": {
                "affiliations": "affiliations1",
                "email": "email1",
                "first_name": "first_name1",
                "last_name": "last_name1",
                "orcid": "orcid1",
                "roles": ["role1", "role2"],
                "permission": "permission1",
                "status": "status1",
            },
        }
    )

    assert study.title == "Study1"
    assert study.description == "This is a test study"
    assert study.image == "https://api.dicebear.com/6.x/adventurer/svg"
    assert study.size == "100 GB"
    assert study.keywords == ["test", "study"]

    assert study.owner.affiliations == "affiliations1"
