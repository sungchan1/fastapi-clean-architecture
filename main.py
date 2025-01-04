import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from example.ch08_03.env_ex import router as env_ex_routers
from user.interface.controllers.user_controller import router as user_routers
from note.interface.controllers.note_controller import router as note_routers
from containers import Container
app = FastAPI()
app.container = Container()
app.include_router(user_routers)
app.include_router(note_routers)
# app.include_router(env_ex_routers)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
):
    return JSONResponse(
        status_code=400,
        content=exc.errors(),
    )
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", reload=True)