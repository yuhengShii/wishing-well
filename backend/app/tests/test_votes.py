import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db

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


def _create_wish(client: TestClient, title="测试愿望") -> int:
    res = client.post("/wishes/", json={"title": title})
    return res.json()["id"]


class TestVotesAPI:
    """投票接口单元测试"""

    def test_vote_success(self, client):
        """投票成功，票数增加"""
        wish_id = _create_wish(client)
        res = client.post(f"/wishes/{wish_id}/vote")
        assert res.status_code == 200
        assert res.json()["vote_count"] == 1

    def test_vote_twice_rejected(self, client):
        """重复投票返回 400"""
        wish_id = _create_wish(client)
        client.post(f"/wishes/{wish_id}/vote")
        res = client.post(f"/wishes/{wish_id}/vote")
        assert res.status_code == 400
        assert "已经投过票" in res.json()["detail"]

    def test_vote_wish_not_found(self, client):
        """对不存在的愿望投票返回 404"""
        res = client.post("/wishes/9999/vote")
        assert res.status_code == 404

    def test_unvote_success(self, client):
        """取消投票成功，票数减少"""
        wish_id = _create_wish(client)
        client.post(f"/wishes/{wish_id}/vote")
        res = client.delete(f"/wishes/{wish_id}/vote")
        assert res.status_code == 200
        assert res.json()["vote_count"] == 0

    def test_unvote_without_voting(self, client):
        """未投票就取消返回 400"""
        wish_id = _create_wish(client)
        res = client.delete(f"/wishes/{wish_id}/vote")
        assert res.status_code == 400
        assert "尚未投过票" in res.json()["detail"]

    def test_check_voted_false(self, client):
        """未投票时返回 false"""
        wish_id = _create_wish(client)
        res = client.get(f"/wishes/{wish_id}/voted")
        assert res.status_code == 200
        assert res.json()["voted"] is False

    def test_check_voted_true(self, client):
        """投票后返回 true"""
        wish_id = _create_wish(client)
        client.post(f"/wishes/{wish_id}/vote")
        res = client.get(f"/wishes/{wish_id}/voted")
        assert res.status_code == 200
        assert res.json()["voted"] is True

    def test_different_client_can_vote(self, client):
        """不同客户端可以给同一愿望投票"""
        wish_id = _create_wish(client)
        client.post(f"/wishes/{wish_id}/vote", headers={"X-Client-ID": "user_a"})
        res = client.post(
            f"/wishes/{wish_id}/vote", headers={"X-Client-ID": "user_b"}
        )
        assert res.status_code == 200
        assert res.json()["vote_count"] == 2

    def test_list_sorted_by_votes(self, client):
        """列表按票数排序正确"""
        id1 = _create_wish(client, "愿望A")
        id2 = _create_wish(client, "愿望B")
        id3 = _create_wish(client, "愿望C")
        client.post(f"/wishes/{id2}/vote", headers={"X-Client-ID": "u1"})
        client.post(f"/wishes/{id2}/vote", headers={"X-Client-ID": "u2"})
        client.post(f"/wishes/{id3}/vote", headers={"X-Client-ID": "u1"})

        res = client.get("/wishes/?sort=votes")
        titles = [w["title"] for w in res.json()]
        assert titles == ["愿望B", "愿望C", "愿望A"]
