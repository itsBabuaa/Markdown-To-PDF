# Markdown to PDF Converter

A professional Streamlit web application for converting Markdown files to beautifully formatted PDFs.

## Requirements

- Python 3.10 or higher (recommended: 3.10.11)

## Features

- **Multiple Input Methods**: Upload files OR type/paste markdown directly
- **Live Preview**: See rendered HTML or raw markdown before converting
- **Single File Conversion**: Convert one Markdown file at a time
- **Batch Conversion**: Convert multiple Markdown files simultaneously
- **Professional Styling**: GitHub-inspired design with proper typography
- **Download Options**: 
  - Download individual PDFs
  - Download all PDFs as a ZIP file
- **Markdown Support**:
  - Headers and formatting
  - Tables with styling
  - Code blocks with syntax highlighting
  - Lists and blockquotes
  - Links and images
  - Smart typography

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

That's it! Pure Python solution - no system dependencies or browser installation needed.

## Usage

### Run the Streamlit App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Using the Command Line Script

```bash
python md_to_pdf.py
```

## How to Use the Web App

1. **Single File Mode**:
   - Choose input method: Upload file OR Type/Paste markdown
   - Preview your content (Rendered HTML or Raw Markdown)
   - Click "Convert to PDF"
   - Download your PDF

2. **Multiple Files Mode**:
   - Upload multiple Markdown files
   - Choose download option (ZIP or individual)
   - Click "Convert All to PDF"
   - Download your files

## Technical Details

- Built with Streamlit for the web interface
- Uses xhtml2pdf for PDF generation (pure Python, no system dependencies!)
- Python-Markdown for parsing
- Supports GitHub-flavored Markdown extensions
- Simple, lightweight, and works everywhere
