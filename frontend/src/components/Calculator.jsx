import { useState, useEffect } from 'react';
import calculatorService from '../services/calculatorService';
import './Calculator.css';

const Calculator = ({ onCalculate }) => {
  const [display, setDisplay] = useState('0');
  const [currentValue, setCurrentValue] = useState(null);
  const [operator, setOperator] = useState(null);
  const [waitingForOperand, setWaitingForOperand] = useState(false);
  const [chainOperations, setChainOperations] = useState([]);
  const [chainMode, setChainMode] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Limpiar display
  const clearDisplay = () => {
    setDisplay('0');
    setCurrentValue(null);
    setOperator(null);
    setWaitingForOperand(false);
    setChainOperations([]);
    setChainMode(false);
    setError('');
  };

  // Ingresar dígito
  const inputDigit = (digit) => {
    if (waitingForOperand) {
      setDisplay(String(digit));
      setWaitingForOperand(false);
    } else {
      setDisplay(display === '0' ? String(digit) : display + digit);
    }
    setError('');
  };

  // Ingresar punto decimal
  const inputDecimal = () => {
    if (waitingForOperand) {
      setDisplay('0.');
      setWaitingForOperand(false);
    } else if (display.indexOf('.') === -1) {
      setDisplay(display + '.');
    }
  };

  // Cambiar signo
  const toggleSign = () => {
    const newValue = parseFloat(display) * -1;
    setDisplay(String(newValue));
  };

  // Ingresar porcentaje
  const inputPercent = () => {
    const value = parseFloat(display);
    setDisplay(String(value / 100));
  };

  // Realizar operación
  const performOperation = async (nextOperator) => {
    const inputValue = parseFloat(display);

    if (currentValue === null) {
      setCurrentValue(inputValue);
    } else if (operator) {
      setLoading(true);
      try {
        let result;
        
        if (chainMode && chainOperations.length > 0) {
          // Agregar operación a la cadena
          const newOp = {
            operator: operator,
            num2: inputValue
          };
          
          const updatedChain = [...chainOperations, newOp];
          
          // Calcular toda la cadena
          const data = await calculatorService.calculateChain(updatedChain);
          result = data.result;
          
          setChainOperations(updatedChain);
        } else {
          // Operación simple
          const data = await calculatorService.calculate(currentValue, inputValue, operator);
          result = data.result;
          
          if (chainMode) {
            // Iniciar cadena
            setChainOperations([{
              num1: currentValue,
              operator: operator,
              num2: inputValue
            }]);
          }
        }

        setCurrentValue(result);
        setDisplay(String(result));
        onCalculate();
      } catch (err) {
        setError(err.message);
        setDisplay('Error');
        setCurrentValue(null);
        setChainOperations([]);
      } finally {
        setLoading(false);
      }
    }

    setWaitingForOperand(true);
    setOperator(nextOperator);
  };

  // Calcular resultado (=)
  const calculateResult = async () => {
    const inputValue = parseFloat(display);

    if (operator && currentValue !== null) {
      setLoading(true);
      try {
        let result;
        
        if (chainMode && chainOperations.length > 0) {
          // Completar cadena
          const finalChain = [...chainOperations, {
            operator: operator,
            num2: inputValue
          }];
          
          const data = await calculatorService.calculateChain(finalChain);
          result = data.result;
        } else {
          // Operación simple
          const data = await calculatorService.calculate(currentValue, inputValue, operator);
          result = data.result;
        }

        setDisplay(String(result));
        setCurrentValue(null);
        setOperator(null);
        setWaitingForOperand(true);
        setChainOperations([]);
        onCalculate();
      } catch (err) {
        setError(err.message);
        setDisplay('Error');
        setCurrentValue(null);
        setChainOperations([]);
      } finally {
        setLoading(false);
      }
    }
  };

  // Toggle modo cadena
  const toggleChainMode = () => {
    setChainMode(!chainMode);
    clearDisplay();
  };

  return (
    <div className="calculator">
      <div className="calculator-display">
        <div className="display-mode">
          {chainMode && <span className="chain-badge">⛓️ Modo Cadena</span>}
          {chainOperations.length > 0 && (
            <span className="chain-count">Operaciones: {chainOperations.length}</span>
          )}
        </div>
        <div className="display-value">
          {loading ? 'Calculando...' : display}
        </div>
        {error && <div className="display-error">{error}</div>}
      </div>

      <div className="calculator-keypad">
        <div className="calculator-row">
          <button className="key key-function" onClick={clearDisplay}>AC</button>
          <button className="key key-function" onClick={toggleSign}>±</button>
          <button className="key key-function" onClick={inputPercent}>%</button>
          <button className="key key-operator" onClick={() => performOperation('/')}>÷</button>
        </div>

        <div className="calculator-row">
          <button className="key" onClick={() => inputDigit(7)}>7</button>
          <button className="key" onClick={() => inputDigit(8)}>8</button>
          <button className="key" onClick={() => inputDigit(9)}>9</button>
          <button className="key key-operator" onClick={() => performOperation('*')}>×</button>
        </div>

        <div className="calculator-row">
          <button className="key" onClick={() => inputDigit(4)}>4</button>
          <button className="key" onClick={() => inputDigit(5)}>5</button>
          <button className="key" onClick={() => inputDigit(6)}>6</button>
          <button className="key key-operator" onClick={() => performOperation('-')}>−</button>
        </div>

        <div className="calculator-row">
          <button className="key" onClick={() => inputDigit(1)}>1</button>
          <button className="key" onClick={() => inputDigit(2)}>2</button>
          <button className="key" onClick={() => inputDigit(3)}>3</button>
          <button className="key key-operator" onClick={() => performOperation('+')}>+</button>
        </div>

        <div className="calculator-row">
          <button className="key key-zero" onClick={() => inputDigit(0)}>0</button>
          <button className="key" onClick={inputDecimal}>.</button>
          <button className="key key-equals" onClick={calculateResult}>=</button>
        </div>

        <div className="calculator-row">
          <button 
            className={`key key-chain ${chainMode ? 'active' : ''}`} 
            onClick={toggleChainMode}
          >
            {chainMode ? '⛓️ Desactivar Cadena' : '⛓️ Activar Cadena'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Calculator;
