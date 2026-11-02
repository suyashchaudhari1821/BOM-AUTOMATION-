"""
comparator.py — Core Tooling BOM Diff Engine.

Compares Old BOM vs New BOM DataFrames and produces structured change rows.

Logic:
  - Keyed by REPERE (Item / Balloon Number)
  - Standard Parts : int(REPERE) >= STANDARD_THRESHOLD
  - Non-Standard   : int(REPERE) <  STANDARD_THRESHOLD
  - For each partition: detect New, Deleted, and field-level Modified items
  - All values normalized before comparison (no false positives from whitespace/float)
  - Output is fully dynamic — no hardcoded counts or expected values
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

import pandas as pd

from tooling_bom.column_config import (
    CHANGE_TYPE_MAP,
    CORE_TRACKED_COLUMNS,
    PART_CATEGORY_NON_STANDARD,
    PART_CATEGORY_STANDARD,
    STANDARD_THRESHOLD,
    get_change_type,
    get_column_display,
)


# ── Type alias ─────────────────────────────────────────────────────────────────
ChangeRow = dict[str, str]


# ── Public API ─────────────────────────────────────────────────────────────────

def compare(
    old_df: pd.DataFrame,
    new_df: pd.DataFrame,
    columns_to_compare: list[tuple[str, str, str]] | None = None,
    nonstd_columns_to_compare: list[tuple[str, str, str]] | None = None,
) -> dict:
    """
    Compare two BOM DataFrames and return structured change results.

    Parameters
    ----------
    old_df                    : DataFrame from loader (must have 'REPERE' column)
    new_df                    : DataFrame from loader (must have 'REPERE' column)
    columns_to_compare        : list of (internal_key, en_name, fr_name) for Standard parts.
                                If None, defaults to CORE_TRACKED_COLUMNS.
    nonstd_columns_to_compare : list of (internal_key, en_name, fr_name) for Non-Standard parts.
                                If None, defaults to columns_to_compare.

    Returns
    -------
    dict:
        "standard"          : list[ChangeRow] — change rows for REPERE >= 4000
        "non_standard"      : list[ChangeRow] — change rows for REPERE < 4000
        "summary"           : dict with computed counts (fully dynamic, nothing hardcoded)
        "old_count_std"     : int — total Standard parts in old BOM
        "new_count_std"     : int — total Standard parts in new BOM
        "old_count_nonstd"  : int — total Non-Standard parts in old BOM
        "new_count_nonstd"  : int — total Non-Standard parts in new BOM
    """
    if columns_to_compare is None:
        columns_to_compare = CORE_TRACKED_COLUMNS
    if nonstd_columns_to_compare is None:
        nonstd_columns_to_compare = columns_to_compare

    # ── Build lookup dicts keyed by REPERE ────────────────────────────────────
    old_dict = _build_lookup(old_df)
    new_dict = _build_lookup(new_df)

    # ── Partition by Standard / Non-Standard ──────────────────────────────────
    old_std, old_nonstd = _partition(old_dict)
    new_std, new_nonstd = _partition(new_dict)

    # ── Run comparison for each partition ─────────────────────────────────────
    std_rows    = _compare_partition(old_std,    new_std,    PART_CATEGORY_STANDARD,     columns_to_compare)
    nonstd_rows = _compare_partition(old_nonstd, new_nonstd, PART_CATEGORY_NON_STANDARD, nonstd_columns_to_compare)

    # ── Compute summary counts (all dynamic from actual data) ─────────────────
    summary = _compute_summary(std_rows, nonstd_rows)

    return {
        "standard":          std_rows,
        "non_standard":      nonstd_rows,
        "summary":           summary,
        "old_count_std":     len(old_std),
        "new_count_std":     len(new_std),
        "old_count_nonstd":  len(old_nonstd),
        "new_count_nonstd":  len(new_nonstd),
    }


# ── Internal Helpers ───────────────────────────────────────────────────────────

def _build_lookup(df: pd.DataFrame) -> dict[str, dict[str, str]]:
    """Build {repere_str: {col_key: value}} from a DataFrame."""
    lookup: dict[str, dict[str, str]] = {}
    if df is None or df.empty or "REPERE" not in df.columns:
        return lookup
    for _, row in df.iterrows():
        rep = str(row["REPERE"]).strip()
        if not rep:
            continue
        lookup[rep] = {col: _normalize(row.get(col, "")) for col in df.columns if col != "REPERE"}
    return lookup


def _partition(data: dict[str, dict]) -> tuple[dict, dict]:
    """Split lookup dict into (standard, non_standard) based on REPERE threshold."""
    std:    dict[str, dict] = {}
    nonstd: dict[str, dict] = {}
    for rep, row in data.items():
        try:
            if int(rep) >= STANDARD_THRESHOLD:
                std[rep] = row
            else:
                nonstd[rep] = row
        except (ValueError, TypeError):
            # REPERE not parseable as integer — skip with no crash
            continue
    return std, nonstd


def _compare_partition(
    old: dict[str, dict],
    new: dict[str, dict],
    category: str,
    columns_to_compare: list[tuple[str, str, str]],
) -> list[ChangeRow]:
    """
    Compare one partition (std or non-std) and return all change rows.
    Order: Modified first (sorted by REPERE), then New, then Deleted.
    """
    old_keys = set(old.keys())
    new_keys = set(new.keys())

    added_keys   = new_keys - old_keys
    deleted_keys = old_keys - new_keys
    common_keys  = old_keys & new_keys

    rows: list[ChangeRow] = []

    # ── Modified items (field-level diffs on common parts) ────────────────────
    for rep in sorted(common_keys, key=lambda x: int(x)):
        old_row = old[rep]
        new_row = new[rep]
        for (col_key, en_name, fr_name) in columns_to_compare:
            old_val = _normalize(old_row.get(col_key, ""))
            new_val = _normalize(new_row.get(col_key, ""))
            if old_val == new_val:
                continue  # no change — no noise
            change_en, change_fr = get_change_type(col_key)
            rows.append({
                "item_no":         rep,
                "part_category":   category,
                "change_type_en":  change_en,
                "change_type_fr":  change_fr,
                "column_en":       en_name,
                "column_fr":       fr_name,
                "old_value":       old_val if old_val else "(Blank / Vide)",
                "new_value":       new_val if new_val else "(Blank / Vide)",
            })

    # ── New items (present in new BOM only) ───────────────────────────────────
    for rep in sorted(added_keys, key=lambda x: int(x)):
        change_en, change_fr = CHANGE_TYPE_MAP["_NEW_ITEM"]
        rows.append({
            "item_no":         rep,
            "part_category":   category,
            "change_type_en":  change_en,
            "change_type_fr":  change_fr,
            "column_en":       "-",
            "column_fr":       "-",
            "old_value":       "-",
            "new_value":       "Added / Ajoute",
        })

    # ── Deleted items (present in old BOM only) ───────────────────────────────
    for rep in sorted(deleted_keys, key=lambda x: int(x)):
        change_en, change_fr = CHANGE_TYPE_MAP["_DELETED"]
        rows.append({
            "item_no":         rep,
            "part_category":   category,
            "change_type_en":  change_en,
            "change_type_fr":  change_fr,
            "column_en":       "-",
            "column_fr":       "-",
            "old_value":       "Present",
            "new_value":       "Removed / Supprime",
        })

    return rows


def _compute_summary(
    std_rows: list[ChangeRow],
    nonstd_rows: list[ChangeRow],
) -> dict[str, int]:
    """Compute all KPI counts dynamically from the actual change rows."""
    def _counts(rows: list[ChangeRow]) -> dict[str, int]:
        new_rows     = [r for r in rows if r["change_type_en"] == "New Item"]
        del_rows     = [r for r in rows if r["change_type_en"] == "Deleted Item"]
        field_rows   = [r for r in rows if r["change_type_en"] not in ("New Item", "Deleted Item")]
        mod_items    = len(set(r["item_no"] for r in field_rows))
        return {
            "new":            len(new_rows),
            "deleted":        len(del_rows),
            "modified":       mod_items,
            "changed_fields": len(field_rows),
        }

    sc = _counts(std_rows)
    nc = _counts(nonstd_rows)

    return {
        "std_new":            sc["new"],
        "std_deleted":        sc["deleted"],
        "std_modified":       sc["modified"],
        "std_changed_fields": sc["changed_fields"],
        "nonstd_new":            nc["new"],
        "nonstd_deleted":        nc["deleted"],
        "nonstd_modified":       nc["modified"],
        "nonstd_changed_fields": nc["changed_fields"],
    }


def _normalize(val: Any) -> str:
    """
    Normalize a value to a clean comparable string.
    - None / empty / "nan" -> ""
    - Keeps exact raw string value without number conversions
    - Strips leading/trailing whitespace
    """
    if val is None:
        return ""
    s = str(val).strip()
    if s in ("", "None", "nan", "NaN", "NULL", "N/A"):
        return ""
    return s


def rows_to_dataframe(rows: list[ChangeRow]) -> pd.DataFrame:
    """Convert a list of change rows to a display DataFrame."""
    if not rows:
        return pd.DataFrame(columns=[
            "item_no", "part_category", "change_type_en", "change_type_fr",
            "column_en", "column_fr", "old_value", "new_value"
        ])
    return pd.DataFrame(rows)
