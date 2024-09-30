import json

def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post(f"/votes", json={"post_id": test_posts[0].id})
    
    assert res.status_code == 201
    
def test_vote_twice_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post(f"/votes", json={"post_id": test_vote.post_id})
    
    assert res.status_code == 409

def test_vote_post_not_exist(authorized_client):
    res = authorized_client.post(f"/votes", json={"post_id": 99999})
    
    assert res.status_code == 404
    
def test_vote_unauthorized_user(client, test_posts):
    res = client.post(f"/votes", json={"post_id": test_posts[0].id})
    
    assert res.status_code == 401