from datetime import datetime
from fastapi import HTTPException
from app.repositories.repository import MonitoringRepository

class MonitoringService:
    def __init__(self):
        self.repository = MonitoringRepository()

    def get_all_services_status(self):
        services_data = self.repository.get_services_status()

        if "error" in services_data:
            return services_data

        status = {}
        for service_data in services_data:
            service = service_data["service"]
            print("service", service)
            status[service["name"]] = {
                "suspended": service.get("suspended", "unknown"),
                "created_at": service.get("createdAt"),
                "url": service.get("serviceDetails", {}).get("url"),
                "last_updated": service.get("updatedAt"),
                "build_command": service.get("serviceDetails", {}).get("envSpecificDetails", {}).get("buildCommand"),
                "start_command": service.get("serviceDetails", {}).get("envSpecificDetails", {}).get("startCommand"),
            }
        return status
    
    def get_services(self):
        services_data = self.repository.get_services_status()

        if "error" in services_data:
            return services_data

        services = []
        for service_data in services_data:
            service = service_data["service"]
            services.append(
                service["name"]
            )
        return services
    
    def get_service_status(self, service_name: str):
        services_data = self.repository.get_services_status()

        if "error" in services_data:
            return services_data

        status = {}
        for service_data in services_data:
            if service_data["service"]["name"] != service_name:
                continue
            
            created_at = service_data["service"]["createdAt"]
            updated_at = service_data["service"]["updatedAt"]
            url = service_data["service"]["serviceDetails"]["url"]
            suspended = service_data["service"]["suspended"]

            if suspended == "not_suspended":
                suspended = "active"

            created_at = created_at[:-1]
            updated_at = updated_at[:-1]

            created_at_dt = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S.%f")
            updated_at_dt = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%S.%f")

            time_running = datetime.utcnow() - updated_at_dt

            days = time_running.days
            hours, remainder = divmod(time_running.seconds, 3600)
            minutes, _ = divmod(remainder, 60)

            time_running_str = f"{days} días, {hours} horas, {minutes} minutos"

            print("service id ", service_data["service"]["id"])

            cpu_usage = self.repository.get_cpu_usage(service_data["service"]["id"])
            memory_usage = self.repository.get_memory_usage(service_data["service"]["id"])

            return {
                "createdAt": created_at_dt,
                "timeRunning": time_running_str,
                "url": url,
                "status": suspended,
                "cpu_usage": cpu_usage,
                "memory_usage": memory_usage
            }

        return status
    
    def suspend_service(self, service_name: str):
        services_data = self.repository.get_services_status()

        if "error" in services_data:
            return services_data

        for service_data in services_data:
            if service_data["service"]["name"] != service_name:
                continue
            response = self.repository.suspend_service(service_data["service"]["id"])
            if response.status_code != 204:
                raise HTTPException(status_code=response.status_code, detail=response.text)
            return {"message": "Service suspended"}
        return {"error": "Service not found"}
    
    def resume_service(self, service_name: str):
        services_data = self.repository.get_services_status()

        if "error" in services_data:
            return services_data

        for service_data in services_data:
            if service_data["service"]["name"] != service_name:
                continue
            response = self.repository.resume_service(service_data["service"]["id"])
            if response.status_code != 204:
                raise HTTPException(status_code=response.status_code, detail=response.text)
            return {"message": "Service resumed"}
        return {"error": "Service not found"}
    
    def get_metrics(self):
        return self.repository.get_metrics()
    
    def add_metric(self, metric_name: str, value: str):
        # Validar que la métrica existe
        valid_metrics = [
            "signups", "signups_failed", "logins", "logins_failed",
            "logins_google", "logins_google_failed", "blocks",
            "password_recovers", "password_recover_failed", "geographic_zones"
        ]
        if metric_name not in valid_metrics:
            raise ValueError(f"Metric '{metric_name}' is not a valid metric.")
        
        if metric_name in ["signups", "signups_failed", "logins", "logins_failed", "logins_google", "logins_google_failed", "password_recovers", "password_recover_failed"]:
            try:
                value = float(value)
            except ValueError:
                raise ValueError("Value must be an integer.")
        elif metric_name == "geographic_zones":
            country = value.split(",")[0]
            
            metrics = self.repository.get_metrics()
            prev_geographics_zones = metrics.get("geographic_zones", {})
            print("prev_geographics_zones", prev_geographics_zones)
            prev_value = 0
            for zone in prev_geographics_zones:
                prev_country = zone.split(",")[0]
                if prev_country == country:
                    prev_value = int(zone.split(",")[1])
                    self.repository.delete_geographic_zone(zone)
                    break
            value_act = int(value.split(",")[1])
            value = f"{country},{str(prev_value + value_act)}"


        self.repository.add_metric(metric_name, value)