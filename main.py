import os

import uvicorn
from dotenv import load_dotenv

from server.app import app

load_dotenv()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT") or 5000))
