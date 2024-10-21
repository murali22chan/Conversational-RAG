function sendQuestion() {
    const userInput = document.getElementById('user-input').value;

    if (userInput === "") return;

    const chatContainer = document.getElementById('chat-container');
    chatContainer.innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;

    $.ajax({
        url: '/ask',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ question: userInput }),
        success: function(response) {
            chatContainer.innerHTML += `<p><strong>AI:</strong> ${response.answer}</p>`;
            
            if (response.context) {
                chatContainer.innerHTML += `<p><em>Retrieved Context:</em> ${response.context}</p>`;
            }
            if (response.source) {
                chatContainer.innerHTML += `<p><em>Context Sources:</em> ${response.source}</p>`;
            }

            chatContainer.innerHTML += `<p><em>Time Taken:</em> ${response.retrieval_time} seconds</p>`;
            
            chatContainer.scrollTop = chatContainer.scrollHeight;
            document.getElementById('user-input').value = '';
        },
        error: function() {
            chatContainer.innerHTML += `<p><strong>Error:</strong> Something went wrong!</p>`;
        }
    });
}

function clearHistory() {
    const chatContainer = document.getElementById('chat-container');
    $.ajax({
        url: '/clear_history',
        type: 'POST',
        success: function(response) {
            chatContainer.innerHTML = '';
        },
        error: function() {
            chatContainer.innerHTML += `<p><strong>Error:</strong> Could not clear history!</p>`;
        }
    });
}
