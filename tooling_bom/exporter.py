"""
exporter.py — Excel Report Generator for Tooling BOM Comparison.

Generates a .xlsx file matching the structure and styling of the
reference expected outcome.xlsx file, including:
  - Bilingual headers (English + French)
  - KPI summary block (New / Deleted / Modified / Changed Fields)
  - Color-coded rows (green for New, red for Deleted, white for Modified)
  - Two sheets: "Standard Parts" and "Non-Standard Parts"
"""

from __future__ import annotations

import io
from typing import Any

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

from tooling_bom.comparator import ChangeRow


# ── Styling constants ──────────────────────────────────────────────────────────
FONT_NAME = "Aptos Narrow"

# Fill colors
FILL_TITLE       = PatternFill("solid", fgColor="1F4E79")   # dark navy
FILL_KPI         = PatternFill("solid", fgColor="DDEBF7")   # light blue
FILL_HEADER_EN   = PatternFill("solid", fgColor="4472C4")   # blue
FILL_HEADER_FR   = PatternFill("solid", fgColor="9BC2E6")   # lighter blue
FILL_NEW         = PatternFill("solid", fgColor="C6EFCE")   # soft green (new item)
FILL_DELETED     = PatternFill("solid", fgColor="FFC7CE")   # soft red (deleted item)
FILL_CHANGE_TYPE = PatternFill("solid", fgColor="FFEB9C")   # soft yellow / gold (change type)
FILL_COLUMN_NAME = PatternFill("solid", fgColor="FCE4D6")   # soft peach / orange (column name)
FILL_OLD_VAL     = PatternFill("solid", fgColor="FFC7CE")   # soft red (old value)
FILL_NEW_VAL     = PatternFill("solid", fgColor="C6EFCE")   # soft green (new value)

# Font colors
WHITE_FONT  = Font(name=FONT_NAME, bold=True,  color="FFFFFF")
BOLD_FONT   = Font(name=FONT_NAME, bold=True,  color="000000")
NORMAL_FONT = Font(name=FONT_NAME, bold=False, color="000000")

# Borders
THIN_SIDE   = Side(style="thin", color="BFBFBF")
CELL_BORDER = Border(left=THIN_SIDE, right=THIN_SIDE, top=THIN_SIDE, bottom=THIN_SIDE)

# Column widths (A-H)
COL_WIDTHS = [12, 18, 38, 38, 30, 30, 48, 48]


# ── Public API ─────────────────────────────────────────────────────────────────

def export_to_excel(
    std_rows:     list[ChangeRow],
    nonstd_rows:  list[ChangeRow],
    summary:      dict[str, int],
    old_filename: str = "",
    new_filename: str = "",
) -> bytes:
    """
    Build the comparison Excel workbook and return it as bytes.

    Parameters
    ----------
    std_rows      : change rows for Standard Parts (REPERE >= 4000)
    nonstd_rows   : change rows for Non-Standard Parts (REPERE < 4000)
    summary       : summary counts dict from comparator.compare()
    old_filename  : original filename of the Old BOM (displayed in header)
    new_filename  : original filename of the New BOM (displayed in header)

    Returns
    -------
    bytes : Excel file content ready for st.download_button
    """
    wb = openpyxl.Workbook()
    wb.remove(wb.active)  # remove default sheet

    _build_sheet(
        wb,
        sheet_title        = "Standard Parts",
        title_en           = "STANDARD PARTS COMPARISON",
        title_fr           = "COMPARAISON DES PIECES STANDARD",
        rows               = std_rows,
        new_count          = summary["std_new"],
        deleted_count      = summary["std_deleted"],
        modified_count     = summary["std_modified"],
        changed_fields     = summary["std_changed_fields"],
        old_filename       = old_filename,
        new_filename       = new_filename,
    )

    _build_sheet(
        wb,
        sheet_title        = "Non-Standard Parts",
        title_en           = "NON-STANDARD PARTS COMPARISON",
        title_fr           = "COMPARAISON DES PIECES NON STANDARD",
        rows               = nonstd_rows,
        new_count          = summary["nonstd_new"],
        deleted_count      = summary["nonstd_deleted"],
        modified_count     = summary["nonstd_modified"],
        changed_fields     = summary["nonstd_changed_fields"],
        old_filename       = old_filename,
        new_filename       = new_filename,
    )

    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()


# ── Sheet Builder ──────────────────────────────────────────────────────────────

def _build_sheet(
    wb:            openpyxl.Workbook,
    sheet_title:   str,
    title_en:      str,
    title_fr:      str,
    rows:          list[ChangeRow],
    new_count:     int,
    deleted_count: int,
    modified_count:int,
    changed_fields:int,
    old_filename:  str,
    new_filename:  str,
) -> None:
    ws = wb.create_sheet(title=sheet_title)

    # ── Row 1: English title ──────────────────────────────────────────────────
    ws.merge_cells("A1:H1")
    _write_cell(ws, 1, 1, title_en, fill=FILL_TITLE, font=WHITE_FONT, align="left")

    # ── Row 2: French title ───────────────────────────────────────────────────
    ws.merge_cells("A2:H2")
    _write_cell(ws, 2, 1, title_fr, fill=FILL_TITLE, font=WHITE_FONT, align="left")

    # ── Row 3: Old BOM reference ──────────────────────────────────────────────
    _write_cell(ws, 3, 1, "Old BOM / Ancienne BOM", font=BOLD_FONT)
    _write_cell(ws, 3, 2, old_filename, font=NORMAL_FONT)

    # ── Row 4: New BOM reference ──────────────────────────────────────────────
    _write_cell(ws, 4, 1, "New BOM / Nouvelle BOM", font=BOLD_FONT)
    _write_cell(ws, 4, 2, new_filename, font=NORMAL_FONT)

    # ── Row 5: Empty ──────────────────────────────────────────────────────────
    ws.row_dimensions[5].height = 8

    # ── Row 6: KPI counts ────────────────────────────────────────────────────
    ws.row_dimensions[6].height = 24
    kpi_data = [
        ("New items",       new_count),
        ("Deleted items",   deleted_count),
        ("Modified items",  modified_count),
        ("Changed fields",  changed_fields),
    ]
    for i, (label, count) in enumerate(kpi_data):
        col_label = i * 2 + 1
        col_value = i * 2 + 2
        _write_cell(ws, 6, col_label, label, fill=FILL_KPI, font=BOLD_FONT, align="center", border=CELL_BORDER)
        _write_cell(ws, 6, col_value, count,  fill=FILL_KPI, font=BOLD_FONT, align="center", border=CELL_BORDER)

    # ── Row 7: Empty separator ───────────────────────────────────────────────
    ws.row_dimensions[7].height = 8

    # ── Row 8: English column headers ─────────────────────────────────────────
    ws.row_dimensions[8].height = 24
    headers_en = [
        "Item No.", "Part Category",
        "Change Type", "Change Type",
        "Changed Column", "Changed Column",
        "Old Value", "New Value",
    ]
    for col, h in enumerate(headers_en, 1):
        _write_cell(ws, 8, col, h, fill=FILL_HEADER_EN, font=WHITE_FONT, align="center" if col <= 2 else "left", border=CELL_BORDER)

    # ── Row 9: French column headers ─────────────────────────────────────────
    ws.row_dimensions[9].height = 24
    headers_fr = [
        "No. Repere", "Categorie de piece",
        "Type of Change", "Type de modification",
        "English Column Name", "Nom de colonne francais",
        "Ancienne valeur", "Nouvelle valeur",
    ]
    for col, h in enumerate(headers_fr, 1):
        _write_cell(ws, 9, col, h, fill=FILL_HEADER_FR, font=BOLD_FONT, align="center" if col <= 2 else "left", border=CELL_BORDER)

    # ── Row 10+: Data rows ────────────────────────────────────────────────────
    data_start_row = 10
    last_row = data_start_row
    for row_idx, change in enumerate(rows, start=data_start_row):
        last_row = row_idx
        ws.row_dimensions[row_idx].height = 20
        change_type = change.get("change_type_en", "")

        values = [
            change.get("item_no",        ""),
            change.get("part_category",  ""),
            change.get("change_type_en", ""),
            change.get("change_type_fr", ""),
            change.get("column_en",      ""),
            change.get("column_fr",      ""),
            change.get("old_value",      ""),
            change.get("new_value",      ""),
        ]

        if change_type == "New Item":
            fills = [FILL_NEW] * 8
            fonts = [NORMAL_FONT] * 8
        elif change_type == "Deleted Item":
            fills = [FILL_DELETED] * 8
            fonts = [NORMAL_FONT] * 8
        else:
            # Field-level modified item
            fills = [
                None,              # Col 1: Item No
                None,              # Col 2: Category
                FILL_CHANGE_TYPE,  # Col 3: Change Type (EN) - Yellow
                FILL_CHANGE_TYPE,  # Col 4: Change Type (FR) - Yellow
                FILL_COLUMN_NAME,  # Col 5: Changed Column (EN) - Peach
                FILL_COLUMN_NAME,  # Col 6: Changed Column (FR) - Peach
                FILL_OLD_VAL,      # Col 7: Old Value - Soft Red
                FILL_NEW_VAL,      # Col 8: New Value - Soft Green
            ]
            fonts = [
                NORMAL_FONT,
                BOLD_FONT,
                BOLD_FONT,
                BOLD_FONT,
                NORMAL_FONT,
                NORMAL_FONT,
                NORMAL_FONT,
                NORMAL_FONT,
            ]

        for col, (val, cell_fill, cell_font) in enumerate(zip(values, fills, fonts), 1):
            align_dir = "center" if col in (1, 2) else "left"
            _write_cell(ws, row_idx, col, val, fill=cell_fill, font=cell_font, align=align_dir, border=CELL_BORDER)

    # ── Column widths ─────────────────────────────────────────────────────────
    for col_idx, width in enumerate(COL_WIDTHS, 1):
        ws.column_dimensions[get_column_letter(col_idx)].width = width

    # ── Title row heights ─────────────────────────────────────────────────────
    ws.row_dimensions[1].height = 26
    ws.row_dimensions[2].height = 22
    ws.row_dimensions[3].height = 20
    ws.row_dimensions[4].height = 20

    # ── Freeze panes at row 10 (data area) ───────────────────────────────────
    ws.freeze_panes = f"A{data_start_row}"

    # ── Auto-filter on header row ─────────────────────────────────────────────
    if last_row >= data_start_row:
        ws.auto_filter.ref = f"A8:H{last_row}"

    # ── Show Gridlines ────────────────────────────────────────────────────────
    ws.views.sheetView[0].showGridLines = True


# ── Cell Writer Helper ─────────────────────────────────────────────────────────

def _write_cell(
    ws,
    row:    int,
    col:    int,
    value:  Any,
    fill:   PatternFill | None = None,
    font:   Font               = NORMAL_FONT,
    align:  str                = "left",
    border: Border | None      = None,
) -> None:
    cell = ws.cell(row=row, column=col, value=value)
    cell.font = font
    if fill is not None:
        cell.fill = fill
    if border is not None:
        cell.border = border
    cell.alignment = Alignment(horizontal=align, vertical="center", wrap_text=False)
