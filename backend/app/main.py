from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import os
import uuid

app = FastAPI()

# Allow frontend requests from any origin (change later for production security)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace "*" with ["http://localhost:5173"] for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "EPUB to PDF API is running!"}

@app.post("/convert")
async def convert_epub_to_pdf(file: UploadFile = File(...)):
    # Save uploaded EPUB
    input_filename = f"{uuid.uuid4()}.epub"
    with open(input_filename, "wb") as f:
        f.write(await file.read())

    # Output PDF filename
    output_filename = f"{uuid.uuid4()}.pdf"

    # Run Calibre CLI
    subprocess.run(["ebook-convert", input_filename, output_filename], check=True)

    # Remove EPUB after conversion
    os.remove(input_filename)

    # Return the PDF file for download
    return FileResponse(output_filename, media_type="application/pdf", filename="converted.pdf")
