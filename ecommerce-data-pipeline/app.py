import pandas as pd
import streamlit as st

# -------------------------------
# App Title
# -------------------------------
st.title("🛒 E-commerce Data Engineering Prototype")
st.write("Demonstrating a simple data engineering lifecycle with product recommendations.")

# -------------------------------
# Step 1 & 2: Data Generation + Storage
# -------------------------------
data = {
    "user_id": [1, 1, 2, 2, 3, 3],
    "product_id": [101, 104, 102, 105, 101, 105],
    "product_name": ["Shoes", "Jacket", "Laptop", "Mouse", "Shoes", "Mouse"],
    "category": ["Fashion", "Fashion", "Electronics", "Electronics", "Fashion", "Electronics"],
    "purchase_date": [
        "2025-11-01", "2025-11-01",
        "2025-11-02", "2025-11-02",
        "2025-11-03", "2025-11-03"
    ]
}

raw_data = pd.DataFrame(data)
raw_data.to_csv("purchases.csv", index=False)

# -------------------------------
# Step 3: Data Ingestion
# -------------------------------
st.header("📥 Raw Purchase Data (Ingestion)")
df = pd.read_csv("purchases.csv")
st.dataframe(df)

# -------------------------------
# Step 4: Data Transformation
# -------------------------------
st.header("🔄 Transformed Data")

clean_data = df.drop_duplicates()
user_purchases = clean_data.groupby("user_id")["product_name"].apply(list).reset_index()

st.dataframe(user_purchases)

# -------------------------------
# Step 5: Data Serving (Recommendations)
# -------------------------------
st.header("🎯 Product Recommendations")

recommendations = {}

for index, row in user_purchases.iterrows():
    user_id = row["user_id"]
    user_items = set(row["product_name"])
    similar_items = set()

    for _, other_row in user_purchases.iterrows():
        if other_row["user_id"] != user_id:
            other_items = set(other_row["product_name"])
            if user_items & other_items:
                similar_items |= other_items

    recommendations[user_id] = list(similar_items - user_items)

# Display recommendations
for user, recs in recommendations.items():
    st.write(f"**User {user} recommendations:** {recs if recs else 'No recommendations'}")

# -------------------------------
# Step 6: Monitoring
# -------------------------------
st.header("📊 Pipeline Monitoring")

st.metric("Total Records Processed", len(clean_data))
st.metric("Unique Users", clean_data["user_id"].nunique())
st.success("Pipeline executed successfully ✅")
