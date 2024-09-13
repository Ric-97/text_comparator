import pandas as pd
import streamlit as st
from annotated_text import annotated_text
import difflib
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from io import BytesIO

st.set_page_config(layout='wide')

st.title("Text Comparison App")

# File uploader
uploaded_file = st.file_uploader("Choose a PKL file", type="pkl")

if uploaded_file is not None:
    # Read the uploaded file
    check_content_df = pd.read_pickle(uploaded_file)
    check_content_df = check_content_df[['content_id','key','processed_text','text', 'title', 'category', "publication_date"]].drop_duplicates()

    selected_model = st.radio("Select the model", ['Model 2', 'Model 4'])
    st.title(f"We are checking {uploaded_file.name}")

    with st.expander("Expand selected dataset"):
        st.dataframe(check_content_df)

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

    st.title("Text Comparison")

    processing = st.toggle("Compare text processing")

    col1, col2 = st.columns(2)
    with col1:
        id_1 = st.selectbox("Select key 1", options=check_content_df['key'])
        selected_id_1 = check_content_df.loc[check_content_df['key'] == id_1, 'text'].values[0]
        selected_id_1_processed = check_content_df.loc[check_content_df['key'] == id_1, 'processed_text'].values[0]
        text1 = st.text_area("Text 1", value=selected_id_1, height=200)
        if not processing:
            text1_processed = st.text_area("Text 1 processed", value=selected_id_1_processed, height=200)
    with col2:
        if not processing:
            id_2 = st.selectbox("Select key 2", options=check_content_df['key'])
            selected_id_2 = check_content_df.loc[check_content_df['key'] == id_2, 'text'].values[0]
            selected_id_2_processed = check_content_df.loc[check_content_df['key'] == id_2, 'processed_text'].values[0]
            text2 = st.text_area("Text 2", value=selected_id_2, height=200)
            text2_processed = st.text_area("Text 2 processed", value=selected_id_2_processed, height=200)
        else:
            text2 = selected_id_1_processed
            text1_processed = st.text_area("Text 1 processed", value=selected_id_1_processed, height=200)

    if text1 and text2:
        diff1, diff2 = highlight_diff(text1, text2)
        
        st.subheader("Differences:")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Text 1**")
            for tag, line in diff1:
                if tag == 'equal':
                    annotated_text((line, ""))
                elif tag == 'delete':
                    annotated_text(("- " + line, "", "#faa"))
                elif tag == 'empty':
                    st.write("")
        
        with col2:
            st.markdown("**Text 2**")
            for tag, line in diff2:
                if tag == 'equal':
                    annotated_text((line, ""))
                elif tag == 'insert':
                    annotated_text(("+ " + line, "", "#afa"))
                elif tag == 'empty':
                    st.write("")

        pdf_buffer = create_pdf(diff1, diff2)
        st.download_button(
            label="Download PDF with differences",
            data=pdf_buffer,
            file_name="differences.pdf",
            mime="application/pdf"
        )
else:
    st.warning("Please upload a PKL file to proceed.")