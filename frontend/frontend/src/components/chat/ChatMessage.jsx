import ReactMarkdown from "react-markdown";

function ChatMessage({ message }) {

  const isUser = message.role === "user";

  return (
    <div
      className={`message-row ${
        isUser ? "message-user" : "message-assistant"
      }`}
    >

      {!isUser && (
        <div className="message-avatar">
          F
        </div>
      )}

      <div className="message-content">

        {isUser ? (
          <p>{message.content}</p>
        ) : (
          <ReactMarkdown>
            {message.content}
          </ReactMarkdown>
        )}

      </div>

    </div>
  );
}

export default ChatMessage;