import { useState, useEffect } from "react";
import "./styles.css";
import GameHeader from "./components/GameHeader";
import GuessInput from "./components/GuessInput";
import VerdictDisplay from "./components/VerdictDisplay";
import GuessHistory from "./components/GuessHistory";
import ControlPanel from "./components/ControlPanel";
import confetti from "canvas-confetti";

function App() {
  const [seed, setSeed] = useState("Rock");
  const [guess, setGuess] = useState("");
  const [guesses, setGuesses] = useState([]);
  const [message, setMessage] = useState("");
  const [explanation, setExplanation] = useState("");
  const [gameOver, setGameOver] = useState(false);
  const [score, setScore] = useState(0);
  const [globalGuesses, setGlobalGuesses] = useState(0);
  const API_BASE_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";
  // Clear cache when page loads
  useEffect(() => {
    const clearCacheOnLoad = async () => {
      try {
        await fetch(`${API_BASE_URL}/game/clear-cache`);
        console.log("Cache cleared on load");
      } catch (error) {
        console.error("Failed to clear cache on load:", error);
      }
    };
    clearCacheOnLoad();
  }, []);

  const triggerConfetti = () => {
    confetti({
      particleCount: 100,
      spread: 70,
      origin: { y: 0.6 }
    });
  };

  const handleGuess = async () => {
    if (!guess.trim()) {
      setMessage("Please enter a guess!");
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/game/guess`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ guess, persona: "cheery" }),
      });

      if (!response.ok) {
        const err = await response.json();
        setMessage(typeof err.detail === "object" ? err.detail.message : err.detail);
        setExplanation(typeof err.detail === "object" ? err.detail.explanation : "");
        setGameOver(true);
        return;
      }

      const data = await response.json();
      setSeed(data.seed);
      setGuesses(data.guesses_so_far);
      setMessage(data.result);
      setExplanation(data.explanation);
      setGuess("");
      setGlobalGuesses(data.global_guesses || 0);
      
      // Increment score on successful guess
      setScore(prevScore => prevScore + 1);
      
      // Trigger confetti for successful guess
      triggerConfetti();

    } catch (error) {
      console.error(error);
      setMessage("Something went wrong!");
      setExplanation("");
    }
  };

  const handleClearCache = async () => {
    try {
      await fetch(`${API_BASE_URL}/game/clear-cache`);
      setMessage("Cache cleared!");
      setExplanation("");
    } catch (error) {
      console.error(error);
      setMessage("Failed to clear cache.");
      setExplanation("");
    }
  };

  const handleRestart = () => {
    setSeed("Rock");
    setGuesses([]);
    setMessage("");
    setExplanation("");
    setGuess("");
    setGameOver(false);
    // Reset score on game restart
    setScore(0);
  };

  return (
    <div className="container">
      <GameHeader seed={seed} score={score} globalGuesses={globalGuesses} />
      <GuessInput 
        guess={guess} 
        onChange={setGuess} 
        onSubmit={handleGuess} 
        showRestart={gameOver} 
      />
      <VerdictDisplay 
        message={message} 
        explanation={explanation} 
        success={!gameOver && message && !message.includes("wrong")} 
      />
      <GuessHistory guesses={guesses} />
      <ControlPanel 
        onClear={handleClearCache} 
        onRestart={handleRestart} 
        showRestart={gameOver} 
        score={score}
      />
    </div>
  );
}

export default App;