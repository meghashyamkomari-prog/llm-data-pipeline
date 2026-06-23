import pandas as pd
import random
import os
from datetime import datetime, timedelta

random.seed(42)
base_path = "/mnt/c/Users/megha/llm-data-pipeline"
os.makedirs(f"{base_path}/data/raw", exist_ok=True)

# Transaction types and descriptions
transaction_types = [
    ('Restaurant', 'Lunch at Olive Garden'),
    ('Grocery', 'Walmart grocery shopping'),
    ('Gas', 'Shell gas station'),
    ('Healthcare', 'Doctor appointment co-pay'),
    ('Entertainment', 'Movie tickets Cinemark'),
    ('Utilities', 'Electric bill payment'),
    ('Transportation', 'Uber ride to downtown'),
    ('Shopping', 'Amazon online purchase'),
    ('Insurance', 'Car insurance monthly'),
    ('Subscriptions', 'Netflix monthly subscription'),
]

transactions = []
for i in range(5000):
    trans_date = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 365))
    trans_type, description = random.choice(transaction_types)
    amount = round(random.uniform(5, 500), 2)
    
    transactions.append({
        'transaction_id': f'TXN{i+1:06d}',
        'amount': amount,
        'description': description,
        'merchant': description.split()[1:3] if len(description.split()) > 2 else description.split()[:2],
        'transaction_date': trans_date.strftime('%Y-%m-%d'),
        'category': trans_type,
        'account_id': f'ACC{random.randint(1000, 9999)}'
    })

df = pd.DataFrame(transactions)
df['merchant'] = df['merchant'].apply(lambda x: ' '.join(x) if isinstance(x, list) else x)
df.to_csv(f'{base_path}/data/raw/transactions.csv', index=False)
print(f"Generated {len(df)} transactions")
print(df.head())
print("Done!")
