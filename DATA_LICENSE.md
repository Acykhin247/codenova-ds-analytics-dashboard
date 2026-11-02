# Data License and Attribution

**Dataset:** [Superstore Sales Dataset on Kaggle] by [AUTHOR FROM KAGGLE PAGE]
**Source:** [[KAGGLE URL](https://www.kaggle.com/datasets/amirmotefaker/superstore-sales-dataset)]
**License:** Community Data License Agreement – Sharing, Version 1.0 (CDLA-Sharing-1.0). Full text in `LICENSE-DATA.txt`.

## Changes made to the data
`data/superstore_dashboard.csv` is a **modified version** of the original `superstore_sales.xlsx` ("Orders" sheet):
- 12 of the 21 columns were kept (order_id, order_date, market, region, country, category, sub_category, segment, sales, quantity, discount, profit)
- order dates were converted to YYYY-MM-DD text
- the file was saved as CSV
- no rows were removed or edited (51,290 rows)

This modified file is shared under the same license (CDLA-Sharing-1.0). The code in this repository is separate from the data.