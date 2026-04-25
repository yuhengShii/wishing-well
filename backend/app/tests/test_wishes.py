import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db

# 测试专用数据库（内存 SQLite，速度快且互不干扰）
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
    """每个测试前重建表结构，确保测试隔离"""
    Base.metadata.create_all(bind=TEST_ENGINE)
    yield
    Base.metadata.drop_all(bind=TEST_ENGINE)


@pytest.fixture
def client():
    """FastAPI 测试客户端，注入测试数据库"""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


class TestWishesAPI:
    """愿望 CRUD 单元测试"""

    def test_create_wish(self, client):
        """创建愿望成功"""
        res = client.post("/wishes/", json={
            "title": "希望有个记账功能",
            "description": "每天记流水太麻烦了",
            "category": "生活",
        })
        assert res.status_code == 201
        data = res.json()
        assert data["title"] == "希望有个记账功能"
        assert data["status"] == "pending"
        assert data["id"] is not None

    def test_create_wish_missing_title(self, client):
        """缺少必填字段返回 422"""
        res = client.post("/wishes/", json={"description": "没有标题"})
        assert res.status_code == 422

    def test_list_wishes(self, client):
        """列表返回正确数据"""
        client.post("/wishes/", json={"title": "愿望1", "category": "工作"})
        client.post("/wishes/", json={"title": "愿望2", "category": "生活"})
        res = client.get("/wishes/")
        assert res.status_code == 200
        assert len(res.json()) == 2

    def test_list_wishes_filter_category(self, client):
        """按分类过滤"""
        client.post("/wishes/", json={"title": "愿望1", "category": "工作"})
        client.post("/wishes/", json={"title": "愿望2", "category": "生活"})
        res = client.get("/wishes/?category=生活")
        assert len(res.json()) == 1
        assert res.json()[0]["title"] == "愿望2"

    def test_get_wish(self, client):
        """获取单个愿望"""
        create_res = client.post("/wishes/", json={"title": "测试愿望"})
        wish_id = create_res.json()["id"]
        res = client.get(f"/wishes/{wish_id}")
        assert res.status_code == 200
        assert res.json()["title"] == "测试愿望"

    def test_get_wish_not_found(self, client):
        """不存在的愿望返回 404"""
        res = client.get("/wishes/9999")
        assert res.status_code == 404

    def test_update_wish(self, client):
        """更新愿望"""
        create_res = client.post("/wishes/", json={"title": "旧标题"})
        wish_id = create_res.json()["id"]
        res = client.put(f"/wishes/{wish_id}", json={"title": "新标题", "status": "approved"})
        assert res.status_code == 200
        assert res.json()["title"] == "新标题"
        assert res.json()["status"] == "approved"

    def test_delete_wish(self, client):
        """删除愿望（软删除）"""
        create_res = client.post("/wishes/", json={"title": "待删除"})
        wish_id = create_res.json()["id"]

        del_res = client.delete(f"/wishes/{wish_id}")
        assert del_res.status_code == 200

        # 再次获取应返回 404
        get_res = client.get(f"/wishes/{wish_id}")
        assert get_res.status_code == 404
