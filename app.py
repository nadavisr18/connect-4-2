from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from server import game_router, session_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("templates/index.html") as f:
        return HTMLResponse(content=f.read())


@app.get("/{session_id}", response_class=HTMLResponse)
async def read_session(session_id: str):
    with open("templates/index.html") as f:
        return HTMLResponse(content=f.read())


app.include_router(session_router)
app.include_router(game_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="10.0.0.171", port=8000)
