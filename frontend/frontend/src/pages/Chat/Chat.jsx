import { useEffect } from "react";
import { useLocation } from "react-router-dom";

import ChatWindow from "../../components/chat/ChatWindow";
import ChatInput from "../../components/chat/ChatInput";

import SuggestedQuestions from "../../components/chat/SuggestedQuestions";

import useChat from "../../hooks/useChat";

function Chat() {

  const location = useLocation();

  const {
    messages,
    loading,
    error,
    sendMessage,
    clearChat,
  } = useChat();


  useEffect(() => {

    const initialQuestion =
      location.state?.question;

    if (initialQuestion) {

      sendMessage(initialQuestion);

      window.history.replaceState(
        {},
        document.title
      );

    }

  }, []);


  return (
    <section className="chat-page">

      <div className="chat-header">

        <div>

          <span className="chat-eyebrow">
            FASTAPI DOCUMENTATION
          </span>

          <h1>
            Documentation Assistant
          </h1>

        </div>


        {messages.length > 0 && (

          <button
            className="clear-chat"
            onClick={clearChat}
          >
            Clear chat
          </button>

        )}

      </div>


      {messages.length === 0 ? (

        <div className="empty-chat">

          <div className="empty-icon">
            ?
          </div>

          <h2>
            What would you like to know?
          </h2>

          <p>
            Ask anything about FastAPI.
          </p>

          <SuggestedQuestions
            onSelect={sendMessage}
          />

        </div>

      ) : (

        <ChatWindow
          messages={messages}
          loading={loading}
        />

      )}


      {error && (

        <div className="error-banner">
          {error}
        </div>

      )}


      <ChatInput
        onSend={sendMessage}
        loading={loading}
      />

    </section>
  );
}

export default Chat;