from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import planner, user

app = FastAPI(
    title="FitFusion Planner",
    description="Backend for fitness and wellness planner using AI agents",
    version="1.0.0",
)

#CORS setup so frontend can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(planner.router)
app.include_router(user.router) 

@app.get("/")
async def root():
    return {"message": "Welcome to the FitFusion Planner API!"}

