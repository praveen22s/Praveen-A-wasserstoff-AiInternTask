import React from "react";

function GameHeader({ seed, score, globalGuesses }) {
  return (
    <div className="game-header">
      <h1>What Beats It?</h1>
      <div className="stats-container">
        <div className="stat-box score">
          <span className="stat-label">Score:</span>
          <span className="stat-value">{score}</span>
        </div>
        <div className="stat-box current-seed">
          <span className="stat-label">Current Seed:</span>
          <span className="stat-value">{seed}</span>
        </div>
        <div className="stat-box global-guesses">
          <span className="stat-label">Global Guesses:</span>
          <span className="stat-value">{globalGuesses}</span>
        </div>
      </div>
    </div>
  );
}

export default GameHeader;