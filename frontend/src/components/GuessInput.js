const GuessInput = ({ guess, onChange, onSubmit ,showRestart}) => (
    <div>
      <input
        type="text"
        placeholder="Your guess..."
        value={guess}
        onChange={(e) => onChange(e.target.value)}
      />
      {!showRestart && <button onClick={onSubmit}>Submit Guess</button>}
    </div>
  );
  
  export default GuessInput;
  