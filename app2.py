import pandas as pd
import streamlit as st
from annotated_text import annotated_text
import utils

st.set_page_config(layout='wide')

st.title("Text Comparison App")

# File uploader
uploaded_file = st.file_uploader("Choose a PKL file", type="pkl")

if uploaded_file is not None:
    # Read the uploaded file
    check_content_df = pd.read_pickle(uploaded_file)
    check_content_df = check_content_df[['content_id','key','processed_text','text', 'title', 'category', "publication_date"]].drop_duplicates()

    selected_model = st.radio("Select the model", ['Model 2', 'Model 4'], disabled=True)
    
    st.title(f"We are checking {uploaded_file.name}")

    with st.expander("Expand selected dataset"):
        st.dataframe(check_content_df)

    st.title("Text Comparison")

    processing = st.toggle("Inspect only text processing")

    col1, col2 = st.columns(2)
    with col1:
        id_1 = st.selectbox("Select key 1", options=check_content_df['key'])
        selected_id_1_title = check_content_df.loc[check_content_df['key'] == id_1, 'title'].values[0]
        selected_id_1 = check_content_df.loc[check_content_df['key'] == id_1, 'text'].values[0]
        selected_id_1_processed = check_content_df.loc[check_content_df['key'] == id_1, 'processed_text'].values[0]
        st.write(f'Title:{selected_id_1_title}')
        text1 = st.text_area("Text 1", value=selected_id_1)
        if not processing:
            text1_processed = st.text_area("Text 1 processed", value=selected_id_1_processed)
    with col2:
        if not processing:
            id_2 = st.selectbox("Select key 2", options=check_content_df['key'])
            selected_id_2_title = check_content_df.loc[check_content_df['key'] == id_2, 'title'].values[0]
            selected_id_2 = check_content_df.loc[check_content_df['key'] == id_2, 'text'].values[0]
            selected_id_2_processed = check_content_df.loc[check_content_df['key'] == id_2, 'processed_text'].values[0]
            st.write(f'Title:{selected_id_2_title}')
            text2 = st.text_area("Text 2", value=selected_id_2, height=200)
            text2_processed = st.text_area("Text 2 processed", value=selected_id_2_processed)
        else:
            text2 = selected_id_1_processed
            text1_processed = st.text_area("Text 1 processed", value=selected_id_1_processed)

    if text1 and text2:
        diff1, diff2 = utils.highlight_diff(text1, text2)
        
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

        pdf_buffer = utils.create_pdf(diff1, diff2)
        st.download_button(
            label="Download PDF with differences",
            data=pdf_buffer,
            file_name="differences.pdf",
            mime="application/pdf"
        )
else:
    st.warning("Please upload a PKL file to proceed.")