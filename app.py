import streamlit as st
import markdown
from pathlib import Path
import tempfile
import zipfile
from io import BytesIO

CSS = """
* {
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  padding: 40px 60px;
  line-height: 1.6;
  color: #24292f;
  max-width: 1200px;
  margin: 0 auto;
}

h1, h2, h3, h4, h5, h6 {
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.25;
  page-break-after: avoid;
}

h1 {
  font-size: 2em;
  border-bottom: 2px solid #d0d7de;
  padding-bottom: 0.3em;
  margin-top: 0;
}

h2 {
  font-size: 1.5em;
  border-bottom: 1px solid #d0d7de;
  padding-bottom: 0.3em;
}

h3 { font-size: 1.25em; }
h4 { font-size: 1em; }
h5 { font-size: 0.875em; }
h6 { font-size: 0.85em; color: #57606a; }

p {
  margin-top: 0;
  margin-bottom: 16px;
}

a {
  color: #0969da;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

ul, ol {
  margin-top: 0;
  margin-bottom: 16px;
  padding-left: 2em;
}

li {
  margin-bottom: 4px;
}

li > p {
  margin-bottom: 8px;
}

code {
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 0.85em;
  background-color: #f6f8fa;
  padding: 0.2em 0.4em;
  border-radius: 3px;
}

pre {
  background-color: #f6f8fa;
  border-radius: 6px;
  padding: 16px;
  overflow-x: auto;
  margin-bottom: 16px;
  page-break-inside: avoid;
}

pre code {
  background-color: transparent;
  padding: 0;
  font-size: 0.9em;
  line-height: 1.45;
}

blockquote {
  margin: 0 0 16px 0;
  padding: 0 1em;
  color: #57606a;
  border-left: 4px solid #d0d7de;
}

hr {
  height: 2px;
  padding: 0;
  margin: 24px 0;
  background-color: #d0d7de;
  border: 0;
}

table {
  border-collapse: collapse;
  width: 100%;
  margin: 16px 0;
  border: 1px solid #d0d7de;
  overflow: hidden;
  page-break-inside: avoid;
}

thead {
  background-color: #f6f8fa;
}

th, td {
  border: 1px solid #d0d7de;
  padding: 10px 13px;
  text-align: left;
  vertical-align: top;
}

th {
  font-weight: 600;
}

tr:nth-child(even) td {
  background-color: #fafbfc;
}

img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 16px 0;
}

.page-break {
  page-break-after: always;
}

@media print {
  body {
    padding: 20px;
  }
  
  h1, h2, h3, h4, h5, h6 {
    page-break-after: avoid;
  }
  
  pre, blockquote, table {
    page-break-inside: avoid;
  }
  
  img {
    page-break-inside: avoid;
  }
}
"""


def markdown_to_pdf(md_content, pdf_path):
    """Convert markdown content to PDF using fpdf2."""
    try:
        from fpdf import FPDF, HTMLMixin
        
        class PDF(FPDF, HTMLMixin):
            pass
        
        html_body = markdown.markdown(
            md_content,
            extensions=[
                "fenced_code",
                "tables",
                "nl2br",
                "sane_lists",
                "smarty",
                "toc",
                "attr_list",
            ]
        )

        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)
        
        # Write HTML content
        pdf.write_html(html_body)
        
        pdf.output(pdf_path)
        return True
    except ImportError:
        st.error("fpdf2 not installed. Please run: pip install fpdf2")
        return False
    except Exception as e:
        st.error(f"Error generating PDF: {str(e)}")
        return False


# Streamlit App
st.set_page_config(
    page_title="Markdown to PDF Converter",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Markdown to PDF Converter")
st.markdown("Convert your Markdown files to beautifully formatted PDFs")

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    st.subheader("Page Margins")
    col1, col2 = st.columns(2)
    with col1:
        top_margin = st.number_input("Top (mm)", value=20, min_value=0, max_value=50)
        bottom_margin = st.number_input("Bottom (mm)", value=20, min_value=0, max_value=50)
    with col2:
        left_margin = st.number_input("Left (mm)", value=20, min_value=0, max_value=50)
        right_margin = st.number_input("Right (mm)", value=20, min_value=0, max_value=50)
    
    st.divider()
    st.markdown("### 📖 Supported Features")
    st.markdown("""
    - Headers & Formatting
    - Tables
    - Code Blocks
    - Lists & Quotes
    - Links & Images
    - Smart Typography
    """)

# Main content
tab1, tab2 = st.tabs(["📝 Single File", "📚 Multiple Files"])

with tab1:
    st.subheader("Convert Single Markdown File")
    
    # Input method selection
    input_method = st.radio(
        "Choose input method",
        ["📁 Upload File", "✍️ Type/Paste Markdown"],
        horizontal=True
    )
    
    md_content = None
    output_name = "output.pdf"
    
    if input_method == "📁 Upload File":
        uploaded_file = st.file_uploader(
            "Upload a Markdown file",
            type=['md', 'markdown'],
            key="single"
        )
        
        if uploaded_file:
            md_content = uploaded_file.read().decode('utf-8')
            output_name = uploaded_file.name.replace('.md', '.pdf').replace('.markdown', '.pdf')
    
    else:
        md_content = st.text_area(
            "Type or paste your Markdown here",
            height=300,
            placeholder="# Your Markdown Here\n\nStart typing or paste your markdown content...",
            key="text_input"
        )
        output_name = st.text_input("Output PDF name", value="output.pdf")
    
    if md_content:
        
        # Preview options
        preview_col1, preview_col2 = st.columns([1, 1])
        with preview_col1:
            preview_mode = st.radio(
                "Preview Mode",
                ["Rendered HTML", "Raw Markdown"],
                horizontal=True
            )
        
        # Live Preview
        st.markdown("### 👁️ Live Preview")
        preview_container = st.container()
        
        with preview_container:
            if preview_mode == "Rendered HTML":
                # Render markdown as HTML with custom styling
                html_body = markdown.markdown(
                    md_content,
                    extensions=[
                        "fenced_code",
                        "tables",
                        "nl2br",
                        "sane_lists",
                        "smarty",
                        "toc",
                        "attr_list",
                    ]
                )
                
                # Apply similar CSS for preview
                preview_html = f"""
                <style>
                    .preview-container {{
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                        line-height: 1.6;
                        color: #24292f;
                        padding: 20px;
                        background: white;
                        border: 1px solid #d0d7de;
                        border-radius: 6px;
                        max-height: 600px;
                        overflow-y: auto;
                    }}
                    .preview-container h1 {{
                        font-size: 2em;
                        border-bottom: 2px solid #d0d7de;
                        padding-bottom: 0.3em;
                        margin-top: 0;
                    }}
                    .preview-container h2 {{
                        font-size: 1.5em;
                        border-bottom: 1px solid #d0d7de;
                        padding-bottom: 0.3em;
                    }}
                    .preview-container h3 {{ font-size: 1.25em; }}
                    .preview-container h4 {{ font-size: 1em; }}
                    .preview-container table {{
                        border-collapse: collapse;
                        width: 100%;
                        margin: 16px 0;
                        border: 1px solid #d0d7de;
                    }}
                    .preview-container th, .preview-container td {{
                        border: 1px solid #d0d7de;
                        padding: 10px 13px;
                        text-align: left;
                    }}
                    .preview-container th {{
                        background-color: #f6f8fa;
                        font-weight: 600;
                    }}
                    .preview-container tr:nth-child(even) td {{
                        background-color: #fafbfc;
                    }}
                    .preview-container code {{
                        background-color: #f6f8fa;
                        padding: 0.2em 0.4em;
                        border-radius: 3px;
                        font-family: 'Consolas', 'Monaco', monospace;
                        font-size: 0.85em;
                    }}
                    .preview-container pre {{
                        background-color: #f6f8fa;
                        border-radius: 6px;
                        padding: 16px;
                        overflow-x: auto;
                    }}
                    .preview-container pre code {{
                        background-color: transparent;
                        padding: 0;
                    }}
                    .preview-container blockquote {{
                        border-left: 4px solid #d0d7de;
                        padding-left: 1em;
                        margin: 0 0 16px 0;
                        color: #57606a;
                    }}
                    .preview-container ul, .preview-container ol {{
                        padding-left: 2em;
                        margin-bottom: 16px;
                    }}
                    .preview-container p {{
                        margin-bottom: 16px;
                    }}
                    .preview-container a {{
                        color: #0969da;
                        text-decoration: none;
                    }}
                    .preview-container a:hover {{
                        text-decoration: underline;
                    }}
                </style>
                <div class="preview-container">
                    {html_body}
                </div>
                """
                st.markdown(preview_html, unsafe_allow_html=True)
            else:
                # Show raw markdown
                st.code(md_content, language='markdown', line_numbers=True)
        
        st.divider()
        
        if st.button("🚀 Convert to PDF", type="primary", use_container_width=True):
            with st.spinner("Converting to PDF..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    if markdown_to_pdf(md_content, tmp_file.name):
                        with open(tmp_file.name, 'rb') as f:
                            pdf_data = f.read()
                        
                        st.success("✅ PDF generated successfully!")
                        st.download_button(
                            label="📥 Download PDF",
                            data=pdf_data,
                            file_name=output_name,
                            mime="application/pdf",
                            use_container_width=True
                        )
                        
                        Path(tmp_file.name).unlink()

with tab2:
    st.subheader("Convert Multiple Markdown Files")
    
    uploaded_files = st.file_uploader(
        "Upload Markdown files",
        type=['md', 'markdown'],
        accept_multiple_files=True,
        key="multiple"
    )
    
    if uploaded_files:
        st.info(f"📁 {len(uploaded_files)} file(s) uploaded")
        
        with st.expander("📋 File List", expanded=True):
            for idx, file in enumerate(uploaded_files, 1):
                st.text(f"{idx}. {file.name}")
        
        col1, col2 = st.columns(2)
        with col1:
            download_option = st.radio(
                "Download option",
                ["Individual PDFs (ZIP)", "Individual Downloads"],
                horizontal=True
            )
        
        if st.button("🚀 Convert All to PDF", type="primary", use_container_width=True):
            with st.spinner(f"Converting {len(uploaded_files)} file(s)..."):
                pdf_files = []
                progress_bar = st.progress(0)
                
                for idx, uploaded_file in enumerate(uploaded_files):
                    md_content = uploaded_file.read().decode('utf-8')
                    pdf_name = uploaded_file.name.replace('.md', '.pdf').replace('.markdown', '.pdf')
                    
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        if markdown_to_pdf(md_content, tmp_file.name):
                            with open(tmp_file.name, 'rb') as f:
                                pdf_data = f.read()
                            
                            pdf_files.append((pdf_name, pdf_data))
                            Path(tmp_file.name).unlink()
                    
                    progress_bar.progress((idx + 1) / len(uploaded_files))
                
                if pdf_files:
                    st.success(f"✅ Successfully converted {len(pdf_files)} file(s)!")
                    
                    if download_option == "Individual PDFs (ZIP)":
                        # Create ZIP file
                        zip_buffer = BytesIO()
                        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                            for pdf_name, pdf_data in pdf_files:
                                zip_file.writestr(pdf_name, pdf_data)
                        
                        st.download_button(
                            label="📥 Download All as ZIP",
                            data=zip_buffer.getvalue(),
                            file_name="converted_pdfs.zip",
                            mime="application/zip",
                            use_container_width=True
                        )
                    else:
                        # Individual download buttons
                        st.markdown("### 📥 Download Individual PDFs")
                        for pdf_name, pdf_data in pdf_files:
                            st.download_button(
                                label=f"📄 {pdf_name}",
                                data=pdf_data,
                                file_name=pdf_name,
                                mime="application/pdf",
                                use_container_width=True
                            )

# Footer
st.divider()
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>Made with ❤️ using Streamlit | Supports GitHub-flavored Markdown</p>
    </div>
    """,
    unsafe_allow_html=True
)
