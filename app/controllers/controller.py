from fastapi import APIRouter
from app.services.service import MonitoringService

router = APIRouter()
service = MonitoringService()

@router.get("/services/")
def get_services():
    return service.get_services()

@router.get("/services/{service_name}")
def get_service_status(service_name: str):
    return service.get_service_status(service_name)

@router.post("/services/{service_name}/suspend")
def suspend_service(service_name: str):
    return service.suspend_service(service_name)

@router.post("/services/{service_name}/resume")
def unsuspend_service(service_name: str):
    return service.resume_service(service_name)