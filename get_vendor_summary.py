import pandas as pd
import numpy as np
import sqlite3
import logging
import os

logging.basicConfig(
    filename='logs/get_vendor_summary.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)

def create_vendor_summary_table(conn):
    '''Creates the vendor_sales_summary dataframe by merging different tables.'''
    try:
        vendor_sales_summary = pd.read_sql('''WITH FreightSummary AS ( 
                                    SELECT VendorNumber, SUM(Freight) as FreightCost 
                                    FROM vendor_invoice 
                                    GROUP BY VendorNumber),
                                   
                                   PurchaseSummary AS (
                                SELECT
                                    p.VendorNumber,
                                    p.VendorName,
                                    p.Brand,
                                    p.Description,
                                    p.PurchasePrice,
                                    pp.Price AS ActualPrice,
                                    pp.Volume,
                                    SUM(p.Quantity) AS TotalPurchaseQuantity,
                                    SUM(p.Dollars) AS TotalPurchaseDollars
                                FROM purchases p
                                JOIN purchase_prices pp
                                    ON p.Brand = pp.Brand
                                WHERE p.PurchasePrice > 0
                                GROUP BY p.VendorNumber, p.VendorName, p.Brand, 
                                        p.Description, p.PurchasePrice, pp.Price, pp.Volume
                                ),
                                   
                                   SalesSummary AS (
                                        SELECT
                                            VendorNo,
                                            Brand,
                                            SUM(SalesQuantity) AS TotalSalesQuantity,
                                            SUM(SalesDollars) AS TotalSalesDollars,
                                            SUM(SalesPrice) AS TotalSalesPrice,
                                            SUM(ExciseTax) AS TotalExciseTax
                                        FROM sales
                                        GROUP BY VendorNo, Brand
                                    )
                                   
                                   SELECT
                                        ps.VendorNumber,
                                        ps.VendorName,
                                        ps.Brand,
                                        ps.Description,
                                        ps.PurchasePrice,
                                        ps.ActualPrice,
                                        ps.Volume,
                                        ps.TotalPurchaseQuantity,
                                        ps.TotalPurchaseDollars,
                                        ss.TotalSalesQuantity,
                                        ss.TotalSalesDollars,
                                        ss.TotalSalesPrice,
                                        ss.TotalExciseTax,
                                        fs.FreightCost
                                    FROM PurchaseSummary ps
                                    LEFT JOIN SalesSummary ss
                                        ON ps.VendorNumber = ss.VendorNo
                                    AND ps.Brand = ss.Brand
                                    LEFT JOIN FreightSummary fs
                                        ON ps.VendorNumber = fs.VendorNumber
                                    ORDER BY ps.TotalPurchaseDollars DESC;
                                   ''', conn)
        logging.info("vendor_sales_summary dataframe created successfully.")
        return vendor_sales_summary
    except Exception as e:
        logging.error(f"Error creating vendor_sales_summary dataframe: {e}")
        return pd.DataFrame()

def clean_data(df):
    '''Cleans the vendor_sales_summary dataframe'''

    df['Volume'] = df['Volume'].astype('float64')

    df.fillna(0, inplace=True)

    df['VendorName'] = df['VendorName'].str.strip()
    df['Description'] = df['Description'].str.strip()

    df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']
    df['ProfitMargin'] = np.where(df['TotalSalesDollars'] > 0,
                                (df['GrossProfit'] / df['TotalSalesDollars']) * 100,
                                0)
    df['StockTurnover'] = np.where(df['TotalPurchaseQuantity'] > 0,
                                df['TotalSalesQuantity'] / df['TotalPurchaseQuantity'],
                                0)
    df['SalesToPurchaseRatio'] = np.where(df['TotalPurchaseDollars'] > 0,
                                        df['TotalSalesDollars'] / df['TotalPurchaseDollars'],
                                        0)

    return df

def ingest_db(df, table_name, conn):
    '''Appends df into db. If table doesn't exist, creates it with schema + PK.'''
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name=?;
    """, (table_name,))
    exists = cursor.fetchone()

    if not exists:
        logging.info(f"Table {table_name} does not exist. Creating with schema + PK...")
        cursor.execute(f"""
            CREATE TABLE {table_name} (
            VendorNumber INT,
            VendorName VARCHAR(100),
            Brand INT,
            Description VARCHAR(100),
            PurchasePrice DECIMAL(10,2),
            ActualPrice DECIMAL(10,2),
            Volume DECIMAL(10,2),
            TotalPurchaseQuantity INT,
            TotalPurchaseDollars DECIMAL(15,2),
            TotalSalesQuantity INT,
            TotalSalesDollars DECIMAL(15,2),
            TotalSalesPrice DECIMAL(15,2),
            TotalExciseTax DECIMAL(15,2),
            FreightCost DECIMAL(15,2),
            GrossProfit DECIMAL(15,2),
            ProfitMargin DECIMAL(15,2),
            StockTurnover DECIMAL(15,2),
            SalesToPurchaseRatio DECIMAL(15,2),
            PRIMARY KEY (VendorNumber, Brand)
        );
        """)
        conn.commit()

    df.to_sql(table_name, con=conn, if_exists='append', index=False)

    logging.info(f"Data appended to {table_name} successfully.")


if __name__ == "__main__":

    conn = sqlite3.connect('vendor_data.db')

    logging.info("Creating Vendor Sales Summary Table...")
    summary_df = create_vendor_summary_table(conn)
    logging.info(summary_df.head())

    logging.info("Cleaning Data...")
    cleaned_df = clean_data(summary_df)
    logging.info(cleaned_df.head())

    logging.info("Ingesting cleaned data into vendor_sales_summary table...")
    ingest_db(cleaned_df, 'vendor_sales_summary', conn)
    logging.info("Data ingestion completed.")
