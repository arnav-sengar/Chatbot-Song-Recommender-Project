from flask import Flask, render_template, request, jsonify
import nltk
import random
import string
from nltk.corpus import stopwords
from datetime import datetime
from songs import songs

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# Responses for multiple languages and user interactions
responses = {
    "greeting": {
        "en": ["Hello!", "Hi there!", "How can I assist you today?", "Hey! How are you?"],
        "es": ["¡Hola!", "¡Hola! ¿Cómo estás?", "¿Cómo puedo ayudarte hoy?"],
        "fr": ["Bonjour!", "Salut! Comment ça va?", "Comment puis-je vous aider?"],
        "de": ["Hallo!", "Wie geht's?", "Wie kann ich dir helfen?"],
        "hi": ["Namaste!", "Namaskar!", "Pranam!", "Hello, how can I help you?"],
        "ur": ["Adaab!", "Hello! Kaise ho aap?"],
        "punjabi": ["Sat Sri Akal!", "Hello ji, kiwen ho?"],
        # Add more languages if needed
    },
    "good_morning": ["Good morning!", "Morning! Hope you have a great day ahead!"],
    "good_afternoon": ["Good afternoon!", "Hello! Hope your afternoon is going well!"],
    "good_evening": ["Good evening!", "Hi! Hope you're having a relaxing evening!"],
    "good_night": ["Good night!", "Sweet dreams!", "Take care and good night!"],
    "happy_birthday": ["Happy birthday!", "Wishing you a fantastic birthday filled with joy!"],
    "name": [
        "I am your friendly song recommender chatbot!",
        "You can call me Chatbot.",
        "I am Melodia, your personalized song recommender chatbot."
    ],
    "small_talk": [
        "I'm here to help with song recommendations or a quick chat!",
        "Tell me more about your favorite music!",
        "What genre of music do you enjoy?",
        "How's your day going?",
    ],
    "unknown": ["Sorry, I didn't understand that.", "Can you rephrase that?", "I'm not sure what you mean."],
    "can_play_song": [
        "Sorry, I can only recommend you a song.",
        "For playing music, you should refer to music playing apps like Spotify or JioSaavn.",
        "I can suggest songs, but to play them, you will need to use apps like Spotify, Apple Music, or JioSaavn."
    ],
    "how_are_you": [
        "I'm doing great, thanks for asking! How about you?",
        "I'm doing well, thank you! How are you doing?"
    ],
    "good_response": [
        "That's great to hear! I'm happy you're doing well!",
        "Awesome! Glad to hear you're feeling good.",
        "That's wonderful! Keep it up!"
    ],
    "who_are_you": [
        "I am Melodia, your personalized song recommender chatbot.",
        "I'm Melodia, here to recommend songs based on your preferences.",
        "I am Melodia, your friendly chatbot who loves music!"
    ]
}

# Process input text by removing punctuation and stopwords, and tokenize
def preprocess_input(text):
    text = text.lower()
    text = ''.join([char for char in text if char not in string.punctuation])
    words = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    return words

# Detect greetings based on keywords in multiple languages
def detect_greeting(user_words):
    greeting_keywords = {
        "en": ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "good night", "happy birthday"],
        "es": ["hola", "buenos días", "buenas tardes", "buenas noches"],
        "fr": ["bonjour", "salut", "bonsoir"],
        "de": ["hallo", "guten morgen", "guten tag", "guten abend"],
        "hi": ["namaste", "namaskar", "pranam", "salaam", "hello"],
        "ur": ["adaab", "salaam", "namaste"],
        "punjabi": ["sat sri akal", "hello ji", "kiwen ho", "namaskar"],
        # Add more languages if needed
    }
    
    # Special case for "Sat Sri Akal" to ensure it is detected correctly
    if "sat sri akal" in [word.lower() for word in user_words]:
        return "punjabi"  # Explicitly return Punjabi for "Sat Sri Akal"
    
    for lang, keywords in greeting_keywords.items():
        if any(keyword in user_words for keyword in keywords):
            return lang  # Return the language code for greeting
    return None

# Match user input to appropriate response
def match_input(user_input):
    user_words = preprocess_input(user_input)
    lang = detect_greeting(user_words)

    if lang:
        return random.choice(responses["greeting"][lang])
    
    # Detect time-specific greetings
    if "good morning" in user_input.lower():
        return random.choice(responses["good_morning"])
    elif "good afternoon" in user_input.lower():
        return random.choice(responses["good_afternoon"])
    elif "good evening" in user_input.lower():
        return random.choice(responses["good_evening"])
    elif "good night" in user_input.lower():
        return random.choice(responses["good_night"])
    elif "happy birthday" in user_input.lower():
        return random.choice(responses["happy_birthday"])

    # Handle specific keywords
    if "bye" in user_words or "goodbye" in user_words:
        return random.choice(responses["goodbye"])
    elif "name" in user_words:
        return random.choice(responses["name"])
    elif "song" in user_words or "recommend" in user_words:
        return recommend_song(user_input)
    elif "how are you" in user_input.lower():
        return random.choice(responses["how_are_you"])
    elif "play me a song" in user_input.lower():
        return random.choice(responses["can_play_song"])
    elif "who are you" in user_input.lower():
        return random.choice(responses["who_are_you"])
    elif any(word in user_words for word in ["how", "what", "why", "who", "when"]):
        return random.choice(responses["small_talk"])
    
    # Handle responses when user says they are good
    elif any(phrase in user_input.lower() for phrase in ["i am good", "i am doing well", "i am fine", "i am great", "i feel good"]):
        return random.choice(responses["good_response"])

    else:
        return random.choice(responses["unknown"])

# Recommend a song based on the user's input
def recommend_song(user_input):
    user_words = preprocess_input(user_input)
    recommended_songs = []

    genres = {song["genre"].lower() for song in songs}
    moods = {song["mood"].lower() for song in songs}
    artists = {song["artist"].lower() for song in songs}

    for word in user_words:
        if word in genres:
            recommended_songs.extend([song for song in songs if song["genre"].lower() == word])
        elif word in moods:
            recommended_songs.extend([song for song in songs if song["mood"].lower() == word])
        elif word in artists:
            recommended_songs.extend([song for song in songs if song["artist"].lower() == word])

    if recommended_songs:
        recommended_songs.sort(key=lambda x: x['title'])
        song = random.choice(recommended_songs)
        return f"I recommend '{song['title']}' by {song['artist']}! It's a great {song['genre']} song that fits your mood."
    else:
        return "Sorry, I couldn't find a song that matches your preferences."

# Flask route to render the frontend
@app.route('/')
def index():
    return render_template('index.html')

# Flask route to handle chat messages
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    response = match_input(user_input)
    return jsonify({'reply': response})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)