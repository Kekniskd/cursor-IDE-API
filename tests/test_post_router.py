from fastapi.testclient import TestClient
from uuid import UUID

def test_create_post(client: TestClient):
    post_data = {
        "title": "Test Post",
        "content": "This is a test post",
        "author": "Test Author"
    }
    
    response = client.post("/posts/", json=post_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == post_data["title"]
    assert data["content"] == post_data["content"]
    assert data["author"] == post_data["author"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data
    
    # Store post_id for other tests
    return data["id"]

def test_get_all_posts(client: TestClient):
    response = client.get("/posts/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_post(client: TestClient):
    # First create a post
    post_id = test_create_post(client)
    
    # Get the post
    response = client.get(f"/posts/{post_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == post_id

def test_update_post(client: TestClient):
    # First create a post
    post_id = test_create_post(client)
    
    update_data = {
        "title": "Updated Title",
        "content": "Updated content",
        "author": "Updated Author"
    }
    
    response = client.put(f"/posts/{post_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["content"] == update_data["content"]
    assert data["author"] == update_data["author"]

def test_delete_post(client: TestClient):
    # First create a post
    post_id = test_create_post(client)
    
    # Delete the post
    response = client.delete(f"/posts/{post_id}")
    assert response.status_code == 204
    
    # Verify post is deleted
    response = client.get(f"/posts/{post_id}")
    assert response.status_code == 404 