from fastapi import FastAPI
from changelog_cli.web.routes import router

app = FastAPI()
app.include_router(router)
