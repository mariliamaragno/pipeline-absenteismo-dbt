import pandas as pd
from sqlalchemy import create_engine
import statsmodels.api as sm

engine = create_engine("postgresql://dbt_user:dbt_pass@localhost:5433/absenteeismo")

query = """
    SELECT age, distance_to_work_km, hit_target,
           transportation_expense, is_social_drinker, season_code,
           absenteeism_hours
    FROM dbt_marilia.int_absenteeism_enriched
    WHERE reason_code IN (13, 19)
"""
df = pd.read_sql(query, engine)

df["is_winter"] = (df["season_code"] == 3).astype(int)
df = df.drop(columns=["season_code"])

X = df.drop(columns=["absenteeism_hours"])
y = df["absenteeism_hours"]

X = sm.add_constant(X)

model = sm.OLS(y, X).fit()
print(model.summary())
