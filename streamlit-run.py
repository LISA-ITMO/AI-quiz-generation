import streamlit as st
import time
import random

# Define your questions, answers, and tips
questions = [
    {
        "question": "What aspect of retinal ganglion cells is primarily examined in the study?",
        "correct": "Precision of spike trains",
        "tip": "Focuses on temporal precision and reliability of spike trains in response to visual stimuli.",
        "wrong": ["Color adaptation mechanisms", "Synaptic plasticity", "Photoreceptor types"]
    },
    {
        "question": "What type of stimuli was used to stimulate the retinal ganglion cells?",
        "correct": "High contrast spatially uniform intensity modulation",
        "tip": "Uniform intensity modulation allows controlled study of response to light intensity changes.",
        "wrong": ["Complex visual scenes", "Directional motion stimuli", "Color changing stimuli"]
    },
    {
        "question": "What was the observed variability in spike timing across trials?",
        "correct": "As low as 1 ms",
        "tip": "Highlights high temporal precision in firing patterns.",
        "wrong": ["Greater than 10 ms", "Constant across all cells", "Dependent on color wavelength"]
    },
    {
        "question": "How does spike count variability compare to the mean?",
        "correct": "Much lower than the mean",
        "tip": "Indicates precision and reliability in response, inconsistent with Poisson statistics.",
        "wrong": ["Equal to the mean", "Higher than the mean", "Unrelated to the mean"]
    },
    {
        "question": "What potential consequence does the spike train precision in retinal ganglion cells have on visual processing?",
        "correct": "Influences the accuracy of visual performance",
        "tip": "Precision of retinal signals sets a foundational limit on visual processing accuracy.",
        "wrong": ["No impact on visual acuity", "Only affects color perception", "Limits the field of view"]
    }
]


def shuffle_questions():
    if 'questions_shuffled' not in st.session_state or not st.session_state.questions_shuffled:
        random.shuffle(questions)
        st.session_state.questions_shuffled = True

def display_question(question_info):
    st.subheader(question_info["question"])
    answers = [question_info["correct"]] + question_info["wrong"]
    random.shuffle(answers)
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
        st.write("File uploaded successfully!")
        st.write("Running model...")
        shuffle_questions()
        
        with st.spinner('Generating questions... Please wait.'):
            wait_time = random.randint(5, 10)  # Random wait time between 5 to 10 seconds
            time.sleep(wait_time)

            if 'question_index' not in st.session_state:
                st.session_state.question_index = 0
                st.session_state.selected_answer = None  # Initialize selected_answer here

            current_question = questions[st.session_state.question_index]
            display_question(current_question)

            if st.session_state.answer_selected:  # Check if an answer has been selected
                if st.button("To next question"):
                    st.session_state.question_index = (st.session_state.question_index + 1) % len(questions)
                    st.session_state.answer_selected = False  # Reset for the next question
                    st.session_state.selected_answer = None  # Reset selected answer
                    wait_time = random.randint(5, 10)
                    with st.spinner(f'Generating next question... (Waiting {wait_time} seconds)'):
                        time.sleep(wait_time)
                    st.experimental_rerun()

if __name__ == "__main__":
    main()
