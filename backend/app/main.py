"""
Aplicación principal de FastAPI.
Principio SOLID: Dependency Inversion - Los endpoints dependen de abstracciones.
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
from .calculator import Calculator
from .schemas import (
    OperationRequest,
    ChainOperationRequest,
    OperationResponse,
    HistoryResponse,
    ErrorResponse,
)

# Crear instancia de FastAPI
app = FastAPI(
    title="Calculadora API",
    description="API REST para calculadora con operaciones básicas y en cadena",
    version="1.0.0",
)

# Configurar CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:9001",
        "http://localhost:9002",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instancia global de la calculadora (Singleton pattern)
calculator = Calculator()


@app.get("/", tags=["Root"])
async def read_root() -> Dict[str, str]:
    """Endpoint raíz para verificar que la API está funcionando."""
    return {"message": "Calculadora API - Backend funcionando correctamente", "version": "1.0.0"}


@app.get("/operations", tags=["Operations"])
async def get_operations() -> Dict[str, Any]:
    """Obtiene la lista de operaciones soportadas."""
    return {
        "operations": calculator.get_supported_operations(),
        "count": len(calculator.get_supported_operations()),
    }


@app.post(
    "/calculate",
    response_model=OperationResponse,
    responses={400: {"model": ErrorResponse}},
    tags=["Calculator"],
)
async def calculate(request: OperationRequest) -> OperationResponse:
    """
    Realiza una operación matemática simple.

    Args:
        request: Objeto con num1, num2 y operator

    Returns:
        Resultado de la operación
    """
    try:
        result = calculator.calculate(request.num1, request.num2, request.operator)
        return OperationResponse(
            result=result, message=f"{request.num1} {request.operator} {request.num2} = {result}"
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error inesperado: {str(e)}"
        )


@app.post(
    "/calculate-chain",
    response_model=OperationResponse,
    responses={400: {"model": ErrorResponse}},
    tags=["Calculator"],
)
async def calculate_chain(request: ChainOperationRequest) -> OperationResponse:
    """
    Realiza operaciones en cadena.

    Args:
        request: Lista de operaciones a realizar en secuencia

    Returns:
        Resultado final de todas las operaciones
    """
    try:
        operations = [op.dict() for op in request.operations]
        result = calculator.calculate_chain(operations)
        return OperationResponse(
            result=result, message="Operaciones en cadena ejecutadas exitosamente"
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error inesperado: {str(e)}"
        )


@app.get("/history", response_model=HistoryResponse, tags=["History"])
async def get_history() -> HistoryResponse:
    """Obtiene el historial de operaciones realizadas."""
    history = calculator.get_history()
    return HistoryResponse(history=history, count=len(history))


@app.delete("/history", tags=["History"])
async def clear_history() -> Dict[str, str]:
    """Limpia el historial de operaciones."""
    calculator.clear_history()
    return {"message": "Historial limpiado exitosamente"}


@app.get("/health", tags=["Health"])
async def health_check() -> Dict[str, str]:
    """Endpoint de verificación de salud del servicio."""
    return {"status": "healthy", "service": "calculator-api"}
