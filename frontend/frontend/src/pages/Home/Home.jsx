import { useNavigate } from "react-router-dom";

import SuggestedQuestions from "../../components/chat/SuggestedQuestions";

function Home() {

  const navigate = useNavigate();


  const openChat = (question = "") => {

    navigate("/chat", {
      state: {
        question,
      },
    });

  };


  return (
    <section className="home-page">

      <div className="home-hero">

        <div className="hero-icon">
          F
        </div>

        <span className="eyebrow">
          FASTAPI DOCUMENTATION
        </span>

        <h1>
          Understand FastAPI
          <br />
          without digging through docs.
        </h1>

        <p>
          Ask questions about FastAPI and get
          documentation-based answers using
          Retrieval-Augmented Generation.
        </p>

        <button
          className="hero-button"
          onClick={() => openChat()}
        >
          Start asking
          <span>→</span>
        </button>

      </div>


      <div className="home-section">

        <div className="section-heading">

          <span>
            TRY A QUESTION
          </span>

          <p>
            Explore what the assistant can answer.
          </p>

        </div>

        <SuggestedQuestions
          onSelect={openChat}
        />

      </div>

    </section>
  );
}

export default Home;