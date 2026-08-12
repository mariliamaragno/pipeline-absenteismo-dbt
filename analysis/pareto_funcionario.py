import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

engine = create_engine("postgresql://dbt_user:dbt_pass@localhost:5433/absenteeismo")

query = """
    SELECT employee_id, absenteeism_hours
    FROM dbt_marilia.int_absenteeism_enriched
    WHERE reason_code IN (13, 19)
"""
df = pd.read_sql(query, engine)

by_employee = df.groupby("employee_id")["absenteeism_hours"].sum().reset_index()
by_employee = by_employee.sort_values("absenteeism_hours", ascending=False).reset_index(drop=True)

by_employee["cum_hours"] = by_employee["absenteeism_hours"].cumsum()
by_employee["cum_pct"] = 100 * by_employee["cum_hours"] / by_employee["absenteeism_hours"].sum()

total_employees = len(by_employee)
employees_for_80pct = (by_employee["cum_pct"] <= 80).sum() + 1

print(f"Total de funcionários com ausência por osteomuscular/lesões: {total_employees}")
print(f"Funcionários necessários para atingir 80% das horas: {employees_for_80pct} ({100*employees_for_80pct/total_employees:.1f}% do grupo)")
print()
print(by_employee.head(15).to_string(index=False))

fig, ax1 = plt.subplots(figsize=(12, 6))

ax1.bar(range(len(by_employee)), by_employee["absenteeism_hours"], color="steelblue")
ax1.set_ylabel("Horas de ausência")
ax1.set_xlabel("Funcionários (ordenados do maior para o menor)")

ax2 = ax1.twinx()
ax2.plot(range(len(by_employee)), by_employee["cum_pct"], color="darkorange")
ax2.set_ylabel("% acumulado")
ax2.axhline(80, color="gray", linestyle="--", linewidth=1)

plt.title("Concentração de horas (osteomuscular + lesões) por funcionário")
plt.tight_layout()
plt.savefig("pareto_funcionario.png", dpi=150)
print("\nGráfico salvo em pareto_funcionario.png")
