const GuessHistory = ({ guesses }) => (
    <div>
      <h3>Guesses So Far:</h3>
      <ul>
        {guesses.map((g, index) => (
          <li key={index}>{g}</li>
        ))}
      </ul>
    </div>
  );
  
  export default GuessHistory;
  