# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "fastapi",
#   "uvicorn",
#   "pandas",
#   "python-multipart",
#   "fastapi[all]"
# ]
# ///

from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import pandas as pd
import time

# Load CSV data
df = pd.read_csv("q-fastapi.csv")

app = FastAPI()

# Enable CORS for all origins (GET requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Logging middleware (X-Process-Time header)
@app.middleware("http")
async def add_timing(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    response.headers["X-Process-Time"] = str(time.time() - start)
    return response

# REST API endpoint
@app.get("/api")
async def get_students(class_: Optional[List[str]] = Query(default=None, alias="class")):
    if class_:
        filtered_df = df[df["class"].isin(class_)]
    else:
        filtered_df = df

    result = {
        "students": filtered_df.to_dict(orient="records")
    }
    return JSONResponse(content=result)
