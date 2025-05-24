import streamlit as st
import random

# Define grid labels
grid_labels = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']

# Assign unique numbers 1-9 randomly to grid positions
@st.cache_data
def generate_grid():
    numbers = list(range(1, 10))
    random.shuffle(numbers)
    return dict(zip(grid_labels, numbers))

# Define the questions and their answers
questions = {
    'A1': ("How many strings does a standard violin have?", 4),
    'A2': ("What’s 3 divided by 3?", 1),
    'A3': ("You have 4 apples. You give 1 away, then eat 1. How many are left?", 2),
    'B1': ("What is 3 + 3?", 6),
    'B2': ("How many legs does a tricycle have?", 3),
    'B3': ("🕘 This clock emoji shows what number?", 9),
    'C1': ("How many continents are there on Earth?", 7),
    'C2': ("I am an even number. I am less than 3. What number am I?", 2),
    'C3': ("What is 10 minus half of 10?", 5),
}

st.title("🎮 Grid of 9 Game")

# Load grid numbers
grid_numbers = generate_grid()

# Game state
game_state = st.session_state.setdefault('guesses', {})

st.write("Click a box and answer the question. The correct answer will fill the grid.")

# Display 3x3 Grid
for row in ['A', 'B', 'C']:
    cols = st.columns(3)
    for i, col in enumerate(cols):
        key = row + str(i+1)
        if key in game_state:
            col.success(f"{game_state[key]}")
        else:
            if col.button(f"❓ {key}", key=f"btn_{key}"):
                q, answer = questions[key]
                user_answer = st.number_input(f"{key} - {q}", min_value=1, max_value=9, step=1, key=f"input_{key}")
                if st.button(f"Submit Answer for {key}", key=f"submit_{key}"):
                    if user_answer == answer:
                        game_state[key] = answer
                        st.success(f"Correct! {key} is {answer}.")
                    else:
                        st.error("Incorrect. Try again!")
