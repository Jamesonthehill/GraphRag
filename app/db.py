import mysql.connector


def save_chat(user_input: str, model_output: str):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_sql_password",
        database="graphrag_chat"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO chat_messages (user_input, model_output)
        VALUES (%s, %s)
        """,
        (user_input, model_output)
    )

    conn.commit()
    cursor.close()
    conn.close()