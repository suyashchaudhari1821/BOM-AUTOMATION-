import re
from datetime import datetime

def generate_comparison_filename(old_name=None, new_name=None):
    """Generates COMPARISON_REPORT_<DATE>.xlsx or combined dates if names are provided."""
    
    def extract_date(filename):
        if not filename: return None
        match = re.search(r'(\d{1,2}_[a-zA-Z]+_\d{4})', filename, re.IGNORECASE)
        if match:
            return match.group(1).upper()
        return None

    if old_name and new_name:
        old_date = extract_date(old_name)
        new_date = extract_date(new_name)
        if old_date and new_date:
            return f"COMPARISON_REPORT_{old_date}_TO_{new_date}.xlsx"
            
    now = datetime.now()
    date_str = now.strftime("%d_%b_%Y").upper()
    return f"COMPARISON_REPORT_{date_str}.xlsx"
