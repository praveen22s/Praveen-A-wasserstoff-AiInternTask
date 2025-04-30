import React, { useEffect, useState } from "react";

function VerdictDisplay({ message, explanation, success }) {
  const [animate, setAnimate] = useState(false);

  useEffect(() => {
    if (message) {
      setAnimate(true);
      const timer = setTimeout(() => setAnimate(false), 500);
      return () => clearTimeout(timer);
    }
  }, [message]);

  if (!message) return null;

  return (
    <div className={`verdict-display ${success ? 'success' : 'error'} ${animate ? (success ? 'pulse' : 'shake') : ''}`}>
      <h3>{success ? '🎉 ' : '❌ '}{message}</h3>
      {explanation && <p>{explanation}</p>}
      {success && (
        <div className="emoji-feedback">
          ✨ 🎮 🏆
        </div>
      )}
      {!success && (
        <div className="emoji-feedback">
          😔 🎮 ⏱️
        </div>
      )}
    </div>
  );
}

export default VerdictDisplay;