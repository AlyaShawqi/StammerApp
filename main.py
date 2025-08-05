from fastapi import FastAPI
from routes import users, kids  # ✅ works now that main.py is in root

app = FastAPI()

app.include_router(users.router)
app.include_router(kids.router)