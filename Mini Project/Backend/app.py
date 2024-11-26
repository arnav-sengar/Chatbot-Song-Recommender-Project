from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load the song database
with open('songs_db.json', 'r') as f:
    songs_db = json.load(f)

@app.route('/')
def hello():
    return "Welcome to the Song Recommender Chatbot!"

@app.route('/recommend', methods=['GET'])
def recommend_song():
    # Get query parameters
    genre = request.args.get('genre')
    mood = request.args.get('mood')

    # Filter songs based on genre or mood
    filtered_songs = []
    
    for song in songs_db:
        if genre and song['genre'].lower() == genre.lower():
            filtered_songs.append(song)
        elif mood and song['mood'].lower() == mood.lower():
            filtered_songs.append(song)

    if not filtered_songs:
        return jsonify({"message": "No songs found for the given criteria."}), 404

    return jsonify(filtered_songs), 200

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')

    # Basic natural language understanding
    if "pop" in user_input.lower():
        return recommend_song(), 200
    elif "rock" in user_input.lower():
        return recommend_song(), 200
    elif "sad" in user_input.lower():
        return recommend_song(), 200
    elif "happy" in user_input.lower():
        return recommend_song(), 200
    else:
        return jsonify({"message": "Sorry, I didn't understand that. Can you specify a genre or mood?"}), 400

if __name__ == '__main__':
    app.run(debug=True)
