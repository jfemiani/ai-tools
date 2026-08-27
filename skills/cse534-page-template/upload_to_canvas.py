#!/usr/bin/env python3
"""
Upload HTML page and optional PDF to Canvas course.

Usage:
    python3 upload_to_canvas.py <html_file> <page_title> [pdf_file]

Example:
    python3 upload_to_canvas.py \
        ~/Courses/CSE534-live/cse534-course-demos/mathematical_foundations/pages/6.\ Normal\ Distributions\ and\ Gaussian\ Regression.html \
        "6. Normal Distributions and Gaussian Regression" \
        ~/Courses/CSE534-live/cse534-course-demos/mathematical_foundations/slides/6.\ Normal\ Distributions\ and\ Gaussian\ Regression\ Slides.pdf

Environment variables required:
    CANVAS_ACCESS_TOKEN - Canvas API token
    CANVAS_BASE_URL - Canvas instance URL (default: https://miamioh.instructure.com)
    CANVAS_COURSE_ID - Course ID (default: 243761)

Get a token from: https://miamioh.instructure.com/profile/settings
"""

import os
import sys
from pathlib import Path
from canvasapi import Canvas

# Load .env file - try current directory first, then look for repo .env
try:
    from dotenv import load_dotenv, find_dotenv
    # Try to find .env in current directory or parent directories
    dotenv_path = find_dotenv(usecwd=True)
    if dotenv_path:
        load_dotenv(dotenv_path)
    else:
        # Fallback: try loading from current directory
        load_dotenv()
except ImportError:
    pass

# Canvas configuration from environment
CANVAS_URL = os.environ.get('CANVAS_BASE_URL', 'https://miamioh.instructure.com')
COURSE_ID = os.environ.get('CANVAS_COURSE_ID', '243761')
CANVAS_TOKEN = os.environ.get('CANVAS_ACCESS_TOKEN', '')

if not CANVAS_TOKEN:
    print("ERROR: Canvas token not found.")
    print(f"Create a key by visiting: {CANVAS_URL}/profile/settings")
    print("Please set the CANVAS_ACCESS_TOKEN environment variable")
    sys.exit(1)

def upload_page(html_file: Path, page_title: str, pdf_file: Path = None):
    """Upload HTML page and optional PDF to Canvas."""
    
    print(f"Connecting to Canvas at {CANVAS_URL}...")
    canvas = Canvas(CANVAS_URL, CANVAS_TOKEN)
    
    print(f"Accessing course {COURSE_ID}...")
    course = canvas.get_course(COURSE_ID)
    
    # Read HTML content
    print(f"Reading HTML from {html_file}...")
    if not html_file.exists():
        print(f"ERROR: HTML file not found: {html_file}")
        sys.exit(1)
        
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Check if page exists, create or update
    print(f"Uploading page: {page_title}...")
    try:
        page = course.get_page(page_title)
        print(f"  Page exists, updating...")
        page.edit(wiki_page={'body': html_content})
        print(f"  ✓ Page updated successfully")
    except:
        print(f"  Page doesn't exist, creating...")
        page = course.create_page(wiki_page={
            'title': page_title,
            'body': html_content,
            'published': True
        })
        print(f"  ✓ Page created successfully")
    
    # Upload PDF file if provided
    if pdf_file and pdf_file.exists():
        print(f"Uploading PDF: {pdf_file.name}...")
        try:
            # Upload file to course files
            upload_result = course.upload(pdf_file)
            if upload_result[0]:
                file_obj = upload_result[1]
                print(f"  ✓ PDF uploaded successfully (File ID: {file_obj['id']})")
                
                # Add link to PDF in page body
                pdf_link = f'\n\n<p><a href="/courses/{COURSE_ID}/files/{file_obj["id"]}/download">📄 Download Slides PDF</a></p>'
                updated_body = html_content + pdf_link
                page.edit(wiki_page={'body': updated_body})
                print(f"  ✓ PDF link added to page")
            else:
                print(f"  ⚠ PDF upload failed")
        except Exception as e:
            print(f"  ⚠ Error uploading PDF: {e}")
    elif pdf_file:
        print(f"  ⚠ PDF file not found: {pdf_file}")
    
    page_url = f"{CANVAS_URL}/courses/{COURSE_ID}/pages/{page.url}"
    print(f"\n✓ Done! Page URL: {page_url}")
    return page_url

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    
    html_file = Path(sys.argv[1]).expanduser().resolve()
    page_title = sys.argv[2]
    pdf_file = Path(sys.argv[3]).expanduser().resolve() if len(sys.argv) > 3 else None
    
    upload_page(html_file, page_title, pdf_file)

if __name__ == '__main__':
    main()
