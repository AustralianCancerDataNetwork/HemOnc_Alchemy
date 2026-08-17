"""
Author-facing schema compiler — NOT part of the runtime.

Installed via `hemonc-alchemy[author]`. 

This module reads the real HemOnc data dictionary workbook 
and CSV snapshots to produces interim JSON registry snapshot 
plus the generated data model specification files in ../model/ 
(entities.py, enums.py).

Never imported by ../model/ or ../toolbox/ (enforced by importlinter)
"""
