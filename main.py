from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google_drive import guardar_en_drive
import datetime
import requests

# Configuración
SHEET_ID = "12DeLHKDeClHc_e-bahUpfqZFBUUpCdcP"
SHEET_NAME = "Equivalencias"

# API
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GuardarRequest(BaseModel):
    codigos: list
    nombre: str

@app.get("/")
def root():
    return {"mensaje": "API Pickeo desde Google Sheets"}

@app.post("/guardar")
def guardar_archivo(data: GuardarRequest):
    # Crear archivo TXT con los códigos
    nombre_archivo = data.nombre.strip().replace(" ", "_") + ".txt"
    with open(nombre_archivo, "w") as f:
        for c in data.codigos:
            f.write(f"{c}\n")

    # Subir a Google Drive
    file_id = guardar_en_drive(nombre_archivo)

    # Eliminar el archivo local después de subir
    os.remove(nombre_archivo)

    return {"archivo": nombre_archivo, "drive_id": file_id}