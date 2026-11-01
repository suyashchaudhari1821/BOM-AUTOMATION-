from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# Create a high-res 2400x1350 canvas (16:9 4K crisp)
W, H = 2400, 1350
img = Image.new("RGBA", (W, H), (11, 7, 20, 255)) # Expleo deep matte navy-black #0B0714
draw = ImageDraw.Draw(img)

# Load fonts
try:
    font_logo = ImageFont.truetype("segoeuib.ttf", 44)
    font_pipe = ImageFont.truetype("segoeui.ttf", 38)
    font_title = ImageFont.truetype("segoeuib.ttf", 34)
    font_head = ImageFont.truetype("segoeuib.ttf", 25)
    font_bold = ImageFont.truetype("segoeuib.ttf", 22)
    font_norm = ImageFont.truetype("segoeui.ttf", 20)
    font_sm = ImageFont.truetype("segoeui.ttf", 17)
except Exception:
    font_logo = font_pipe = font_title = font_head = font_bold = font_norm = font_sm = ImageFont.load_default()

# ── Color Palette (Expleo Corporate) ──
BG_DARK = (11, 7, 20)
EXPLEO_VIOLET = (92, 53, 181)       # #5C35B5
EXPLEO_ACCENT = (104, 70, 198)     # #6846C6
CARD_BG = (22, 16, 38)
BORDER_COLOR = (104, 70, 198)
TEXT_WHITE = (255, 255, 255)
TEXT_MUTED = (160, 174, 192)
LINE_COLOR = (128, 92, 229)

# Outcomes
GREEN_BG = (16, 45, 30)
GREEN_BORDER = (16, 185, 129)
GREEN_TEXT = (52, 211, 153)

RED_BG = (45, 18, 22)
RED_BORDER = (239, 68, 68)
RED_TEXT = (248, 113, 113)

YELLOW_BG = (45, 32, 14)
YELLOW_BORDER = (245, 158, 11)
YELLOW_TEXT = (251, 191, 36)

# Unchanged / Filtered
GRAY_BG = (18, 22, 34)
GRAY_BORDER = (100, 116, 139)
GRAY_TEXT = (148, 163, 184)

# ── 1. Top Expleo Header (BOM Intelligence) ──
draw.text((120, 50), "( expleo )", font=font_logo, fill=TEXT_WHITE)
draw.text((370, 52), "|", font=font_pipe, fill=LINE_COLOR)
draw.text((410, 54), "BOM Intelligence", font=font_title, fill=TEXT_WHITE)
draw.line([(120, 120), (W - 120, 120)], fill=(255, 255, 255, 40), width=2)

# Helper function to draw rounded card with border
def draw_card(box, fill_c, border_c, radius=16, border_w=2):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill_c, outline=border_c, width=border_w)

def draw_arrow(start, end, color=LINE_COLOR, width=3, arrow_size=11):
    x0, y0 = start
    x1, y1 = end
    draw.line([start, end], fill=color, width=width)
    if y1 > y0 and x1 == x0: # pointing down
        draw.polygon([(x1 - arrow_size, y1 - arrow_size), (x1 + arrow_size, y1 - arrow_size), (x1, y1)], fill=color)
    elif y1 < y0 and x1 == x0: # pointing up
        draw.polygon([(x1 - arrow_size, y1 + arrow_size), (x1 + arrow_size, y1 + arrow_size), (x1, y1)], fill=color)
    elif x1 > x0 and y1 == y0: # pointing right
        draw.polygon([(x1 - arrow_size, y1 - arrow_size), (x1 - arrow_size, y1 + arrow_size), (x1, y1)], fill=color)

# ── 2. Top Pipeline: Perfectly Centered Across 2400px ──
b1_x0, b1_x1 = 190, 810
b2_x0, b2_x1 = 890, 1510
b3_x0, b3_x1 = 1590, 2210
top_y0, top_y1 = 160, 250

# Box 1: Start
draw_card([b1_x0, top_y0, b1_x1, top_y1], EXPLEO_VIOLET, (150, 120, 255), radius=18)
draw.text((b1_x0 + 30, 180), "START: Login & Access", font=font_head, fill=TEXT_WHITE)
draw.text((b1_x0 + 30, 215), "Verify corporate credentials & open workspace", font=font_sm, fill=(225, 215, 255))

draw_arrow((b1_x1, 205), (b2_x0, 205), color=LINE_COLOR, width=4, arrow_size=12)

# Box 2: Upload Files
draw_card([b2_x0, top_y0, b2_x1, top_y1], CARD_BG, EXPLEO_ACCENT, radius=18)
draw.text((b2_x0 + 30, 180), "Upload Old & New BOM Files", font=font_head, fill=TEXT_WHITE)
draw.text((b2_x0 + 30, 215), "Load old BOM file & new BOM file", font=font_sm, fill=TEXT_MUTED)

draw_arrow((b2_x1, 205), (b3_x0, 205), color=LINE_COLOR, width=4, arrow_size=12)

# Box 3: Read & Match
draw_card([b3_x0, top_y0, b3_x1, top_y1], CARD_BG, EXPLEO_ACCENT, radius=18)
draw.text((b3_x0 + 30, 180), "Read Files & Match Rows by Part ID", font=font_head, fill=TEXT_WHITE)
draw.text((b3_x0 + 30, 215), "Automatically read headers & match parts", font=font_sm, fill=TEXT_MUTED)

# ── 3. Central Symmetrical Distribution Bus ──
draw.line([(1900, 250), (1900, 290)], fill=LINE_COLOR, width=4)
draw.line([(1900, 290), (1200, 290)], fill=LINE_COLOR, width=4)
draw.line([(1200, 290), (1200, 320)], fill=LINE_COLOR, width=4)

c1_center = 330
c2_center = 890
c3_group_center = 1760
c3_center = 1510
c4_center = 2100

# Symmetrical horizontal bus
draw.line([(c1_center, 320), (c3_group_center, 320)], fill=LINE_COLOR, width=4)
draw_arrow((c1_center, 320), (c1_center, 365), color=LINE_COLOR, width=4, arrow_size=12)
draw_arrow((c2_center, 320), (c2_center, 365), color=LINE_COLOR, width=4, arrow_size=12)
draw_arrow((c3_group_center, 320), (c3_group_center, 365), color=LINE_COLOR, width=4, arrow_size=12)

# ═════════════════════════════════════════════════════════════════════════════
# COLUMN 1: In New File Only? ➔ ADDED PART
# ═════════════════════════════════════════════════════════════════════════════
col1_x0, col1_x1 = 80, 580

# Condition Card
draw_card([col1_x0, 365, col1_x1, 455], CARD_BG, EXPLEO_ACCENT, radius=14)
draw.text((col1_x0 + 25, 385), "In New File Only?", font=font_head, fill=TEXT_WHITE)
draw.text((col1_x0 + 25, 420), "Part exists in new BOM, absent in old BOM", font=font_sm, fill=TEXT_MUTED)

draw_arrow((c1_center, 455), (c1_center, 525), color=GREEN_BORDER, width=4, arrow_size=12)
draw.text((c1_center + 15, 480), "YES", font=font_bold, fill=GREEN_TEXT)

# Outcome Card: ADDED PART
draw_card([col1_x0, 525, col1_x1, 805], GREEN_BG, GREEN_BORDER, radius=20, border_w=3)
draw.text((col1_x0 + 30, 555), "[+] ADDED PART", font=font_title, fill=GREEN_TEXT)
draw.text((col1_x0 + 30, 615), "Classification: New Item", font=font_bold, fill=TEXT_WHITE)
draw.text((col1_x0 + 30, 670), "• Added to new BOM file", font=font_norm, fill=TEXT_WHITE)
draw.text((col1_x0 + 30, 715), "• Highlighted in Soft Green in Excel", font=font_norm, fill=TEXT_WHITE)

# ═════════════════════════════════════════════════════════════════════════════
# COLUMN 2: In Old File Only? ➔ DELETED PART
# ═════════════════════════════════════════════════════════════════════════════
col2_x0, col2_x1 = 640, 1140

# Condition Card
draw_card([col2_x0, 365, col2_x1, 455], CARD_BG, EXPLEO_ACCENT, radius=14)
draw.text((col2_x0 + 25, 385), "In Old File Only?", font=font_head, fill=TEXT_WHITE)
draw.text((col2_x0 + 25, 420), "Part exists in old BOM, missing in new BOM", font=font_sm, fill=TEXT_MUTED)

draw_arrow((c2_center, 455), (c2_center, 525), color=RED_BORDER, width=4, arrow_size=12)
draw.text((c2_center + 15, 480), "YES", font=font_bold, fill=RED_TEXT)

# Outcome Card: DELETED PART
draw_card([col2_x0, 525, col2_x1, 805], RED_BG, RED_BORDER, radius=20, border_w=3)
draw.text((col2_x0 + 30, 555), "[-] DELETED PART", font=font_title, fill=RED_TEXT)
draw.text((col2_x0 + 30, 615), "Classification: Removed Part", font=font_bold, fill=TEXT_WHITE)
draw.text((col2_x0 + 30, 670), "• Removed from new BOM file", font=font_norm, fill=TEXT_WHITE)
draw.text((col2_x0 + 30, 715), "• Highlighted in Soft Red in Excel", font=font_norm, fill=TEXT_WHITE)

# ═════════════════════════════════════════════════════════════════════════════
# COLUMNS 3 & 4: Part in Both Files? (Two Possibilities: Differ vs Match)
# ═════════════════════════════════════════════════════════════════════════════
col3_x0, col3_x1 = 1200, 1820
col4_x0, col4_x1 = 1880, 2320

# Shared Condition Card for Both Files
draw_card([1200, 365, 2320, 455], CARD_BG, EXPLEO_ACCENT, radius=14)
draw.text((1200 + 30, 385), "Part in Both Files? (Matched by Part ID)", font=font_head, fill=TEXT_WHITE)
draw.text((1200 + 30, 420), "Compares tracked fields: Quantity, Material, Supplier, Drawing # across both files", font=font_sm, fill=TEXT_MUTED)

# Branch 1: Values Differ? ➔ MODIFIED PART (Included in Report)
draw_arrow((c3_center, 455), (c3_center, 525), color=YELLOW_BORDER, width=4, arrow_size=12)
draw.text((c3_center - 220, 480), "Values Differ (YES)", font=font_bold, fill=YELLOW_TEXT)

# Outcome Card: MODIFIED PART
draw_card([col3_x0, 525, col3_x1, 805], YELLOW_BG, YELLOW_BORDER, radius=20, border_w=3)
draw.text((col3_x0 + 30, 555), "[Δ] MODIFIED PART", font=font_title, fill=YELLOW_TEXT)
draw.text((col3_x0 + 30, 605), "Row-by-Row Value Changes:", font=font_bold, fill=TEXT_WHITE)
draw.text((col3_x0 + 30, 642), "• Compares each cell: Old -> New Value", font=font_norm, fill=TEXT_WHITE)
draw.text((col3_x0 + 30, 675), "• Quantity: 4 -> 8   |   Material: Alloy -> Tool Steel", font=font_sm, fill=(245, 230, 190))
draw.text((col3_x0 + 30, 705), "• Supplier: Acme Tools -> Expleo Precision", font=font_sm, fill=(245, 230, 190))
draw.text((col3_x0 + 30, 745), "• Highlighted in Soft Yellow in Excel", font=font_norm, fill=YELLOW_TEXT)

# Branch 2: Values Match? ➔ UNCHANGED (Filtered out / Excluded from Report)
draw_arrow((c4_center, 455), (c4_center, 525), color=GRAY_BORDER, width=4, arrow_size=12)
draw.text((c4_center + 15, 480), "Values Match (NO)", font=font_bold, fill=GRAY_TEXT)

# Outcome Card: UNCHANGED PART
draw_card([col4_x0, 525, col4_x1, 805], GRAY_BG, GRAY_BORDER, radius=20, border_w=3)
draw.text((col4_x0 + 25, 555), "[=] UNCHANGED PART", font=font_title, fill=GRAY_TEXT)
draw.text((col4_x0 + 25, 605), "Classification: No Change", font=font_bold, fill=TEXT_WHITE)
draw.text((col4_x0 + 25, 650), "• All tracked values identical", font=font_norm, fill=TEXT_WHITE)
draw.text((col4_x0 + 25, 690), "• Present in both BOM files", font=font_norm, fill=TEXT_MUTED)
draw.text((col4_x0 + 25, 730), "• Filtered out to avoid noise", font=font_norm, fill=GRAY_TEXT)

# Filtered out indicator below Unchanged Card
draw.line([(c4_center, 805), (c4_center, 875)], fill=GRAY_BORDER, width=3)
pill_w = 320
pill_x0 = c4_center - pill_w // 2
pill_x1 = c4_center + pill_w // 2
draw_card([pill_x0, 875, pill_x1, 935], (28, 16, 24), (190, 70, 85), radius=28, border_w=2)
draw.text((pill_x0 + 38, 893), "Excluded from Report", font=font_bold, fill=(248, 113, 113))

# ═════════════════════════════════════════════════════════════════════════════
# 4. BOTTOM CONVERGENCE: Only Added, Deleted, and Modified Feed into Report
# ═════════════════════════════════════════════════════════════════════════════
draw.line([(c1_center, 805), (c1_center, 890)], fill=GREEN_BORDER, width=4)
draw.line([(c2_center, 805), (c2_center, 890)], fill=RED_BORDER, width=4)
draw.line([(c3_center, 805), (c3_center, 890)], fill=YELLOW_BORDER, width=4)

# Symmetrical Convergence Bus across Cols 1, 2, 3
draw.line([(c1_center, 890), (c3_center, 890)], fill=EXPLEO_ACCENT, width=4)
# Route to center of report (x = 1000)
rep_center = 1000
draw_arrow((rep_center, 890), (rep_center, 950), color=EXPLEO_ACCENT, width=4, arrow_size=14)

# Final Box: Generate Report (Centered at x = 1000)
rep_w = 980
rep_x0 = rep_center - rep_w // 2
rep_x1 = rep_center + rep_w // 2
draw_card([rep_x0, 950, rep_x1, 1070], EXPLEO_VIOLET, (160, 130, 255), radius=22, border_w=3)
draw.text((rep_x0 + 40, 975), "Generate Excel Comparison Report & Dashboard", font=font_title, fill=TEXT_WHITE)
draw.text((rep_x0 + 40, 1025), "Compiles only Added (Green), Deleted (Red), and Modified (Yellow) changes", font=font_norm, fill=(230, 220, 255))

draw_arrow((rep_center, 1070), (rep_center, 1140), color=LINE_COLOR, width=4, arrow_size=14)

# End Terminal
end_w = 460
end_x0 = rep_center - end_w // 2
end_x1 = rep_center + end_w // 2
draw_card([end_x0, 1140, end_x1, 1220], (25, 18, 45), (140, 100, 240), radius=40, border_w=2)
draw.text((end_x0 + 105, 1165), "END: Audit Complete", font=font_head, fill=TEXT_WHITE)

# Save the image to the project root
dest_path = Path(r"c:\Users\HP\Downloads\ICAS\bom_intelligence_flowchart.png")
img.save(dest_path, "PNG")
print("SUCCESSFULLY SAVED TO WORKSPACE:", dest_path)

# Also copy to current artifact directory
artifact_dir = Path(r"C:\Users\HP\.gemini\antigravity-ide\brain\3a93140f-00be-41e5-bb3f-fa774c6aa5fb")
if artifact_dir.exists():
    artifact_img = artifact_dir / "bom_intelligence_flowchart.png"
    img.save(artifact_img, "PNG")
    print("SAVED TO ARTIFACT DIR:", artifact_img)
