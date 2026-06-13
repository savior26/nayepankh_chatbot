// Local tracking token establishing clean memory sessions
const chatSessionToken = "session_" + Math.random().toString(36).substr(2, 9);

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        submitMessage();
    }
}

function sendPreset(textValue) {
    appendMessage(textValue, 'user-msg');
    executeServerRequest(textValue);
}

function submitMessage() {
    const inputElement = document.getElementById('userInput');
    const rawText = inputElement.value.trim();
    
    if (rawText === "") return;

    appendMessage(rawText, 'user-msg');
    inputElement.value = ""; // Empty form input element clear
    
    executeServerRequest(rawText);
}

function appendMessage(text, className) {
    const chatWindow = document.getElementById('chatWindow');
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${className}`;
    msgDiv.innerText = text;
    
    chatWindow.appendChild(msgDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight; // Keep view locked to newest tokens
    return msgDiv;
}

async function executeServerRequest(messageText) {
    // Generate transient visual loader notification placeholder
    const loadingPlaceholder = appendMessage("NayePankh Guide is typing...", "bot-msg loading-dots");

    try {
        const networkResponse = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: chatSessionToken,
                message: messageText
            })
        });

        const targetData = await networkResponse.json();
        
        // Remove loading state element and reveal live response
        loadingPlaceholder.remove();
        
        // Check if response was successful
        if (!networkResponse.ok) {
            console.error("Server error:", targetData);
            const errorMsg = targetData.error || "Server error occurred. Please try again.";
            appendMessage(errorMsg, 'bot-msg');
            return;
        }
        
        if (targetData.reply) {
            appendMessage(targetData.reply, 'bot-msg');
        } else {
            appendMessage("I ran into an unexpected processing issue. Please try again shortly.", 'bot-msg');
        }

    } catch (networkError) {
        loadingPlaceholder.remove();
        appendMessage("Network communication failure. Ensure your Flask server is running locally.", 'bot-msg');
        console.error("Critical API Trace:", networkError);
    }
}