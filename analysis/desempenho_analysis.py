import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

engine = create_engine("postgresql://dbt_user:dbt_pass@localhost:5433/absenteeismo")

query = """
    SELECT service_time_years, hit_target, disciplinary_failure, workload_avg_day, absenteeism_hours
    FROM dbt_marilia.int_absenteeism_enriched
"""
df = pd.read_sql(query, engine)

# Faixas de tempo de serviço
df["service_time_group"] = pd.cut(
    df["service_time_years"],
    bins=[0, 5, 10, 15, 100],
    labels=["Até 5 anos", "6-10 anos", "11-15 anos", "16+ anos"]
)

# Faixas de meta atingida (hit_target)
df["hit_target_group"] = pd.cut(
    df["hit_target"],
    bins=[0, 90, 95, 100],
    labels=["Até 90%", "91-95%", "96-100%"]
)

# --- Por tempo de serviço ---
service_summary = df.groupby("service_time_group", observed=True).agg(
    total_hours=("absenteeism_hours", "sum"),
    avg_hours=("absenteeism_hours", "mean"),
    count=("absenteeism_hours", "count")
).round(2)
print("=== Por tempo de serviço ===")
print(service_summary)
print()

# --- Por faixa de meta atingida ---
target_summary = df.groupby("hit_target_group", observed=True).agg(
    total_hours=("absenteeism_hours", "sum"),
    avg_hours=("absenteeism_hours", "mean"),
    count=("absenteeism_hours", "count")
).round(2)
print("=== Por faixa de meta atingida (hit target) ===")
print(target_summary)
print()

# --- Por falha disciplinar ---
disciplinary_summary = df.groupby("disciplinary_failure").agg(
    total_hours=("absenteeism_hours", "sum"),
    avg_hours=("absenteeism_hours", "mean"),
    count=("absenteeism_hours", "count")
).round(2)
print("=== Por falha disciplinar (0=não, 1=sim) ===")
print(disciplinary_summary)
print()

# --- Correlação entre carga de trabalho média e horas de ausência ---
correlation = df["workload_avg_day"].corr(df["absenteeism_hours"])
print(f"=== Correlação entre carga de trabalho média e horas de ausência ===")
print(f"Coeficiente: {correlation:.3f}")

# --- Gráficos ---
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

service_summary["avg_hours"].plot(kind="bar", ax=axes[0], color="steelblue")
axes[0].set_title("Média de horas por tempo de serviço")
axes[0].set_ylabel("Horas (média)")
axes[0].tick_params(axis='x', rotation=0)

target_summary["avg_hours"].plot(kind="bar", ax=axes[1], color="darkorange")
axes[1].set_title("Média de horas por meta atingida")
axes[1].set_ylabel("Horas (média)")
axes[1].tick_params(axis='x', rotation=0)

disciplinary_labels = ["Sem falha disciplinar", "Com falha disciplinar"]
axes[2].bar(disciplinary_labels, disciplinary_summary["avg_hours"], color="seagreen")
axes[2].set_title("Média de horas: falha disciplinar")
axes[2].set_ylabel("Horas (média)")

plt.tight_layout()
plt.savefig("desempenho_analysis.png", dpi=150)
print("\nGráfico salvo em desempenho_analysis.png")
