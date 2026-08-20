async function sendQuestion() {

    const input = document.getElementById("question");
    const chatBox = document.getElementById("chat-box");

    const question = input.value.trim();

    if (!question) {
        return;
    }

    // ==============================
    // Display user message
    // ==============================

    const userMessage = document.createElement("div");

    userMessage.className = "message user";

    userMessage.textContent = question;

    chatBox.appendChild(userMessage);

    // Clear input
    input.value = "";

    // ==============================
    // Display loading message
    // ==============================

    const botMessage = document.createElement("div");

    botMessage.className = "message bot";

    botMessage.textContent = "Thinking...";

    chatBox.appendChild(botMessage);

    // Scroll to bottom
    chatBox.scrollTop = chatBox.scrollHeight;

    try {

        // ==============================
        // Send request to FastAPI
        // ==============================

        const response = await fetch(
            "http://127.0.0.1:8000/ask",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    question: question
                })
            }
        );

        // ==============================
        // Convert response to JSON
        // ==============================

        const data = await response.json();

        // ==============================
        // Display answer
        // ==============================

        botMessage.textContent = data.answer;

    } catch (error) {

        console.error(error);

        botMessage.textContent =
            "Error: Could not connect to the backend.";

    }

    // Scroll to bottom
    chatBox.scrollTop = chatBox.scrollHeight;
}