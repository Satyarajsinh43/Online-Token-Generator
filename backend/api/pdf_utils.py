import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO

def generate_token_receipt(token_obj):
    """
    Generates a PDF receipt for the given token object.
    Returns: BytesIO object containing the PDF.
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Formatting
    c.setLineWidth(1)
    c.setFont("Helvetica-Bold", 16)
    
    # Header
    c.drawString(1 * inch, height - 1 * inch, "Online Token System - Gujarat")
    c.setFont("Helvetica", 10)
    c.drawString(1 * inch, height - 1.25 * inch, "Government of Gujarat")
    
    c.line(1 * inch, height - 1.4 * inch, width - 1 * inch, height - 1.4 * inch)
    
    # Token Details
    y_pos = height - 2 * inch
    
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(width / 2, y_pos, token_obj.token_number)
    
    y_pos -= 0.5 * inch
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2, y_pos, f"Status: {token_obj.status}")
    
    y_pos -= 0.8 * inch
    
    # Info Table-like structure
    c.setFont("Helvetica", 12)
    left_margin = 1.5 * inch
    line_height = 0.35 * inch
    
    info_items = [
        ("Office:", token_obj.office.office_name),
        ("Service:", token_obj.service.name if token_obj.service else "N/A"),
        ("Date:", token_obj.created_at.strftime("%Y-%m-%d %I:%M %p")),
        ("Customer Name:", token_obj.customer_name),
        ("District:", token_obj.district.name if token_obj.district else "N/A"),
        ("Taluka:", token_obj.taluka.name if token_obj.taluka else "N/A"),
    ]
    
    if token_obj.village:
        info_items.append(("Village:", token_obj.village.name))
        
    for label, value in info_items:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(left_margin, y_pos, label)
        c.setFont("Helvetica", 12)
        c.drawString(left_margin + 2 * inch, y_pos, value)
        y_pos -= line_height

    # Blockchain Info
    y_pos -= 0.2 * inch
    c.setLineWidth(0.5)
    c.line(1 * inch, y_pos + 0.1 * inch, width - 1 * inch, y_pos + 0.1 * inch)
    
    y_pos -= 0.3 * inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(left_margin, y_pos, "Blockchain Record:")
    
    y_pos -= line_height
    c.setFont("Helvetica", 9)
    # Using simplistic wrapping for hashes, normally you'd use a Paragraph
    c.drawString(left_margin, y_pos, f"Token Hash: {token_obj.token_hash if token_obj.token_hash else 'Pending'}")
    
    y_pos -= line_height
    c.drawString(left_margin, y_pos, f"Txn Hash: {token_obj.blockchain_tx if token_obj.blockchain_tx else 'Pending/N/A'}")

    y_pos -= 0.2 * inch
    
    # Generate and draw QR Code
    if token_obj.token_hash:
        try:
            import qrcode
            # Assume verification URL is hosted on the same domain as API/Frontend
            # The user might need to change the domain.
            verify_url = f"http://localhost:5173/verify-token/{token_obj.token_hash}" # Default dev URL
            
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(verify_url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Save QR to a temporary file-like object or a temp file
            import tempfile
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            img.save(temp_file, format='PNG')
            temp_file.close()
            
            # Draw Image to PDF
            qr_size = 1.5 * inch
            # Positioned at bottom center, above footer
            c.drawImage(temp_file.name, (width - qr_size) / 2, 1.5 * inch, width=qr_size, height=qr_size)
            
            # Clean up
            os.remove(temp_file.name)
            
        except ImportError:
            c.drawString(left_margin, y_pos, "QR code generation disabled (qrcode module not found)")
        except Exception as e:
            print(f"Failed to generate QR: {e}")

    # Footer
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(width / 2, 1 * inch, "This is a computer-generated receipt secured by Polygon Blockchain.")
    
    c.showPage()
    c.save()
    
    buffer.seek(0)
    return buffer
