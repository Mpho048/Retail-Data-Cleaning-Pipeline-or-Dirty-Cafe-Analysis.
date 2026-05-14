"""
Project: Automated Retail Data Integrity Pipeline
Author: Mpho Kgoloko Mohlala
Objective: Clean, validate, and impute missing values in sales data.
"""

import pandas as pd
import numpy as np
import create_pdf  as cpdf
import matplotlib.pyplot as plt 

# --- 1. DATA LOADING ---
df = pd.read_csv("dirty_cafe_sales.csv")
total_df = len(df)
nall_count = df.isna().sum()
nall_count.name = "Missing Values"
# --- 2. DATA TYPE ENFORCEMENT ---
df["Transaction Date"] = pd.to_datetime(df["Transaction Date"], errors="coerce")

df["Total Spent"] = pd.to_numeric(df["Total Spent"], errors="coerce")

df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")

df["Price Per Unit"] = pd.to_numeric(df["Price Per Unit"], errors="coerce")


# --- 3. DATA RECOVERY (IMPUTATION) ---

# A. Dates: ffill handles impossible dates like Feb 31st
df["Transaction Date"] = df["Transaction Date"].ffill()

# B. Items: Mapping prices to names
price_map = {
    2.0: "Coffee",
    3.0: "Cake",    # Cake is the primary $3.0 item
    1.0: "Cookie",
    5.0: "Salad",
    1.5: "Tea",
    4.0: "Smoothie",
    4.5: "Sandwich"
}

item_mask = df["Item"].isna() | df["Item"].isin(["ERROR", "UNKNOWN"])
df.loc[item_mask, "Item"] = df.loc[item_mask, "Price Per Unit"].map(price_map)

# Handle the Juice/Cake collision: If Price is 3.0 but Item is still missing, call it Juice
juice_mask = (df["Item"].isna()) & (df["Price Per Unit"] == 3.0)
df.loc[juice_mask, "Item"] = "Juice"

# C. Prices: Mapping names back to prices to fix those last 60 NaNs
item_to_price = {v: k for k, v in price_map.items()}
item_to_price["Juice"] = 3.0 # Explicitly adding Juice back to the price logic
price_mask = df["Price Per Unit"].isna()
df.loc[price_mask, "Price Per Unit"] = df.loc[price_mask, "Item"].map(item_to_price)

# D. Quantity: Using Algebra (Total / Price) to fix those 456 NaNs
q_mask = df["Quantity"].isna()
df.loc[q_mask, "Quantity"] = (df.loc[q_mask, "Total Spent"] / df.loc[q_mask, "Price Per Unit"]).round()

# E. Total Spent: Final recalculation for any remaining gaps
calc_mask = df["Total Spent"].isna()
df.loc[calc_mask, "Total Spent"] = df.loc[calc_mask, "Quantity"] * df.loc[calc_mask, "Price Per Unit"]

# --- 4. CATEGORICAL & FINAL CLEANUP ---
df["Payment Method"] = df["Payment Method"].replace({"ERROR":np.nan})
df["Payment Method"] = df["Payment Method"].str.title().fillna(df["Payment Method"].mode()[0])

df["Location"] = df["Location"].replace({"ERROR": "Other", "UNKNOWN": "Other"}).fillna("Other")

# Remove top 2.5% outliers and any remaining stubborn NaNs
upper_limit = df["Total Spent"].quantile(0.975)
df = df[df["Total Spent"] <= upper_limit].dropna()
after_clean = len(df)
# --- 5. FINAL REPORT ---
print("--- FINAL DATA AUDIT ---")
print(f"Total Clean Rows: {len(df)}")
print("Remaining Missing Values:\n", df.isnull().sum())
print(f"Total Clean Revenue: R{df['Total Spent'].sum():.2f}")
df.to_csv("clean_cafe_sales.csv",index = False )

#Make a pdf Report 
pdf = cpdf.PDF()
#Before cliening
pdf.add_page()
pdf.Set_title("Cafe Sale Analysis Report",no_color = "N")
pdf.Set_title("Showing how many missing(NaN) vaule are in each col/row",no_color = "Y")
pdf.single_col(nall_count,col= "Cols")
words = """
I convert Total Spent,Quantity and price per unit  to numeric data using to_numeric() method,which set all text to NaN values(including 'ERROR' and 'UNKNOWN').
Used to_datetime() convert Transaction date to dates,which remove all false value.
The dataset contains 3 numeric columns,4 categorical columns, and 1 date column.
"""
pdf.write_txt(f"Total data before cleaning is {total_df} rows and 7 colums",)
pdf.write_txt(words,multi = True)


# After cleaning
pdf.add_page()
pdf.Set_title("After Cleaning the Data",no_color = "N")
price  = pd.Series(item_to_price,name= "Price Per Unit")
pdf.Set_title("Each Item price in the cafe",no_color  = "Y")
pdf.single_col(price,col = "Item")
pdf.write_txt(f"Total Clean Revenue: R{df['Total Spent'].sum():.2f}")
rept = """
Recovered missing numeric values using
mathematical relationships between
Quantity, Price Per Unit, and Total Spent.
Used mapping dictionaries to restore missing
Item names and prices.
For categorical or text data i used mode and 'other' to replace all the missing data.
Removed extreme outlier values using quantile(0.975).
All 7 colums are still in the data
"""
pdf.write_txt(rept,multi = True)
pdf.write_txt(f"Total data after cleaning {len(df)}")
pdf.write_txt(f"About {total_df-len(df)}  rows have been removed")

#Bar of Item and Total Spent
pdf.add_page()
pdf.Set_title("Revenue by Item")

item_sales = (
    df.groupby("Item")["Total Spent"]
    .sum()
    .reset_index()
    .sort_values(by="Total Spent", ascending=False)
)
plt.barh(item_sales["Item"],item_sales["Total Spent"])
plt.title("Total Spent  vs Item")
plt.xlabel("Total Spent")
plt.ylabel("Item")
plt.savefig("File1.png")
plt.close()
pdf.image("File1.png",x = 50,w =130)
pdf.ln(10)
sales_summary = """
This chart shows the total revenue generated
by each product sold in the cafe.

The analysis helps identify high-performing
items that contribute most to total sales.
Products with lower revenue may require
marketing improvements or pricing adjustments.

The chart also provides insight into
customer purchasing behavior and
popular menu choices.
"""

pdf.write_txt(sales_summary, multi=True)



# payment methods
pdf.add_page()
payments = df["Payment Method"].value_counts()
fig,ax = plt.subplots(figsize =(10,10))
ax.pie(payments,shadow = True, autopct = "%1.1f%%",labels = payments.index,explode =[0,0.1,0,0])
pdf.Set_title("Payment Method Breakdown")
fig.savefig("File2.png")
plt.close(fig)
pdf.image("File2.png",x = 60,w = 120)
pdf.ln(10)
payment_summary = """
This pie chart illustrates the distribution
of customer payment methods used during sales.

The results help understand customer
payment preferences and transaction behavior.

Card and digital payments can indicate
higher adoption of cashless transactions,
while cash payments may reflect customer
accessibility and convenience preferences.
"""

pdf.write_txt(payment_summary, multi=True)






#Add line graph for trends
pdf.add_page()
monthly_sales = (
    df.groupby(df["Transaction Date"].dt.month)["Total Spent"]
    .sum()
)#use month_name()/angle them
print("Tt:\n", monthly_sales)
f,x = plt.subplots(figsize =(10,10))
x.plot(monthly_sales.index,monthly_sales)
x.set_xlabel("Month")
x.set_ylabel("Sum of Sales")
f.savefig("File3.png")
plt.close(f)
pdf.Set_title("Monthly Sales Trend")
pdf.image("File3.png",x = 40,w = 150)
pdf.ln(10)
trend_summary = """
This line graph displays monthly sales trends
based on total revenue over time.

The visualization helps identify periods
of high and low sales activity within the cafe.

Sales trends are useful for forecasting,
inventory planning, staffing decisions,
and identifying seasonal customer behavior.
"""

pdf.write_txt(trend_summary, multi=True)

pdf.output("report.pdf")
