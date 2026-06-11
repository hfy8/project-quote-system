"""FastAPI 路由 - 数据同步 (迁移版)"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from app.tasks import trigger_sync_now
from api_app.main import get_db, get_current_user_id, _flask_app

router = APIRouter()


@router.post("/trigger")
def trigger_sync(user_id: str = Depends(get_current_user_id)):
    """手动触发数据同步"""
    try:
        trigger_sync_now(_flask_app)
        return JSONResponse(
            content={"message": "同步任务已触发，请查看日志获取同步结果"},
            status_code=200,
        )
    except Exception as e:
        return JSONResponse(
            content={"error": f"同步失败: {str(e)}"},
            status_code=500,
        )


@router.get("/status")
def sync_status():
    """获取同步任务状态"""
    return JSONResponse(
        content={
            "message": "定时同步任务已配置，每晚22:00自动执行",
            "schedule": "22:00 每日",
        },
        status_code=200,
    )
