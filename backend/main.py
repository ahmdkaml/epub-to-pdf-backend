# backend/main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import tempfile, zipfile, os
from ebooklib import epub
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

app = FastAPI()

@app.post("/convert")
async def convert_epub(file: UploadFile = File(...)):
    # Save uploaded file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".epub") as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name

    # Parse EPUB
    book = epub.read_epub(tmp_path)
    text_parts = []
    for item in book.get_items():
        if item.get_type() == epub.EpubHtml:
            soup = BeautifulSoup(item.get_content(), "html.parser")
            text_parts.append(soup.get_text())

    # Generate PDF
    pdf_path = tmp_path.replace(".epub", ".pdf")
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4
    y = height - 50
    for part in text_parts:
        for line in part.splitlines():
            if not line.strip():
                continue
            c.drawString(50, y, line[:100])  # truncate long lines
            y -= 15
            if y < 50:  # new page
                c.showPage()
                y = height - 50
    c.save()

    return FileResponse(pdf_path, media_type="application/pdf", filename="output.pdf")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)