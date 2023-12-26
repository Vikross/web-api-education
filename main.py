from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.websockets import WebSocket, WebSocketDisconnect

from utils.sockets import manager
from routers import router as api_router_v1

from database import engine
import models

models.Base.metadata.create_all(bind=engine)

# Templates
templates = Jinja2Templates(directory="templates")

app = FastAPI(
    title="Управление образовательными курсами",
    summary="API для управления образовательными курсами",
    description=
    """
    Все эндпоинты (students, courses, lessons, enrollments) выполняют CRUD операции над одноимёнными моделями.
    Независимыми эндпоинтами являются 'student' и 'courses', они не требуют связанных между собой данных.
    'lessons' - связан только с 'courses';
    'enrollments' - связан и с 'courses' и с 'student', посредством ID.
    Все наименования взяты на английском языке, передающие мысль. На всякий случай напишу значения эндпоинтов:
    'students', 'courses', 'lessons' - выполняют CRUD операции над "студентами", "курсами", "уроками" соответственно.
    'enrollments' - осуществляет работу над "зачислением", записью студента на курс по их ID     
    """,
    version="0.0.1",
)


@app.websocket("/ws/{client_name}")
async def websocket_endpoint(websocket: WebSocket, client_name: str):
    await manager.connect(websocket)
    await manager.broadcast(f"Client #{client_name} joined the chat")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_name} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_name} left the chat")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    http_protocol = request.headers.get("x-forwarded-proto", "http")
    ws_protocol = "wss" if http_protocol == "https" else "ws"
    server_urn = request.url.netloc
    return templates.TemplateResponse("index.html",
                                      {"request": request,
                                       "http_protocol": http_protocol,
                                       "ws_protocol": ws_protocol,
                                       "server_urn": server_urn})


# Подключаем созданные роутеры в приложение
app.include_router(api_router_v1, prefix='/api')

if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
