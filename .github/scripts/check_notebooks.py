#!/usr/bin/env python3
"""Check that notebook outputs are cleared."""

import json
import sys
import glob

has_outputs = False
for notebook_path in glob.glob('learning-resources/notebooks/*.ipynb'):
    with open(notebook_path, 'r') as f:
        nb = json.load(f)
    
    notebook_has_output = False
    for cell in nb['cells']:
        if cell['cell_type'] == 'code' and cell.get('outputs', []):
            print(f'ERROR: {notebook_path} has output that should be cleared')
            has_outputs = True
            notebook_has_output = True
    
    if not notebook_has_output:
        print(f'OK: {notebook_path}')

sys.exit(1 if has_outputs else 0)