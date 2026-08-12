import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

engine = create_engine("postgresql://dbt_user:dbt_pass@localhost:5433/absenteeismo")

query = """
    SELECT age, is_social_drinker, is_social_smoker, distance_to_work_km, absenteeism_hours
    FROM dbt_marilia.int_absenteeism_enriched
"""
df = pd.read_sql(query, engine)

# Faixas etárias
df["age_group"] = pd.cut(
    df["age"],
    bins=[0, 29, 39, 49, 100],
    labels=["Até 29", "30-39", "40-49", "50+"]
)

# Faixas de distância
df["distance_group"] = pd.cut(
    df["distance_to_work_km"],
    bins=[0, 10, 20, 30, 100],
    labels=["Até 10km", "11-20km", "21-30km", "31km+"]
)

# --- Análise por faixa etária ---
age_summary = df.groupby("age_group", observed=True).agg(
    total_hours=("absenteeism_hours", "sum"),
    avg_hours=("absenteeism_hours", "mean"),
    count=("absenteeism_hours", "count")
).round(2)
print("=== Por faixa etária ===")
print(age_summary)
print()

# --- Análise por fumante/bebedor social ---
drinker_summary = df.groupby("is_social_drinker").agg(
    total_hours=("absenteeism_hours", "sum"),
    avg_hours=("absenteeism_hours", "mean"),
    count=("absenteeism_hours", "count")
).round(2)
print("=== Por bebedor social (0=não, 1=sim) ===")
print(drinker_summary)
print()

smoker_summary = df.groupby("is_social_smoker").agg(
    total_hours=("absenteeism_hours", "sum"),
    avg_hours=("absenteeism_hours", "mean"),
    count=("absenteeism_hours", "count")
).round(2)
print("=== Por fumante social (0=não, 1=sim) ===")
print(smoker_summary)
print()

# --- Análise por distância ---
distance_summary = df.groupby("distance_group", observed=True).agg(
    total_hours=("absenteeism_hours", "sum"),
    avg_hours=("absenteeism_hours", "mean"),
    count=("absenteeism_hours", "count")
).round(2)
print("=== Por faixa de distância até o trabalho ===")
print(distance_summary)

# --- Gráficos ---
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

age_summary["avg_hours"].plot(kind="bar", ax=axes[0], color="steelblue")
axes[0].set_title("Média de horas por faixa etária")
axes[0].set_ylabel("Horas (média)")
axes[0].tick_params(axis='x', rotation=0)

distance_summary["avg_hours"].plot(kind="bar", ax=axes[1], color="darkorange")
axes[1].set_title("Média de horas por distância até o trabalho")
axes[1].set_ylabel("Horas (média)")
axes[1].tick_params(axis='x', rotation=0)

drinker_labels = ["Não bebedor", "Bebedor social"]
axes[2].bar(drinker_labels, drinker_summary["avg_hours"], color="seagreen")
axes[2].set_title("Média de horas: bebedor social")
axes[2].set_ylabel("Horas (média)")

plt.tight_layout()
plt.savefig("demografico_analysis.png", dpi=150)
print("\nGráfico salvo em demografico_analysis.png")
