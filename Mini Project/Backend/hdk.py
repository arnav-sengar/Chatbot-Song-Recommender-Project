import nltk
import random
import string
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')

songs = [
    {"title": "Blinding Lights", "artist": "The Weeknd", "genre": "Pop", "mood": "Energetic"},
    {"title": "Shape of You", "artist": "Ed Sheeran", "genre": "Pop", "mood": "Happy"},
    {"title": "Someone Like You", "artist": "Adele", "genre": "Pop", "mood": "Sad"},
    {"title": "Bohemian Rhapsody", "artist": "Queen", "genre": "Rock", "mood": "Dramatic"},
    {"title": "Smells Like Teen Spirit", "artist": "Nirvana", "genre": "Rock", "mood": "Angry"},
    {"title": "Blowin' in the Wind", "artist": "Bob Dylan", "genre": "Folk", "mood": "Thoughtful"},
    {"title": "Stay", "artist": "Justin Bieber", "genre": "Pop", "mood": "Romantic"},
    {"title": "Let it Be", "artist": "The Beatles", "genre": "Rock", "mood": "Hopeful"}
]

responses = {
    "greeting": ["Hello!", "Hi there!", "How can I assist you today?", "Hey! How are you?"],
    "goodbye": ["Goodbye!", "See you later!", "Take care!"],
    "name": ["I am your friendly song recommender chatbot!", "You can call me Chatbot."],
    "unknown": ["Sorry, I didn't understand that.", "Can you rephrase that?", "I'm not sure what you mean."]
}

def preprocess_input(text):
    text = text.lower()
    text = ''.join([char for char in text if char not in string.punctuation])
    words = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    return words

def match_input(user_input):
    user_words = preprocess_input(user_input)
    
    if "hello" in user_words or "hi" in user_words:
        return random.choice(responses["greeting"])
    elif "bye" in user_words or "goodbye" in user_words:
        return random.choice(responses["goodbye"])
    elif "name" in user_words:
        return random.choice(responses["name"])
    elif "song" in user_words or "recommend" in user_words:
        return recommend_song(user_input)
    else:
        return random.choice(responses["unknown"])

def recommend_song(user_input):
    user_words = preprocess_input(user_input)
    recommended_songs = []
    
    if "pop" in user_words:
        recommended_songs = [song for song in songs if song["genre"].lower() == "pop"]
    elif "rock" in user_words:
        recommended_songs = [song for song in songs if song["genre"].lower() == "rock"]
    elif "folk" in user_words:
        recommended_songs = [song for song in songs if song["genre"].lower() == "folk"]
    elif "energetic" in user_words:
        recommended_songs = [song for song in songs if song["mood"].lower() == "energetic"]
    elif "happy" in user_words:
        recommended_songs = [song for song in songs if song["mood"].lower() == "happy"]
    elif "sad" in user_words:
        recommended_songs = [song for song in songs if song["mood"].lower() == "sad"]
    elif "romantic" in user_words:
        recommended_songs = [song for song in songs if song["mood"].lower() == "romantic"]

    if recommended_songs:
        song = random.choice(recommended_songs)
        return f"I recommend '{song['title']}' by {song['artist']}! It's a great {song['genre']} song that fits your mood."
    else:
        return "Sorry, I couldn't find a song that matches your preferences."

def chat():
    print("Chatbot: Hello! How can I assist you today?")
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Chatbot: " + random.choice(responses["goodbye"]))
            break
        
        response = match_input(user_input)
        print("Chatbot: " + response)

if __name__ == "__main__":
    chat()
