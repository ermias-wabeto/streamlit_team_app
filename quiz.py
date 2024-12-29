import sqlite3
import streamlit as st
import smtplib
from email.message import EmailMessage

# Create the database and add questions
def create_database():
    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()

    # Create table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY,
            topic TEXT,
            question TEXT,
            option_a TEXT,
            option_b TEXT,
            option_c TEXT,
            option_d TEXT,
            correct_option TEXT
        )
    """)
    # Insert questions
    questions = [
        ("Biology", "How many sense organs do human beings have?", "2", "3", "4", "5", "D"),
        ("IT", "Which of the following DBMS is used for training and prototyping?", "Oracle", "MSSQL", "SQLite", "PostgreSQL", "C"),
        ("Maths", "What is the whole number between the number 5 and 7?", "6", "4", "8", "35", "A"),
        ("Geography", "How many continents are there in the world?", "5", "7", "6", "9", "B"),
        ("English", "What is the past tense of the word 'go'?", "Went", "Go", "Gone", "Goied", "A")
    ]
    cursor.executemany("""
        INSERT INTO questions (topic, question, option_a, option_b, option_c, option_d, correct_option)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, questions)

    conn.commit()
    conn.close()

# Database interaction
def get_questions(topic):
    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions WHERE topic = ?", (topic,))
    questions = cursor.fetchall()
    conn.close()
    return questions

# Send email function
def send_email(score, email):
    msg = EmailMessage()
    msg["Subject"] = "Your Quiz Results"
    msg["From"] = "your_email@example.com"
    msg["To"] = email
    msg.set_content(f"Congratulations! Your quiz score is {score}.")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login("your_email@example.com", "your_password")
        server.send_message(msg)

# Main app logic
def main():
    st.title("Interactive Quiz App")

    # Select quiz topic
    topic = st.selectbox("Choose a quiz topic:", ["Biology", "IT", "Maths", "Geography", "English"])

    # Load questions
    questions = get_questions(topic)

    if not questions:
        st.error(f"No questions available for the topic: {topic}.")
        return

    # Display questions and collect answers
    score = 0
    answers = {}
    for question in questions:
        st.write(question[2])
        options = {
            "A": question[3],
            "B": question[4],
            "C": question[5],
            "D": question[6]
        }
        answer = st.radio(f"Choose an answer for question {question[0]}:", list(options.keys()), key=question[0])
        answers[question[0]] = answer
        if answer == question[7]:
            score += 1

    if st.button("Submit"):
        st.success(f"Your score: {score}/{len(questions)}")
        email = st.text_input("Enter your email to receive results:")
        if st.button("Send Results"):
            send_email(score, email)
            st.success("Results sent to your email!")

if __name__ == "__main__":
    create_database()
    main()
