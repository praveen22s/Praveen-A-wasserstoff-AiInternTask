const ControlPanel = ({ onClear, onRestart, showRestart }) => (
    <div>
      <button onClick={onClear}>Clear Cache</button>
      {showRestart && <button onClick={onRestart}>Restart Game</button>}
    </div>
  );
  
  export default ControlPanel;
  