import os
import json
from datetime import datetime
import threading

# Use project root for data directory
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
ACTIVITY_LOG_FILE = os.path.join(DATA_DIR, "activity_log.json")
SUMMARY_FILE = os.path.join(DATA_DIR, "latest_comparison_summary.json")

# Ensure thread-safe file writing since Streamlit runs multiple threads
_log_lock = threading.Lock()

def _ensure_data_dir():
    """Ensure the data directory exists."""
    if not os.path.exists(DATA_DIR):
        try:
            os.makedirs(DATA_DIR, exist_ok=True)
        except Exception:
            pass

def log_activity(
    title: str, 
    status: str, 
    status_color: str, 
    icon: str,
    duration_seconds: float = None,
    rows_processed: int = None,
    operation_type: str = "System",
    user: str = "System"
):
    """
    Appends a new activity to the JSON log file safely.
    Keeps a maximum of 50 activities to prevent file bloat.
    """
    _ensure_data_dir()
    
    new_entry = {
        "icon": icon,
        "title": title,
        "timestamp": datetime.now().strftime("%b %d, %Y %I:%M %p"),
        "status": status,
        "status_color": status_color,
        "duration_seconds": duration_seconds,
        "rows_processed": rows_processed,
        "operation_type": operation_type,
        "user": user
    }

    with _log_lock:
        activities = []
        if os.path.exists(ACTIVITY_LOG_FILE):
            try:
                with open(ACTIVITY_LOG_FILE, "r", encoding="utf-8") as f:
                    activities = json.load(f)
            except Exception:
                activities = []
        
        # Insert at the beginning (newest first)
        activities.insert(0, new_entry)
        
        # Keep only the last 50 activities
        activities = activities[:50]
        
        try:
            with open(ACTIVITY_LOG_FILE, "w", encoding="utf-8") as f:
                json.dump(activities, f, indent=2)
        except Exception as e:
            print(f"Failed to write activity log: {e}")

def update_comparison_summary(no_change: int, modified: int, added: int, deleted: int):
    """
    Writes the latest comparison metadata summary to a JSON file.
    """
    _ensure_data_dir()
    
    total = no_change + modified + added + deleted
    
    # Calculate percentages for the frontend
    def safe_percent(val):
        return round((val / total) * 100, 1) if total > 0 else 0

    summary = {
        "total": f"{total:,}",
        "segments": [
            {"label": "No Change", "value": f"{no_change:,}", "percent": safe_percent(no_change), "color": "#3B82F6"},
            {"label": "Modified", "value": f"{modified:,}", "percent": safe_percent(modified), "color": "#F59E0B"},
            {"label": "Added", "value": f"{added:,}", "percent": safe_percent(added), "color": "#10B981"},
            {"label": "Deleted", "value": f"{deleted:,}", "percent": safe_percent(deleted), "color": "#EF4444"},
        ]
    }
    
    with _log_lock:
        try:
            with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
                json.dump(summary, f, indent=2)
        except Exception as e:
            print(f"Failed to write comparison summary: {e}")
