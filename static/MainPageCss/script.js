const chatInput = document.querySelector("#chat-input");
const sendButton = document.querySelector("#send-btn");
const chatContainer = document.querySelector(".chat-container");
const themeButton = document.querySelector("#theme-btn-menu");
const deleteButton = document.querySelector("#delete-btn-menu");
const recordButton = document.getElementById('rec-btn');
const recSound = document.getElementById('recClickSound')
var uidElement = document.getElementById('uid-data');
var uid = uidElement.dataset.uid;

//load chat History function in backend

const loadDataFromBackend = async (userId) => {
    try {
        const getCookie = (name) => {
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${name}=`);
            if (parts.length === 2) return parts.pop().split(';').shift();
        }
        const csrftoken = getCookie('csrftoken'); 
        const response = await fetch('/get_chat_history/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken 
            },
            body: JSON.stringify({uid:userId })
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error('Failed to fetch chat history');
        }
        console.log(data.message)
        let storedChats = '';
        if (data.chatHistory && data.chatHistory.length > 0) {
            data.chatHistory.forEach(chat => {
                storedChats += `<div class="chat outgoing">
                                    <div class="chat-content">
                                        <div class="chat-details">  
                                            <ion-icon name="contact" style="font-size:250%" role="img" class="md hydrated" aria-label="contact"></ion-icon>
                                            <p>${chat.input}</p>
                                        </div>
                                    </div>
                                </div>
                                <div class="chat incoming">
                                    <div class="chat-content">
                                        <div class="chat-details">
                                            <ion-icon name="code-working" style="font-size:250%" role="img" class="md hydrated" aria-label="code working"></ion-icon>
                                            <p>${chat.reply}</p>
                                        </div>
                                        <span onclick="copyResponse(this)" class="material-symbols-rounded">content_copy</span>
                                    </div>
                                </div>`;
            });
        } else {
            storedChats = `<div class="default-text">
                                <h1>ChatBotX</h1>
                                <p>Start a conversation <br> Your chat history will be displayed here.</p>
                            </div>`;
        }
        chatContainer.innerHTML = storedChats;
        chatContainer.scrollTo(0, chatContainer.scrollHeight);
    } catch (error) {
        console.log('Error loading chat history:', error);
        chatContainer.innerHTML = `<div class="default-text">
                                        <h1>ChatBotX</h1>
                                        <p>Error loading chat history. Please try again later.</p>
                                    </div>`;
    }
};



// save the chat history to backend function
const saveChatToBackend = async (userId,user_input,reply_message) => {
    try {
        const getCookie = (name) => {
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${name}=`);
            if (parts.length === 2) return parts.pop().split(';').shift();
        }
        const csrftoken = getCookie('csrftoken'); 
        const response = await fetch('/save_chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken 
            },
            body: JSON.stringify({uid:userId , input:user_input, reply:reply_message  })
        });
        const data = await response.json();
        if (!response.ok) {
            console.error('Failed to save chat:', data.error);
        }
    } catch (error) {
        console.error('Error saving chat:', error);
    }
};

//delate the chat history to backend function 
const deleteChatToBackend = async (userId) => {
    try {
        const getCookie = (name) => {
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${name}=`);
            if (parts.length === 2) return parts.pop().split(';').shift();
        }
        const csrftoken = getCookie('csrftoken');
        const response = await fetch('/delete_chat_history/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken 
            },
            body: JSON.stringify({ uid: userId })
        });
        const data = await response.json();
        if (response.ok) {
            console.log(data.message); 
        } else {
            console.error('Failed to delete chat history:', data.error);
        }
    } catch (error) {
        console.error('Error deleting chat history:', error);
    }
};

    // Load saved chats and theme from local storage and apply/add on the page
const loadDataFromLocalstorage = () => {
    const themeColor = localStorage.getItem("themeColor");

    document.body.classList.toggle("light-mode", themeColor === "light_mode");
    themeButton.innerText = document.body.classList.contains("light-mode") ? "dark_mode" : "light_mode";
}

//Creating new chat element function

const createChatElement = (content, className) => {
    const chatDiv = document.createElement("div");
    chatDiv.classList.add("chat", className);

    chatDiv.innerHTML = content;
    return chatDiv; // Return the created chat div
}

//Getting the Chat Response from Open AI By Posting UserInput and get the responce Function
  const generateReplyFromDjango = async (userText) => {
    try {
        const getCookie = (name) => {
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${name}=`);
            if (parts.length === 2) return parts.pop().split(';').shift();
        }
        const csrftoken = getCookie('csrftoken'); 
        const response = await fetch('/generate_reply/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken 
            },
            body: JSON.stringify({ 'user_input': userText })
        });
        const data = await response.json();
        if (response.ok) {
            return data.reply;
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        throw new Error('Error sending user input to Django:', error);
    }
};


//Passing the userInput and Fetch the responce to frontend Function

const getChatResponse = async (incomingChatDiv,outgoingChatDiv) => {
    const pElement = document.createElement("p");

    try {
        
        const chatDetailsP = outgoingChatDiv.querySelector(".chat-details p");
        if (!chatDetailsP) {
           console.log("Could not find '.chat-details p' element.");
        }
        const userMessage = chatDetailsP.textContent;
        const reply = await generateReplyFromDjango(userMessage);
        pElement.textContent = reply;
        saveChatToBackend(uid,userMessage,reply);
    } catch (error) {
        pElement.classList.add("error");
        pElement.textContent = "Oops! Something went wrong while retrieving the response. Please try again.";
        console.error(error);
    }

    incomingChatDiv.querySelector(".typing-animation").remove();
    incomingChatDiv.querySelector(".chat-details").appendChild(pElement);
    chatContainer.scrollTo(0, chatContainer.scrollHeight);
};

//copy the content to clipboard Function

const copyResponse = (copyBtn) => {
    // Copy the text content of the response to the clipboard
    const reponseTextElement = copyBtn.parentElement.querySelector("p");
    navigator.clipboard.writeText(reponseTextElement.textContent);
    copyBtn.textContent = "done";
    setTimeout(() => copyBtn.textContent = "content_copy", 1000);
}

//show the typing animation in frontent

const showTypingAnimation = (outgoingChatDiv) => {
    // Display the typing animation and call the getChatResponse function
    const html = `<div class="chat-content">
                    <div class="chat-details">
                    <ion-icon name="code-working" style="font-size:250%"></ion-icon>
                        <div class="typing-animation">
                            <div class="typing-dot" style="--delay: 0.2s"></div>
                            <div class="typing-dot" style="--delay: 0.3s"></div>
                            <div class="typing-dot" style="--delay: 0.4s"></div>
                        </div>
                    </div>
                    <span onclick="copyResponse(this)" class="material-symbols-rounded">content_copy</span>
                </div>`;
    // Create an incoming chat div with typing animation and append it to chat container
    const incomingChatDiv = createChatElement(html, "incoming");
    chatContainer.appendChild(incomingChatDiv);
    chatContainer.scrollTo(0, chatContainer.scrollHeight);
    getChatResponse(incomingChatDiv,outgoingChatDiv);
}
//first funtion to execue all the functions 

const handleOutgoingChat = () => {
    userText = chatInput.value.trim();
    if(!userText) return; // If chatInput is empty return from here
    // Clear the input field and reset its height
    chatInput.value = "";
    chatInput.style.height = `${initialInputHeight}px`;

    const html = `<div class="chat-content">
                    <div class="chat-details">  
                    <ion-icon name="contact" style="font-size:250%"></ion-icon>
                        <p>${userText}</p>
                    </div>
                </div>`;

    // Create an outgoing chat div with user's message and append it to chat container
    const outgoingChatDiv = createChatElement(html, "outgoing");
    chatContainer.querySelector(".default-text")?.remove();
    chatContainer.appendChild(outgoingChatDiv);
    chatContainer.scrollTo(0, chatContainer.scrollHeight);
    setTimeout(() => showTypingAnimation(outgoingChatDiv), 500);
}

//delete  the chat history function 
deleteButton.addEventListener("click", async () => {
    // Remove the chats from local storage and call loadDataFromBackend function
    if (confirm("Are you sure you want to delete all the chats?")) {
        try {
            await deleteChatToBackend(uid);
            loadDataFromBackend(uid);
        } catch (error) {
            console.error('Error:', error);
        }
    }
});

//theme button function

themeButton.addEventListener("click", () => {
    // Toggle body's class for the theme mode and save the updated theme to the local storage 
    document.body.classList.toggle("light-mode");
    localStorage.setItem("themeColor", themeButton.innerText);
    themeButton.innerText = document.body.classList.contains("light-mode") ? "dark_mode" : "light_mode";
});

const initialInputHeight = chatInput.scrollHeight;

chatInput.addEventListener("input", () => {   
    // Adjust the height of the input field dynamically based on its content
    chatInput.style.height =  `${initialInputHeight}px`;
    chatInput.style.height = `${chatInput.scrollHeight}px`;
});

chatInput.addEventListener("keydown", (e) => {
    // If the Enter key is pressed without Shift and the window width is larger 
    // than 800 pixels, handle the outgoing chat
    if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
        e.preventDefault();
        handleOutgoingChat();
    }
});

loadDataFromBackend(uid);
sendButton.addEventListener("click", handleOutgoingChat);

//audio-text coversion
const convertVoiceToText = () => {
    const getCookie = (name) => {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }
    const csrftoken = getCookie('csrftoken'); 
    fetch('/convert_voice_to_text/', {
        method: 'POST',    
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken 
        }
    })
    .then(response => {
        if (!response.ok) {
            console.log('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
       
        if ('text' in data) {
            chatInput.value = data.text;
        } else if ('error' in data) {
            console.log('Error converting voice to a text:', data.error);
            // Handle error, e.g., display an error message to the user
        } else {
            console.log('Unexpected response:', data);
            // Handle unexpected response
        }
    })  
    .catch(error => {
        console.log('Error converting voice to text:', error);
        // Handle error if necessary
    });
};

//event listener for record button 

recordButton.addEventListener('click',function() {
    recSound.play();
    convertVoiceToText();

});