import sqlite3

DATABASE_FILE = r'C:\Users\Zain Farooqi\Desktop\DAtasks\TASK5\Chinook_Sqlite.sqlite'
QUERY_TOP_PRODUCTS = """
WITH RankedProducts AS (
    SELECT
        T.Name AS TrackName,
        G.Name AS Genre,
        SUM(IL.Quantity) AS TotalUnitsSold,
        -- Assigns a rank based on units sold (DESC). Ties receive the same rank.
        RANK() OVER (ORDER BY SUM(IL.Quantity) DESC) as SalesRank
    FROM
        InvoiceLine AS IL
    JOIN
        Track AS T ON IL.TrackId = T.TrackId
    JOIN
        Genre AS G ON T.GenreId = G.GenreId
    GROUP BY
        T.TrackId, T.Name, G.Name
)
SELECT
    TrackName,
    Genre,
    TotalUnitsSold,
    SalesRank
FROM
    RankedProducts
WHERE
    SalesRank <= 10;
"""

QUERY_REGIONAL_REVENUE = """
SELECT
    I.BillingCountry AS Region,
    ROUND(SUM(I.Total), 2) AS TotalRevenue,
    COUNT(I.InvoiceId) AS TotalOrders
FROM
    Invoice AS I
GROUP BY
    I.BillingCountry
ORDER BY
    TotalRevenue DESC;
"""

QUERY_MONTHLY_PERFORMANCE = """
SELECT
    STRFTIME('%Y-%m', InvoiceDate) AS SalesMonth,
    ROUND(SUM(Total), 2) AS MonthlyRevenue,
    COUNT(InvoiceId) AS TotalInvoices
FROM
    Invoice
GROUP BY
    SalesMonth
ORDER BY
    SalesMonth;
"""

def run_sales_analysis(db_file, query_title, sql_query):
    
    print("\n" + "=" * 80)
    print(f"--- {query_title} ---")
    print("=" * 80)
    
    try:
        
        with sqlite3.connect(db_file) as conn:
            
            conn.row_factory = sqlite3.Row 
            cursor = conn.cursor()
            
            cursor.execute(sql_query)
            results = cursor.fetchall()
            
            if not results:
                print("No data found for this query.")
                return

            column_names = results[0].keys()
            header = " | ".join(column_names)
            
            print(header)
            print("-" * 80)
            
            for row in results:
                row_values = []
                for col in column_names:
                    value = row[col]
                    
                    if col in ['TotalRevenue', 'MonthlyRevenue']:
                        
                        formatted_value = f"${value:.2f}"
                    else:
                        formatted_value = str(value)
                        
                    row_values.append(formatted_value)
                    
                print(" | ".join(row_values))
                
    except sqlite3.Error as e:
        print(f"Database Error running '{query_title}': {e}")


if __name__ == "__main__":
    
    try:
        with open(DATABASE_FILE, 'r'):
            print(f"Connected successfully to {DATABASE_FILE}")
    except FileNotFoundError:
        print(f"Error: Database file '{DATABASE_FILE}' not found. Please ensure it is in the same directory.")
        exit()

    run_sales_analysis(
        DATABASE_FILE, 
        "TOP 10 TRACKS BY UNITS SOLD (Ranked)",
        QUERY_TOP_PRODUCTS
    )

    run_sales_analysis(
        DATABASE_FILE, 
        "TOTAL REVENUE PER REGION",
        QUERY_REGIONAL_REVENUE
    )

    run_sales_analysis(
        DATABASE_FILE, 
        "SALES PERFORMANCE BY MONTH (YYYY-MM)",
        QUERY_MONTHLY_PERFORMANCE
    )
