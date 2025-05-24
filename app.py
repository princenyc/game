import streamlit as st
import random
import time

# Define grid labels
grid_labels = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']

# All available questions
all_questions = [
    ("How many strings does a standard violin have?", 4),
    ("What’s 3 divided by 3?", 1),
    ("You have 4 apples. You give 1 away, then eat 1. How many are left?", 2),
    ("What is 3 + 3?", 6),
    ("How many legs does a tricycle have?", 3),
    ("🕘 This clock emoji shows what number?", 9),
    ("How many continents are there on Earth?", 7),
    ("I am an even number. I am less than 3. What number am I?", 2),
    ("What is 10 minus half of 10?", 5),
    ("How many planets are in the solar system (as of 2025)?", 8),
    ("What’s the square root of 9?", 3),
    ("If a spider has 8 legs and loses 1, how many does it have left?", 7),
    ("How many sides does a hexagon have?", 6),
    ("How many wheels does a car usually have?", 4),
    ("What is 5 x 1?", 5),
]

@st.cache_data
def generate_grid():
    numbers = list(range(1, 10))
    random.shuffle(numbers)
    selected_questions = random.sample(all_questions, 9)
    questions_map = dict(zip(grid_labels, selected_questions))
    return dict(zip(grid_labels, numbers)), questions_map

st.title("🎮 Grid of 9 Game")

# Reset functionality
if st.button("🔄 Reset Game"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()

# Initialize or load game data
grid_numbers, questions = generate_grid()
game_state = st.session_state.setdefault('guesses', {})
score = st.session_state.setdefault('score', 0)
total_correct = st.session_state.setdefault('total_correct', 0)
start_time = st.session_state.setdefault('start_time', time.time())

# Timer display
elapsed = int(time.time() - st.session_state['start_time'])
st.markdown(f"**⏱️ Time Elapsed:** {elapsed} seconds")

# Score display
st.markdown(f"**✅ Score This Round:** {len(game_state)} / 9")
st.markdown(f"**🏅 Total Correct Answers Across Rounds:** {st.session_state['total_correct']}")

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
                    correct_answer = answer
                    if user_answer == correct_answer:
                        game_state[key] = correct_answer
                        st.session_state['total_correct'] += 1
                        st.success(f"Correct! {key} is {correct_answer}.")
                        st.experimental_rerun()
                    else:
                        st.error("Incorrect. Try again!")
