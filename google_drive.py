import os

def guardar_en_drive(codigos, nombre_archivo):
    safe_name = nombre_archivo.replace(" ", "_").replace(":", "-") + ".txt"
    with open(safe_name, "w") as f:
        for codigo in codigos:
            f.write(str(codigo) + "\n")
    return safe_name
