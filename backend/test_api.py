"""简单接口测试：使用 FastAPI TestClient 走通注册、登录与面试全流程。

运行方式（在 backend/ 目录下）：
    pytest test_api.py -v
"""
import uuid

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def _register_and_login() -> dict:
    """注册一个唯一用户并返回请求头。"""
    username = f"user_{uuid.uuid4().hex[:8]}"
    resp = client.post(
        "/api/auth/register",
        json={"username": username, "password": "123456"},
    )
    assert resp.status_code == 200, resp.text
    token = resp.json()["token"]
    return {"Authorization": f"Bearer {token}", "username": username}


def test_register_and_login():
    username = f"user_{uuid.uuid4().hex[:8]}"
    payload = {"username": username, "password": "123456"}

    # 注册成功
    resp = client.post("/api/auth/register", json=payload)
    assert resp.status_code == 200
    assert resp.json()["username"] == username
    assert resp.json()["token"]

    # 重复注册应返回 400
    resp = client.post("/api/auth/register", json=payload)
    assert resp.status_code == 400

    # 正确密码登录成功
    resp = client.post("/api/auth/login", json=payload)
    assert resp.status_code == 200
    assert resp.json()["token"]

    # 错误密码应返回 401
    resp = client.post(
        "/api/auth/login",
        json={"username": username, "password": "wrongpass"},
    )
    assert resp.status_code == 401


def test_interview_flow():
    headers = _register_and_login()

    # 开始面试
    resp = client.post(
        "/api/interview/start",
        json={"job_type": "后端开发", "difficulty": "中级"},
        headers=headers,
    )
    assert resp.status_code == 200, resp.text
    session_id = resp.json()["session_id"]

    # 获取题目并回答
    for _ in range(5):
        q = client.get(f"/api/interview/{session_id}/question", headers=headers)
        assert q.status_code == 200, q.text
        question_id = q.json()["id"]

        ans = client.post(
            f"/api/interview/{session_id}/answer",
            json={"question_id": question_id, "answer": "这是我的回答内容。"},
            headers=headers,
        )
        assert ans.status_code == 200, ans.text
        assert "score" in ans.json()
        assert "evaluation" in ans.json()

    # 答满 5 题后应提示面试完成
    resp = client.get(f"/api/interview/{session_id}/question", headers=headers)
    assert resp.status_code == 400

    # 面试报告
    resp = client.get(f"/api/interview/{session_id}/report", headers=headers)
    assert resp.status_code == 200, resp.text
    report = resp.json()
    assert report["status"] == "completed"
    assert len(report["questions"]) == 5
    assert report["total_score"] is not None

    # 历史列表
    resp = client.get("/api/interview/history", headers=headers)
    assert resp.status_code == 200
    assert len(resp.json()["sessions"]) >= 1
