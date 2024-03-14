import pytest
from app import schema
import uuid

# GET Endpoints Tests
def test_get_all_posts(authorized_client, test_user, test_posts):
    res = authorized_client.get("/posts/")
    def validate(post):
        return schema.PostOut(**post)
    posts_map = map(validate, res.json()['data'])
    posts_list = list(posts_map)
    user_posts = [post for post in test_posts if str(post.user_id) == str(test_user['id'])]
    assert len(res.json()['data']) == len(user_posts)
    assert res.status_code == 200
    
def test_unauthorized_user_get_all_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401
def test_get_post_not_exist(authorized_client, test_posts):
    non_existent_uuid = uuid.uuid4()
    res = authorized_client.get(f"/posts/{non_existent_uuid}")
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post_data = res.json().get('post_detail')  # extract the 'post_detail' from the response
    post = schema.PostOut(**post_data)
    assert post.id == test_posts[0].id

# POST Endpoint Tests
@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "i love pepperoni", False),
    ("tallest skyscrapers", "wahoo", True),
])
def test_create_post(authorized_client, test_user, title, content, published):
    res = authorized_client.post(
        "/posts/", json={"title": title, "content": content, "published": published})

    created_post = schema.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert str(created_post.user_id) == test_user['id']

def test_create_post_default_published_true(authorized_client, test_user):
    res = authorized_client.post(
        "/posts/", json={"title": "arbitrary title", "content": "content lang"})

    created_post = schema.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "arbitrary title"
    assert created_post.content == "content lang"
    assert created_post.published == True
    assert str(created_post.user_id) == test_user['id']

def test_unauthorized_user_create_post(client, test_user):
    res = client.post(
        "/posts/", json={"title": "arbitrary title", "content": "content lang"})
    assert res.status_code == 401

# DELETE Endpoint Tests
def test_unauthorized_user_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post_success(authorized_client, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[0].id}")

    assert res.status_code == 204

def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    non_existent_uuid = uuid.uuid4()
    res = authorized_client.delete(
        f"/posts/{non_existent_uuid}")
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

# UPDATE Endpoints Test
def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": str(test_posts[0].id)

    }
    res = authorized_client.put(f"/posts/{str(test_posts[0].id)}", json=data)
    updated_post = schema.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']


def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": str(test_posts[3].id)

    }
    res = authorized_client.put(f"/posts/{str(test_posts[3].id)}", json=data)
    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_user, test_posts):
    res = client.put(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": str(test_posts[3].id)

    }
    non_existent_uuid = uuid.uuid4()
    res = authorized_client.put(
        f"/posts/{non_existent_uuid}", json=data)
    assert res.status_code == 404