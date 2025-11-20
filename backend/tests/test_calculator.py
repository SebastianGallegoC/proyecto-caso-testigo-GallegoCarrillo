"""
Tests unitarios para la calculadora.
Prueba operaciones simples, en cadena e historial.
"""
import pytest
from app.calculator import Calculator


class TestCalculatorBasicOperations:
    """Tests para operaciones básicas de la calculadora."""
    
    def setup_method(self):
        """Configuración antes de cada test."""
        self.calculator = Calculator()
    
    def test_calculate_addition(self):
        """Prueba cálculo de suma."""
        result = self.calculator.calculate(10, 5, "+")
        assert result == 15
    
    def test_calculate_subtraction(self):
        """Prueba cálculo de resta."""
        result = self.calculator.calculate(10, 5, "-")
        assert result == 5
    
    def test_calculate_multiplication(self):
        """Prueba cálculo de multiplicación."""
        result = self.calculator.calculate(10, 5, "*")
        assert result == 50
    
    def test_calculate_division(self):
        """Prueba cálculo de división."""
        result = self.calculator.calculate(10, 5, "/")
        assert result == 2
    
    def test_calculate_division_by_zero(self):
        """Prueba que división por cero lance error."""
        with pytest.raises(ValueError, match="No se puede dividir por cero"):
            self.calculator.calculate(10, 0, "/")
    
    def test_calculate_invalid_operator(self):
        """Prueba que operador inválido lance error."""
        with pytest.raises(ValueError, match="Operación no soportada"):
            self.calculator.calculate(10, 5, "%")


class TestCalculatorChainOperations:
    """Tests para operaciones en cadena."""
    
    def setup_method(self):
        """Configuración antes de cada test."""
        self.calculator = Calculator()
    
    def test_chain_two_operations(self):
        """Prueba cadena con dos operaciones: (10 + 5) * 2 = 30"""
        operations = [
            {"num1": 10, "operator": "+", "num2": 5},
            {"operator": "*", "num2": 2}
        ]
        result = self.calculator.calculate_chain(operations)
        assert result == 30
    
    def test_chain_three_operations(self):
        """Prueba cadena con tres operaciones: ((10 + 5) * 2) - 3 = 27"""
        operations = [
            {"num1": 10, "operator": "+", "num2": 5},
            {"operator": "*", "num2": 2},
            {"operator": "-", "num2": 3}
        ]
        result = self.calculator.calculate_chain(operations)
        assert result == 27
    
    def test_chain_four_operations(self):
        """Prueba cadena con cuatro operaciones: (((100 - 50) / 2) * 3) + 10 = 85"""
        operations = [
            {"num1": 100, "operator": "-", "num2": 50},
            {"operator": "/", "num2": 2},
            {"operator": "*", "num2": 3},
            {"operator": "+", "num2": 10}
        ]
        result = self.calculator.calculate_chain(operations)
        assert result == 85
    
    def test_chain_with_decimals(self):
        """Prueba cadena con decimales: (5.5 + 2.5) * 2 = 16"""
        operations = [
            {"num1": 5.5, "operator": "+", "num2": 2.5},
            {"operator": "*", "num2": 2}
        ]
        result = self.calculator.calculate_chain(operations)
        assert result == 16.0
    
    def test_chain_empty_list(self):
        """Prueba que lista vacía lance error."""
        with pytest.raises(ValueError, match="Se requiere al menos una operación"):
            self.calculator.calculate_chain([])
    
    def test_chain_missing_num1(self):
        """Prueba que falta num1 en primera operación lance error."""
        operations = [
            {"operator": "+", "num2": 5}
        ]
        with pytest.raises(ValueError, match="La primera operación debe incluir 'num1'"):
            self.calculator.calculate_chain(operations)
    
    def test_chain_missing_operator(self):
        """Prueba que falta operador lance error."""
        operations = [
            {"num1": 10, "operator": "+", "num2": 5},
            {"num2": 2}
        ]
        with pytest.raises(ValueError, match="Cada operación debe tener 'operator' y 'num2'"):
            self.calculator.calculate_chain(operations)
    
    def test_chain_division_by_zero(self):
        """Prueba que división por cero en cadena lance error."""
        operations = [
            {"num1": 10, "operator": "+", "num2": 5},
            {"operator": "/", "num2": 0}
        ]
        with pytest.raises(ValueError, match="No se puede dividir por cero"):
            self.calculator.calculate_chain(operations)


class TestCalculatorHistory:
    """Tests para el historial de la calculadora."""
    
    def setup_method(self):
        """Configuración antes de cada test."""
        self.calculator = Calculator()
    
    def test_history_starts_empty(self):
        """Prueba que el historial inicie vacío."""
        history = self.calculator.get_history()
        assert len(history) == 0
    
    def test_history_saves_operation(self):
        """Prueba que las operaciones se guarden en el historial."""
        self.calculator.calculate(10, 5, "+")
        history = self.calculator.get_history()
        assert len(history) == 1
        assert history[0]["num1"] == 10
        assert history[0]["num2"] == 5
        assert history[0]["operator"] == "+"
        assert history[0]["result"] == 15
    
    def test_history_saves_multiple_operations(self):
        """Prueba que múltiples operaciones se guarden."""
        self.calculator.calculate(10, 5, "+")
        self.calculator.calculate(20, 4, "/")
        self.calculator.calculate(3, 7, "*")
        
        history = self.calculator.get_history()
        assert len(history) == 3
    
    def test_history_from_chain(self):
        """Prueba que operaciones en cadena se guarden en historial."""
        operations = [
            {"num1": 10, "operator": "+", "num2": 5},
            {"operator": "*", "num2": 2}
        ]
        self.calculator.calculate_chain(operations)
        
        history = self.calculator.get_history()
        assert len(history) == 2  # Dos operaciones
    
    def test_clear_history(self):
        """Prueba limpiar el historial."""
        self.calculator.calculate(10, 5, "+")
        self.calculator.calculate(20, 4, "/")
        
        self.calculator.clear_history()
        history = self.calculator.get_history()
        assert len(history) == 0
    
    def test_get_supported_operations(self):
        """Prueba obtener operaciones soportadas."""
        operations = self.calculator.get_supported_operations()
        assert len(operations) == 4
        assert "+" in operations
        assert "-" in operations
        assert "*" in operations
        assert "/" in operations
