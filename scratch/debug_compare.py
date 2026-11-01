from tooling_bom.loader import load_bom
from tooling_bom.comparator import compare
from tooling_bom.column_config import CORE_TRACKED_COLUMNS

old = load_bom(r'C:\Users\HP\Downloads\Old_1414162_TRACTION_BATTERY_HOUSING_LONGITUDIN__BOM1.xlsm')
new = load_bom(r'C:\Users\HP\Downloads\New_1414162_TRACTION_BATTERY_HOUSING_LONGITUDIN__BOM1.xlsm')

print("Old DF shape:", old['df'].shape)
print("New DF shape:", new['df'].shape)

results = compare(old['df'], new['df'], CORE_TRACKED_COLUMNS)
s = results['summary']
print('Our result:')
print(f'  Standard:    new={s["std_new"]} del={s["std_deleted"]} mod={s["std_modified"]} fields={s["std_changed_fields"]}')
print(f'  NonStandard: new={s["nonstd_new"]} del={s["nonstd_deleted"]} mod={s["nonstd_modified"]} fields={s["nonstd_changed_fields"]}')
print()
print('Expected:')
print('  Standard:    new=60 del=0 mod=20 fields=66')
print('  NonStandard: new=2  del=4  mod=1  fields=1')
print()

print("--- First 15 Standard rows ---")
for r in results['standard'][:15]:
    print(f"  {r['item_no']:8s} | {r['change_type_en']:40s} | {r['column_en']:30s} | {str(r['old_value'])[:20]:20s} -> {str(r['new_value'])[:20]}")

print()
print("--- First 15 Non-Standard rows ---")
for r in results['non_standard'][:15]:
    print(f"  {r['item_no']:8s} | {r['change_type_en']:40s} | {r['column_en']:30s} | {str(r['old_value'])[:20]:20s} -> {str(r['new_value'])[:20]}")
