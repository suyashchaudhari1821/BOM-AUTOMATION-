import sys
sys.path.insert(0, '.')
from tooling_bom.loader import load_bom
from tooling_bom.comparator import compare
from tooling_bom.exporter import export_to_excel
from tooling_bom.column_config import CORE_TRACKED_COLUMNS

OLD = r'C:\Users\HP\Downloads\BOM Comparison Data\BOM Comparison Data\Old_1414162_TRACTION_BATTERY_HOUSING_LONGITUDIN__BOM.xlsm'
NEW = r'C:\Users\HP\Downloads\BOM Comparison Data\BOM Comparison Data\New_1414162_TRACTION_BATTERY_HOUSING_LONGITUDIN__BOM.xlsm'

print('Loading Old BOM...')
old_result = load_bom(OLD)
print('  Sheet:', old_result['sheet_name'], '  Rows:', len(old_result['df']))
print('  Warnings:', old_result['warnings'])

print('Loading New BOM...')
new_result = load_bom(NEW)
print('  Sheet:', new_result['sheet_name'], '  Rows:', len(new_result['df']))
print('  Warnings:', new_result['warnings'])

print('Comparing with CORE_TRACKED_COLUMNS...')
results = compare(old_result['df'], new_result['df'], CORE_TRACKED_COLUMNS)
s = results['summary']
print()
print('=== RESULTS ===')
print('Standard Parts:     New=%d  Deleted=%d  Modified=%d  Fields=%d' % (
    s['std_new'], s['std_deleted'], s['std_modified'], s['std_changed_fields']))
print('Non-Standard Parts: New=%d  Deleted=%d  Modified=%d  Fields=%d' % (
    s['nonstd_new'], s['nonstd_deleted'], s['nonstd_modified'], s['nonstd_changed_fields']))

print()
print('Generating Excel...')
xls = export_to_excel(results['standard'], results['non_standard'], s, 'Old BOM.xlsm', 'New BOM.xlsm')
print('Excel generated: %d bytes' % len(xls))
print('ALL DONE - Full pipeline OK')
