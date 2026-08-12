import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://dbt_user:dbt_pass@localhost:5433/absenteeismo")

top_employee_ids = [36, 11, 34, 20, 3, 14, 13, 24, 26]

query = "SELECT employee_id, reason_code, absenteeism_hours FROM dbt_marilia.int_absenteeism_enriched"
df = pd.read_sql(query, engine)

total_company_hours = df["absenteeism_hours"].sum()
total_employees = df["employee_id"].nunique()

top_group = df[df["employee_id"].isin(top_employee_ids)]
top_group_all_reasons_hours = top_group["absenteeism_hours"].sum()

top_group_1319_hours = top_group[top_group["reason_code"].isin([13, 19])]["absenteeism_hours"].sum()

print(f"Total de horas de ausência na empresa (todos os motivos): {total_company_hours}")
print(f"Total de funcionários na empresa: {total_employees}")
print()
print(f"Grupo concentrado: {len(top_employee_ids)} funcionários ({100*len(top_employee_ids)/total_employees:.1f}% do total de funcionários)")
print()
print(f"Horas do grupo concentrado (SÓ osteomuscular+lesões): {top_group_1319_hours}")
print(f"Horas do grupo concentrado (TODOS os motivos): {top_group_all_reasons_hours}")
print()
print(f"% do total de horas da empresa (todos motivos) que vem desse grupo de 9: {100*top_group_all_reasons_hours/total_company_hours:.1f}%")
