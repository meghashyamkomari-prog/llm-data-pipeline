import pandas as pd
import os

base_path = "/mnt/c/Users/megha/llm-data-pipeline"
os.chdir(base_path)

print("Loading transactions...")
df = pd.read_csv("data/raw/transactions.csv")

# Keyword-based classification rules
category_keywords = {
    'Restaurant': ['restaurant', 'cafe', 'lunch', 'dinner', 'olive', 'pizza', 'bar'],
    'Grocery': ['walmart', 'grocery', 'supermarket', 'whole', 'costco', 'trader'],
    'Gas': ['shell', 'chevron', 'exxon', 'gas', 'bp', 'mobil'],
    'Healthcare': ['doctor', 'hospital', 'pharmacy', 'health', 'clinic', 'medical'],
    'Entertainment': ['movie', 'cinema', 'theater', 'netflix', 'hulu', 'disney'],
    'Utilities': ['electric', 'gas bill', 'water', 'utility', 'power'],
    'Transportation': ['uber', 'lyft', 'taxi', 'transit', 'metro'],
    'Shopping': ['amazon', 'mall', 'store', 'retail', 'target', 'best'],
    'Insurance': ['insurance', 'allstate', 'state farm'],
    'Subscriptions': ['netflix', 'hulu', 'subscription', 'membership']
}

classifications = []

for idx, row in df.iterrows():
    desc_lower = row['description'].lower()
    matched_category = 'Unknown'
    
    for category, keywords in category_keywords.items():
        if any(kw in desc_lower for kw in keywords):
            matched_category = category
            break
    
    classifications.append({
        'transaction_id': row['transaction_id'],
        'description': row['description'],
        'ai_category': matched_category,
        'original_category': row['category'],
        'confidence': 0.85 if matched_category != 'Unknown' else 0.0
    })

results_df = pd.DataFrame(classifications)
os.makedirs("data/processed", exist_ok=True)
results_df.to_csv("data/processed/classified_transactions.csv", index=False)

print(f"Classified {len(results_df)} transactions")
print("\nSample classifications:")
print(results_df[['description', 'ai_category', 'original_category']].head(10))
print("\nAccuracy check (AI vs Original):")
match_count = (results_df['ai_category'] == results_df['original_category']).sum()
accuracy = (match_count / len(results_df)) * 100
print(f"Matching: {match_count}/{len(results_df)} ({accuracy:.1f}%)")
print("Done!")
