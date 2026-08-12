import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

engine = create_engine("postgresql://dbt_user:dbt_pass@localhost:5433/absenteeismo")

query = """
    SELECT absence_month, season_code, reason_code, reason_description, absenteeism_hours
    FROM dbt_marilia.int_absenteeism_enriched
    WHERE absence_month BETWEEN 1 AND 12
"""
df = pd.read_sql(query, engine)

season_map = {1: "Verão", 2: "Outono", 3: "Inverno", 4: "Primavera"}
df["season_name"] = df["season_code"].map(season_map)

month_map = {
    1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr", 5: "Mai", 6: "Jun",
    7: "Jul", 8: "Ago", 9: "Set", 10: "Out", 11: "Nov", 12: "Dez"
}
df["month_name"] = df["absence_month"].map(month_map)

by_month = df.groupby(["absence_month", "month_name"])["absenteeism_hours"].sum().reset_index()
by_month = by_month.sort_values("absence_month")
print("=== Horas de ausência por mês ===")
print(by_month[["month_name", "absenteeism_hours"]].to_string(index=False))
print()

by_season = df.groupby("season_name")["absenteeism_hours"].agg(["sum", "count"]).sort_values("sum", ascending=False)
by_season.columns = ["total_hours", "total_occurrences"]
by_season["avg_hours"] = round(by_season["total_hours"] / by_season["total_occurrences"], 2)
print("=== Horas de ausência por estação (com contagem) ===")
print(by_season)
print()

respiratorio = df[df["reason_code"] == 10]
resp_by_season = respiratorio.groupby("season_name")["absenteeism_hours"].agg(["sum", "count"]).sort_values("sum", ascending=False)
resp_by_season.columns = ["total_hours", "total_occurrences"]
print("=== Doenças respiratórias (CID 10) por estação ===")
print(resp_by_season)
print()

osteo_lesoes = df[df["reason_code"].isin([13, 19])]
osteo_by_season = osteo_lesoes.groupby("season_name")["absenteeism_hours"].agg(["sum", "count"]).sort_values("sum", ascending=False)
osteo_by_season.columns = ["total_hours", "total_occurrences"]
osteo_by_season["avg_hours"] = round(osteo_by_season["total_hours"] / osteo_by_season["total_occurrences"], 2)
print("=== Osteomuscular + Lesões (CID 13 e 19) por estação ===")
print(osteo_by_season)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

by_month_ordered = by_month.set_index("month_name").reindex(
    ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]
)
axes[0].plot(by_month_ordered.index, by_month_ordered["absenteeism_hours"], marker="o", color="steelblue")
axes[0].set_title("Horas de ausência por mês")
axes[0].set_ylabel("Horas")
axes[0].tick_params(axis='x', rotation=45)

by_season["total_hours"].plot(kind="bar", ax=axes[1], color="darkorange")
axes[1].set_title("Horas de ausência por estação")
axes[1].set_ylabel("Horas")
axes[1].tick_params(axis='x', rotation=0)

plt.tight_layout()
plt.savefig("sazonalidade_analysis.png", dpi=150)
print("\nGráfico salvo em sazonalidade_analysis.png")
