from fastapi import FastAPI
from app.routes import telegram, reminders, users

app = FastAPI(
    title="Aarogya Saathi API",
    description="Backend for AI-Driven Public Health Chatbot",
    version="1.0.0"
)

# Include Routers
app.include_router(telegram.router, prefix="/api", tags=["Telegram"])
app.include_router(reminders.router, prefix="/api/reminders", tags=["Reminders"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Aarogya Saathi Backend is running"}
