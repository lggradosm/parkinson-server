from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.audio import router as audio_router
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las orígenes, puedes restringirlo a tu dominio específico
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(audio_router,prefix="/api")

@app.get("/")
def index():
  return "Api creada con FastAPI"