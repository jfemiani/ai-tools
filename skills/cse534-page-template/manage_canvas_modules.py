#!/usr/bin/env python3
"""
Manage Canvas modules: list, delete, rename, and update prerequisites.

Usage:
    python3 manage_canvas_modules.py list
    python3 manage_canvas_modules.py delete <module_id> [--yes]
    python3 manage_canvas_modules.py rename <module_id> <new_name>
    python3 manage_canvas_modules.py rename-page <page_url> <new_title>
    python3 manage_canvas_modules.py set-prereq <module_id> <prerequisite_module_id>
    python3 manage_canvas_modules.py remove-prereq <module_id> <prerequisite_module_id>

Environment variables required:
    CANVAS_ACCESS_TOKEN - Canvas API token
    CANVAS_BASE_URL - Canvas instance URL (default: https://miamioh.instructure.com)
    CANVAS_COURSE_ID - Course ID (default: 243761)
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

def list_modules():
    """List all modules with their IDs and prerequisites."""
    canvas = Canvas(CANVAS_URL, CANVAS_TOKEN)
    course = canvas.get_course(COURSE_ID)
    
    print(f"\nModules in course {COURSE_ID}:\n")
    modules = list(course.get_modules())
    
    for i, module in enumerate(modules, 1):
        prereqs = getattr(module, 'prerequisites', [])
        prereq_text = ""
        if prereqs:
            prereq_names = []
            for p in prereqs:
                if p.get('type') == 'context_module':
                    prereq_id = p.get('id')
                    # Find the prerequisite module name
                    prereq_module = next((m for m in modules if m.id == prereq_id), None)
                    if prereq_module:
                        prereq_names.append(f"{prereq_module.name} (ID: {prereq_id})")
            if prereq_names:
                prereq_text = f"\n     Prerequisites: {', '.join(prereq_names)}"
        
        print(f"{i:2}. [{module.id}] {module.name}{prereq_text}")

def delete_module(module_id, skip_confirm=False):
    """Delete a module by ID."""
    canvas = Canvas(CANVAS_URL, CANVAS_TOKEN)
    course = canvas.get_course(COURSE_ID)
    
    module = course.get_module(module_id)
    print(f"Deleting module: {module.name} (ID: {module_id})")
    
    if not skip_confirm:
        confirm = input("Are you sure? (yes/no): ")
        if confirm.lower() != 'yes':
            print("✗ Cancelled")
            return
    
    module.delete()
    print("✓ Module deleted")

def rename_module(module_id, new_name):
    """Rename a module."""
    canvas = Canvas(CANVAS_URL, CANVAS_TOKEN)
    course = canvas.get_course(COURSE_ID)
    
    module = course.get_module(module_id)
    old_name = module.name
    
    print(f"Renaming module {module_id}:")
    print(f"  From: {old_name}")
    print(f"  To:   {new_name}")
    
    module.edit(module={'name': new_name})
    print("✓ Module renamed")

def rename_page(page_url, new_title):
    """Rename a page by its URL."""
    canvas = Canvas(CANVAS_URL, CANVAS_TOKEN)
    course = canvas.get_course(COURSE_ID)
    
    page = course.get_page(page_url)
    old_title = page.title
    
    print(f"Renaming page:")
    print(f"  From: {old_title}")
    print(f"  To:   {new_title}")
    
    page.edit(wiki_page={'title': new_title})
    print("✓ Page renamed")

def set_prerequisite(module_id, prereq_module_id):
    """Set a prerequisite for a module."""
    canvas = Canvas(CANVAS_URL, CANVAS_TOKEN)
    course = canvas.get_course(COURSE_ID)
    
    module = course.get_module(module_id)
    prereq_module = course.get_module(prereq_module_id)
    
    print(f"Setting prerequisite:")
    print(f"  Module: {module.name} (ID: {module_id})")
    print(f"  Prerequisite: {prereq_module.name} (ID: {prereq_module_id})")
    
    # Get existing prerequisites
    existing_prereqs = getattr(module, 'prerequisites', [])
    
    # Add new prerequisite
    new_prereq = {'type': 'context_module', 'id': prereq_module_id}
    if new_prereq not in existing_prereqs:
        existing_prereqs.append(new_prereq)
    
    module.edit(module={'prerequisites': existing_prereqs})
    print("✓ Prerequisite set")

def remove_prerequisite(module_id, prereq_module_id):
    """Remove a specific prerequisite from a module."""
    canvas = Canvas(CANVAS_URL, CANVAS_TOKEN)
    course = canvas.get_course(COURSE_ID)
    
    module = course.get_module(module_id)
    
    # Get existing prerequisites
    existing_prereqs = list(getattr(module, 'prerequisites', []))
    
    # Remove the specified prerequisite
    existing_prereqs = [p for p in existing_prereqs 
                       if not (p.get('type') == 'context_module' and p.get('id') == prereq_module_id)]
    
    module.edit(module={'prerequisites': existing_prereqs})
    print(f"✓ Removed prerequisite {prereq_module_id} from module {module_id}")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    skip_confirm = '--yes' in sys.argv or '-y' in sys.argv
    
    if command == 'list':
        list_modules()
    elif command == 'delete' and len(sys.argv) >= 3:
        delete_module(int(sys.argv[2]), skip_confirm)
    elif command == 'rename' and len(sys.argv) >= 4:
        rename_module(int(sys.argv[2]), ' '.join(sys.argv[3:]))
    elif command == 'rename-page' and len(sys.argv) >= 4:
        rename_page(sys.argv[2], ' '.join(sys.argv[3:]))
    elif command == 'set-prereq' and len(sys.argv) >= 4:
        set_prerequisite(int(sys.argv[2]), int(sys.argv[3]))
    elif command == 'remove-prereq' and len(sys.argv) >= 4:
        remove_prerequisite(int(sys.argv[2]), int(sys.argv[3]))
    else:
        print(__doc__)
        sys.exit(1)

if __name__ == '__main__':
    main()
