from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def index():
    return {
        "server": "fastapi",
        "adapter": "a2wsgi",
    }
