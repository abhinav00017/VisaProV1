window.onload = () => {
    const sidebar = document.getElementById('sidebar');
    const threads = document.getElementById('Recent_btns');
    const HS1 = document.getElementById('HS1');
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');
    const newchat = document.getElementById('New_chat');
    

    var lastThread;
    var last_threadId;
    var NoThreads = false;

    let threadCount = 0;
    let maxthreadCount = 18;

    function fetchThreads() {
        sendBtn.disabled = true;

        threads.innerHTML = ''; 
        const loadingdiv = document.createElement('div');
        const loadingGif = document.createElement('img');
        loadingGif.setAttribute('src', '/static/loading.gif');
        loadingGif.setAttribute('alt', 'Loading...');
        loadingGif.style.height = "50px";
        loadingGif.style.width = "50px"; 

        const loadingText = document.createElement('span');
        loadingText.textContent = "Loading...";

        loadingText.style.paddingTop = "10px";
        loadingdiv.appendChild(loadingGif);
        loadingdiv.appendChild(loadingText);
        loadingdiv.style.display = "flex";
        loadingdiv.style.flexDirection = "column";
        loadingdiv.style.width = "100%";
        loadingdiv.style.alignItems = "center";

        threads.appendChild(loadingdiv);   
        

        fetch('/visagpt/threads')
            .then(response => response.json())
            .then(data => {
                console.log(data);
                threads.innerHTML = ''; // Clear the threads list before appending new ones
                if (data.threads_list.length > 0) {
                    data.threads_list.forEach(thread  => {
                    threadCount++;
                    const button = document.createElement('button');
                    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");

                    svg.setAttribute('viewBox', '0 0 24 24');
                    svg.setAttribute('fill', 'currentColor');
                    svg.setAttribute('class', 'w-6 h-6');

                    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
                    path.setAttribute('fill-rule', 'evenodd');
                    path.setAttribute('d', "M9 4.5a.75.75 0 0 1 .721.544l.813 2.846a3.75 3.75 0 0 0 2.576 2.576l2.846.813a.75.75 0 0 1 0 1.442l-2.846.813a3.75 3.75 0 0 0-2.576 2.576l-.813 2.846a.75.75 0 0 1-1.442 0l-.813-2.846a3.75 3.75 0 0 0-2.576-2.576l-2.846-.813a.75.75 0 0 1 0-1.442l2.846-.813A3.75 3.75 0 0 0 7.466 7.89l.813-2.846A.75.75 0 0 1 9 4.5ZM18 1.5a.75.75 0 0 1 .728.568l.258 1.036c.236.94.97 1.674 1.91 1.91l1.036.258a.75.75 0 0 1 0 1.456l-1.036.258c-.94.236-1.674.97-1.91 1.91l-.258 1.036a.75.75 0 0 1-1.456 0l-.258-1.036a2.625 2.625 0 0 0-1.91-1.91l-1.036-.258a.75.75 0 0 1 0-1.456l1.036-.258a2.625 2.625 0 0 0 1.91-1.91l.258-1.036A.75.75 0 0 1 18 1.5ZM16.5 15a.75.75 0 0 1 .712.513l.394 1.183c.15.447.5.799.948.948l1.183.395a.75.75 0 0 1 0 1.422l-1.183.395c-.447.15-.799.5-.948.948l-.395 1.183a.75.75 0 0 1-1.422 0l-.395-1.183a1.5 1.5 0 0 0-.948-.948l-1.183-.395a.75.75 0 0 1 0-1.422l1.183-.395c.447-.15.799-.5.948-.948l.395-1.183A.75.75 0 0 1 16.5 15Z")
                    path.setAttribute('clip-rule', 'evenodd');
                    svg.appendChild(path);

                    button.appendChild(svg);

                    let parts = thread.id.split('_');
                    let lastFourValues = parts[parts.length - 1].slice(-4);
                    console.log(lastFourValues);
                    button.appendChild(document.createTextNode("thread_"+lastFourValues));

                    button.addEventListener('click', () => loadThread(thread.id));
                    threads.prepend(button);
                    });
                }
                else {
                    threads.textContent = "No threads available.";
                    NoThreads = true;
                }
            }).then(() => {
                sendBtn.disabled = false;
            });
    }

    function addMessage(sender, message) {
        const lines = message.split('\n');
        const messageDiv = document.createElement('div');
        messageDiv.className = sender;
        for (let line of lines) {
            const lineDiv = document.createElement('div');
            lineDiv.textContent = line;
            messageDiv.appendChild(lineDiv);
        }
        HS1.appendChild(messageDiv);
        window.requestAnimationFrame(() => {
            const container = document.querySelector('.HS1');
            container.scrollTop = container.scrollHeight;
        });
    }

    function scrollToBottom() {
        var container = document.querySelector('.HS1');
        console.log('scrolling to bottom:HS1 '+container.scrollHeight, container.scrollTop, container);
        container.scrollTop = container.scrollHeight;
    }
    
    // Call scrollToBottom() whenever a new message is added
    scrollToBottom();


    function loadThread(threadId) {
        HS1.innerHTML = '';
        last_threadId = threadId;
        fetch(`/visagpt/threads/${threadId}`)
            .then(response => response.json())
            .then(data => {
                console.log(data);
                data.messages.forEach(msg => {
                    addMessage(msg.sender, msg.content);
                });
                scrollToBottom();
            });
        }

    fetchThreads();

    function addCurrentMessage(sender, message, threadId) {
        console.log(threadId);
        const lines = message.split('\n');
        const messageDiv = document.createElement('div');
        if (sender === 'assistant' && threadId === last_threadId) {
            messageDiv.className = 'assistant';
            for (let line of lines) {
                const lineDiv = document.createElement('div');
                lineDiv.textContent = line;
                messageDiv.appendChild(lineDiv);
            }
            if (HS1.lastChild) {
                HS1.replaceChild(messageDiv, HS1.lastChild);
            } else {
                HS1.appendChild(messageDiv);
            }
            scrollToBottom();
        }
    }

    sendBtn.addEventListener('click', () => {
        const message = userInput.value;
        sendBtn.disabled = true;
        if (message.trim() !== '') {
            if (threadCount > maxthreadCount && last_threadId === undefined) {
                document.getElementById('alertMessage').textContent = "You have reached the maximum limit of 10 threads. Use some Existing thread to continue...";
                document.getElementById('customAlert').style.display = 'block';
                
                setTimeout(() => {
                    document.getElementById('customAlert').style.display = 'none';
                }, 5000);

                sendBtn.disabled = false;
            }
            else{
                console.log("here...."+last_threadId);
                if (last_threadId === undefined) {
                    
                    HS1.innerHTML = '';
                    const button = document.createElement('button');

                    if (NoThreads) {
                        threads.textContent = '';
                        NoThreads = false;
                    }

                    const thread_loadingGif = document.createElement('img');
                    thread_loadingGif.setAttribute('src', '/static/loading.gif');
                    thread_loadingGif.setAttribute('alt', 'Loading...');
                    thread_loadingGif.style.height = "20px";
                    thread_loadingGif.style.width = "20px";

                    const thread_loadingText = document.createElement('span');
                    thread_loadingText.textContent = "Creating...";
                    thread_loadingText.style.marginLeft = "5px";

                    button.appendChild(thread_loadingGif);
                    button.appendChild(thread_loadingText);
                    threads.prepend(button);
                }
                addMessage('user', message);

                const messageDiv = document.createElement('div');
                messageDiv.className = 'assistant';
                const loadingGif = document.createElement('img');
                loadingGif.setAttribute('src', '/static/loading.gif');
                loadingGif.setAttribute('alt', 'Loading...');
                loadingGif.style.height = "20px";
                loadingGif.style.width = "20px";

                const loadingText = document.createElement('span');
                loadingText.textContent = "Reserching...";
                loadingText.style.marginLeft = "5px";

                messageDiv.appendChild(loadingGif);
                messageDiv.appendChild(loadingText);
                HS1.appendChild(messageDiv);
                if (last_threadId === undefined) {
                    threadCount++;
                    createThread().then(newThread => {
                        console.log(newThread);
                        lastThread = newThread;

                        scrollToBottom();
                        addNewThread(newThread);
                        fetch('/visagpt/chat', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ message, threadId: last_threadId })
                        })
                        .then(response => response.json())
                        .then(data => {
                            addCurrentMessage('assistant', data.response, data.threadId);
                            sendBtn.disabled = false;
                        })
                        .catch(error => {
                            console.error('Error:', error);
                            sendBtn.disabled = false;
                        });
                        userInput.value = '';
                    });
                }
                else{
                    scrollToBottom();
                    fetch('/visagpt/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message, threadId: last_threadId })
                    })
                    .then(response => response.json())
                    .then(data => {
                        addCurrentMessage('assistant', data.response, data.threadId);
                        sendBtn.disabled = false;
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        sendBtn.disabled = false;
                    });
                    userInput.value = '';
                }
            }  
        }
    });

    function addNewThread(newThread) {
        if (newThread !== undefined) {
            
            const button = document.createElement('button');
            const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");

            svg.setAttribute('viewBox', '0 0 24 24');
            svg.setAttribute('fill', 'currentColor');
            svg.setAttribute('class', 'w-6 h-6');

            const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
            path.setAttribute('fill-rule', 'evenodd');
            path.setAttribute('d', "M9 4.5a.75.75 0 0 1 .721.544l.813 2.846a3.75 3.75 0 0 0 2.576 2.576l2.846.813a.75.75 0 0 1 0 1.442l-2.846.813a3.75 3.75 0 0 0-2.576 2.576l-.813 2.846a.75.75 0 0 1-1.442 0l-.813-2.846a3.75 3.75 0 0 0-2.576-2.576l-2.846-.813a.75.75 0 0 1 0-1.442l2.846-.813A3.75 3.75 0 0 0 7.466 7.89l.813-2.846A.75.75 0 0 1 9 4.5ZM18 1.5a.75.75 0 0 1 .728.568l.258 1.036c.236.94.97 1.674 1.91 1.91l1.036.258a.75.75 0 0 1 0 1.456l-1.036.258c-.94.236-1.674.97-1.91 1.91l-.258 1.036a.75.75 0 0 1-1.456 0l-.258-1.036a2.625 2.625 0 0 0-1.91-1.91l-1.036-.258a.75.75 0 0 1 0-1.456l1.036-.258a2.625 2.625 0 0 0 1.91-1.91l.258-1.036A.75.75 0 0 1 18 1.5ZM16.5 15a.75.75 0 0 1 .712.513l.394 1.183c.15.447.5.799.948.948l1.183.395a.75.75 0 0 1 0 1.422l-1.183.395c-.447.15-.799.5-.948.948l-.395 1.183a.75.75 0 0 1-1.422 0l-.395-1.183a1.5 1.5 0 0 0-.948-.948l-1.183-.395a.75.75 0 0 1 0-1.422l1.183-.395c.447-.15.799-.5.948-.948l.395-1.183A.75.75 0 0 1 16.5 15Z")
            path.setAttribute('clip-rule', 'evenodd');
            svg.appendChild(path);

            button.appendChild(svg);

            let parts = newThread.split('_');
            let lastFourValues = parts[parts.length - 1].slice(-4);
            console.log(lastFourValues);
            button.appendChild(document.createTextNode("thread_"+lastFourValues));

            button.addEventListener('click', () => loadThread(newThread));
            if (threads.lastChild) {
                threads.replaceChild(button, threads.firstChild);
            } else {
                threads.appendChild(li);
            }
        }
    }

    newchat.addEventListener('click', () => {
        console.log(threadCount);
        if (threadCount < maxthreadCount) {
            HS1.innerHTML = '';
            last_threadId = undefined;
            const newchatDiv = document.createElement('div');
            newchatDiv.className = 'recommended_q';

            const h2Element = document.createElement('h2');
            h2Element.textContent = "Type Something to start a new conversation...";
            newchatDiv.appendChild(h2Element);
            HS1.appendChild(newchatDiv);
            
        }
        else{
            document.getElementById('alertMessage').textContent = "You have reached the maximum limit of 10 threads. Use some Existing thread to continue...";
            document.getElementById('customAlert').style.display = 'block';
            
            setTimeout(() => {
                document.getElementById('customAlert').style.display = 'none';
            }, 5000);
        }
        // const button = document.createElement('button');

        // const loadingGif = document.createElement('img');
        // loadingGif.setAttribute('src', '/static/loading.gif');
        // loadingGif.setAttribute('alt', 'Loading...');
        // loadingGif.style.height = "20px";
        // loadingGif.style.width = "20px";

        // const loadingText = document.createElement('span');
        // loadingText.textContent = "Creating...";
        // loadingText.style.marginLeft = "5px";

        // button.appendChild(loadingGif);
        // button.appendChild(loadingText);
        // threads.prepend(button);
        // createThread().then(newThread => {
        //     console.log(newThread);
        //     lastThread = newThread;
        //     addNewThread(newThread);
        // });
    });

    async function createThread() {
        const response = await fetch(`/add_thread`);
        const data = await response.json();
        lastThread = data;
        last_threadId = lastThread.id;
        return lastThread.id;
    }


    const profile = document.getElementById('profile');
    const profile_menu = document.querySelector('.profile_menu');

    profile.addEventListener('click',function(){
        if(profile_menu.style.right === "-160px"){
            profile_menu.style.right = "30px";
        }
        else {
            profile_menu.style.right = "-160px";
        }
    });

    profile.addEventListener('mouseover',function(){
        if(profile_menu.style.right === "-160px"){
            profile_menu.style.right = "30px";
        }
        else {
            profile_menu.style.right = "-160px";
        }
    });


    const profile_btn = document.getElementById('profile_btn');
    profile_btn.addEventListener('click',function(){
        window.location.href = "/profile";
    })


    const Upgrade_btn = document.getElementById('Upgrade_btn');
    const upgrade_menu = document.getElementById('upgrade_monthly');
    const close_btn = document.getElementById('upgrade_close_btn');
    const body = document.querySelector('body');

    Upgrade_btn.addEventListener('click',function(){
        upgrade_menu.style.display = "block";
        body.style.backgroundColor = "";
    });

    close_btn.addEventListener('click',function(){
        upgrade_menu.style.display = "none";
    });


    const plan_btns = document.querySelectorAll('.plan_btn');
    const Monthly_plan = document.getElementById('Monthly_plan');
    const Yearly_plan = document.getElementById('Yearly_plan'); 
    const monthly_info = document.getElementById('priceInfo');
    const price_tag = document.getElementById('price_tag');
    const time_p = document.getElementById('time_p');
    const elements = document.querySelectorAll('.upgrade_main > .plans> button');


    plan_btns.forEach(function(plan_btn) { 
        plan_btn.addEventListener('click', function() { 
        elements.style.Color = "#F65434";   
        });
    });

    Monthly_plan.addEventListener('click',function(){
        price_tag.textContent = "5";
        time_p.textContent = "per month";
    });

    Yearly_plan.addEventListener('click',function(){
        price_tag.textContent = "60";
        time_p.textContent = "annually, billed $5 per month";
    });


    const Search_btn = document.getElementById('searchButton');
    const parentmain = document.getElementById('main_screen');
    console.log(Search_btn, parentmain);   
};