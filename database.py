import psycopg2 

# Function to connect to PostgreSQL
def connect_db():
    return psycopg2.connect(
        dbname="pooja_path",
        user="postgres",
        password="newpassword",
        host="localhost",
        port="5432"
    )