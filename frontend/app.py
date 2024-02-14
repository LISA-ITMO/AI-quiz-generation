"""
RAG frontend logic.
"""

import base64
import logging
import requests
import streamlit as st

# Set up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def display_question(question_info):
    st.subheader(question_info["question"])
    answers = [question_info["correct"]] + question_info["wrong"]
    correct_answer = question_info["correct"]
    tip = question_info["tip"]

    if 'selected_answer' not in st.session_state:
        st.session_state.selected_answer = None
        st.session_state.display_feedback = False  # Flag to control feedback display

    for i, answer in enumerate(answers):
        if st.button(answer, key=f"answer_{i}_{st.session_state.question_index}"):
            st.session_state.selected_answer = answer
            st.session_state.display_feedback = True  # Set flag to display feedback

    # Show feedback only if the flag is set
    if st.session_state.display_feedback:
        if st.session_state.selected_answer == correct_answer:
            st.success("Correct!")
        else:
            st.error("Incorrect!")
        st.info(f"Tip: {tip}")
        st.session_state.display_feedback = False


def main():
    st.title("Quiz Quest")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if 'answer_selected' not in st.session_state:
        st.session_state.answer_selected = False  # Initialize answer_selected
        
    if uploaded_file is not None:
        # Once file and question received
        # Update user with messages
        message = st.chat_message("user") 

        # Encode the PDF file as base64 string
        logger.info("Encoding PDF file as base64 string")
        encoded_pdf = base64.b64encode(uploaded_file.read()).decode("ascii")
        json_payload = {"pdf": encoded_pdf}

        st.write("File uploaded successfully!")
        st.write("Running model...")
        
        with st.spinner('Generating questions... Please wait.'):
            # Send request and display answer to user
            logger.info("Sending request to backend")
            response = requests.post("http://backend:8000/ask", json=json_payload, timeout=120)

            logger.info("Showing response from backend")
            message.write(response.json())

            if 'question_index' not in st.session_state:
                st.session_state.question_index = 0
                st.session_state.selected_answer = None  # Initialize selected_answer here

            current_question = response[st.session_state.question_index]
            display_question(current_question)

            if st.session_state.answer_selected:  # Check if an answer has been selected
                if st.button("To next question"):
                    st.session_state.question_index = (st.session_state.question_index + 1) % len(questions)
                    st.session_state.answer_selected = False  # Reset for the next question
                    st.session_state.selected_answer = None  # Reset selected answer
                    st.experimental_rerun()