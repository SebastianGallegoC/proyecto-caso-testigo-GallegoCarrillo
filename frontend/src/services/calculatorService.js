/**
 * Servicio para comunicación con la API de la calculadora.
 * Implementa el patrón Singleton para la instancia de axios.
 */
import axios from 'axios';

const API_BASE_URL = 'http://localhost:9000';

// Instancia configurada de axios
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 5000,
});

/**
 * Servicio de la calculadora
 */
class CalculatorService {
  /**
   * Realiza una operación simple
   * @param {number} num1 - Primer número
   * @param {number} num2 - Segundo número
   * @param {string} operator - Operador (+, -, *, /)
   * @returns {Promise} Promesa con el resultado
   */
  async calculate(num1, num2, operator) {
    try {
      const response = await apiClient.post('/calculate', {
        num1: parseFloat(num1),
        num2: parseFloat(num2),
        operator,
      });
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Realiza operaciones en cadena
   * @param {Array} operations - Array de operaciones
   * @returns {Promise} Promesa con el resultado
   */
  async calculateChain(operations) {
    try {
      const response = await apiClient.post('/calculate-chain', {
        operations,
      });
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Obtiene el historial de operaciones
   * @returns {Promise} Promesa con el historial
   */
  async getHistory() {
    try {
      const response = await apiClient.get('/history');
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Limpia el historial de operaciones
   * @returns {Promise} Promesa con confirmación
   */
  async clearHistory() {
    try {
      const response = await apiClient.delete('/history');
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Obtiene las operaciones soportadas
   * @returns {Promise} Promesa con las operaciones
   */
  async getOperations() {
    try {
      const response = await apiClient.get('/operations');
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Verifica el estado de la API
   * @returns {Promise} Promesa con el estado
   */
  async healthCheck() {
    try {
      const response = await apiClient.get('/health');
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Maneja los errores de las peticiones
   * @param {Error} error - Error de axios
   * @returns {Error} Error formateado
   */
  handleError(error) {
    if (error.response) {
      // El servidor respondió con un código de error
      const message = error.response.data.detail || error.response.data.error || 'Error en la operación';
      return new Error(message);
    } else if (error.request) {
      // La petición se hizo pero no hubo respuesta
      return new Error('No se pudo conectar con el servidor. Verifica que esté ejecutándose.');
    } else {
      // Error al configurar la petición
      return new Error('Error al realizar la petición: ' + error.message);
    }
  }
}

// Exportar instancia única (Singleton)
export default new CalculatorService();
