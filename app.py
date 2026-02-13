import streamlit as st
import markdown
from pathlib import Path
import tempfile
import zipfile
from io import BytesIO


def markdown_to_pdf(md_content, pdf_path):
    """Convert markdown content to PDF using fpdf2."""
    try:
        from fpdf import FPDF, HTMLMixin
        
        class PDF(FPDF, HTMLMixin):
            def error(self, msg):
                """Override error to handle missing images gracefully."""
                if "No such file or directory" in str(msg) or "image" in str(msg).lower():
                    pass  # Ignore missing image errors
                else:
                    super().error(msg)
        
        # Remove image references from markdown
        import re
        md_content = re.sub(r'!\[.*?\]\(.*?\)', '[Image removed]', md_content)
        
        html_body = markdown.markdown(
            md_content,
            extensions=["fenced_code", "tables", "nl2br", "sane_lists"]
        )

        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=11)
        pdf.write_html(html_body)
        pdf.output(pdf_path)
        return True
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False


# App Config
st.set_page_config(page_title="Markdown to PDF", page_icon="📄", layout="centered")

st.title("📄 Markdown to PDF Converter")
st.markdown("Simple tool to convert Markdown files to PDF")

# Tabs
tab1, tab2 = st.tabs(["Single File", "Multiple Files"])

# Tab 1: Single File
with tab1:
    input_method = st.radio("Input Method", ["Upload File", "Paste Text"], horizontal=True)
    
    md_content = None
    output_name = "output.pdf"
    
    if input_method == "Upload File":
        uploaded_file = st.file_uploader("Upload Markdown file", type=['md', 'markdown'])
        if uploaded_file:
            md_content = uploaded_file.read().decode('utf-8')
            output_name = uploaded_file.name.replace('.md', '.pdf').replace('.markdown', '.pdf')
    else:
        md_content = st.text_area("Paste your Markdown here", height=300, 
                                   placeholder="# Your Markdown\n\nStart typing...")
        output_name = st.text_input("PDF filename", value="output.pdf")
    
    if md_content and st.button("Convert to PDF", type="primary", use_container_width=True):
        with st.spinner("Converting..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                if markdown_to_pdf(md_content, tmp.name):
                    with open(tmp.name, 'rb') as f:
                        pdf_data = f.read()
                    
                    st.success("✅ Done!")
                    st.download_button("📥 Download PDF", pdf_data, output_name, 
                                     "application/pdf", use_container_width=True)
                    Path(tmp.name).unlink()

# Tab 2: Multiple Files
with tab2:
    uploaded_files = st.file_uploader("Upload Markdown files", type=['md', 'markdown'], 
                                     accept_multiple_files=True)
    
    if uploaded_files:
        st.info(f"📁 {len(uploaded_files)} file(s) uploaded")
        
        if st.button("Convert All", type="primary", use_container_width=True):
            with st.spinner(f"Converting {len(uploaded_files)} file(s)..."):
                pdf_files = []
                progress = st.progress(0)
                
                for idx, file in enumerate(uploaded_files):
                    md_content = file.read().decode('utf-8')
                    pdf_name = file.name.replace('.md', '.pdf').replace('.markdown', '.pdf')
                    
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                        if markdown_to_pdf(md_content, tmp.name):
                            with open(tmp.name, 'rb') as f:
                                pdf_files.append((pdf_name, f.read()))
                            Path(tmp.name).unlink()
                    
                    progress.progress((idx + 1) / len(uploaded_files))
                
                if pdf_files:
                    st.success(f"✅ Converted {len(pdf_files)} file(s)!")
                    
                    # Create ZIP
                    zip_buffer = BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
                        for name, data in pdf_files:
                            zf.writestr(name, data)
                    
                    st.download_button("📥 Download ZIP", zip_buffer.getvalue(), 
                                     "converted_pdfs.zip", "application/zip", 
                                     use_container_width=True)

st.divider()
st.markdown("<p style='text-align: center; color: #666;'>Made with Streamlit</p>", 
           unsafe_allow_html=True)
