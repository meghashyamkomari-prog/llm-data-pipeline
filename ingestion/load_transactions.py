import pandas as pd
from sqlalchemy import create_engine
import os

base_path = "/mnt/c/Users/megha/llm-data-pipeline"
os.chdir(base_path)

DB_URL = "postgresql://postgres:Mad%4012345@localhost:5432/financial_db"

print("Loading classified transactions to PostgreSQL...")

df = pd.read_csv("data/processed/classified_transactions.csv")

engine = create_engine(DB_URL)
df.to_sql('llm_classified_transactions', engine, if_exists='replace', index=False)

print(f"Loaded {len(df)} classified transactions")
print(f"Accuracy: {(df['ai_category'] == df['original_category']).sum() / len(df) * 100:.1f}%")
print("Done!")
