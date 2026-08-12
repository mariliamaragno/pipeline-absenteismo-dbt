import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import numpy as np

engine = create_engine("postgresql://dbt_user:dbt_pass@localhost:5433/absenteeismo")

query = """
    SELECT age, distance_to_work_km, service_time_years, hit_target,
           transportation_expense, is_social_drinker, season_code,
           absenteeism_hours
    FROM dbt_marilia.int_absenteeism_enriched
    WHERE reason_code IN (13, 19)
"""
df = pd.read_sql(query, engine)

df["is_winter"] = (df["season_code"] == 3).astype(int)
df = df.drop(columns=["season_code"])

corr_matrix = df.corr()
print("=== Matriz de correlação (osteomuscular + lesões) ===")
print(corr_matrix["absenteeism_hours"].sort_values(ascending=False))

fig, ax = plt.subplots(figsize=(9, 7))
im = ax.imshow(corr_matrix, cmap="coolwarm", vmin=-1, vmax=1)

ax.set_xticks(range(len(corr_matrix.columns)))
ax.set_yticks(range(len(corr_matrix.columns)))
ax.set_xticklabels(corr_matrix.columns, rotation=45, ha="right")
ax.set_yticklabels(corr_matrix.columns)

for i in range(len(corr_matrix.columns)):
    for j in range(len(corr_matrix.columns)):
        ax.text(j, i, f"{corr_matrix.iloc[i, j]:.2f}", ha="center", va="center", color="black", fontsize=8)

plt.colorbar(im)
plt.title("Correlação entre variáveis (osteomuscular + lesões)")
plt.tight_layout()
plt.savefig("correlacao_cid.png", dpi=150)
print("\nGráfico salvo em correlacao_cid.png")
