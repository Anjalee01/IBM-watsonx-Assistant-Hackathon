
// Watson Assistant API Integration
const chatbotContainer = document.getElementById('chatbot-container');

// Initialize Watson Assistant UI
function initializeChatbot() {
    chatbotContainer.innerHTML = `
        <div class="chat-header">
            <h4>Chat with Watson</h4>
            <button class="close-chat" onclick="closeChat()">X</button>
        </div>
        <div class="chat-messages"></div>
        <div class="chat-input">
            <input type="text" id="user-message" placeholder="Type your message..." />
            <button id="send-button">Send</button>
        </div>
    `;

    const sendButton = document.getElementById('send-button');
    const userInput = document.getElementById('user-message');

    sendButton.addEventListener('click', () => {
        const userMessage = userInput.value.trim();
        if (userMessage) {
            displayUserMessage(userMessage);
            userInput.value = '';
            sendMessageToWatson(userMessage);
        }
    });
}

// Display User Message in Chat Window
function displayUserMessage(message) {
    const chatMessages = document.querySelector('.chat-messages');
    const userMessageElement = document.createElement('div');
    userMessageElement.className = 'user-message';
    userMessageElement.innerText = message;
    chatMessages.appendChild(userMessageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Display Watson Response in Chat Window
function displayWatsonMessage(message) {
    const chatMessages = document.querySelector('.chat-messages');
    const watsonMessageElement = document.createElement('div');
    watsonMessageElement.className = 'watson-message';
    watsonMessageElement.innerText = message;
    chatMessages.appendChild(watsonMessageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Send User Message to Watson Assistant
function sendMessageToWatson(message) {
    fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.reply) {
                displayWatsonMessage(data.reply);
            } else {
                displayWatsonMessage('Sorry, I could not process your request.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            displayWatsonMessage('An error occurred. Please try again.');
        });
}

// Close Chat Function
function closeChat() {
    chatbotContainer.innerHTML = '';
}

// Initialize Chatbot on Page Load
document.addEventListener('DOMContentLoaded', initializeChatbot);

