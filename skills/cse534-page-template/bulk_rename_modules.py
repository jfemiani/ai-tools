#!/usr/bin/env python3
"""
Bulk rename Canvas modules and pages to add numbering.

This script renames:
- Modules: Add numbers (1, 2, 3...) to content modules
- Pages: Add sub-numbers (1.1, 1.2...) to pages within modules
"""

import os
import sys
from canvasapi import Canvas

# Load .env file
try:
    from dotenv import load_dotenv, find_dotenv
    dotenv_path = find_dotenv(usecwd=True)
    if dotenv_path:
        load_dotenv(dotenv_path)
    else:
        load_dotenv()
except ImportError:
    pass

# Canvas configuration
CANVAS_URL = os.environ.get('CANVAS_BASE_URL', 'https://miamioh.instructure.com')
COURSE_ID = int(os.environ.get('CANVAS_COURSE_ID', '243761'))
CANVAS_TOKEN = os.environ.get('CANVAS_ACCESS_TOKEN', '')

if not CANVAS_TOKEN:
    print("ERROR: CANVAS_ACCESS_TOKEN not found")
    sys.exit(1)

# Module renaming map: {module_id: (number, new_name_without_number)}
MODULE_RENAMES = {
    852255: (1, "Introduction to Generative AI and its Applications"),
    895478: (2, "Prompt Engineering and API Integration"),
    895481: (3, "Mathematical Foundations"),
    938503: (4, "LangChain Fundamentals and Function Calling"),
    895482: (5, "Vector Databases and RAG"),
    895483: (6, "Ethics, Evaluation, and Responsible AI"),
    895485: (7, "RNNs - Recurrent Neural Networks"),
    895486: (8, "LSTMs and Advanced Sequence Modeling"),
    895487: (9, "Transformers and Attention"),
    895488: (10, "Variational Autoencoders"),
    895489: (11, "Generative Adversarial Networks (GANs)"),
    895490: (12, "Advanced GANs and Diffusion Models"),
    895491: (13, "Diffusion Models"),
    895492: (14, "Advanced Architectures and Multimodal Models"),
}

def rename_modules(dry_run=True):
    """Rename modules with numbers."""
    canvas = Canvas(CANVAS_URL, CANVAS_TOKEN)
    course = canvas.get_course(COURSE_ID)
    
    print("=" * 70)
    print("MODULE RENAMING")
    print("=" * 70)
    
    for module_id, (num, new_name_base) in MODULE_RENAMES.items():
        try:
            module = course.get_module(module_id)
            old_name = module.name
            new_name = f"{num}. {new_name_base}"
            
            print(f"\nModule {module_id}:")
            print(f"  Old: {old_name}")
            print(f"  New: {new_name}")
            
            if not dry_run:
                module.edit(module={'name': new_name})
                print("  ✓ Renamed")
            else:
                print("  [DRY RUN - not changed]")
                
        except Exception as e:
            print(f"  ✗ Error: {e}")

def rename_pages_in_module(module_id, module_num, dry_run=True):
    """Rename pages within a module to add sub-numbers."""
    import re
    
    canvas = Canvas(CANVAS_URL, CANVAS_TOKEN)
    course = canvas.get_course(COURSE_ID)
    
    module = course.get_module(module_id)
    print(f"\n--- Pages in Module {module_num}: {module.name} ---")
    
    items = list(module.get_module_items())
    page_count = 0
    
    for item in items:
        if item.type == 'Page':
            page_count += 1
            sub_num = f"{module_num}.{page_count}"
            
            try:
                page = course.get_page(item.page_url)
                old_title = page.title
                
                # Skip if already numbered with module.page format
                if old_title.startswith(f"{module_num}."):
                    print(f"  {sub_num} [{item.page_url}] Already numbered: {old_title}")
                    continue
                
                # Strip existing standalone numbers (e.g., "1. Title" -> "Title")
                title_without_number = re.sub(r'^\d+\.\s*', '', old_title)
                
                new_title = f"{sub_num}. {title_without_number}"
                
                print(f"  {sub_num} [{item.page_url}]")
                print(f"    Old: {old_title}")
                print(f"    New: {new_title}")
                
                if not dry_run:
                    page.edit(wiki_page={'title': new_title})
                    print("    ✓ Renamed")
                else:
                    print("    [DRY RUN - not changed]")
                    
            except Exception as e:
                print(f"    ✗ Error: {e}")

def rename_all_pages(dry_run=True):
    """Rename all pages in numbered modules."""
    print("\n" + "=" * 70)
    print("PAGE RENAMING")
    print("=" * 70)
    
    for module_id, (num, _) in sorted(MODULE_RENAMES.items(), key=lambda x: x[1][0]):
        rename_pages_in_module(module_id, num, dry_run)

def main():
    dry_run = '--yes' not in sys.argv and '-y' not in sys.argv
    
    if dry_run:
        print("\n*** DRY RUN MODE ***")
        print("Add --yes or -y to actually apply changes\n")
    else:
        print("\n*** APPLYING CHANGES ***\n")
    
    rename_modules(dry_run)
    rename_all_pages(dry_run)
    
    if dry_run:
        print("\n" + "=" * 70)
        print("DRY RUN COMPLETE - No changes made")
        print("Run with --yes to apply changes")
        print("=" * 70)

if __name__ == '__main__':
    main()
