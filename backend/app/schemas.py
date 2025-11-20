"""
Esquemas de datos para validación con Pydantic.
Principio SOLID: Interface Segregation - Interfaces específicas para cada caso de uso.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional


class OperationRequest(BaseModel):
    """Esquema para una operación simple."""

    num1: float = Field(..., description="Primer número")
    num2: float = Field(..., description="Segundo número")
    operator: str = Field(..., description="Operador matemático: +, -, *, /")

    @validator("operator")
    def validate_operator(cls, v):
        if v not in ["+", "-", "*", "/"]:
            raise ValueError("Operador debe ser: +, -, *, /")
        return v

    class Config:
        schema_extra = {"example": {"num1": 10, "num2": 5, "operator": "+"}}


class ChainOperationItem(BaseModel):
    """Esquema para un elemento de operación en cadena."""

    num1: Optional[float] = Field(None, description="Primer número (solo en primera operación)")
    num2: float = Field(..., description="Segundo número")
    operator: str = Field(..., description="Operador matemático: +, -, *, /")

    @validator("operator")
    def validate_operator(cls, v):
        if v not in ["+", "-", "*", "/"]:
            raise ValueError("Operador debe ser: +, -, *, /")
        return v


class ChainOperationRequest(BaseModel):
    """Esquema para operaciones en cadena."""

    operations: List[ChainOperationItem] = Field(..., min_items=1)

    class Config:
        schema_extra = {
            "example": {
                "operations": [
                    {"num1": 10, "operator": "+", "num2": 5},
                    {"operator": "*", "num2": 2},
                    {"operator": "-", "num2": 3},
                ]
            }
        }


class OperationResponse(BaseModel):
    """Esquema de respuesta para operaciones."""

    result: float = Field(..., description="Resultado de la operación")
    message: str = Field(default="Operación exitosa")

    class Config:
        schema_extra = {"example": {"result": 15.0, "message": "Operación exitosa"}}


class HistoryItem(BaseModel):
    """Esquema para un elemento del historial."""

    num1: float
    num2: float
    operator: str
    result: float


class HistoryResponse(BaseModel):
    """Esquema de respuesta para el historial."""

    history: List[HistoryItem]
    count: int

    class Config:
        schema_extra = {
            "example": {
                "history": [{"num1": 10, "num2": 5, "operator": "+", "result": 15}],
                "count": 1,
            }
        }


class ErrorResponse(BaseModel):
    """Esquema de respuesta para errores."""

    error: str
    detail: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {"error": "Error en la operación", "detail": "No se puede dividir por cero"}
        }
