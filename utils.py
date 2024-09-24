import difflib
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from io import BytesIO
from reportlab.lib.pagesizes import letter, landscape

def highlight_diff(text1, text2):
        s = difflib.SequenceMatcher(None, text1.splitlines(), text2.splitlines())
        diff1, diff2 = [], []
        for tag, i1, i2, j1, j2 in s.get_opcodes():
            if tag == 'equal':
                for line in text1.splitlines()[i1:i2]:
                    diff1.append(('equal', line))
                    diff2.append(('equal', line))
            elif tag == 'replace':
                for line in text1.splitlines()[i1:i2]:
                    diff1.append(('delete', line))
                for line in text2.splitlines()[j1:j2]:
                    diff2.append(('insert', line))
            elif tag == 'delete':
                for line in text1.splitlines()[i1:i2]:
                    diff1.append(('delete', line))
                    diff2.append(('empty', ''))
            elif tag == 'insert':
                for line in text2.splitlines()[j1:j2]:
                    diff1.append(('empty', ''))
                    diff2.append(('insert', line))
        return diff1, diff2

def create_pdf(diff1, diff2):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(letter))
    width, height = landscape(letter)
    c.setFont("Helvetica", 10)
    y = height - 50
    line_height = 15
    col_width = width / 2 - 60

    c.drawString(50, height - 30, "Text 1")
    c.drawString(width/2 + 10, height - 30, "Text 2")

    for (tag1, line1), (tag2, line2) in zip(diff1, diff2):
        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 10)
            y = height - 50
            c.drawString(50, height - 30, "Text 1")
            c.drawString(width/2 + 10, height - 30, "Text 2")

        # Handle Text 1
        if tag1 == 'equal':
            c.setFillColor(colors.black)
            text1 = line1
        elif tag1 == 'delete':
            c.setFillColor(colors.red)
            text1 = "- " + line1
        else:  # empty
            text1 = ""
        
        wrapped_text1 = [text1[i:i+80] for i in range(0, len(text1), 80)]
        for line in wrapped_text1:
            c.drawString(50, y, line)
            y -= line_height

        # Handle Text 2
        if tag2 == 'equal':
            c.setFillColor(colors.black)
            text2 = line2
        elif tag2 == 'insert':
            c.setFillColor(colors.green)
            text2 = "+ " + line2
        else:  # empty
            text2 = ""
        
        wrapped_text2 = [text2[i:i+80] for i in range(0, len(text2), 80)]
        for line in wrapped_text2:
            c.drawString(width/2 + 10, y, line)
            y -= line_height

        # Adjust y for the next pair of lines
        y -= line_height * (max(len(wrapped_text1), len(wrapped_text2)) - 1)

    c.save()
    buffer.seek(0)
    return buffer