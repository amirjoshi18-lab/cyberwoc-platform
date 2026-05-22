import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime

# Technical PDF Engine
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Rect, String, Line

app = FastAPI()

class EvaluationData(BaseModel):
    solutionNames: List[str]
    objectives: List[str]
    weights: List[float]
    scores: List[List[float]]
    totals: List[float]
    winner: str
    teamName: str
    rationales: Dict[str, str]  # Collects key justification phrases from the interface

@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("index.html", "r") as f:
        return f.read()

@app.post("/publish-pdf")
def publish_pdf(data: EvaluationData):
    try:
        pdf_filename = "Strategic_System_Evaluation_Briefing.pdf"
        
        # Build document with tight padding for an absolute single-to-double page fit
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter, rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54)
        styles = getSampleStyleSheet()
        
        # Professional Typography Hierarchy Styles
        title_style = ParagraphStyle('DocTitle', fontName='Helvetica-Bold', fontSize=20, spaceAfter=4, textColor=colors.HexColor('#0f172a'))
        meta_style = ParagraphStyle('MetaText', fontName='Helvetica-Oblique', fontSize=9, spaceAfter=20, textColor=colors.HexColor('#64748b'))
        section_style = ParagraphStyle('SecTitle', fontName='Helvetica-Bold', fontSize=12, spaceBefore=14, spaceAfter=8, textColor=colors.HexColor('#0284c7'))
        body_style = ParagraphStyle('BodyTextCustom', fontName='Helvetica', fontSize=10.5, leading=16, spaceAfter=12, textColor=colors.HexColor('#334155'))
        bullet_style = ParagraphStyle('BulletCustom', fontName='Helvetica', fontSize=10, leading=15, leftIndent=15, firstLineIndent=-10, spaceAfter=6, textColor=colors.HexColor('#334155'))

        story = []
        
        # 1. Executive Identification Header
        story.append(Paragraph("STRATEGIC SYSTEM ARCHITECTURE DETERMINATION", title_style))
        story.append(Paragraph(f"INVESTIGATION PANEL LOG IDENTIFIER: {data.teamName.upper()}  |  COMPILED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", meta_style))
        
        # 2. Executive Strategic Determination Summary Paragraphs
        story.append(Paragraph("ENGINEERING DETERMINATION DISCLOSURE", section_style))
        p1 = f"Following a rigorous multi-criteria optimization filtering matrix evaluation process, this structural technical architecture brief officially confirms that <b>'{data.winner}'</b> has been quantified as the optimal target selection path. Based on specific category elements and operational parameters investigated during the multi-phase analysis, this particular solution option proved structurally viable for full architectural deployment lifecycle integration."
        story.append(Paragraph(p1, body_style))
        
        p2 = "The decision framework mathematically normalized technical criteria metrics across a constrained 10-point scoring spectrum, mitigating baseline analytical bias. By weighing discrete technical parameters against qualitative real-world constraints, the engineering team has successfully minimized integration dependencies while maximizing future scalability thresholds."
        story.append(Paragraph(p2, body_style))

        # 3. Dynamic Technical Justification Matrix Bullet Points
        story.append(Paragraph("ARCHITECTURAL JUSTIFICATION LEDGER CORRELATION", section_style))
        p3 = f"The selected structural pathway, '{data.winner}', meets or exceeds target parameters due to specialized operational criteria mapped during Phase 1 configuration profiles. Specifically, the evaluation panel isolated the following core variables as strategic drivers:"
        story.append(Paragraph(p3, body_style))

        # Dynamically inject student keywords into formal technical bullet points
        for obj, phrase in data.rationales.items():
            clean_phrase = phrase.strip() if phrase else "Standard protocol alignment"
            bullet_text = f"• <b>{obj}:</b> Core architectural scoring profile was structurally driven by student investigator evaluation parameters identifying: <i>\"{clean_phrase}\"</i>."
            story.append(Paragraph(bullet_text, bullet_style))

        story.append(Spacer(1, 15))

        # 4. Embedded Vector Performance Analytical Visual Graphic Chart
        story.append(Paragraph("DECISION OPTIMIZATION PERFORMANCE VECTOR GRAPH", section_style))
        
        # Native ReportLab Drawing Elements to eliminate client chart dependency errors
        drawing = Drawing(400, 140)
        max_score = 10.0
        chart_height = 100
        
        # Base structural axis lines grid
        drawing.add(Line(50, 20, 380, 20, strokeColor=colors.HexColor('#cbd5e1'), strokeWidth=1))
        drawing.add(Line(50, 20, 50, 120, strokeColor=colors.HexColor('#cbd5e1'), strokeWidth=1))
        
        # Dynamic bar chart rendering loop configurations
        bar_colors = [colors.HexColor('#06b6d4'), colors.HexColor('#a855f7'), colors.HexColor('#ec4899')]
        for i, val in enumerate(data.totals[:3]):
            bar_w = 45
            x_pos = 90 + (i * 95)
            # Normalize mathematical values safely up into vector height limits
            scaled_h = (val / max_score) * chart_height
            
            # Append bar block shape coordinates
            drawing.add(Rect(x_pos, 20, bar_w, scaled_h, fillColor=bar_colors[i % 3], strokeColor=None))
            # Score value text overlays
            drawing.add(String(x_pos + 12, scaled_h + 25, f"{val:.2f}", fontName="Helvetica-Bold", fontSize=9, fillColor=colors.HexColor('#1e293b')))
            # Normalized bottom labels
            short_label = data.solutionNames[i][:15] + "..." if len(data.solutionNames[i]) > 15 else data.solutionNames[i]
            drawing.add(String(x_pos - 10, 5, short_label, fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#64748b')))

        story.append(KeepTogether([drawing]))
        
        doc.build(story)
        return FileResponse(path=pdf_filename, filename="Strategic_System_Evaluation_Briefing.pdf", media_type="application/pdf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))