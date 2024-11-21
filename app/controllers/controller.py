from fastapi import APIRouter, Depends, HTTPException, status
from app.controllers.auth import get_admin_from_token
from app.services.service import MonitoringService

router = APIRouter()
service = MonitoringService()

@router.get("/services/")
def get_services(_ = Depends(get_admin_from_token)):
    return service.get_services()

@router.get("/services/{service_name}")
def get_service_status(service_name: str, _ = Depends(get_admin_from_token)):
    return service.get_service_status(service_name)

@router.post("/services/{service_name}/suspend")
def suspend_service(service_name: str, _ = Depends(get_admin_from_token)):
    return service.suspend_service(service_name)

@router.post("/services/{service_name}/resume")
def unsuspend_service(service_name: str, _ = Depends(get_admin_from_token)):
    return service.resume_service(service_name)

@router.get("/metrics")
def get_metrics(_ = Depends(get_admin_from_token)):
    return service.get_metrics()

@router.post("/metrics/{metric_name}")
def add_metric(metric_name: str, value, _ = Depends(get_admin_from_token)):
    try:
        service.add_metric(metric_name, value)
        return {"message": f"Metric '{metric_name}' updated successfully with value {value}."}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    

