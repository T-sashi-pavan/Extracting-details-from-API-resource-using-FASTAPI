import { useState, useEffect } from 'react';
import './App.css';

function App() {
  // State management
  const [players, setPlayers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [fetchMessage, setFetchMessage] = useState(null);

  // Backend API URL
  const API_URL = 'http://localhost:8000';

  /**
   * Fetch players from database
   */
  const loadPlayers = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_URL}/players`);
      if (!response.ok) {
        throw new Error('Failed to fetch players from database');
      }
      const data = await response.json();
      setPlayers(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Fetch players from external API and store in database
   */
  const fetchFromAPI = async () => {
    setLoading(true);
    setError(null);
    setFetchMessage(null);
    try {
      const response = await fetch(`${API_URL}/fetch-players`);
      if (!response.ok) {
        throw new Error('Failed to fetch from external API');
      }
      const data = await response.json();
      setFetchMessage(data.message);
      // Reload players after fetching
      await loadPlayers();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Load players on component mount
   */
  useEffect(() => {
    loadPlayers();
  }, []);

  return (
    <div className="App">
      {/* Header */}
      <header className="header">
        <h1>⚽ Sports Players Database</h1>
        <p>Powered by FastAPI + React</p>
      </header>

      {/* Action Buttons */}
      <div className="actions">
        <button 
          className="btn btn-primary" 
          onClick={fetchFromAPI}
          disabled={loading}
        >
          {loading ? 'Loading...' : 'Fetch Players from API'}
        </button>
        <button 
          className="btn btn-secondary" 
          onClick={loadPlayers}
          disabled={loading}
        >
          Refresh Players
        </button>
      </div>

      {/* Messages */}
      {fetchMessage && (
        <div className="message success">
          ✅ {fetchMessage}
        </div>
      )}

      {error && (
        <div className="message error">
          ❌ Error: {error}
        </div>
      )}

      {/* Loading State */}
      {loading && (
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading players...</p>
        </div>
      )}

      {/* Players Display */}
      {!loading && players.length === 0 && (
        <div className="empty-state">
          <p>No players found. Click "Fetch Players from API" to get started!</p>
        </div>
      )}

      {!loading && players.length > 0 && (
        <div className="players-container">
          <h2>Players List ({players.length})</h2>
          <div className="players-grid">
            {players.map((player) => (
              <div key={player.id} className="player-card">
                <div className="player-header">
                  <h3>{player.name}</h3>
                </div>
                <div className="player-info">
                  <div className="info-row">
                    <span className="label">Team:</span>
                    <span className="value">{player.team}</span>
                  </div>
                  <div className="info-row">
                    <span className="label">Nationality:</span>
                    <span className="value">{player.nationality || 'N/A'}</span>
                  </div>
                  <div className="info-row">
                    <span className="label">Position:</span>
                    <span className="value">{player.position || 'N/A'}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
