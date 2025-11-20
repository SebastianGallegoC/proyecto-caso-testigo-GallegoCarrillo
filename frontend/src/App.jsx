import { useState } from 'react';
import Calculator from './components/Calculator';
import History from './components/History';
import './App.css';

function App() {
  const [showHistory, setShowHistory] = useState(false);
  const [historyUpdate, setHistoryUpdate] = useState(0);

  const handleCalculation = () => {
    // Actualizar el componente de historial
    setHistoryUpdate(prev => prev + 1);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🧮 Calculadora Avanzada</h1>
        <p className="subtitle">React + FastAPI | Operaciones en Cadena</p>
      </header>

      <main className="app-main">
        <div className="calculator-section">
          <Calculator onCalculate={handleCalculation} />
        </div>

        <div className="history-section">
          <div className="history-toggle">
            <button 
              className="toggle-btn"
              onClick={() => setShowHistory(!showHistory)}
            >
              {showHistory ? '📊 Ocultar Historial' : '📋 Mostrar Historial'}
            </button>
          </div>
          
          {showHistory && (
            <History key={historyUpdate} onClear={() => setHistoryUpdate(prev => prev + 1)} />
          )}
        </div>
      </main>

      <footer className="app-footer">
        <p>Desarrollado con principios SOLID y patrones de diseño</p>
      </footer>
    </div>
  );
}

export default App;
