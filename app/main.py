from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
import tempfile
import subprocess
import os
import uuid

app = FastAPI()

# --- Calcular ruta absoluta a lilypond, subiendo un nivel desde app/ ---
base_dir = os.path.dirname(os.path.abspath(__file__))  # carpeta app/
parent_dir = os.path.dirname(base_dir)                 # carpeta proyecto/
LILYPOND_PATH = os.path.join(parent_dir, "lilypond-bin", "bin", "lilypond")

@app.post("/compile")
async def compile_lilypond(code: str = Form(...)):
    temp_dir = tempfile.mkdtemp()
    file_id = uuid.uuid4().hex
    ly_path = os.path.join(temp_dir, f"{file_id}.ly")
    pdf_path = os.path.join(temp_dir, f"{file_id}.pdf")

    with open(ly_path, "w", encoding="utf-8") as f:
        f.write(code)

    try:
        subprocess.run(
            [LILYPOND_PATH, "-o", os.path.join(temp_dir, file_id), ly_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    except subprocess.CalledProcessError as e:
        return {"error": "Error compilando LilyPond", "details": e.stderr.decode("utf-8")}

    # Comprobamos si el PDF existe
    if os.path.exists(pdf_path):
        print(f"PDF generado en: {pdf_path}")
    else:
        print("PDF no encontrado después de compilar.")

    return FileResponse(pdf_path, media_type="application/pdf")