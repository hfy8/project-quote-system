"""手动触发数据同步 / 查看定时任务状态"""
import logging
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from app.tasks import trigger_sync_now

logger = logging.getLogger("fastapi-sync")

router = APIRouter()


@router.post("/trigger")
def trigger_sync_endpoint():
    """手动触发数据同步（22:00 自动同步太慢时用）"""
    try:
        # trigger_sync_now 是 sync_task 提供的便利函数，内部用 create_app() 创建临时 app
        trigger_sync_now(None)
        return JSONResponse(content={"message": "同步任务已触发，请查看日志获取同步结果"})
    except Exception as e:
        logger.exception("手动同步失败")
        raise HTTPException(status_code=500, detail=f"同步失败: {str(e)}")


@router.get("/status")
def sync_status_endpoint():
    """获取同步任务状态"""
    from apscheduler.schedulers.background import BackgroundScheduler
    # BackgroundScheduler 不维护全局索引，靠 logger 记录的 jobs。
    # 这里直接给出静态描述（接口对齐 Flask legacy）
    return JSONResponse(content={
        "message": "定时同步任务已配置，每晚22:00自动执行",
        "schedule": "22:00 每日",
        "owner": "FastAPI lifespan（避免与 Flask legacy 重复触发）",
    })
