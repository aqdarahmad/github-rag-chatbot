import { useEffect, useRef } from "react";

import ChatMessage from "./ChatMessage";
import LoadingMessage from "./LoadingMessage";

function ChatWindow({
  messages,
  loading,
}) {

  const bottomRef = useRef(null);


  useEffect(() => {

    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });

  }, [messages, loading]);


  return (
    <div className="chat-window">

      {messages.map((message) => (

        <ChatMessage
          key={message.id}
          message={message}
        />

      ))}

      {loading && <LoadingMessage />}

      <div ref={bottomRef}></div>

    </div>
  );
}

export default ChatWindow;