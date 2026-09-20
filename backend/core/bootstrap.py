from backend.engines.manager import EngineManager

from backend.engines.database.manager import DatabaseEngine
from backend.engines.storage.manager import StorageEngine
from backend.engines.security.manager import SecurityEngine
from backend.engines.api.manager import APIEngine
from backend.engines.ai.manager import AIEngine
from backend.engines.foundation.manager import FoundationEngine
from backend.engines.work_business import WorkBusinessEngine
from backend.engines.leads_business import LeadsBusinessEngine
from backend.engines.sales_business import SalesBusinessEngine
from backend.engines.customer_business import CustomerBusinessEngine


class Bootstrap:
    def __init__(self):
        self.engine_manager = EngineManager()

    def register_engines(self):
        self.engine_manager.register_engine("database", DatabaseEngine())
        self.engine_manager.register_engine("storage", StorageEngine())
        self.engine_manager.register_engine("security", SecurityEngine())
        self.engine_manager.register_engine("api", APIEngine())
        self.engine_manager.register_engine("ai", AIEngine())
        self.engine_manager.register_engine("foundation", FoundationEngine())
        self.engine_manager.register_engine("work_business", WorkBusinessEngine())
        self.engine_manager.register_engine("leads_business", LeadsBusinessEngine())
        self.engine_manager.register_engine("sales_business", SalesBusinessEngine())
        self.engine_manager.register_engine("customer_business", CustomerBusinessEngine())

    def boot(self):
        self.register_engines()
        self.engine_manager.start_all()

        return {
            "foundation": "MAIN BASE FOUNDATION",
            "version": "1.0.0",
            "status": "RUNNING",
            "engines": self.engine_manager.engine_status(),
            "modules": [
                "Core",
                "Config",
                "Identity",
                "Authentication",
                "Database",
                "Storage",
                "Security",
                "API",
                "AI",
                "Foundation",
                "Leads Business",
                "Sales Business",
                "Customer Business",
                "Work Business",
                "Users",
                "Organizations",
                "Roles",
                "Permissions",
                "File Manager",
                "Registry",
                "Synchronization",
                "Dependencies",
                "Audit",
            ],
        }

    def shutdown(self):
        self.engine_manager.stop_all()
        return {"status": "STOPPED"}
