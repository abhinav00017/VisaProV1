document.addEventListener('DOMContentLoaded', function() {

    const contentAIChatDisplayDiv = document.getElementById('contentAIChatDisplay');

    // window.setInterval(function() {
    //     contentAIChatDisplayDiv.scrollTop = contentAIChatDisplayDiv.scrollHeight;
    //   }, 50);

    function aiGenerateResponse(query, threadId=0) {
        return new Promise((resolve, reject) => {    
            const xhr = new XMLHttpRequest();
            const url = '/visagpt/chat';

            xhr.onerror = function() {
                console.error('Request failed', xhr.statusText);
                reject(xhr.statusText);
            };

            body = {
                'message': query,
                'threadId': threadId
            };

            headers = {
                'Content-Type': 'application/json'
            };

            console.log('threadId:', threadId);

            xhr.open('POST', url, true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.send(JSON.stringify(body));

            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4 && xhr.status == 200) {
                    const response = JSON.parse(xhr.responseText);
                    resolve(response);
                }
            };
        });
    }

    var contentAIQueryDiv = document.getElementById('contentAIQuery');
    var contentAIQueryP = document.getElementById('contentAIQuery-p');

    var contentAIResponseDiv = document.getElementById('contentAIResponse');
    var contentAIResponseP = document.getElementById('contentAIResponse-p');
    var loadingGifDiv = document.getElementById('loadingGif');

    var chatInputInput = document.getElementById('chatInput-input');

    var chatInputBtn = document.getElementById('chatInput-btn');
    var chatInputSvg = document.getElementById('chatInput-svg');   

    chatInputInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            functionSendQuery();
        }
    });

    async function ChatConversation(query, threadId) {
        chatInputInput = document.getElementById('chatInput-input');
        chatInputInput.value = "";

        contentAIQueryDiv.style.display = '';
        contentAIResponseDiv.style.display = '';
        loadingGifDiv.style.display = '';

        chatInputBtn.disabled = true;
        chatInputBtn.style.cursor = "not-allowed";
        chatInputSvg.classList.add('disabled');

        contentAIQueryP.innerText = query;
        contentAIChatDisplayDiv.appendChild(contentAIQueryDiv.cloneNode(true));
        contentAIChatDisplayDiv.scrollTop = contentAIChatDisplayDiv.scrollHeight;

        contentAIResponseP.innerText = "";
        contentAIResponseP.appendChild(loadingGifDiv.cloneNode(true));
        contentAIChatDisplayDiv.appendChild(contentAIResponseDiv.cloneNode(true));
        contentAIChatDisplayDiv.scrollTop = contentAIChatDisplayDiv.scrollHeight;

        const response = await aiGenerateResponse(query, threadId);
        console.log('response:', response);

        contentAIResponseP.removeChild(contentAIResponseP.firstChild);
        contentAIResponseP.innerHTML = "";
        contentAIResponseP.innerText = response.response;

        contentAIChatDisplayDiv.removeChild(contentAIChatDisplayDiv.lastChild);
        contentAIChatDisplayDiv.appendChild(contentAIResponseDiv.cloneNode(true));
        contentAIChatDisplayDiv.scrollTop = contentAIChatDisplayDiv.scrollHeight;

        chatInputBtn.disabled = false;
        chatInputBtn.style.cursor = "pointer";
        chatInputSvg.classList.remove('disabled');

    }

    window.functionChatStarter = async function(button) {

        contentAIChatDisplayDiv.innerHTML = "";
        const query = button.textContent;

        ChatConversation(query, "thread_DRDB30xSgUFamJghXHcG8dvY");
    };

    window.functionSendQuery = function() {
        const query = document.getElementById('chatInput-input').value;

        if (query === "") {
            return;
        }

        if (document.getElementById('contentAIWelcome')) {
            contentAIChatDisplayDiv.innerHTML = "";
        }

        
        ChatConversation(query, "thread_DRDB30xSgUFamJghXHcG8dvY");
    }
});