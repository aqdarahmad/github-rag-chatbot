import { Link } from "react-router-dom";

function NotFound() {

  return (
    <section className="not-found">

      <span className="not-found-code">
        404
      </span>

      <h1>
        Page not found
      </h1>

      <p>
        The page you're looking for doesn't exist.
      </p>

      <Link
        to="/"
        className="hero-button"
      >
        Back to home
      </Link>

    </section>
  );
}

export default NotFound;