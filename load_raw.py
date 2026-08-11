import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv("absenteeism_data/Absenteeism_at_work.csv", sep=";")
engine = create_engine("postgresql://dbt_user:dbt_pass@localhost:5433/absenteeismo")
df.to_sql("raw_absenteeism", engine, if_exists="replace", index=False)
print("Carregado:", df.shape)
