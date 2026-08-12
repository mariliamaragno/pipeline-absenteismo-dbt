import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://dbt_user:dbt_pass@localhost:5433/absenteeismo")

query = """
    SELECT employee_id, reason_code, absenteeism_hours, age, is_social_drinker,
           season_code, education_level, bmi, weight_kg, height_cm,
           distance_to_work_km, service_time_years
    FROM dbt_marilia.int_absenteeism_enriched
    WHERE reason_code IN (13, 19)
"""
df = pd.read_sql(query, engine)

# --- Recriar o Pareto por funcionário para identificar o grupo dos 80% ---
by_employee = df.groupby("employee_id")["absenteeism_hours"].sum().reset_index()
by_employee = by_employee.sort_values("absenteeism_hours", ascending=False).reset_index(drop=True)
by_employee["cum_pct"] = 100 * by_employee["absenteeism_hours"].cumsum() / by_employee["absenteeism_hours"].sum()

n_top = (by_employee["cum_pct"] <= 80).sum() + 1
top_employee_ids = by_employee.head(n_top)["employee_id"].tolist()

print(f"Grupo concentrado: {n_top} funcionários responsáveis por 80% das horas")
print(f"IDs: {top_employee_ids}\n")

# --- Perfil demográfico por funcionário (um registro por pessoa) ---
profile = df.groupby("employee_id").agg(
    age=("age", "first"),
    is_social_drinker=("is_social_drinker", "first"),
    education_level=("education_level", "first"),
    bmi=("bmi", "first"),
    weight_kg=("weight_kg", "first"),
    height_cm=("height_cm", "first"),
    distance_to_work_km=("distance_to_work_km", "first"),
    service_time_years=("service_time_years", "first"),
    winter_occurrences=("season_code", lambda x: (x == 3).sum()),
    total_occurrences=("season_code", "count"),
).reset_index()

profile["is_top"] = profile["employee_id"].isin(top_employee_ids)
profile["pct_winter"] = round(100 * profile["winter_occurrences"] / profile["total_occurrences"], 1)

# --- Comparação: grupo concentrado vs. restante ---
comparison = profile.groupby("is_top").agg(
    n_employees=("employee_id", "count"),
    avg_age=("age", "mean"),
    pct_drinker=("is_social_drinker", "mean"),
    avg_bmi=("bmi", "mean"),
    avg_distance=("distance_to_work_km", "mean"),
    avg_service_time=("service_time_years", "mean"),
    avg_pct_winter=("pct_winter", "mean"),
).round(2)
comparison["pct_drinker"] = round(comparison["pct_drinker"] * 100, 1)
print("=== Comparação: grupo concentrado (True) vs. restante (False) ===")
print(comparison)
print()

# --- Educação: distribuição no grupo concentrado vs. restante ---
education_dist = pd.crosstab(profile["is_top"], profile["education_level"], normalize="index").round(3) * 100
print("=== Distribuição de nível educacional (%) ===")
print(education_dist)
print()

# --- BMI: correlação direta com horas de ausência ---
hours_by_employee = df.groupby("employee_id")["absenteeism_hours"].sum().reset_index()
bmi_check = hours_by_employee.merge(profile[["employee_id", "bmi"]], on="employee_id")
corr_bmi = bmi_check["bmi"].corr(bmi_check["absenteeism_hours"])
print(f"=== Correlação entre BMI e horas totais de ausência (por funcionário) ===")
print(f"Coeficiente: {corr_bmi:.3f}")
