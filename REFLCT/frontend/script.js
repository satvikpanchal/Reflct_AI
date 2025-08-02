document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');

    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const userMessage = userInput.value.trim();

        if (userMessage) {
            appendMessage(userMessage, 'user-message');
            userInput.value = '';
            getJarvisResponse(userMessage);
        }
    });

    function appendMessage(message, className) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('chat-message', className);
        messageElement.textContent = message;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to the latest message
    }

    async function getJarvisResponse(userMessage) {
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: userMessage })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            const jarvisMessage = data.response;
            appendMessage(jarvisMessage, 'jarvis-message');

        } catch (error) {
            console.error("Error fetching Jarvis response:", error);
            appendMessage("Sorry, I couldn't connect to Jarvis. Please check the server.", "jarvis-message");
        }
    }

    // Initial greeting from Jarvis
    setTimeout(() => {
        appendMessage("Hello! I am Jarvis. How can I assist you today?", "jarvis-message");
    }, 500);
});
