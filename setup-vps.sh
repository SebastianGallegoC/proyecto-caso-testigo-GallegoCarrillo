#!/bin/bash

# Script de configuración inicial del VPS Ubuntu para la Calculadora
# Ejecutar este script UNA SOLA VEZ en tu servidor VPS

set -e  # Salir si hay algún error

echo "🚀 Iniciando configuración del VPS Ubuntu..."

# Actualizar sistema
echo "📦 Actualizando sistema..."
sudo apt update && sudo apt upgrade -y

# Instalar dependencias básicas
echo "📦 Instalando dependencias básicas..."
sudo apt install -y \
    git \
    curl \
    wget \
    nano \
    ufw \
    ca-certificates \
    gnupg \
    lsb-release

# Instalar Docker
echo "🐳 Instalando Docker..."
if ! command -v docker &> /dev/null; then
    # Agregar repositorio oficial de Docker
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    sudo apt update
    sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    
    # Agregar usuario actual al grupo docker
    sudo usermod -aG docker $USER
    
    echo "✅ Docker instalado correctamente"
else
    echo "✅ Docker ya está instalado"
fi

# Instalar Docker Compose (standalone)
echo "🐳 Instalando Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    echo "✅ Docker Compose instalado correctamente"
else
    echo "✅ Docker Compose ya está instalado"
fi

# Configurar firewall
echo "🔥 Configurando firewall UFW..."
sudo ufw allow OpenSSH
sudo ufw allow 9000/tcp  # Backend API
sudo ufw allow 9001/tcp  # Frontend
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw --force enable

# Crear directorio para la aplicación
echo "📁 Creando directorio de la aplicación..."
APP_DIR="/home/$USER/calculadora-app"
mkdir -p $APP_DIR
cd $APP_DIR

# Configurar Git (si no está configurado)
if [ -z "$(git config --global user.name)" ]; then
    echo "⚙️ Configurando Git..."
    read -p "Ingresa tu nombre para Git: " git_name
    read -p "Ingresa tu email para Git: " git_email
    git config --global user.name "$git_name"
    git config --global user.email "$git_email"
fi

# Clonar repositorio
echo "📥 Clonando repositorio..."
echo "Por favor ingresa la URL de tu repositorio:"
read -p "URL del repositorio: " repo_url

if [ ! -d "$APP_DIR/.git" ]; then
    git clone $repo_url $APP_DIR
else
    echo "✅ Repositorio ya existe, actualizando..."
    git pull
fi

# Configurar clave SSH para GitHub (si no existe)
if [ ! -f "$HOME/.ssh/id_rsa" ]; then
    echo "🔑 Generando clave SSH para GitHub..."
    ssh-keygen -t rsa -b 4096 -C "$USER@$(hostname)" -N "" -f $HOME/.ssh/id_rsa
    
    echo ""
    echo "=========================================="
    echo "📋 COPIA ESTA CLAVE PÚBLICA Y AGRÉGALA A GITHUB:"
    echo "=========================================="
    cat $HOME/.ssh/id_rsa.pub
    echo "=========================================="
    echo ""
    echo "Instrucciones:"
    echo "1. Copia la clave SSH de arriba"
    echo "2. Ve a GitHub → Settings → SSH and GPG keys"
    echo "3. Click en 'New SSH key'"
    echo "4. Pega la clave y guarda"
    echo ""
    read -p "Presiona ENTER cuando hayas agregado la clave a GitHub..."
fi

# Probar conexión SSH con GitHub
echo "🔌 Probando conexión con GitHub..."
ssh -T git@github.com || true

# Configurar variables de entorno (opcional)
echo "⚙️ Configurando variables de entorno..."
if [ ! -f "$APP_DIR/.env" ]; then
    cat > $APP_DIR/.env << 'EOF'
# Variables de entorno para la aplicación
BACKEND_PORT=9000
FRONTEND_PORT=9001
EOF
    echo "✅ Archivo .env creado"
fi

# Crear script de deployment manual
cat > $APP_DIR/deploy.sh << 'EOF'
#!/bin/bash
set -e

echo "🚀 Desplegando aplicación..."

cd "$(dirname "$0")"

echo "📥 Pulling latest changes..."
git pull origin master

echo "🐳 Stopping containers..."
docker-compose down || true

echo "🔨 Building images..."
docker-compose build --no-cache

echo "🚀 Starting containers..."
docker-compose up -d

echo "🧹 Cleaning up..."
docker image prune -f

echo "✅ Deployment complete!"
docker-compose ps
EOF

chmod +x $APP_DIR/deploy.sh

# Crear script de logs
cat > $APP_DIR/logs.sh << 'EOF'
#!/bin/bash
# Script para ver logs de los contenedores

echo "📋 Logs de la aplicación"
echo "========================"
echo ""
echo "Selecciona una opción:"
echo "1) Ver todos los logs"
echo "2) Ver logs del backend"
echo "3) Ver logs del frontend"
echo "4) Seguir logs en tiempo real (todos)"
echo "5) Seguir logs del backend"
echo "6) Seguir logs del frontend"
read -p "Opción: " option

case $option in
    1) docker-compose logs ;;
    2) docker-compose logs backend ;;
    3) docker-compose logs frontend ;;
    4) docker-compose logs -f ;;
    5) docker-compose logs -f backend ;;
    6) docker-compose logs -f frontend ;;
    *) echo "Opción inválida" ;;
esac
EOF

chmod +x $APP_DIR/logs.sh

# Información del sistema
echo ""
echo "=========================================="
echo "✅ CONFIGURACIÓN COMPLETADA"
echo "=========================================="
echo ""
echo "📊 Información del sistema:"
echo "- Usuario: $USER"
echo "- Directorio de la app: $APP_DIR"
echo "- Docker version: $(docker --version)"
echo "- Docker Compose version: $(docker-compose --version)"
echo ""
echo "🌐 Puertos configurados:"
echo "- Backend API: 9000"
echo "- Frontend: 9001"
echo "- HTTP: 80"
echo "- HTTPS: 443"
echo ""
echo "📝 Archivos creados:"
echo "- $APP_DIR/deploy.sh - Script de deployment manual"
echo "- $APP_DIR/logs.sh - Script para ver logs"
echo "- $APP_DIR/.env - Variables de entorno"
echo ""
echo "🚀 Próximos pasos:"
echo "1. Agrega la clave SSH pública a GitHub (si no lo hiciste)"
echo "2. Configura los secretos en GitHub Actions:"
echo "   - VPS_HOST: $(curl -s ifconfig.me)"
echo "   - VPS_USER: $USER"
echo "   - VPS_PATH: $APP_DIR"
echo "   - VPS_SSH_KEY: (ver archivo ~/.ssh/id_rsa)"
echo ""
echo "3. Para deployment manual, ejecuta:"
echo "   cd $APP_DIR && ./deploy.sh"
echo ""
echo "4. Para ver logs:"
echo "   cd $APP_DIR && ./logs.sh"
echo ""
echo "=========================================="
echo ""

# Mostrar IP pública
echo "📍 Tu IP pública es: $(curl -s ifconfig.me)"
echo ""

# Opcional: hacer primer deployment
read -p "¿Quieres hacer el primer deployment ahora? (y/n): " deploy_now
if [ "$deploy_now" = "y" ] || [ "$deploy_now" = "Y" ]; then
    cd $APP_DIR
    ./deploy.sh
fi

echo ""
echo "✅ ¡Todo listo! Tu VPS está configurado."
echo ""
echo "⚠️ IMPORTANTE: Reinicia tu sesión SSH para que los cambios de grupo docker surtan efecto:"
echo "   exit"
echo "   ssh usuario@servidor"
