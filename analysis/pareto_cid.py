import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

engine = create_engine("postgresql://dbt_user:dbt_pass@localhost:5433/absenteeismo")

query = "SELECT * FROM dbt_marilia.mart_absenteeism_by_reason ORDER BY total_absence_hours DESC"
df = pd.read_sql(query, engine)

df["cum_hours"] = df["total_absence_hours"].cumsum()
df["cum_pct"] = 100 * df["cum_hours"] / df["total_absence_hours"].sum()

print(df[["reason_description", "total_absence_hours", "cum_pct"]].to_string(index=False))

fig, ax1 = plt.subplots(figsize=(12, 6))

ax1.bar(df["reason_description"], df["total_absence_hours"], color="steelblue")
ax1.set_ylabel("Horas de ausência")
ax1.set_xticks(range(len(df)))
ax1.set_xticklabels(df["reason_description"], rotation=75, ha="right")

ax2 = ax1.twinx()
ax2.plot(df["reason_description"], df["cum_pct"], color="darkorange", marker="o")
ax2.set_ylabel("% acumulado")
ax2.axhline(80, color="gray", linestyle="--", linewidth=1)

plt.title("Pareto de horas de ausência por motivo (CID)")
plt.tight_layout()
plt.savefig("pareto_cid.png", dpi=150)
print("\nGráfico salvo em pareto_cid.png")
