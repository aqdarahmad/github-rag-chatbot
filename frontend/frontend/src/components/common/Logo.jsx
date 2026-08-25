import { Link } from "react-router-dom";

function Logo() {

  return (
    <Link to="/" className="logo">

      <div className="logo-mark">
        F
      </div>

      <div className="logo-text">

        <strong>FastAPI Docs</strong>

        <span>RAG Assistant</span>

      </div>

    </Link>
  );
}

export default Logo;