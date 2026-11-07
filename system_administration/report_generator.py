import docx
from docx.shared import Pt
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class ReportGenerator:
    @staticmethod
    def create_system_report(drives: list, programs: list) -> str:
        """Erstellt einen Word-Bericht und gibt den Dateipfad zurück."""
        doc = docx.Document()
        
        # Titel
        title = doc.add_heading('J.A.R.V.I.S. – Systemanalyse', 0)
        
        # Datum
        doc.add_paragraph(f"Datum der Analyse: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
        
        # Laufwerksdaten
        doc.add_heading('Speicherplatz', level=1)
        for drive in drives:
            doc.add_paragraph(
                f"Laufwerk {drive['drive']} – Gesamt: {drive['total_gb']} GB | "
                f"Belegt: {drive['used_gb']} GB | Frei: {drive['free_gb']} GB ({drive['percent']}% voll)"
            )
            
        # Programm-Tabelle
        doc.add_heading('Größte installierte Programme', level=1)
        doc.add_paragraph("Hier sind die Programme, die am meisten Speicherplatz auf Ihrem System verbrauchen.")
        
        table = doc.add_table(rows=1, cols=4)
        table.style = 'Table Grid'
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Programmname'
        hdr_cells[1].text = 'Größe (GB)'
        hdr_cells[2].text = 'Empfehlung'
        hdr_cells[3].text = 'Aktion'
        
        # Top 15 Programme
        for prog in programs[:15]:
            row_cells = table.add_row().cells
            row_cells[0].text = prog['name']
            row_cells[1].text = str(prog['size_gb'])
            row_cells[2].text = "Überprüfen" if prog['size_gb'] > 1.0 else "Behalten"
            row_cells[3].text = "Deinstallieren?" if prog['size_gb'] > 1.0 else "-"
            
        # Speichern
        reports_dir = BASE_DIR / "Reports"
        reports_dir.mkdir(exist_ok=True)
        filename = f"Systemanalyse_{datetime.now().strftime('%Y%m%d_%H%M')}.docx"
        filepath = reports_dir / filename
        
        doc.save(filepath)
        return str(filepath)