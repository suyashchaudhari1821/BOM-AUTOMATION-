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
    "REPERE":       ["REPERE", "Baloon #", "Balloon #", "Item No", "Item No.", "Item Number", "Item #", "Item", "No. Repere", "repere", "No Repere"],
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
    "COMMANDE":     ["COMMANDE", "Commande", "Order", "Order Code"],
    "Source Base":  ["Source Base", "source base", "Base Source"],
    "PR Specifique":["PR Specifique", "PR Spec", "Specific PR"],
    "TRAITEMENT":   ["TRAITEMENT", "Traitement", "Treatment", "Heat Treatment"],
    "FOURNISSEUR":  ["FOURNISSEUR", "Fournisseur", "Supplier", "Vendor"],
    "CODE":         ["CODE", "Code"],
    "NORME":        ["N° NORME", "N°NORME", "NORME", "Norme", "Standard Norm", "Standard No"],
}

# ── Core Tracked Columns ───────────────────────────────────────────────────────
# Tuple: (internal_key, english_display_name, french_display_name)
CORE_TRACKED_COLUMNS: list[tuple[str, str, str]] = [
    ("NOPLAN",       "Drawing No.",               "No. Plan"),
    ("NOPLANCHE",    "Sheet / Page No.",          "No. Planche"),
    ("DESIGN",       "French Description",        "Designation francaise"),
    ("DESIGN EN",    "English Description",       "Designation anglaise"),
    ("CONSTRUCTEUR", "Manufacturer",              "Constructeur"),
    ("REFCONST",     "Manufacturer Part Number",  "Reference constructeur"),
    ("CodeIM",       "IM Code",                   "Code IM"),
    ("MABEC",        "MABEC Code",                "Code MABEC"),
    ("COEF",         "Quantity",                  "Quantite"),
    ("PR",           "Spare Part",                "Piece de rechange"),
    ("SOUSENS",      "Sub Assembly",              "Sous Ensemble"),
    ("INDICE",       "Release Index",             "Indice"),
    ("MATIERE",      "Material",                  "Matiere"),
    ("DIMENSIONS",   "Dimensions",                "Dimensions"),
    ("MASSE",        "Weight",                    "Masse"),
    ("CATEGORIE",    "Category",                  "Categorie"),
    ("FIXATION",     "Fastening",                 "Fixation"),
    ("COMMANDE",     "Order Code",                "Commande"),
    ("Source Base",  "Base Source",               "Source Base"),
    ("PR Specifique","Specific PR",               "PR Specifique"),
    ("TRAITEMENT",   "Treatment",                 "Traitement"),
    ("FOURNISSEUR",  "Supplier",                  "Fournisseur"),
    ("CODE",         "Code",                      "Code"),
    ("NORME",        "Standard Norm",             "Norme"),
]

# ── All Trackable Columns ─────────────────────────────────────────────────────
ALL_TRACKABLE_COLUMNS: list[tuple[str, str, str]] = CORE_TRACKED_COLUMNS

# ── Bilingual Change Type Descriptions ─────────────────────────────────────────
# Maps internal_key -> (english_change_type, french_change_type)
CHANGE_TYPE_MAP: dict[str, tuple[str, str]] = {
    "NOPLAN":        ("Drawing Number Changed",             "No. Plan modifie"),
    "NOPLANCHE":     ("Sheet Number Changed",               "No. Planche modifie"),
    "DESIGN":        ("French Description Changed",         "Designation francaise modifiee"),
    "DESIGN EN":     ("Description Changed",                "Designation modifiee"),
    "CONSTRUCTEUR":  ("Manufacturer Changed",               "Constructeur modifie"),
    "REFCONST":      ("Manufacturer Part Number Changed",   "Reference constructeur modifiee"),
    "CodeIM":        ("IM Code Changed",                    "Code IM modifie"),
    "MABEC":         ("MABEC Code Changed",                 "Code MABEC modifie"),
    "COEF":          ("Quantity Changed",                   "Quantite modifiee"),
    "PR":            ("Spare Part Status Changed",          "Statut piece de rechange modifie"),
    "SOUSENS":       ("Sub Assembly Changed",               "Sous Ensemble modifie"),
    "INDICE":        ("Release Index Changed",              "Indice modifie"),
    "MATIERE":       ("Material Changed",                   "Matiere modifiee"),
    "DIMENSIONS":    ("Dimensions Changed",                 "Dimensions modifiees"),
    "MASSE":         ("Weight Changed",                     "Masse modifiee"),
    "CATEGORIE":     ("Category Changed",                   "Categorie modifiee"),
    "FIXATION":      ("Fastening Changed",                  "Fixation modifiee"),
    "COMMANDE":      ("Order Code Changed",                 "Commande modifiee"),
    "Source Base":   ("Base Source Changed",                "Source Base modifiee"),
    "PR Specifique": ("Specific PR Changed",                "PR Specifique modifiee"),
    "TRAITEMENT":    ("Treatment Changed",                  "Traitement modifie"),
    "FOURNISSEUR":   ("Supplier Changed",                   "Fournisseur modifie"),
    "CODE":          ("Code Changed",                       "Code modifie"),
    "NORME":         ("Standard Norm Changed",              "Norme modifiee"),
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

