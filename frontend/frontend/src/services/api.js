const API_URL =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export async function askQuestion(question) {

  const response = await fetch(`${API_URL}/ask`, {

    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      question,
    }),

  });

  if (!response.ok) {

    throw new Error(
      `Request failed with status ${response.status}`
    );

  }

  const data = await response.json();

  return data;
}