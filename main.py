from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google_drive import guardar_en_drive

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GuardarRequest(BaseModel):
    codigos: list[str]
    nombre: str

def obtener_datos_hoja():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key("12DeLHKDeClHc_e-bahUpfqZFBUUpCdcP").worksheet("Equivalencias")
    data = sheet.get_all_records()
    return data

@app.get("/")
def raiz():
    return {"mensaje": "API Pickeo desde Google Sheets"}

@app.get("/articulos")
def obtener_articulos():
    data = obtener_datos_hoja()
    return data

@app.post("/guardar")
def guardar_pedido(data: GuardarRequest):
    if not data.codigos:
        raise HTTPException(status_code=400, detail="Lista vacía de códigos")
    nombre_archivo = guardar_en_drive(data.codigos, data.nombre)
    return {"mensaje": "Guardado OK", "archivo": nombre_archivo}
