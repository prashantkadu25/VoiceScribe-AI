from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
import tempfile


def create_txt(text):
    return text.encode("utf-8")


def create_pdf(text):

    temp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    )

    doc = SimpleDocTemplate(temp.name)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph("<b>VoiceScribe Transcript</b>", styles["Title"])
    )

    story.append(
        Paragraph(text, styles["BodyText"])
    )

    doc.build(story)

    with open(temp.name, "rb") as f:
        pdf = f.read()

    return pdf