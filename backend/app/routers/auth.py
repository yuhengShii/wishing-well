from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx
import secrets

from ..database import get_db
from ..models import User
from ..core.config import settings

router = APIRouter(prefix="/auth", tags=["认证"])

WECHAT_API_URL = "https://api.weixin.qq.com/sns/jscode2session"


def generate_token():
    """生成简单的会话 token"""
    return secrets.token_urlsafe(32)


@router.post("/login", response_model=dict)
def login(code: str, db: Session = Depends(get_db)):
    """
    微信登录接口
    接收小程序传来的 code，换取 openid，返回 token
    """
    if not code:
        raise HTTPException(status_code=400, detail="code 不能为空")

    if not settings.WECHAT_APPID or not settings.WECHAT_APPSECRET:
        raise HTTPException(status_code=500, detail="微信配置未设置，请检查环境变量 WECHAT_APPID 和 WECHAT_APPSECRET")

    try:
        with httpx.Client() as client:
            wechat_data = client.get(
                WECHAT_API_URL,
                params={
                    "appid": settings.WECHAT_APPID,
                    "secret": settings.WECHAT_APPSECRET,
                    "js_code": code,
                    "grant_type": "authorization_code",
                },
                timeout=10.0,
            ).json()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"微信接口调用失败: {str(e)}")

    if "errcode" in wechat_data:
        raise HTTPException(
            status_code=400,
            detail=f"微信登录失败: {wechat_data.get('errmsg', 'unknown error')}"
        )

    openid = wechat_data.get("openid")
    session_key = wechat_data.get("session_key")

    if not openid:
        raise HTTPException(status_code=400, detail="无法获取 openid")

    # 查找或创建用户
    user = db.query(User).filter(User.openid == openid).first()
    if not user:
        user = User(openid=openid, session_key=session_key)
        db.add(user)
    else:
        user.session_key = session_key

    db.commit()
    db.refresh(user)

    # 生成 token
    token = generate_token()

    return {
        "token": token,
        "openid": openid,
        "user_id": user.id,
    }
