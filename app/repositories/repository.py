from datetime import datetime
import time
from fastapi import HTTPException
import requests
from app.configs.config import settings
from app.configs.db import db

class MonitoringRepository:

    def __init__(self):
        self.metrics_collection = db["metrics"]

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

        print("response", response.json())

        if response.json() == []:
            return [0] * 7
        
        cpu_usage = [cpu_usage["value"] for cpu_usage in response.json()[0]["values"]]

        print("cpu_usage", cpu_usage)

        if len(cpu_usage) < 7:
            return [0] * (7-len(cpu_usage)) + cpu_usage
        return cpu_usage
    
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
        return memory_usage
    
    def get_metrics(self):
        metrics = self.metrics_collection.find_one()
        metrics.pop("_id")
        return metrics
    
    def add_metric(self, metric_name: str, value):
        metric = self.metrics_collection.find_one()

        if not metric:
            metric = {metric_name: [value]}
            self.metrics_collection.insert_one(metric)
        else:
            if metric_name in metric:
                if isinstance(metric[metric_name], list):
                    metric[metric_name].append(value)
                elif isinstance(metric[metric_name], float):
                    metric[metric_name] += value
                else:
                    raise ValueError(f"Invalid metric format for '{metric_name}'.")
            else:
                metric[metric_name] = [value]

            self.metrics_collection.update_one(
                {"_id": metric["_id"]},
                {"$set": metric}
            )

    #self.repository.delete_metric("geographic_zones", zone)
    def delete_geographic_zone(self, zone: str):
        metric = self.metrics_collection.find_one()
        if not metric:
            return {"error": "Metric not found."}
        if "geographic_zones" not in metric:
            return {"error": "Metric not found."}
        if zone not in metric["geographic_zones"]:
            return {"error": "Zone not found."}
        metric["geographic_zones"].remove(zone)
        self.metrics_collection.update_one(
            {"_id": metric["_id"]},
            {"$set": metric}
        )
        return {"message": "Zone deleted successfully."}