from database import connect_db

def add_priests():
    conn = connect_db()
    cur = conn.cursor()

    # Check if data exists
    cur.execute("SELECT COUNT(*) FROM priests")
    count = cur.fetchone()[0]  

    if count == 0:  # Insert only if no data is present
        cur.execute("""
            INSERT INTO priests (name, experience, age, availability) 
            VALUES 
            ('Medhansh Acharya', '7 years', '35 years', TRUE),
            ('Pankaj Jha', '4 years', '40 years', FALSE),
            ('Govind Kumar Jha', '6 years', '27 years', TRUE),
            ('Shankar Pandit', '9 years', '39 years', TRUE)
        """)
        conn.commit()
        print("Sample data inserted successfully!")
    else:
        print("Data already exists, skipping insertion.")

    cur.close()
    conn.close()
    
    return "Data added successfully!"

def create_users_table():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    cur.close()
    conn.close()
    return "Users table created successfully!"

