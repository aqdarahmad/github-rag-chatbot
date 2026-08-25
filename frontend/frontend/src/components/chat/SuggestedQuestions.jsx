const questions = [
  "What is a path parameter in FastAPI?",
  "What is the difference between path and query parameters?",
  "How does FastAPI validate request body data?",
  "How do I create a POST endpoint in FastAPI?",
];

function SuggestedQuestions({ onSelect }) {

  return (
    <div className="suggested-questions">

      {questions.map((question) => (

        <button
          key={question}
          className="suggestion-card"
          onClick={() => onSelect(question)}
        >

          <span>{question}</span>

          <span className="suggestion-arrow">
            →
          </span>

        </button>

      ))}

    </div>
  );
}

export default SuggestedQuestions;