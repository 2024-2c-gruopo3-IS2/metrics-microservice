from datetime import datetime
import time
from fastapi import HTTPException
import requests
from app.configs.config import settings

class MonitoringRepository:
    @staticmethod
    def get_services_status():
        headers = {
            "Authorization": f"Bearer {settings.RENDER_API_TOKEN}"
        }
        try:
            response = requests.get(settings.RENDER_API_URL+"/services", headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
        
    def suspend_service(self, service_id: str):
        print("service_id", service_id)
        return {"error": "Not implemented"}
    
    def suspend_service(self, service_id: str):
        headers = {
            "Authorization": f"Bearer {settings.RENDER_API_TOKEN}"
        }

        response = requests.post(f"{settings.RENDER_API_URL}/services/{service_id}/suspend", headers=headers)

        return response
    
    def resume_service(self, service_id: str):
        headers = {
            "Authorization": f"Bearer {settings.RENDER_API_TOKEN}"
        }

        response = requests.post(f"{settings.RENDER_API_URL}/services/{service_id}/resume", headers=headers)

        return response
    
    def get_cpu_usage(self, service_id: str):

        url = 'https://api.render.com/v1/metrics/cpu'

        response = requests.get(
            url,
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {settings.RENDER_API_TOKEN}'
            },
            params={
                'resource': service_id,
                'resolutionSeconds': 60 * 10
            }
        )

        if response.json() == []:
            return [0] * 7
        cpu_usage = [cpu_usage["value"] for cpu_usage in response.json()[0]["values"]]

        if len(cpu_usage) < 7:
            return [0] * (7-len(cpu_usage)) + cpu_usage
    
    def get_memory_usage(self, service_id: str):
        url = 'https://api.render.com/v1/metrics/memory'
        
        response = requests.get(
            url,
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {settings.RENDER_API_TOKEN}'
            },
            params={
                'resource': service_id,
                'resolutionSeconds': 60 * 10
            }

        )
        if response.json() == []:
            return [0] * 7
        
        memory_usage = [memory_usage["value"]/1000000 for memory_usage in response.json()[0]["values"]]

        if len(memory_usage) < 7:
            return [0] * (7-len(memory_usage)) + memory_usage