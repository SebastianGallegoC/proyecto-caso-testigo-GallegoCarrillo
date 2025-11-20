"""
Tests unitarios para el módulo de operaciones.
Prueba cada operación matemática y el factory pattern.
"""
import pytest
from app.operations import (
    Addition,
    Subtraction,
    Multiplication,
    Division,
    OperationFactory
)


class TestAddition:
    """Tests para la operación de suma."""
    
    def test_addition_positive_numbers(self):
        """Prueba suma de números positivos."""
        operation = Addition()
        assert operation.execute(5, 3) == 8
    
    def test_addition_negative_numbers(self):
        """Prueba suma de números negativos."""
        operation = Addition()
        assert operation.execute(-5, -3) == -8
    
    def test_addition_mixed_numbers(self):
        """Prueba suma de números positivos y negativos."""
        operation = Addition()
        assert operation.execute(10, -5) == 5
    
    def test_addition_with_zero(self):
        """Prueba suma con cero."""
        operation = Addition()
        assert operation.execute(10, 0) == 10
    
    def test_addition_decimals(self):
        """Prueba suma de decimales."""
        operation = Addition()
        assert operation.execute(3.5, 2.5) == 6.0
    
    def test_get_symbol(self):
        """Prueba que el símbolo sea correcto."""
        operation = Addition()
        assert operation.get_symbol() == "+"


class TestSubtraction:
    """Tests para la operación de resta."""
    
    def test_subtraction_positive_numbers(self):
        """Prueba resta de números positivos."""
        operation = Subtraction()
        assert operation.execute(10, 3) == 7
    
    def test_subtraction_negative_result(self):
        """Prueba resta que resulta en negativo."""
        operation = Subtraction()
        assert operation.execute(3, 10) == -7
    
    def test_subtraction_negative_numbers(self):
        """Prueba resta de números negativos."""
        operation = Subtraction()
        assert operation.execute(-5, -3) == -2
    
    def test_subtraction_with_zero(self):
        """Prueba resta con cero."""
        operation = Subtraction()
        assert operation.execute(10, 0) == 10
    
    def test_subtraction_decimals(self):
        """Prueba resta de decimales."""
        operation = Subtraction()
        result = operation.execute(5.5, 2.3)
        assert abs(result - 3.2) < 0.0001
    
    def test_get_symbol(self):
        """Prueba que el símbolo sea correcto."""
        operation = Subtraction()
        assert operation.get_symbol() == "-"


class TestMultiplication:
    """Tests para la operación de multiplicación."""
    
    def test_multiplication_positive_numbers(self):
        """Prueba multiplicación de números positivos."""
        operation = Multiplication()
        assert operation.execute(5, 3) == 15
    
    def test_multiplication_negative_numbers(self):
        """Prueba multiplicación de números negativos."""
        operation = Multiplication()
        assert operation.execute(-5, -3) == 15
    
    def test_multiplication_mixed_numbers(self):
        """Prueba multiplicación de números positivos y negativos."""
        operation = Multiplication()
        assert operation.execute(5, -3) == -15
    
    def test_multiplication_with_zero(self):
        """Prueba multiplicación con cero."""
        operation = Multiplication()
        assert operation.execute(10, 0) == 0
    
    def test_multiplication_decimals(self):
        """Prueba multiplicación de decimales."""
        operation = Multiplication()
        assert operation.execute(2.5, 4) == 10.0
    
    def test_get_symbol(self):
        """Prueba que el símbolo sea correcto."""
        operation = Multiplication()
        assert operation.get_symbol() == "*"


class TestDivision:
    """Tests para la operación de división."""
    
    def test_division_positive_numbers(self):
        """Prueba división de números positivos."""
        operation = Division()
        assert operation.execute(10, 2) == 5
    
    def test_division_negative_numbers(self):
        """Prueba división de números negativos."""
        operation = Division()
        assert operation.execute(-10, -2) == 5
    
    def test_division_mixed_numbers(self):
        """Prueba división de números positivos y negativos."""
        operation = Division()
        assert operation.execute(10, -2) == -5
    
    def test_division_decimals(self):
        """Prueba división de decimales."""
        operation = Division()
        assert operation.execute(7.5, 2.5) == 3.0
    
    def test_division_by_zero(self):
        """Prueba que la división por cero lance error."""
        operation = Division()
        with pytest.raises(ValueError, match="No se puede dividir por cero"):
            operation.execute(10, 0)
    
    def test_get_symbol(self):
        """Prueba que el símbolo sea correcto."""
        operation = Division()
        assert operation.get_symbol() == "/"


class TestOperationFactory:
    """Tests para el factory de operaciones."""
    
    def test_create_addition(self):
        """Prueba creación de operación de suma."""
        operation = OperationFactory.create_operation("+")
        assert isinstance(operation, Addition)
        assert operation.execute(5, 3) == 8
    
    def test_create_subtraction(self):
        """Prueba creación de operación de resta."""
        operation = OperationFactory.create_operation("-")
        assert isinstance(operation, Subtraction)
        assert operation.execute(5, 3) == 2
    
    def test_create_multiplication(self):
        """Prueba creación de operación de multiplicación."""
        operation = OperationFactory.create_operation("*")
        assert isinstance(operation, Multiplication)
        assert operation.execute(5, 3) == 15
    
    def test_create_division(self):
        """Prueba creación de operación de división."""
        operation = OperationFactory.create_operation("/")
        assert isinstance(operation, Division)
        assert operation.execute(6, 3) == 2
    
    def test_invalid_operation(self):
        """Prueba que operador inválido lance error."""
        with pytest.raises(ValueError, match="Operación no soportada"):
            OperationFactory.create_operation("%")
    
    def test_get_supported_operations(self):
        """Prueba obtener lista de operaciones soportadas."""
        operations = OperationFactory.get_supported_operations()
        assert len(operations) == 4
        assert "+" in operations
        assert "-" in operations
        assert "*" in operations
        assert "/" in operations
