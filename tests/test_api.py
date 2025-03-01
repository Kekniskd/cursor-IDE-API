from fastapi.testclient import TestClient

def test_root_endpoint(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from cursor-learn!"}

def test_process_name_endpoint(client: TestClient):
    # Test with a valid name
    response = client.post("/name", json={"name": "John"})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello, John!"
    assert data["letter_counts"] == {"j": 1, "o": 1, "h": 1, "n": 1}

    # Test with an empty name
    response = client.post("/name", json={"name": ""})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello, !"
    assert data["letter_counts"] == {}

    # Test with invalid payload
    response = client.post("/name", json={})
    assert response.status_code == 422  # Validation error

    # Test with special characters
    response = client.post("/name", json={"name": "John123!@#"})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello, John123!@#!"
    assert data["letter_counts"] == {"j": 1, "o": 1, "h": 1, "n": 1} 