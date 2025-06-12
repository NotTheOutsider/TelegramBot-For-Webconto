import os
import uvicorn
from services.api.routers import app

log_config_path = os.path.join(os.path.dirname(__file__), "logConfig.json")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_config=log_config_path)