from pathlib import Path
import pandas as pd

SOURCE = Path("source/superstore_sales.xlsx")
OUT = Path("data/superstore_dashboard.csv")
COLUMNS = ["order_id", "order_date", "market", "region", "country", "category",
           "sub_category", "segment", "sales", "quantity", "discount", "profit"]

df = pd.read_excel(SOURCE, sheet_name="Orders")
slim = df[COLUMNS].copy()
slim["order_date"] = slim["order_date"].dt.strftime("%Y-%m-%d")
OUT.parent.mkdir(exist_ok=True)
slim.to_csv(OUT, index=False)

print(slim.shape)
print("Total sales:", round(slim["sales"].sum(), 2))
print("Total profit:", round(slim["profit"].sum(), 2))