import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

engine = create_engine("postgresql://dbt_user:dbt_pass@localhost:5433/absenteeismo")

query = """
    SELECT reason_type, SUM(total_absence_hours) as total_hours, SUM(total_occurrences) as total_occurrences
    FROM dbt_marilia.mart_absenteeism_by_reason
    WHERE reason_type IS NOT NULL
    GROUP BY reason_type
    ORDER BY total_hours DESC
"""
df = pd.read_sql(query, engine)

df["avg_hours_per_occurrence"] = round(df["total_hours"] / df["total_occurrences"], 2)

print(df.to_string(index=False))

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].bar(df["reason_type"], df["total_hours"], color=["steelblue", "darkorange"])
axes[0].set_title("Total de horas de ausência")
axes[0].set_ylabel("Horas")

axes[1].bar(df["reason_type"], df["avg_hours_per_occurrence"], color=["steelblue", "darkorange"])
axes[1].set_title("Média de horas por ocorrência")
axes[1].set_ylabel("Horas (média)")

plt.tight_layout()
plt.savefig("reason_type_comparison.png", dpi=150)
print("\nGráfico salvo em reason_type_comparison.png")
