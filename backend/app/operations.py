"""
Módulo de operaciones matemáticas.
Implementa el patrón Strategy para las operaciones básicas.
Principio SOLID: Single Responsibility - Cada clase tiene una única responsabilidad.
"""

from abc import ABC, abstractmethod
from typing import Union


class Operation(ABC):
    """
    Clase abstracta que define la interfaz para todas las operaciones.
    Principio SOLID: Open/Closed - Abierto para extensión, cerrado para modificación.
    """

    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        """Ejecuta la operación matemática."""
        pass

    @abstractmethod
    def get_symbol(self) -> str:
        """Retorna el símbolo de la operación."""
        pass


class Addition(Operation):
    """Implementación de la operación de suma."""

    def execute(self, a: float, b: float) -> float:
        return a + b

    def get_symbol(self) -> str:
        return "+"


class Subtraction(Operation):
    """Implementación de la operación de resta."""

    def execute(self, a: float, b: float) -> float:
        return a - b

    def get_symbol(self) -> str:
        return "-"


class Multiplication(Operation):
    """Implementación de la operación de multiplicación."""

    def execute(self, a: float, b: float) -> float:
        return a * b

    def get_symbol(self) -> str:
        return "*"


class Division(Operation):
    """Implementación de la operación de división."""

    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("No se puede dividir por cero")
        return a / b

    def get_symbol(self) -> str:
        return "/"


class OperationFactory:
    """
    Factory para crear instancias de operaciones.
    Principio SOLID: Dependency Inversion - Depende de abstracciones, no de concreciones.
    Patrón de diseño: Factory Pattern
    """

    _operations = {
        "+": Addition,
        "-": Subtraction,
        "*": Multiplication,
        "/": Division,
    }

    @classmethod
    def create_operation(cls, operator: str) -> Operation:
        """
        Crea y retorna una instancia de operación basada en el operador.

        Args:
            operator: El símbolo de la operación (+, -, *, /)

        Returns:
            Una instancia de Operation

        Raises:
            ValueError: Si el operador no es válido
        """
        operation_class = cls._operations.get(operator)
        if operation_class is None:
            raise ValueError(f"Operación no soportada: {operator}")
        return operation_class()

    @classmethod
    def get_supported_operations(cls) -> list:
        """Retorna la lista de operaciones soportadas."""
        return list(cls._operations.keys())
