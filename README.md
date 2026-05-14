# ☕ Automated Retail Data Integrity Pipeline
**Developed by Mpho Kgoloko Mohlala**

This project demonstrates a high-integrity data cleaning pipeline built in Python. It transforms a corrupted dataset of 10,000 retail transactions into a verified analytical asset.

## 🛠️ Technical Highlights
- **Algebraic Data Recovery:** Used mathematical relationships (Total = Price × Quantity) to recover 456 missing quantities and 60 missing prices.
- **Collision Resolution:** Implemented logic to distinguish between "Juice" and "Cake" products which shared an identical $3.0 price point.
- **Temporal Consistency:** Fixed impossible dates (e.g., Feb 31st) using forward-fill (ffill) logic.
- **Automated Reporting:** Built a custom PDF generation engine using `FPDF` to audit data quality and visualize sales trends.

## 📊 Key Results
- **Initial Data Quality:** Thousands of missing values across 7 columns.
- **Final Data Quality:** 0 Missing Values (NaNs) in all critical fields.
- **Data Retention:** Preserved 99.25% of the original records by using imputation instead of deletion.
- **Total Validated Revenue:** R88,610.50

## 🧰 Tools Used
- **Python:** Pandas, NumPy, Matplotlib
- **Reporting:** FPDF
- **Environment:** Pydroid 3 (Mobile Development)

