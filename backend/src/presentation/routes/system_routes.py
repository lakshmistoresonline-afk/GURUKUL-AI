from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ...data.repositories.database.db_config import get_db
from sqlalchemy import text
import json
from pathlib import Path

router = APIRouter(prefix="/api/v1/system", tags=["System"])

RUNTIME_ROOT = Path("D:/GURUKUL-AI/runtime-data")

@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return {
        "status": "operational",
        "database": db_status,
        "version": "V60.29"
    }

@router.get("/audits")
async def get_all_audits():
    audit_path = RUNTIME_ROOT / "audits" / "all_classes_audit.json"
    if not audit_path.exists():
        raise HTTPException(status_code=404, detail="Audits not found")
    with open(audit_path, "r", encoding="utf-8") as f:
        return json.load(f)

@router.get("/audits/classes/{class_id}")
async def get_class_audit(class_id: str):
    audit_path = RUNTIME_ROOT / "audits" / f"{class_id}_audit.json"
    if not audit_path.exists():
        raise HTTPException(status_code=404, detail=f"Audit for {class_id} not found")
    with open(audit_path, "r", encoding="utf-8") as f:
        return json.load(f)
