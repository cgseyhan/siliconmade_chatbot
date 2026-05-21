(function() {
    const cbButton = document.getElementById('cb-button');
    const cbWindow = document.getElementById('cb-window');
    const cbClose = document.getElementById('cb-close');
    const cbInput = document.getElementById('cb-input');
    const cbSend = document.getElementById('cb-send');
    const cbMessages = document.getElementById('cb-messages');

    // Toggle Window
    cbButton.onclick = () => {
        cbWindow.style.display = cbWindow.style.display === 'flex' ? 'none' : 'flex';
    };

    cbClose.onclick = () => {
        cbWindow.style.display = 'none';
    };

    // Send Message
    async function sendMessage() {
        const text = cbInput.value.trim();
        if (!text) return;

        // Add user message to UI
        appendMessage('user', text);
        cbInput.value = '';

        try {
            // Send to API (our FastAPI chat endpoint)
            const response = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ messages: [{ role: 'user', content: text }], model: 'ChatGPT-4o' })
            });

            const data = await response.json();
            appendMessage('bot', data.response);
        } catch (error) {
            appendMessage('bot', 'Sorry, an error occurred. Please try again.');
            console.error('Chat Error:', error);
        }
    }

    function appendMessage(sender, text) {
        const div = document.createElement('div');
        div.className = `cb-msg cb-msg-${sender}`;
        div.innerText = text;
        cbMessages.appendChild(div);
        cbMessages.scrollTop = cbMessages.scrollHeight;
    }

    cbSend.onclick = sendMessage;
    cbInput.onkeypress = (e) => {
        if (e.key === 'Enter') sendMessage();
    };
})();
