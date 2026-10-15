// In development the backend runs on port 8000.
// In production (Docker) the backend also serves the frontend,
// so requests go to the same origin.
const API_URL =
  import.meta.env.VITE_API_URL ??
  (import.meta.env.DEV ? "http://127.0.0.1:8000" : "");

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

    const error = new Error(
      `Request failed with status ${response.status}`
    );

    if (response.status === 429) {
      error.userMessage =
        "Too many questions in a short time. Please wait a minute and try again.";
    } else if (response.status === 422) {
      error.userMessage =
        "Your question is too long or invalid. Please shorten it and try again.";
    } else if (response.status >= 500) {
      error.userMessage =
        "The server could not generate an answer. Please try again.";
    }

    throw error;

  }

  const data = await response.json();

  return data;
}