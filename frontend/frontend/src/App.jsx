import { Routes, Route } from "react-router-dom";

import Header from "./components/layout/Header";
import Footer from "./components/layout/Footer";

import Home from "./pages/Home/Home";
import Chat from "./pages/Chat/Chat";
import NotFound from "./pages/NotFound/NotFound";

function App() {
  return (
    <div className="app">

      <Header />

      <main className="main-content">
        <Routes>

          <Route path="/" element={<Home />} />

          <Route path="/chat" element={<Chat />} />

          <Route path="*" element={<NotFound />} />

        </Routes>
      </main>

      <Footer />

    </div>
  );
}

export default App;