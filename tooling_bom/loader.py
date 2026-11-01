"""
loader.py — Smart Tooling BOM Reader.

Reads any .xlsm or .xlsx BOM file robustly:
  - Auto-detects the correct sheet (tries "021" first, then scans all sheets)
  - Auto-detects header rows by searching for REPERE anchor keyword
  - Maps raw column names to internal keys using COLUMN_ALIASES
  - Normalizes REPERE values to clean integer strings
  - Returns a pandas DataFrame + metadata

No hardcoded row or column positions. Works on any BOM layout variant.
"""

from __future__ import annotations

import re
from io import BytesIO
from typing import Any

import pandas as pd
from python_calamine import CalamineWorkbook

from tooling_bom.column_config import COLUMN_ALIASES, STANDARD_THRESHOLD

# ── Constants ──────────────────────────────────────────────────────────────────
HEADER_SCAN_ROWS   = 35          # How many rows to scan for the header
REPERE_ANCHORS     = {"REPERE", "BALOON #", "BALLOON #", "NO. REPERE", "NO REPERE"}
SECONDARY_ANCHORS  = {"CONSTRUCTEUR", "COEF", "CODEÍM", "CODEIM", "MABEC",
                      "MAKER", "MANUFACTURER", "QTY", "QUANTITY"}
MIN_SECONDARY_HITS = 2           # Minimum secondary anchor matches to confirm header
PREFERRED_SHEET    = "021"


# ── Public API ─────────────────────────────────────────────────────────────────

def load_bom(
    file_obj: BytesIO | str,
    sheet_name: str | None = None,
) -> dict:
    """
    Load a Tooling BOM file and return structured data.

    Parameters
    ----------
    file_obj   : BytesIO or file path string
    sheet_name : Force a specific sheet name. If None, auto-detect.

    Returns
    -------
    dict with keys:
        "df"                : pandas DataFrame (columns = internal keys, REPERE as string)
        "sheet_name"        : str — which sheet was used
        "available_columns" : list of (internal_key, en_name, fr_name) detected
        "raw_columns"       : list of raw header names found in the file
        "sheet_options"     : list of str — all candidate sheet names (for UI dropdown)
        "warnings"          : list of str — any non-fatal issues
    """
    warnings: list[str] = []

    # ── 1. Open workbook ───────────────────────────────────────────────────────
    wb = CalamineWorkbook.from_object(file_obj) if isinstance(file_obj, BytesIO) \
         else CalamineWorkbook.from_path(file_obj)

    all_sheet_names = wb.sheet_names

    # ── 2. Sheet detection ────────────────────────────────────────────────────
    if sheet_name:
        if sheet_name not in all_sheet_names:
            raise ValueError(f"Sheet '{sheet_name}' not found. Available: {all_sheet_names}")
        candidate_sheets = [sheet_name]
    else:
        candidate_sheets = _detect_bom_sheets(wb, all_sheet_names)

    if not candidate_sheets:
        raise ValueError(
            "No BOM sheet detected. Expected a sheet named '021' or one containing "
            "a 'REPERE' column. Available sheets: " + ", ".join(all_sheet_names)
        )

    # If multiple sheets qualify, caller can pick via UI dropdown
    chosen_sheet = candidate_sheets[0]

    # ── 3. Read raw rows ───────────────────────────────────────────────────────
    raw_rows: list[list[Any]] = wb.get_sheet_by_name(chosen_sheet).to_python()

    # ── 4. Detect header rows ─────────────────────────────────────────────────
    fr_header_idx = _find_header_row(raw_rows)
    if fr_header_idx is None:
        raise ValueError(
            f"Could not find a header row with 'REPERE' in sheet '{chosen_sheet}'. "
            "Please verify the file format."
        )

    h_fr: list[Any] = raw_rows[fr_header_idx]
    # English header is the row immediately above (if it exists and isn't data)
    h_en: list[Any] = raw_rows[fr_header_idx - 1] if fr_header_idx > 0 else []
    data_start: int = fr_header_idx + 1

    # ── 5. Build column map ────────────────────────────────────────────────────
    col_map, available_columns, raw_cols = _build_column_map(h_fr, h_en, warnings)

    # ── 6. Extract data rows → DataFrame ─────────────────────────────────────
    repere_col_idx = col_map.get("REPERE", {}).get("idx")
    if repere_col_idx is None:
        raise ValueError(
            f"REPERE column not found in sheet '{chosen_sheet}'. "
            f"Headers detected: {h_fr[:15]}"
        )

    records: list[dict] = []
    for row_idx in range(data_start, len(raw_rows)):
        row = raw_rows[row_idx]
        if len(row) <= repere_col_idx:
            continue
        rep_raw = row[repere_col_idx]
        rep_str = _normalize_repere(rep_raw)
        if rep_str is None:
            continue  # skip empty / invalid REPERE rows

        record: dict[str, Any] = {"REPERE": rep_str}
        for internal_key, meta in col_map.items():
            if internal_key == "REPERE":
                continue
            idx = meta["idx"]
            raw_val = row[idx] if idx < len(row) else None
            record[internal_key] = _normalize_value(raw_val)

        records.append(record)

    df = pd.DataFrame(records)

    return {
        "df":                df,
        "sheet_name":        chosen_sheet,
        "available_columns": available_columns,
        "raw_columns":       raw_cols,
        "sheet_options":     candidate_sheets,
        "warnings":          warnings,
    }


def get_sheet_options(file_obj: BytesIO | str) -> list[str]:
    """Quick helper: return all candidate BOM sheet names without loading data."""
    wb = CalamineWorkbook.from_object(file_obj) if isinstance(file_obj, BytesIO) \
         else CalamineWorkbook.from_path(file_obj)
    return _detect_bom_sheets(wb, wb.sheet_names) or wb.sheet_names


# ── Internal Helpers ───────────────────────────────────────────────────────────

def _detect_bom_sheets(wb: CalamineWorkbook, all_sheets: list[str]) -> list[str]:
    """Return ordered list of sheets that look like BOM data sheets."""
    candidates: list[str] = []

    # Preferred: sheet named exactly "021"
    if PREFERRED_SHEET in all_sheets:
        candidates.append(PREFERRED_SHEET)

    # Scan remaining sheets for REPERE anchor
    for sname in all_sheets:
        if sname in candidates:
            continue
        try:
            rows = wb.get_sheet_by_name(sname).to_python()
            if _find_header_row(rows, max_rows=20) is not None:
                candidates.append(sname)
        except Exception:
            continue

    return candidates


def _find_header_row(rows: list[list[Any]], max_rows: int = HEADER_SCAN_ROWS) -> int | None:
    """
    Scan rows to find the French/Technical header row.
    Returns row index (0-based) or None if not found.
    """
    for i, row in enumerate(rows[:max_rows]):
        row_upper = {str(c).strip().upper() for c in row if c is not None and str(c).strip()}
        # Must contain REPERE anchor
        if not row_upper.intersection(REPERE_ANCHORS):
            continue
        # Must contain at least MIN_SECONDARY_HITS secondary anchors
        secondary_hits = row_upper.intersection(SECONDARY_ANCHORS)
        if len(secondary_hits) >= MIN_SECONDARY_HITS:
            return i
    return None


def _build_column_map(
    h_fr: list[Any],
    h_en: list[Any],
    warnings: list[str],
) -> tuple[dict, list[tuple], list[str]]:
    """
    Build internal_key -> {idx, en_name, fr_name} mapping.

    Returns:
        col_map          : {internal_key: {"idx": int, "en_name": str, "fr_name": str}}
        available_columns: [(internal_key, en_name, fr_name), ...]
        raw_columns      : [raw_header_name, ...]
    """
    # Build reverse alias lookup: raw_name_upper -> internal_key
    alias_lookup: dict[str, str] = {}
    for internal_key, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            alias_lookup[alias.upper().strip()] = internal_key

    col_map: dict[str, dict] = {}
    available_columns: list[tuple] = []
    raw_columns: list[str] = []
    seen_keys: set[str] = set()

    for idx, raw_name in enumerate(h_fr):
        if raw_name is None or str(raw_name).strip() == "":
            # Try to get a name from English header
            en_raw = h_en[idx] if idx < len(h_en) else None
            if en_raw is None or str(en_raw).strip() == "" or isinstance(en_raw, (int, float)):
                continue
            raw_name = str(en_raw).strip()
        else:
            raw_name = str(raw_name).strip()

        raw_columns.append(raw_name)
        raw_upper = raw_name.upper().strip()
        internal_key = alias_lookup.get(raw_upper, raw_name)  # fallback: use raw name as key

        # English display name
        en_raw = h_en[idx] if idx < len(h_en) else None
        en_name = str(en_raw).strip() if (en_raw and str(en_raw).strip()
                                           and not isinstance(en_raw, (int, float))) else raw_name

        # Avoid duplicate key assignments
        if internal_key in seen_keys:
            warnings.append(f"Duplicate column mapping for '{internal_key}' (raw: '{raw_name}') — skipping.")
            continue
        seen_keys.add(internal_key)

        col_map[internal_key] = {"idx": idx, "en_name": en_name, "fr_name": raw_name}
        available_columns.append((internal_key, en_name, raw_name))

    return col_map, available_columns, raw_columns


def _normalize_repere(val: Any) -> str | None:
    """
    Normalize a REPERE cell value to a clean integer string.
    Returns None if the value is empty, non-numeric, or a header sentinel.
    """
    if val is None:
        return None
    val_str = str(val).strip()
    if val_str == "" or val_str.upper() in REPERE_ANCHORS:
        return None
    # Float like 4001.0 -> "4001"
    try:
        f = float(val_str.replace(",", "."))
        if f != int(f):
            return None  # Non-integer REPERE — skip
        return str(int(f))
    except (ValueError, TypeError):
        return None


def _normalize_value(val: Any) -> str:
    """
    Normalize a cell value to a clean comparable string.
    Returns "" for blank/null/sentinel values.
    """
    if val is None:
        return ""
    val_str = str(val).strip()
    if val_str in ("", "None", "nan", "NaN", "NULL", "N/A"):
        return ""
    # Float like 4.0 -> "4"
    try:
        f = float(val_str.replace(",", "."))
        if f == int(f):
            return str(int(f))
    except (ValueError, TypeError):
        pass
    return val_str
