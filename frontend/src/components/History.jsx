import { useState, useEffect } from 'react';
import calculatorService from '../services/calculatorService';
import './History.css';

const History = ({ onClear }) => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      setLoading(true);
      const data = await calculatorService.getHistory();
      setHistory(data.history);
      setError('');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleClearHistory = async () => {
    if (window.confirm('¿Estás seguro de que quieres limpiar el historial?')) {
      try {
        await calculatorService.clearHistory();
        setHistory([]);
        onClear();
      } catch (err) {
        setError(err.message);
      }
    }
  };

  const formatOperation = (item) => {
    const operatorSymbols = {
      '+': '+',
      '-': '−',
      '*': '×',
      '/': '÷'
    };
    return `${item.num1} ${operatorSymbols[item.operator] || item.operator} ${item.num2} = ${item.result}`;
  };

  if (loading) {
    return (
      <div className="history">
        <div className="history-header">
          <h2>📋 Historial</h2>
        </div>
        <div className="history-loading">Cargando historial...</div>
      </div>
    );
  }

  return (
    <div className="history">
      <div className="history-header">
        <h2>📋 Historial de Operaciones</h2>
        {history.length > 0 && (
          <button className="clear-history-btn" onClick={handleClearHistory}>
            🗑️ Limpiar
          </button>
        )}
      </div>

      {error && <div className="history-error">{error}</div>}

      {history.length === 0 ? (
        <div className="history-empty">
          <p>No hay operaciones en el historial</p>
          <p className="history-empty-subtitle">Realiza algunos cálculos para verlos aquí</p>
        </div>
      ) : (
        <div className="history-list">
          <div className="history-count">
            Total de operaciones: {history.length}
          </div>
          {history.slice().reverse().map((item, index) => (
            <div key={history.length - index} className="history-item">
              <span className="history-number">#{history.length - index}</span>
              <span className="history-operation">{formatOperation(item)}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default History;
