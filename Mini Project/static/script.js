// Chat functionality
const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-btn');

// User preferences
const userPreferences = {
  favoriteArtists: [],
  favoriteGenres: [],
  favoriteMoods: [],
};

// Send message function
sendButton.addEventListener('click', sendMessage);

// Event listener for the Enter key
userInput.addEventListener('keypress', function (e) {
  if (e.key === 'Enter') {
    sendMessage();
  }
});

// Function to send a message
function sendMessage() {
  const message = userInput.value.trim();
  if (message === '') return;

  // Display user message
  displayMessage(message, 'user');
  userInput.value = '';

  // Show loading indicator
  const loadingDiv = document.createElement('div');
  loadingDiv.classList.add('loading-indicator');
  loadingDiv.textContent = 'Melodia is typing...';
  chatBox.appendChild(loadingDiv);
  chatBox.scrollTop = chatBox.scrollHeight;

  // Send the message to the Flask backend
  fetch('/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ message: message }),
  })
    .then((response) => response.json())
    .then((data) => {
      // Remove loading indicator
      chatBox.removeChild(loadingDiv);

      // Display the chatbot's response
      displayMessage(data.reply, 'bot');

      // Check if the user ended the chat
      if (message.toLowerCase() === 'bye') {
        // Display the rating system
        addRatingSystem(chatBox.lastChild);
      }
    })
    .catch((error) => {
      console.error('Error:', error);

      // Remove loading indicator
      chatBox.removeChild(loadingDiv);

      // Display error message
      displayMessage('Sorry, something went wrong. Please try again.', 'bot');
    });
}

// Display message function
function displayMessage(message, sender) {
  const messageDiv = document.createElement('div');
  messageDiv.classList.add('message', sender);

  // Add message content
  const messageContent = document.createElement('div');
  messageContent.textContent = message;
  messageDiv.appendChild(messageContent);

  // Add timestamp
  const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  const timestampSpan = document.createElement('span');
  timestampSpan.classList.add('timestamp');
  timestampSpan.textContent = timestamp;
  messageDiv.appendChild(timestampSpan);

  chatBox.appendChild(messageDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Add rating system
function addRatingSystem(messageDiv) {
  const ratingDiv = document.createElement('div');
  ratingDiv.classList.add('rating');
  messageDiv.appendChild(ratingDiv);

  // Create 5 star buttons
  for (let i = 1; i <= 5; i++) {
    const ratingButton = document.createElement('button');
    ratingButton.classList.add('rating-button');
    ratingButton.innerHTML = '&#9733;'; // Unicode star symbol
    ratingButton.dataset.rating = i;

    // Highlight stars on hover
    ratingButton.addEventListener('mouseover', () => {
      highlightStars(ratingDiv, i);
    });

    // Reset stars on mouseout (unless a rating is selected)
    ratingButton.addEventListener('mouseout', () => {
      if (!ratingDiv.dataset.selectedRating) {
        resetStars(ratingDiv);
      }
    });

    // Handle click to select a rating
    ratingButton.addEventListener('click', () => {
      const selectedRating = i;
      ratingDiv.dataset.selectedRating = selectedRating;
      highlightStars(ratingDiv, selectedRating);
      alert(`Thank you for your rating of ${selectedRating} stars!`);
    });

    ratingDiv.appendChild(ratingButton);
  }
}

// Function to highlight stars up to a specific rating
function highlightStars(ratingDiv, rating) {
  const stars = ratingDiv.querySelectorAll('.rating-button');
  stars.forEach((star, index) => {
    if (index < rating) {
      star.classList.add('active');
    } else {
      star.classList.remove('active');
    }
  });
}

// Function to reset stars to their default state
function resetStars(ratingDiv) {
  const stars = ratingDiv.querySelectorAll('.rating-button');
  stars.forEach((star) => {
    star.classList.remove('active');
  });
}