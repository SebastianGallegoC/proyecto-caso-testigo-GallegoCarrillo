# Dockerfile para el frontend React + Vite
FROM node:18-alpine

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de configuración de dependencias
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar el resto de los archivos
COPY . .

# Exponer el puerto
EXPOSE 9001

# Comando por defecto (se puede sobrescribir en docker-compose)
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "9001"]
