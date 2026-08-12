import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://dbt_user:dbt_pass@localhost:5433/absenteeismo")

top_employee_ids = [36, 11, 34, 20, 3, 14, 13, 24, 26]

query = """
    SELECT employee_id, day_of_week_name, is_social_drinker, absenteeism_hours
    FROM dbt_marilia.int_absenteeism_enriched
"""
df = pd.read_sql(query, engine)

# --- Teste 1: segundas-feiras vêm mais do grupo concentrado? ---
df["is_top_group"] = df["employee_id"].isin(top_employee_ids)
monday_by_group = df[df["day_of_week_name"] == "Segunda"].groupby("is_top_group")["absenteeism_hours"].sum()
total_by_group = df.groupby("is_top_group")["absenteeism_hours"].sum()
pct_monday_by_group = round(100 * monday_by_group / total_by_group, 1)

print("=== % das horas de cada grupo que caem em segunda-feira ===")
print(pct_monday_by_group)
print()

# --- Teste 2: bebedores sociais têm mais concentração em segunda-feira? ---
monday_by_drinker = df[df["day_of_week_name"] == "Segunda"].groupby("is_social_drinker")["absenteeism_hours"].sum()
total_by_drinker = df.groupby("is_social_drinker")["absenteeism_hours"].sum()
pct_monday_by_drinker = round(100 * monday_by_drinker / total_by_drinker, 1)

print("=== % das horas de cada grupo (bebedor/não) que caem em segunda-feira ===")
print(pct_monday_by_drinker)
