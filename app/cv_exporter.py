from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from pathlib import Path


def export_cv(text, filename="optimized_cv.pdf"):
    output_path = Path("data") / filename

    c = canvas.Canvas(str(output_path), pagesize=A4)
    width, height = A4

    y = height - 40

    for line in text.split("\n"):
        c.drawString(40, y, line[:120])
        y -= 15

        if y < 40:
            c.showPage()
            y = height - 40

    c.save()

    return output_path