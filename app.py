import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from typing import List
from datetime import datetime

# PDF Compilation Stack
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

app = FastAPI()

# Data structure validation for incoming React requests
class EvaluationData(BaseModel):
    solutionNames: List[str]
    objectives: List[str]
    weights: List[float]
    scores: List[List[int]]
    totals: List[float]
    winner: str
    teamName: str

@app.get("/", response_class=HTMLResponse)
def read_root():
    # Serve the React frontend file directly to the browser
    with open("index.html", "r") as f:
        return f.read()

@app.post("/publish-pdf")
def publish_pdf(data: EvaluationData):
    try:
        # Save temporary PDF in the server's local directory
        pdf_filename = "CyberWOC_Executive_Briefing.pdf"
        
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle('DocTitle', fontName='Helvetica-Bold', fontSize=20, spaceAfter=15, textColor=colors.HexColor('#0f172a'))
        body_style = ParagraphStyle('BodyTextCustom', fontName='Helvetica', fontSize=10, leading=15, spaceAfter=12)
        section_title = ParagraphStyle('SecTitle', fontName='Helvetica-Bold', fontSize=13, spaceAfter=10, textColor=colors.HexColor('#0284c7'))
        
        story = []
        story.append(Paragraph("CYBERWOC // SYSTEM INTEGRATION EXECUTIVE DOSSIER", title_style))
        story.append(Paragraph(f"<b>REVIEW PANEL ID:</b> {data.teamName.upper()}<br/><b>GENERATION DATE:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        story.append(Spacer(1, 15))
        
        story.append(Paragraph("1. STRATEGIC DETERMINATION SUMMARY", section_title))
        p1_text = f"Following a rigorous multi-criteria optimization analysis of our deployment targets, the framework confirms that <b>'{data.winner}'</b> stands out as our most viable architectural selection. By evaluating the technical targets against normalized priority profiles rather than relying on subjective technical preference, this matrix provides a clear foundation to support our long-term system integration plan."
        story.append(Paragraph(p1_text, body_style))
        
        story.append(Paragraph("2. ANALYTICS VALUE LEDGER MATRIX", section_title))
        
        table_data = [["Objective Target Criterion", "Weight", data.solutionNames[0], data.solutionNames[1], data.solutionNames[2]]]
        for r in range(10):
            table_data.append([
                data.objectives[r],
                f"{float(data.weights[r]):.2f}",
                str(data.scores[r][0]),
                str(data.scores[r][1]),
                str(data.scores[r][2])
            ])
            
        table_data.append(["FINAL VERIFIED METRIC SCORE", "1.00", f"{data.totals[0]:.2f}", f"{data.totals[1]:.2f}", f"{data.totals[2]:.2f}"])
        
        metrics_table = Table(table_data, colWidths=[210, 45, 95, 95, 95])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('ALIGN', (0,1), (0,-1), 'LEFT'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
            ('BACKGROUND', (0,1), (-1,-2), colors.HexColor('#f8fafc')),
            ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#e2e8f0')),
            ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        
        story.append(metrics_table)
        doc.build(story)
        
        return FileResponse(path=pdf_filename, filename="CyberWOC_Executive_Briefing.pdf", media_type="application/pdf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))