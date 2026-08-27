#!/usr/bin/env python3
"""
Download all Canvas pages and create course outline.

Usage:
    python3 download_canvas_pages.py [output_dir]

Saves pages to output_dir (default: remote_pages/)
Creates outline.md with module structure

Environment variables required:
    CANVAS_ACCESS_TOKEN - Canvas API token
    CANVAS_BASE_URL - Canvas instance URL (default: https://miamioh.instructure.com)
    CANVAS_COURSE_ID - Course ID (default: 243761)
"""

import os
import sys
from pathlib import Path
from canvasapi import Canvas

# Load .env file - try current directory first, then look for repo .env
try:
    from dotenv import load_dotenv, find_dotenv
    dotenv_path = find_dotenv(usecwd=True)
    if dotenv_path:
        load_dotenv(dotenv_path)
    else:
        load_dotenv()
except ImportError:
    pass

# Canvas configuration from environment
CANVAS_URL = os.environ.get('CANVAS_BASE_URL', 'https://miamioh.instructure.com')
COURSE_ID = int(os.environ.get('CANVAS_COURSE_ID', '243761'))
CANVAS_TOKEN = os.environ.get('CANVAS_ACCESS_TOKEN', '')

if not CANVAS_TOKEN:
    print("ERROR: Canvas token not found.")
    print(f"Create a key by visiting: {CANVAS_URL}/profile/settings")
    print("Please set the CANVAS_ACCESS_TOKEN environment variable")
    sys.exit(1)

def download_pages(output_dir: Path):
    """Download all Canvas pages and create outline."""
    
    print(f"Connecting to Canvas at {CANVAS_URL}...")
    canvas = Canvas(CANVAS_URL, CANVAS_TOKEN)
    
    print(f"Accessing course {COURSE_ID}...")
    course = canvas.get_course(COURSE_ID)
    
    # Get modules
    print("Fetching modules...")
    modules = list(course.get_modules())
    
    # Create outline
    outline = f"# CSE 534 Course Outline\n\n"
    outline += f"Downloaded from: {CANVAS_URL}/courses/{COURSE_ID}\n\n"
    
    page_count = 0
    
    for module in modules:
        print(f"\nModule: {module.name}")
        outline += f"## {module.name}\n\n"
        
        # Get module items
        try:
            items = list(module.get_module_items())
            for item in items:
                if item.type == 'Page':
                    page_title = item.title
                    print(f"  - Page: {page_title}")
                    outline += f"- [{page_title}]({CANVAS_URL}/courses/{COURSE_ID}/pages/{item.page_url})\n"
                    
                    # Download page content
                    try:
                        page = course.get_page(item.page_url)
                        
                        # Create module directory
                        module_slug = module.name.lower().replace(' ', '_').replace(':', '').replace('/', '_')
                        module_dir = output_dir / module_slug
                        module_dir.mkdir(parents=True, exist_ok=True)
                        
                        # Save page content
                        page_file = module_dir / f"{page_title}.html"
                        with open(page_file, 'w', encoding='utf-8') as f:
                            f.write(page.body or '')
                        
                        page_count += 1
                        print(f"    → Saved to {page_file}")
                    except Exception as e:
                        print(f"    ✗ Error downloading: {e}")
                
                elif item.type == 'Assignment':
                    outline += f"- 📝 {item.title}\n"
                elif item.type == 'ExternalUrl':
                    outline += f"- 🔗 [{item.title}]({item.external_url})\n"
                elif item.type == 'File':
                    outline += f"- 📄 {item.title}\n"
        except Exception as e:
            print(f"  ✗ Error fetching module items: {e}")
        
        outline += "\n"
    
    # Save outline
    outline_file = output_dir / "outline.md"
    with open(outline_file, 'w', encoding='utf-8') as f:
        f.write(outline)
    
    print(f"\n✓ Downloaded {page_count} pages")
    print(f"✓ Saved outline to {outline_file}")
    print(f"✓ Pages saved to {output_dir}")

def main():
    output_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('remote_pages')
    output_dir = output_dir.resolve()
    
    print(f"Output directory: {output_dir}")
    download_pages(output_dir)

if __name__ == '__main__':
    main()
