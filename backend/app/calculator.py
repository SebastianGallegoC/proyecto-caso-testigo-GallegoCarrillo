"""
Módulo de la calculadora.
Implementa la lógica principal de la calculadora con operaciones en cadena.
Principio SOLID: Single Responsibility
"""
from typing import List, Dict, Any
from .operations import OperationFactory, Operation


class Calculator:
    """
    Clase calculadora que maneja operaciones básicas y en cadena.
    Principio SOLID: Single Responsibility - Solo se encarga de ejecutar cálculos.
    """
    
    def __init__(self):
        self.operation_factory = OperationFactory()
        self.history: List[Dict[str, Any]] = []
    
    def calculate(self, num1: float, num2: float, operator: str) -> float:
        """
        Realiza una operación matemática simple.
        
        Args:
            num1: Primer número
            num2: Segundo número
            operator: Operador matemático (+, -, *, /)
            
        Returns:
            El resultado de la operación
            
        Raises:
            ValueError: Si la operación no es válida o si hay división por cero
        """
        operation = self.operation_factory.create_operation(operator)
        result = operation.execute(num1, num2)
        
        # Guardar en historial
        self.history.append({
            "num1": num1,
            "num2": num2,
            "operator": operator,
            "result": result
        })
        
        return result
    
    def calculate_chain(self, operations: List[Dict[str, Any]]) -> float:
        """
        Realiza operaciones en cadena.
        
        Args:
            operations: Lista de diccionarios con 'num2' y 'operator'
                       El primer elemento debe tener también 'num1'
        
        Returns:
            El resultado final de todas las operaciones
            
        Example:
            operations = [
                {"num1": 10, "operator": "+", "num2": 5},
                {"operator": "*", "num2": 2},
                {"operator": "-", "num2": 3}
            ]
            Resultado: ((10 + 5) * 2) - 3 = 27
        """
        if not operations:
            raise ValueError("Se requiere al menos una operación")
        
        # Primera operación debe incluir num1
        first_op = operations[0]
        if "num1" not in first_op:
            raise ValueError("La primera operación debe incluir 'num1'")
        
        result = self.calculate(
            first_op["num1"],
            first_op["num2"],
            first_op["operator"]
        )
        
        # Continuar con las operaciones en cadena
        for op in operations[1:]:
            if "operator" not in op or "num2" not in op:
                raise ValueError("Cada operación debe tener 'operator' y 'num2'")
            
            result = self.calculate(result, op["num2"], op["operator"])
        
        return result
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Retorna el historial de operaciones."""
        return self.history.copy()
    
    def clear_history(self) -> None:
        """Limpia el historial de operaciones."""
        self.history.clear()
    
    def get_supported_operations(self) -> List[str]:
        """Retorna las operaciones soportadas."""
        return self.operation_factory.get_supported_operations()
