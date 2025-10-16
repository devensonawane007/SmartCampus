const sendBtn = document.getElementById("send-btn");
const userMsgInput = document.getElementById("user-message");
const chatbox = document.getElementById("chatbox");

async function sendMessage() {
    const msg = userMsgInput.value.trim();
    if (!msg) return;

    // Display user message
    chatbox.innerHTML += `<div><b>You:</b> ${msg}</div>`;
    userMsgInput.value = "";

    try {
        const response = await fetch("/chatbot_reply", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: msg })
        });

        const data = await response.json();
        const reply = data.reply;

        // Display AI response
        chatbox.innerHTML += `<div><b>AI:</b> ${reply}</div>`;
        chatbox.scrollTop = chatbox.scrollHeight;
    } catch (error) {
        console.error("Error:", error);
        chatbox.innerHTML += `<div><b>AI:</b> Sorry, something went wrong!</div>`;
        chatbox.scrollTop = chatbox.scrollHeight;
    }
}

// Button click
sendBtn.addEventListener("click", sendMessage);

// Optional: send message on Enter key
userMsgInput.addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
        sendMessage();
        e.preventDefault();
    }
});
