from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import io

def generate_pdf(company_name, ticker, result):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=20,
        textColor=colors.HexColor("#1a1a2e"),
        spaceAfter=6
    )
    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading2"],
        fontSize=13,
        textColor=colors.HexColor("#16213e"),
        spaceBefore=14,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["Normal"],
        fontSize=10,
        leading=15,
        spaceAfter=6
    )
    rec_style = ParagraphStyle(
        "RecStyle",
        parent=styles["Normal"],
        fontSize=14,
        textColor=colors.HexColor("#ffffff"),
        backColor=colors.HexColor("#2e7d32") if result["recommendation"] == "Buy"
                  else colors.HexColor("#f57c00") if result["recommendation"] == "Hold"
                  else colors.HexColor("#c62828"),
        borderPadding=8,
        spaceAfter=10
    )

    story = []

    # Title
    story.append(Paragraph(f"{company_name.upper()} ({ticker.upper()})", title_style))
    story.append(Paragraph("AI Equity Research Report", styles["Heading3"]))
    story.append(Spacer(1, 12))

    # Recommendation badge
    story.append(Paragraph(f"Recommendation: {result['recommendation'].upper()}", rec_style))
    story.append(Spacer(1, 6))

    # Sentiment
    story.append(Paragraph("Market Sentiment", heading_style))
    story.append(Paragraph(
        f"{result['sentiment']} — {result['sentiment_confidence']}% confidence",
        body_style
    ))

    # Rationale
    story.append(Paragraph("Rationale", heading_style))
    story.append(Paragraph(result["recommendation_rationale"], body_style))

    # Full analysis
    story.append(Paragraph("Full Analysis", heading_style))
    for line in result["report"].split("\n"):
        if line.strip():
            story.append(Paragraph(line.strip(), body_style))
            story.append(Spacer(1, 4))

    doc.build(story)
    buffer.seek(0)
    return buffer