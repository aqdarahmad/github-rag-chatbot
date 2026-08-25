import { useState } from "react";

function ChatInput({
  onSend,
  loading,
}) {

  const [value, setValue] = useState("");


  const handleSubmit = () => {

    const question = value.trim();

    if (!question || loading) {
      return;
    }

    onSend(question);

    setValue("");
  };


  const handleKeyDown = (event) => {

    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {

      event.preventDefault();

      handleSubmit();

    }
  };


  return (
    <div className="chat-input-wrapper">

      <div className="chat-input-container">

        <textarea
          value={value}
          onChange={(event) =>
            setValue(event.target.value)
          }
          onKeyDown={handleKeyDown}
          placeholder="Ask about FastAPI..."
          disabled={loading}
          rows={1}
        />

        <button
          className="send-button"
          onClick={handleSubmit}
          disabled={!value.trim() || loading}
          aria-label="Send message"
        >

          <svg
            width="17"
            height="17"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <line
              x1="22"
              y1="2"
              x2="11"
              y2="13"
            />

            <polygon
              points="22 2 15 22 11 13 2 9 22 2"
            />

          </svg>

        </button>

      </div>

      <p className="input-hint">
        Press Enter to send
      </p>

    </div>
  );
}

export default ChatInput;