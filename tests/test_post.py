import pytest
from app import schema
import uuid

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    def validate(post):
        return schema.PostOut(**post)
    posts_map = map(validate, res.json()['data'])
    posts_list = list(posts_map)
    assert len(res.json()['data']) == len(test_posts)
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
        f"/posts/{test_posts[1].id}")
    assert res.status_code == 403
