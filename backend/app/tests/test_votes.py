import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.models import User
from app.core.auth import set_token_user

TEST_ENGINE = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=TEST_ENGINE)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=TEST_ENGINE)
    yield
    Base.metadata.drop_all(bind=TEST_ENGINE)


@pytest.fixture
def client():
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers(client):
    """创建测试用户并返回 Authorization header"""
    db = TestingSessionLocal()
    # 创建一个测试用户
    user = User(openid="test_openid_123")
    db.add(user)
    db.commit()
    db.refresh(user)
    # 生成 token 并保存
    token = "test_token_123"
    set_token_user(token, user.id)
    db.close()
    return {"Authorization": f"Bearer {token}"}


def _create_wish(client: TestClient, title="测试愿望") -> int:
    res = client.post("/wishes/", json={"title": title})
    return res.json()["id"]


class TestVotesAPI:
    """投票接口单元测试"""

    def test_vote_success(self, client, auth_headers):
        """投票成功，票数增加"""
        wish_id = _create_wish(client)
        res = client.post(f"/wishes/{wish_id}/vote", headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["vote_count"] == 1

    def test_vote_twice_rejected(self, client, auth_headers):
        """重复投票返回 400"""
        wish_id = _create_wish(client)
        client.post(f"/wishes/{wish_id}/vote", headers=auth_headers)
        res = client.post(f"/wishes/{wish_id}/vote", headers=auth_headers)
        assert res.status_code == 400
        assert "已经投过票" in res.json()["detail"]

    def test_vote_without_auth(self, client):
        """未登录投票返回 401"""
        wish_id = _create_wish(client)
        res = client.post(f"/wishes/{wish_id}/vote")
        assert res.status_code == 401

    def test_vote_wish_not_found(self, client, auth_headers):
        """对不存在的愿望投票返回 404"""
        res = client.post("/wishes/9999/vote", headers=auth_headers)
        assert res.status_code == 404

    def test_unvote_success(self, client, auth_headers):
        """取消投票成功，票数减少"""
        wish_id = _create_wish(client)
        client.post(f"/wishes/{wish_id}/vote", headers=auth_headers)
        res = client.delete(f"/wishes/{wish_id}/vote", headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["vote_count"] == 0

    def test_unvote_without_voting(self, client, auth_headers):
        """未投票就取消返回 400"""
        wish_id = _create_wish(client)
        res = client.delete(f"/wishes/{wish_id}/vote", headers=auth_headers)
        assert res.status_code == 400
        assert "尚未投过票" in res.json()["detail"]

    def test_check_voted_false(self, client, auth_headers):
        """未投票时返回 false"""
        wish_id = _create_wish(client)
        res = client.get(f"/wishes/{wish_id}/voted", headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["voted"] is False

    def test_check_voted_true(self, client, auth_headers):
        """投票后返回 true"""
        wish_id = _create_wish(client)
        client.post(f"/wishes/{wish_id}/vote", headers=auth_headers)
        res = client.get(f"/wishes/{wish_id}/voted", headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["voted"] is True

    def test_different_user_can_vote(self, client):
        """不同用户可以给同一愿望投票"""
        # 创建两个用户
        db = TestingSessionLocal()
        user1 = User(openid="user1_openid")
        user2 = User(openid="user2_openid")
        db.add(user1)
        db.add(user2)
        db.commit()
        db.refresh(user1)
        db.refresh(user2)
        set_token_user("token_user1", user1.id)
        set_token_user("token_user2", user2.id)
        db.close()

        wish_id = _create_wish(client)
        res = client.post(f"/wishes/{wish_id}/vote", headers={"Authorization": "Bearer token_user1"})
        assert res.status_code == 200
        assert res.json()["vote_count"] == 1

        res = client.post(f"/wishes/{wish_id}/vote", headers={"Authorization": "Bearer token_user2"})
        assert res.status_code == 200
        assert res.json()["vote_count"] == 2

    def test_list_sorted_by_votes(self, client):
        """列表按票数排序正确"""
        # 创建两个用户
        db = TestingSessionLocal()
        user1 = User(openid="sort_user1")
        user2 = User(openid="sort_user2")
        db.add(user1)
        db.add(user2)
        db.commit()
        db.refresh(user1)
        db.refresh(user2)
        set_token_user("sort_token1", user1.id)
        set_token_user("sort_token2", user2.id)
        db.close()

        id1 = _create_wish(client, "愿望A")
        id2 = _create_wish(client, "愿望B")
        id3 = _create_wish(client, "愿望C")

        # 愿望B有2票
        client.post(f"/wishes/{id2}/vote", headers={"Authorization": "Bearer sort_token1"})
        client.post(f"/wishes/{id2}/vote", headers={"Authorization": "Bearer sort_token2"})
        # 愿望C有1票
        client.post(f"/wishes/{id3}/vote", headers={"Authorization": "Bearer sort_token1"})

        res = client.get("/wishes/?sort=votes")
        titles = [w["title"] for w in res.json()]
        assert titles == ["愿望B", "愿望C", "愿望A"]
