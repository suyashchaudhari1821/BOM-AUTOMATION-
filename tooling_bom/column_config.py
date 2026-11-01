"""
column_config.py — Central registry for all BOM column knowledge.

Single source of truth for:
  - Column alias mapping (handles renames, spelling variants, French/English)
  - Core 6 tracked columns (selected by default)
  - All available columns (for "All Columns" mode)
  - Bilingual change type descriptions
  - REPERE threshold for Standard vs Non-Standard classification
"""

# ── Column Aliases ─────────────────────────────────────────────────────────────
# Maps internal key -> list of all known raw names (case-insensitive matching)
COLUMN_ALIASES: dict[str, list[str]] = {
    "REPERE":       ["REPERE", "Baloon #", "Balloon #", "Item No", "No. Repere", "repere", "No Repere"],
    "NOPLAN":       ["NOPLAN", "dwg#", "dwg #", "Drawing No", "No Plan", "NOPLAN"],
    "NOPLANCHE":    ["NOPLANCHE", "page #", "page#", "Page", "No Planche", "NOPLANCHE"],
    "DESIGN":       ["DESIGN", "Designation FRANCAISE", "description FR", "designation", "Description FR"],
    "DESIGN EN":    ["DESIGN EN", "description", "ENGLISH Designation", "English Description", "English Desc"],
    "CONSTRUCTEUR": ["CONSTRUCTEUR", "maker", "Fabricant", "Manufacturer", "Constructeur", "Fournisseur"],
    "REFCONST":     ["REFCONST", "maker  P/N", "maker P/N", "Reference constructeur", "Manufacturer Part Number",
                     "Ref Const", "REFCONST", "MPN", "Part Number"],
    "CodeIM":       ["CodeIM", "Code IM", "IM Code", "IM_Code", "codeIM", "Code_IM"],
    "MABEC":        ["MABEC", "MABEC Code", "Code MABEC", "N MABEC", "No MABEC", "mabec"],
    "COEF":         ["COEF", "Quantite", "Quantité", "Qty", "Quantity", "Qt", "coef", "1"],
    "PR":           ["PR", "Spare", "Spare Part", "Piece Rechange"],
    "SOUSENS":      ["SOUSENS", "sub assy", "Sub Assembly", "Sous Ensemble"],
    "INDICE":       ["INDICE", "realease", "release", "Release", "Index", "Indice"],
    "MATIERE":      ["MATIERE", "material", "Material", "Matiere", "Matière"],
    "DIMENSIONS":   ["DIMENSIONS", "size", "Size", "Dimension", "Dimensions"],
    "MASSE":        ["MASSE", "weight", "Weight", "Masse"],
    "CATEGORIE":    ["CATEGORIE", "Category", "Cat", "Categorie"],
    "FIXATION":     ["FIXATION", "Fixation", "Fastening"],
    "Source Base":  ["Source Base", "source base", "Base Source"],
    "PR Specifique":["PR Specifique", "PR Spec", "Specific PR"],
}

# ── Core Tracked Columns (default selection, pre-checked in UI) ────────────────
# Tuple: (internal_key, english_display_name, french_display_name)
CORE_TRACKED_COLUMNS: list[tuple[str, str, str]] = [
    ("CodeIM",       "IM Code",                   "Code IM"),
    ("CONSTRUCTEUR", "Manufacturer",               "Constructeur"),
    ("REFCONST",     "Manufacturer Part Number",   "Reference constructeur"),
    ("MABEC",        "MABEC Code",                 "Code MABEC"),
    ("COEF",         "Quantity",                   "Quantite"),
    ("DESIGN EN",    "English Description",        "Designation anglaise"),
]

# ── All Trackable Columns (available in "All Columns" mode) ───────────────────
ALL_TRACKABLE_COLUMNS: list[tuple[str, str, str]] = [
    ("CodeIM",       "IM Code",                   "Code IM"),
    ("CONSTRUCTEUR", "Manufacturer",               "Constructeur"),
    ("REFCONST",     "Manufacturer Part Number",   "Reference constructeur"),
    ("MABEC",        "MABEC Code",                 "Code MABEC"),
    ("COEF",         "Quantity",                   "Quantite"),
    ("DESIGN EN",    "English Description",        "Designation anglaise"),
    ("DESIGN",       "French Description",         "Designation francaise"),
    ("MATIERE",      "Material",                   "Matiere"),
    ("DIMENSIONS",   "Dimensions",                 "Dimensions"),
    ("MASSE",        "Weight",                     "Masse"),
    ("PR",           "Spare Part",                 "Piece de rechange"),
    ("INDICE",       "Release Index",              "Indice"),
    ("CATEGORIE",    "Category",                   "Categorie"),
]

# ── Bilingual Change Type Descriptions ─────────────────────────────────────────
# Maps internal_key -> (english_change_type, french_change_type)
CHANGE_TYPE_MAP: dict[str, tuple[str, str]] = {
    "CodeIM":        ("IM Code Changed",                    "Code IM modifie"),
    "CONSTRUCTEUR":  ("Manufacturer Changed",               "Constructeur modifie"),
    "REFCONST":      ("Manufacturer Part Number Changed",   "Reference constructeur modifiee"),
    "MABEC":         ("MABEC Code Changed",                 "Code MABEC modifie"),
    "COEF":          ("Quantity Changed",                   "Quantite modifiee"),
    "DESIGN EN":     ("Description Changed",                "Designation modifiee"),
    "DESIGN":        ("French Description Changed",         "Designation francaise modifiee"),
    "MATIERE":       ("Material Changed",                   "Matiere modifiee"),
    "DIMENSIONS":    ("Dimensions Changed",                 "Dimensions modifiees"),
    "MASSE":         ("Weight Changed",                     "Masse modifiee"),
    "PR":            ("Spare Part Status Changed",          "Statut piece de rechange modifie"),
    "INDICE":        ("Release Index Changed",              "Indice de revision modifie"),
    "CATEGORIE":     ("Category Changed",                   "Categorie modifiee"),
    "_NEW_ITEM":     ("New Item",                           "Nouvel article"),
    "_DELETED":      ("Deleted Item",                       "Article supprime"),
}

# ── Classification Threshold ───────────────────────────────────────────────────
# Parts with REPERE >= this value are "Standard Parts" (STD fasteners, pneumatics)
# Parts with REPERE <  this value are "Non-Standard Parts" (die shoes, machined parts)
STANDARD_THRESHOLD: int = 4000

# ── Part Category Labels ───────────────────────────────────────────────────────
PART_CATEGORY_STANDARD:     str = "STANDARD"
PART_CATEGORY_NON_STANDARD: str = "NON-STANDARD"


def get_column_display(internal_key: str) -> tuple[str, str]:
    """Return (english_name, french_name) for a given internal column key."""
    for key, en, fr in ALL_TRACKABLE_COLUMNS:
        if key == internal_key:
            return en, fr
    return internal_key, internal_key


def get_change_type(internal_key: str) -> tuple[str, str]:
    """Return (english_change_type, french_change_type) for a column key."""
    return CHANGE_TYPE_MAP.get(internal_key, (f"{internal_key} Changed", f"{internal_key} modifie"))
