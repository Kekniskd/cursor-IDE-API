from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_and_read_post():
    # Test creating a post
    post_data = {
        "title": "Test Post",
        "content": "Test Content",
        "author": "Test Author"
    }
    response = client.post("/posts/", json=post_data)
    assert response.status_code == 201
    created_post = response.json()
    post_id = created_post["id"]
    
    # Test reading the created post
    response = client.get(f"/posts/{post_id}")
    assert response.status_code == 200
    assert response.json()["title"] == post_data["title"]
    assert response.json()["content"] == post_data["content"]
    assert response.json()["author"] == post_data["author"]

def test_get_all_posts():
    # Create a test post first
    post_data = {
        "title": "Another Post",
        "content": "More Content",
        "author": "Another Author"
    }
    client.post("/posts/", json=post_data)
    
    # Test getting all posts
    response = client.get("/posts/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_update_post():
    # Create a post first
    post_data = {
        "title": "Original Title",
        "content": "Original Content",
        "author": "Original Author"
    }
    response = client.post("/posts/", json=post_data)
    post_id = response.json()["id"]
    
    # Update the post
    update_data = {
        "title": "Updated Title",
        "content": "Updated Content",
        "author": "Updated Author"
    }
    response = client.put(f"/posts/{post_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["title"] == update_data["title"]
    assert response.json()["content"] == update_data["content"]
    assert response.json()["author"] == update_data["author"]

def test_delete_post():
    # Create a post first
    post_data = {
        "title": "Post to Delete",
        "content": "Content to Delete",
        "author": "Author to Delete"
    }
    response = client.post("/posts/", json=post_data)
    post_id = response.json()["id"]
    
    # Delete the post
    response = client.delete(f"/posts/{post_id}")
    assert response.status_code == 204
    
    # Verify post is deleted
    response = client.get(f"/posts/{post_id}")
    assert response.status_code == 404 