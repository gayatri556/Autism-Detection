import os
from fpdf import FPDF
from datetime import datetime

def generate_pdf(result, suggestion, parent_name="Parent", child_name="Child", confidence=0):
    pdf = FPDF()
    pdf.add_page()

    # ✅ Light watermark image (logo_lightened.png)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(base_dir,  "static", "img", "logo_lightened.png")

    print("[Using image]:", img_path)
    print("Exists?", os.path.exists(img_path))

    if os.path.exists(img_path):
        # Make the watermark larger and centered
        # A4 = 210 x 297 mm, center position
        x = (210 - 160) / 2  # width = 160 mm
        y = (297 - 160) / 2  # height = 160 mm
        pdf.image(img_path, x=x, y=y, w=160, h=160)
    else:
        print("Watermark image not found!")

    # ✅ Now overlay content
    pdf.set_font("Arial", 'B', 18)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(200, 10, "Autism Screening Report", ln=True, align="C")

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 11)
    pdf.cell(200, 10, f"Date: {datetime.today().strftime('%B %d, %Y')}", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, f"Parent Name: {parent_name}", ln=True)
    pdf.cell(200, 10, f"Child Name: {child_name}", ln=True)
    pdf.ln(10)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, f"Prediction Result: {result}", ln=True)

    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, f"Model Confidence: {confidence}%", ln=True)
    pdf.ln(10)

    pdf.set_font("Arial", 'I', 12)
    pdf.multi_cell(0, 10, f"Suggestion:\n{suggestion}")

    # ✅ Save the PDF
    file_path = "autism_report.pdf"
    pdf.output(file_path)
    return file_path

