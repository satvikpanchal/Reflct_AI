document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');
    const micBtn = document.getElementById('mic-btn');
    let micOn = false;

    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const userMessage = userInput.value.trim();
        if (userMessage) {
            appendMessage(userMessage, 'user-message');
            userInput.value = '';
            getJarvisResponse(userMessage);
        }
    });

    micBtn.addEventListener('click', () => {
        micOn = !micOn;
        micBtn.classList.toggle('active', micOn);
        micBtn.textContent = micOn ? "🔴" : "🎤";
        if (micOn) {
            startVoiceMode();
        }
    });

    function appendMessage(message, className) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('chat-message', className);
        messageElement.textContent = message;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    async function getJarvisResponse(userMessage) {
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userMessage })
            });
            const data = await response.json();
            appendMessage(data.response, 'jarvis-message');
        } catch (error) {
            appendMessage("Error connecting to Jarvis", 'jarvis-message');
        }
    }

    async function startVoiceMode() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            const mediaRecorder = new MediaRecorder(stream);
            let chunks = [];

            mediaRecorder.ondataavailable = e => chunks.push(e.data);

            mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(chunks, { type: 'audio/webm' });
                chunks = [];
                await sendAudioToJarvis(audioBlob);

                if (micOn) {
                    startVoiceMode(); // restart if mic still on
                }
            };

            mediaRecorder.start();
            setTimeout(() => mediaRecorder.stop(), 6000); // record in 6 sec chunks
        } catch (err) {
            console.error("Mic error:", err);
        }
    }

    async function sendAudioToJarvis(audioBlob) {
        const formData = new FormData();
        formData.append("audio", audioBlob);

        const response = await fetch("/api/chat/audio", {
            method: "POST",
            body: formData
        });
        const data = await response.json();
        appendMessage(data.response, 'jarvis-message');
    }

    // Initial greeting
    setTimeout(() => {
        appendMessage("Hello! I am Jarvis. How can I assist you today?", "jarvis-message");
    }, 500);
});
