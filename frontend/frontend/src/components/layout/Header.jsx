import { Link, useLocation } from "react-router-dom";

import Logo from "../common/Logo";

function Header() {

  const location = useLocation();

  return (
    <header className="header">

      <div className="header-container">

        <Logo />

        <nav className="navigation">

          <Link
            to="/"
            className={
              location.pathname === "/"
                ? "nav-link active"
                : "nav-link"
            }
          >
            Home
          </Link>

          <Link
            to="/chat"
            className={
              location.pathname === "/chat"
                ? "nav-link active"
                : "nav-link"
            }
          >
            Chat
          </Link>

        </nav>

        <div className="header-status">

          <span className="status-dot"></span>

          <span>Online</span>

        </div>

      </div>

    </header>
  );
}

export default Header;