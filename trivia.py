import streamlit as st
import random
import time

# Define all questions and answers
questions = [
    {"question": "What is the capital of France?", "options": ["Paris", "Berlin", "Madrid", "Rome"], "answer": "Paris"},
    {"question": "Which planet is known as the Red Planet?", "options": ["Earth", "Mars", "Jupiter", "Saturn"], "answer": "Mars"},
    {"question": "Who wrote 'To Kill a Mockingbird'?", "options": ["Harper Lee", "J.K. Rowling", "George Orwell", "Mark Twain"], "answer": "Harper Lee"},
    {"question": "What is the largest mammal?", "options": ["Elephant", "Blue Whale", "Giraffe", "Hippopotamus"], "answer": "Blue Whale"},
    {"question": "Which country is known for sushi?", "options": ["China", "Japan", "Thailand", "Vietnam"], "answer": "Japan"},
    {"question": "What is the square root of 64?", "options": ["6", "7", "8", "9"], "answer": "8"},
    {"question": "Who painted the Mona Lisa?", "options": ["Leonardo da Vinci", "Vincent van Gogh", "Pablo Picasso", "Claude Monet"], "answer": "Leonardo da Vinci"},
    {"question": "What is the smallest prime number?", "options": ["0", "1", "2", "3"], "answer": "2"},
    {"question": "What is the chemical symbol for water?", "options": ["H2O", "O2", "CO2", "NaCl"], "answer": "H2O"},
    {"question": "How many continents are there?", "options": ["5", "6", "7", "8"], "answer": "7"},
    {"question": "What is the currency of the United States?", "options": ["Dollar", "Euro", "Pound", "Yen"], "answer": "Dollar"},
    {"question": "Who discovered penicillin?", "options": ["Alexander Fleming", "Marie Curie", "Isaac Newton", "Albert Einstein"], "answer": "Alexander Fleming"},
    {"question": "What is the capital of Italy?", "options": ["Venice", "Florence", "Rome", "Naples"], "answer": "Rome"},
    {"question": "What is the powerhouse of the cell?", "options": ["Nucleus", "Ribosome", "Mitochondria", "Cytoplasm"], "answer": "Mitochondria"},
    {"question": "What year did World War II end?", "options": ["1945", "1939", "1918", "1963"], "answer": "1945"},
    {"question": "Who is the author of '1984'?", "options": ["George Orwell", "Aldous Huxley", "J.K. Rowling", "Ernest Hemingway"], "answer": "George Orwell"},
    {"question": "Which planet is closest to the sun?", "options": ["Venus", "Earth", "Mercury", "Mars"], "answer": "Mercury"},
    {"question": "What is the boiling point of water in Celsius?", "options": ["90", "100", "110", "120"], "answer": "100"},
    {"question": "Which ocean is the largest?", "options": ["Atlantic", "Indian", "Arctic", "Pacific"], "answer": "Pacific"},
    {"question": "What is the purpose of a marketing funnel?", "options": ["To generate leads", "To convert customers", "To map customer journeys", "All of the above"], "answer": "All of the above"},
    {"question": "Which social media platform is known for its 'Stories' feature?", "options": ["Twitter", "Instagram", "LinkedIn", "Pinterest"], "answer": "Instagram"},
    {"question": "What is SEO?", "options": ["Search Engine Optimization", "Social Engagement Optimization", "Site Engagement Optimization", "Search Enhancement Online"], "answer": "Search Engine Optimization"},
    {"question": "Which is an example of content marketing?", "options": ["Blogging", "Pay-per-click ads", "Cold calling", "Billboards"], "answer": "Blogging"},
    {"question": "What does CPC stand for in digital marketing?", "options": ["Cost Per Conversion", "Click Per Conversion", "Cost Per Click", "Clicks Per Customer"], "answer": "Cost Per Click"},
    {"question": "Which is NOT a key digital marketing channel?", "options": ["Email", "Social Media", "SEO", "Public Libraries"], "answer": "Public Libraries"},
    {"question": "Which metric measures the percentage of website visitors who leave without taking action?", "options": ["CTR", "Bounce Rate", "Impressions", "Engagement"], "answer": "Bounce Rate"},
    {"question": "What is the main goal of influencer marketing?", "options": ["Generate sales", "Build brand trust", "Reach target audience", "All of the above"], "answer": "All of the above"},
    {"question": "What does CRM stand for?", "options": ["Customer Retention Method", "Customer Relationship Management", "Client Revenue Model", "Customer Referral Marketing"], "answer": "Customer Relationship Management"},
    {"question": "What is a KPI?", "options": ["Key Performance Indicator", "Key Product Insight", "Knowledge Process Integration", "Known Product Index"], "answer": "Key Performance Indicator"}
]

# Initialize shared state
if "shared_state" not in st.session_state:
    st.session_state.shared_state = {
        "game_started": False,
        "players": [],
        "scores": {},
        "host_name": "",
        "current_question": 0,
        "time_remaining": 20,
        "player_submitted": {},
        "countdown_shown": False,  # New flag to track if countdown is shown
    }

# Sidebar for joining or hosting the game
with st.sidebar:
    st.markdown("<h3>Game Setup</h3>", unsafe_allow_html=True)
    
    # Host or Join toggle
    is_host = st.checkbox("I am the host")
    if is_host:
        host_name = st.text_input("Enter your name as the host:")
        if host_name:
            st.session_state.shared_state["host_name"] = host_name
            if host_name not in st.session_state.shared_state["players"]:
                st.session_state.shared_state["players"].append(host_name)
                st.session_state.shared_state["scores"][host_name] = 0
                st.success("You are hosting the game!")
    else:
        player_name = st.text_input("Enter your name to join:")
        if player_name and st.button("Join Game"):
            if player_name not in st.session_state.shared_state["players"]:
                st.session_state.shared_state["players"].append(player_name)
                st.session_state.shared_state["scores"][player_name] = 0
                st.success(f"{player_name} has joined the game!")
    
    # Display current players
    st.markdown("### Players in the game:")
    for player in st.session_state.shared_state["players"]:
        st.write(player)
    
    # Start game button (only visible to host)
    if is_host and st.session_state.shared_state["host_name"]:
        if st.button("Start Game"):
            st.session_state.shared_state["game_started"] = True
            st.session_state.shared_state["current_question"] = 0
            st.session_state.shared_state["time_remaining"] = 20
            st.session_state.shared_state["player_submitted"] = {}
            st.session_state.shared_state["countdown_shown"] = False  # Reset countdown flag

# Main game screen
if st.session_state.shared_state["game_started"]:
    # Countdown before the first question
    if st.session_state.shared_state["current_question"] == 0 and not st.session_state.shared_state["countdown_shown"]:
        st.markdown("<h2>Get Ready! The game starts in 10 seconds...</h2>", unsafe_allow_html=True)
        with st.spinner("Starting the game..."):
            time.sleep(10)  # Simulate the countdown
        st.session_state.shared_state["countdown_shown"] = True

    # Timer logic
    time_limit = 20  # seconds per question
    if "start_time" not in st.session_state.shared_state:
        st.session_state.shared_state["start_time"] = time.time()
    elapsed_time = int(time.time() - st.session_state.shared_state["start_time"])
    st.session_state.shared_state["time_remaining"] = max(0, time_limit - elapsed_time)

    # Show question
    current_question = st.session_state.shared_state["current_question"]
    if current_question < len(questions):
        question = questions[current_question]
        st.markdown(f"<h3>Question {current_question + 1}: {question['question']}</h3>", unsafe_allow_html=True)
        
        # Player answer input
        player_name = st.session_state.shared_state["host_name"] if is_host else player_name
        if player_name in st.session_state.shared_state["players"]:
            if player_name not in st.session_state.shared_state["player_submitted"]:
                st.session_state.shared_state["player_submitted"][player_name] = {}
            
            if not st.session_state.shared_state["player_submitted"][player_name].get(current_question, False):
                answer = st.radio("Your answer:", question["options"], key=f"q{current_question}_{player_name}")
                
                # Submit answer
                if st.button("Submit Answer", key=f"submit_{current_question}"):
                    if answer == question["answer"]:
                        st.session_state.shared_state["scores"][player_name] += 1
                        st.success("Correct!")
                    else:
                        st.error(f"Wrong! The correct answer is {question['answer']}")
                    st.session_state.shared_state["player_submitted"][player_name][current_question] = True

        # Show timer
        st.markdown(f"⏳ Time remaining: {st.session_state.shared_state['time_remaining']} seconds")
        
        # Next Question Logic
        if st.session_state.shared_state["time_remaining"] == 0 or st.button("Next Question", key="next_question"):
            st.session_state.shared_state["current_question"] += 1
            st.session_state.shared_state["start_time"] = time.time()
            st.session_state.shared_state["time_remaining"] = time_limit
            st.session_state.shared_state["player_submitted"] = {}

    else:
        # End of game
        st.markdown("<h2>🎉 Game Over! 🎉</h2>", unsafe_allow_html=True)
        st.write("Final Scores:")
        for player, score in sorted(st.session_state.shared_state["scores"].items(), key=lambda x: x[1], reverse=True):
            st.write(f"{player}: {score}")
else:
    st.markdown("<h2>Waiting for the host to start the game...</h2>", unsafe_allow_html=True)