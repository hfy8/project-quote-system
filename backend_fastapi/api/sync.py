"""手动触发数据同步 / 查看定时任务状态"""
import logging
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from core.tasks import trigger_sync_now
from core.auth import get_current_user_id

logger = logging.getLogger("fastapi-sync")

router = APIRouter()


@router.post("/trigger")
def trigger_sync_endpoint(user_id: str = Depends(get_current_user_id)):
    """手动触发数据同步（22:00 自动同步太慢时用）"""
    try:
        # trigger_sync_now 是 sync_task 提供的便利函数，内部用 create_app() 创建临时 app
        trigger_sync_now(None)
        # 记录操作日志 (同步触发, 后台执行; 成功/失败计数见 sync_task 日志)
        from utils.log_helpers import record_crud
        record_crud(
            user_id,
            'sync',
            'submit',
            '触发同步: 数据同步 (manual, 成功=见后台任务日志, 失败=见后台任务日志)',
        )
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
