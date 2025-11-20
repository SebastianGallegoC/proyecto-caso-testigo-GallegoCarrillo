"""
Tests de integración para los endpoints de la API.
Prueba todos los endpoints con diferentes casos.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app, calculator


@pytest.fixture
def client():
    """Fixture para crear un cliente de prueba."""
    # Limpiar historial antes de cada test
    calculator.clear_history()
    return TestClient(app)


class TestRootEndpoints:
    """Tests para endpoints raíz y de información."""
    
    def test_read_root(self, client):
        """Prueba el endpoint raíz."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
    
    def test_health_check(self, client):
        """Prueba el endpoint de salud."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "calculator-api"
    
    def test_get_operations(self, client):
        """Prueba obtener operaciones soportadas."""
        response = client.get("/operations")
        assert response.status_code == 200
        data = response.json()
        assert "operations" in data
        assert len(data["operations"]) == 4


class TestCalculateEndpoint:
    """Tests para el endpoint de cálculo simple."""
    
    def test_calculate_addition(self, client):
        """Prueba suma mediante endpoint."""
        response = client.post(
            "/calculate",
            json={"num1": 10, "num2": 5, "operator": "+"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 15
        assert "message" in data
    
    def test_calculate_subtraction(self, client):
        """Prueba resta mediante endpoint."""
        response = client.post(
            "/calculate",
            json={"num1": 10, "num2": 5, "operator": "-"}
        )
        assert response.status_code == 200
        assert response.json()["result"] == 5
    
    def test_calculate_multiplication(self, client):
        """Prueba multiplicación mediante endpoint."""
        response = client.post(
            "/calculate",
            json={"num1": 10, "num2": 5, "operator": "*"}
        )
        assert response.status_code == 200
        assert response.json()["result"] == 50
    
    def test_calculate_division(self, client):
        """Prueba división mediante endpoint."""
        response = client.post(
            "/calculate",
            json={"num1": 10, "num2": 5, "operator": "/"}
        )
        assert response.status_code == 200
        assert response.json()["result"] == 2
    
    def test_calculate_division_by_zero(self, client):
        """Prueba que división por cero retorne error 400."""
        response = client.post(
            "/calculate",
            json={"num1": 10, "num2": 0, "operator": "/"}
        )
        assert response.status_code == 400
        assert "detail" in response.json()
    
    def test_calculate_invalid_operator(self, client):
        """Prueba que operador inválido retorne error 422."""
        response = client.post(
            "/calculate",
            json={"num1": 10, "num2": 5, "operator": "%"}
        )
        assert response.status_code == 422
    
    def test_calculate_missing_fields(self, client):
        """Prueba que campos faltantes retornen error 422."""
        response = client.post(
            "/calculate",
            json={"num1": 10, "operator": "+"}
        )
        assert response.status_code == 422
    
    def test_calculate_with_decimals(self, client):
        """Prueba cálculo con decimales."""
        response = client.post(
            "/calculate",
            json={"num1": 5.5, "num2": 2.5, "operator": "+"}
        )
        assert response.status_code == 200
        assert response.json()["result"] == 8.0


class TestCalculateChainEndpoint:
    """Tests para el endpoint de operaciones en cadena."""
    
    def test_chain_two_operations(self, client):
        """Prueba cadena con dos operaciones."""
        response = client.post(
            "/calculate-chain",
            json={
                "operations": [
                    {"num1": 10, "operator": "+", "num2": 5},
                    {"operator": "*", "num2": 2}
                ]
            }
        )
        assert response.status_code == 200
        assert response.json()["result"] == 30
    
    def test_chain_three_operations(self, client):
        """Prueba cadena con tres operaciones."""
        response = client.post(
            "/calculate-chain",
            json={
                "operations": [
                    {"num1": 10, "operator": "+", "num2": 5},
                    {"operator": "*", "num2": 2},
                    {"operator": "-", "num2": 3}
                ]
            }
        )
        assert response.status_code == 200
        assert response.json()["result"] == 27
    
    def test_chain_empty_operations(self, client):
        """Prueba que lista vacía retorne error."""
        response = client.post(
            "/calculate-chain",
            json={"operations": []}
        )
        assert response.status_code == 422
    
    def test_chain_missing_num1(self, client):
        """Prueba que falta num1 retorne error."""
        response = client.post(
            "/calculate-chain",
            json={
                "operations": [
                    {"operator": "+", "num2": 5}
                ]
            }
        )
        # Puede ser 400 si la validación backend lo detecta o 500 si falla en el cálculo
        assert response.status_code in [400, 500]
    
    def test_chain_with_division_by_zero(self, client):
        """Prueba división por cero en cadena."""
        response = client.post(
            "/calculate-chain",
            json={
                "operations": [
                    {"num1": 10, "operator": "+", "num2": 5},
                    {"operator": "/", "num2": 0}
                ]
            }
        )
        assert response.status_code == 400


class TestHistoryEndpoints:
    """Tests para endpoints de historial."""
    
    def test_get_empty_history(self, client):
        """Prueba obtener historial vacío."""
        response = client.get("/history")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 0
        assert len(data["history"]) == 0
    
    def test_history_after_calculation(self, client):
        """Prueba historial después de cálculo."""
        client.post("/calculate", json={"num1": 10, "num2": 5, "operator": "+"})
        
        response = client.get("/history")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 1
        assert len(data["history"]) == 1
    
    def test_history_multiple_operations(self, client):
        """Prueba historial con múltiples operaciones."""
        client.post("/calculate", json={"num1": 10, "num2": 5, "operator": "+"})
        client.post("/calculate", json={"num1": 20, "num2": 4, "operator": "/"})
        
        response = client.get("/history")
        data = response.json()
        assert data["count"] == 2
    
    def test_clear_history(self, client):
        """Prueba limpiar historial."""
        client.post("/calculate", json={"num1": 10, "num2": 5, "operator": "+"})
        
        response = client.delete("/history")
        assert response.status_code == 200
        assert "message" in response.json()
        
        # Verificar que está vacío
        response = client.get("/history")
        assert response.json()["count"] == 0
    
    def test_history_from_chain(self, client):
        """Prueba que operaciones en cadena aparezcan en historial."""
        client.post(
            "/calculate-chain",
            json={
                "operations": [
                    {"num1": 10, "operator": "+", "num2": 5},
                    {"operator": "*", "num2": 2}
                ]
            }
        )
        
        response = client.get("/history")
        data = response.json()
        assert data["count"] == 2  # Dos operaciones en la cadena
