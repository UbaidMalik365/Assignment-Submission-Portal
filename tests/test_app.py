import pytest
import app as portal


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Use a temporary file so tests never touch your real submissions.json
    monkeypatch.setattr(portal, "DATA_FILE", str(tmp_path / "test_submissions.json"))
    portal.app.config["TESTING"] = True
    return portal.app.test_client()


def test_valid_submission_is_saved_and_listed(client):
    response = client.post("/", data={
        "name": "Ali Khan",
        "reg_no": "2022-CS-123",
        "title": "DevOps Assignment 1",
        "url": "https://github.com/ali/devops-assignment",
    })
    assert response.status_code == 200
    assert b"Submission saved successfully!" in response.data

    saved = portal.load_submissions()
    assert len(saved) == 1
    assert saved[0]["reg_no"] == "2022-CS-123"

    # It must also appear in the list when the page is loaded again
    page = client.get("/")
    assert b"Ali Khan" in page.data
    assert b"2022-CS-123" in page.data


def test_missing_registration_number_is_rejected(client):
    response = client.post("/", data={
        "name": "Ali Khan",
        "reg_no": "",
        "title": "DevOps Assignment 1",
        "url": "https://github.com/ali/devops-assignment",
    })
    assert b"Registration number is required" in response.data
    assert portal.load_submissions() == []


def test_invalid_url_is_rejected_and_not_saved(client):
    response = client.post("/", data={
        "name": "Ali Khan",
        "reg_no": "2022-CS-123",
        "title": "DevOps Assignment 1",
        "url": "not-a-url",
    })
    assert b"Invalid URL" in response.data
    assert portal.load_submissions() == []