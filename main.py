'''
    Suppose you want to get users' data from different table and export it as csv file.
    There is an array with name "to_find_list". In this array, write the information of the main table (i.e users)
    as an object. 
    Similarly, write the details of other tables 
    Make sure that the first table is the main table

    Once done, set the "db_config" object to connect to your phpmyadmin database

    When you run this code, it will get all the data from the fields you have written and save it as a csv file
    Each row of the csv file will have data of each user from the tables and fields you have mentioned in the "to_find_list"

    Happy exporting!

'''

import mysql.connector
import csv

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'test'
}

# =============================================

to_find_list = [
    {
        'name': 'users',
        'fields': ['ID', 'user_email'],
        'slug': 'u',
        'key': 'ID'
    },
    {
        'name': 'orders', 
        'fields': ['order_id', 'current_status', 'submitdate'],
        'slug': 'o',
        'key': 'user_id'
    }
]

# ===================================================================================
# ----------------------------- Making Query ----------------------------------------
# ===================================================================================
query = "SELECT "

for table in to_find_list:
    table_fields = [f"GROUP_CONCAT({table['slug']}.{f}) AS {f}" for f in table['fields']]
    table_fields = ", ".join(table_fields)
    query += table_fields + ", "

query = query[:len(query) - 2]  # removing ", " from the last
query += " FROM "

p_field = ""
for i, table in enumerate(to_find_list):
    if i==0:    # for first table
        query += f"{table['name']} {table['slug']} "
        p_field = f"{table['slug']}.{table['key']}"
        continue

    # This LEFT JOIN logic will give all the results from main table. And if there is data in other tables.
    query += f"LEFT JOIN {table['name']} {table['slug']} ON {p_field} = {table['slug']}.{table['key']} "

query += f" GROUP BY {to_find_list[0]['slug']}.{to_find_list[0]['key']};"

# ===================================================================================
# ----------------------------- Getting Data ----------------------------------------
# ===================================================================================

conn = mysql.connector.connect(**db_config) # Connect to the database
cursor = conn.cursor()  # Create a cursor to execute SQL statements

# ------------------------------------
cursor.execute(query)
result_set = cursor.fetchall()
total_data_length = len(result_set)

csv_headers_tables = [] # table names
csv_headers_fields = [] # field names

for to_find in to_find_list:
    csv_headers_tables = csv_headers_tables + ( [to_find['name']] * len(to_find['fields']) )
    csv_headers_fields = csv_headers_fields + to_find['fields']


# ============================================================
# ---------------- Writing to the csv file -------------------
# ============================================================

csv_filename = f"./csv_files/users_data.csv"

with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    writer.writerow(csv_headers_fields)   # writing column names
    # writer.writerow(csv_headers_tables)   # writing column names
    
    writer.writerows(result_set)
        
print(f"CSV export completed.")

# ============================================================
# ------------ Closing the cursor and connection -------------
# ============================================================
conn.commit()

cursor.close()
conn.close()

