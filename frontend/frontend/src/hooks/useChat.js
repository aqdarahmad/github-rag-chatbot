import { useState } from "react";

import { askQuestion } from "../services/api";

function useChat() {

  const [messages, setMessages] = useState([]);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState(null);


  const sendMessage = async (question) => {

    const value = question.trim();

    if (!value || loading) {
      return;
    }

    setError(null);

    setMessages((previous) => [
      ...previous,
      {
        id: crypto.randomUUID(),
        role: "user",
        content: value,
      },
    ]);

    setLoading(true);

    try {

      const data = await askQuestion(value);

      setMessages((previous) => [
        ...previous,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content:
            data.answer || "No answer was returned.",
        },
      ]);

    } catch (err) {

      console.error(err);

      setError(
        "Unable to connect to the backend."
      );

    } finally {

      setLoading(false);

    }
  };


  const clearChat = () => {

    setMessages([]);

    setError(null);

  };


  return {
    messages,
    loading,
    error,
    sendMessage,
    clearChat,
  };
}

export default useChat;