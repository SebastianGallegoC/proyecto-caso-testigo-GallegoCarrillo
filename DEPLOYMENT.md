# 🚀 Guía Completa de Deployment en VPS Ubuntu

Esta guía te llevará paso a paso para deployar la calculadora en tu VPS Ubuntu.

## 📋 Requisitos Previos

- ✅ VPS con Ubuntu 20.04 o superior
- ✅ Acceso root o sudo
- ✅ IP pública del VPS
- ✅ Llave privada SSH para conectarte al VPS
- ✅ Repositorio en GitHub

## 🔧 Paso 1: Conectarte a tu VPS

Desde tu computadora local:

```bash
# Conectar vía SSH (reemplaza con tu IP y usuario)
ssh usuario@IP_DEL_VPS

# O si usas llave privada:
ssh -i /ruta/a/tu/llave-privada.pem usuario@IP_DEL_VPS
```

**Ejemplo:**

```bash
ssh -i ~/.ssh/mi-vps-key.pem ubuntu@123.456.78.90
```

## 🛠️ Paso 2: Configurar el VPS (Primera vez)

### Opción A: Usando el script automatizado (Recomendado)

1. **Desde tu computadora local**, copia el script al VPS:

```bash
scp -i /ruta/a/llave-privada.pem setup-vps.sh usuario@IP_DEL_VPS:~/
```

2. **Conéctate al VPS** y ejecuta el script:

```bash
ssh -i /ruta/a/llave-privada.pem usuario@IP_DEL_VPS
chmod +x setup-vps.sh
./setup-vps.sh
```

El script instalará automáticamente:

- ✅ Docker y Docker Compose
- ✅ Git
- ✅ Configuración del firewall
- ✅ Clonará tu repositorio
- ✅ Creará scripts de deployment y logs

### Opción B: Configuración manual

Si prefieres hacerlo paso a paso:

#### 2.1. Actualizar el sistema

```bash
sudo apt update && sudo apt upgrade -y
```

#### 2.2. Instalar Docker

```bash
# Instalar dependencias
sudo apt install -y ca-certificates curl gnupg lsb-release

# Agregar clave GPG de Docker
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Agregar repositorio
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Agregar tu usuario al grupo docker
sudo usermod -aG docker $USER

# Verificar instalación
docker --version
```

#### 2.3. Instalar Docker Compose standalone

```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

#### 2.4. Configurar firewall

```bash
sudo ufw allow OpenSSH
sudo ufw allow 9000/tcp   # Backend
sudo ufw allow 9001/tcp   # Frontend
sudo ufw allow 80/tcp     # HTTP (opcional)
sudo ufw allow 443/tcp    # HTTPS (opcional)
sudo ufw enable
sudo ufw status
```

#### 2.5. Crear directorio y clonar repositorio

```bash
# Crear directorio
mkdir -p ~/calculadora-app
cd ~/calculadora-app

# Configurar Git
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"

# Clonar repositorio
git clone https://github.com/TU-USUARIO/proyecto-caso-testigo-GallegoCarrillo.git .
```

## 🔑 Paso 3: Configurar SSH para GitHub Actions

### 3.1. Generar par de llaves SSH en el VPS

```bash
# En el VPS, genera una nueva llave SSH
ssh-keygen -t rsa -b 4096 -C "deploy-key" -f ~/.ssh/github_deploy_key -N ""

# Agregar llave al agente SSH
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/github_deploy_key
```

### 3.2. Agregar la llave pública al VPS

```bash
# Agregar llave pública a authorized_keys
cat ~/.ssh/github_deploy_key.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

### 3.3. Copiar la llave privada (para GitHub Secrets)

```bash
# Mostrar la llave privada (cópiala completa, incluyendo BEGIN y END)
cat ~/.ssh/github_deploy_key
```

**Salida ejemplo:**

```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABlwAAAAdzc2gtcn
...
(múltiples líneas)
...
-----END OPENSSH PRIVATE KEY-----
```

⚠️ **IMPORTANTE**: Copia TODO el contenido, incluyendo las líneas BEGIN y END.

## 🔐 Paso 4: Configurar Secretos en GitHub

Ve a tu repositorio en GitHub:

1. **Settings** → **Secrets and variables** → **Actions**
2. Click en **"New repository secret"**
3. Agrega cada uno de estos secretos:

### Secretos Requeridos:

#### `VPS_HOST`

- **Descripción**: IP pública de tu VPS
- **Valor**: La IP de tu servidor
- **Ejemplo**: `123.456.78.90`

Para obtenerla en el VPS:

```bash
curl ifconfig.me
```

#### `VPS_USER`

- **Descripción**: Usuario SSH del VPS
- **Valor**: Tu nombre de usuario
- **Ejemplo**: `ubuntu` o `root` o tu usuario personalizado

Para verificar:

```bash
whoami
```

#### `VPS_PATH`

- **Descripción**: Ruta completa donde está la aplicación en el VPS
- **Valor**: Ruta absoluta al directorio
- **Ejemplo**: `/home/ubuntu/calculadora-app`

Para obtenerla en el VPS:

```bash
cd ~/calculadora-app
pwd
```

#### `VPS_SSH_KEY`

- **Descripción**: Llave privada SSH (todo el contenido)
- **Valor**: Contenido completo del archivo `~/.ssh/github_deploy_key`
- **Ejemplo**:

```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABlwAAAAdzc2gtcn
...
-----END OPENSSH PRIVATE KEY-----
```

Para copiarla:

```bash
cat ~/.ssh/github_deploy_key
```

### Resumen Visual de Secretos:

| Secret Name   | Cómo obtenerlo                   | Ejemplo                          |
| ------------- | -------------------------------- | -------------------------------- |
| `VPS_HOST`    | `curl ifconfig.me`               | `123.456.78.90`                  |
| `VPS_USER`    | `whoami`                         | `ubuntu`                         |
| `VPS_PATH`    | `pwd` en el directorio de la app | `/home/ubuntu/calculadora-app`   |
| `VPS_SSH_KEY` | `cat ~/.ssh/github_deploy_key`   | (contenido completo de la llave) |

## 🚀 Paso 5: Primer Deployment Manual

Antes de confiar en el CI/CD automático, haz un deployment manual para verificar que todo funciona:

```bash
# Conectar al VPS
ssh -i tu-llave.pem usuario@IP_DEL_VPS

# Ir al directorio de la app
cd ~/calculadora-app

# Asegurarse de tener la última versión
git pull origin master

# Construir y levantar contenedores
docker-compose build --no-cache
docker-compose up -d

# Verificar que están corriendo
docker-compose ps

# Ver logs
docker-compose logs -f
```

### Verificar que todo funciona:

```bash
# Verificar backend
curl http://localhost:9000/health

# Debería responder: {"status":"healthy"}
```

Desde tu navegador:

- Backend API: `http://TU_IP:9000/docs`
- Frontend: `http://TU_IP:9001`
- Health check: `http://TU_IP:9000/health`

## ✅ Paso 6: Probar el CI/CD Automático

Una vez que el deployment manual funcione:

1. **Haz un cambio pequeño** en tu código local
2. **Commit y push** a master:

```bash
git add .
git commit -m "test: Probar CI/CD deployment"
git push origin master
```

3. **Ve a GitHub** → pestaña **Actions**
4. Verás el workflow ejecutándose automáticamente
5. Si todo está bien, el deployment se hará automáticamente al VPS

## 🔍 Paso 7: Monitoreo y Mantenimiento

### Ver logs de la aplicación

```bash
# Todos los logs
docker-compose logs -f

# Solo backend
docker-compose logs -f backend

# Solo frontend
docker-compose logs -f frontend

# Últimas 100 líneas
docker-compose logs --tail=100
```

### Ver estado de contenedores

```bash
docker-compose ps
```

### Reiniciar servicios

```bash
# Reiniciar todo
docker-compose restart

# Reiniciar solo backend
docker-compose restart backend

# Reiniciar solo frontend
docker-compose restart frontend
```

### Detener la aplicación

```bash
docker-compose down
```

### Actualizar manualmente

```bash
cd ~/calculadora-app
git pull origin master
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Limpiar recursos de Docker

```bash
# Limpiar imágenes antiguas
docker image prune -f

# Limpiar todo (cuidado!)
docker system prune -a -f
```

## 🔒 Paso 8: Seguridad Adicional (Opcional pero Recomendado)

### 8.1. Cambiar puerto SSH (opcional)

```bash
sudo nano /etc/ssh/sshd_config
# Cambiar Port 22 a otro puerto (ej: 2222)
sudo systemctl restart sshd

# Agregar nuevo puerto al firewall
sudo ufw allow 2222/tcp
```

### 8.2. Configurar Fail2Ban

```bash
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 8.3. Actualizar automáticamente

```bash
sudo apt install unattended-upgrades -y
sudo dpkg-reconfigure --priority=low unattended-upgrades
```

### 8.4. Instalar certificado SSL con Let's Encrypt (opcional)

```bash
sudo apt install certbot python3-certbot-nginx -y

# Instalar Nginx como proxy reverso
sudo apt install nginx -y

# Configurar Nginx (ver sección siguiente)
```

## 🌐 Paso 9: Configurar Dominio (Opcional)

Si tienes un dominio, puedes configurar Nginx como proxy reverso:

### 9.1. Instalar Nginx

```bash
sudo apt install nginx -y
```

### 9.2. Crear configuración

```bash
sudo nano /etc/nginx/sites-available/calculadora
```

Pega esto:

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    # Frontend
    location / {
        proxy_pass http://localhost:9001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:9000/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 9.3. Activar configuración

```bash
sudo ln -s /etc/nginx/sites-available/calculadora /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 9.4. Instalar SSL

```bash
sudo certbot --nginx -d tu-dominio.com
```

## 🆘 Troubleshooting

### Problema: No puedo conectarme por SSH

**Solución:**

```bash
# Verifica que el firewall permita SSH
sudo ufw allow OpenSSH
sudo ufw status

# Verifica que el servicio SSH esté corriendo
sudo systemctl status sshd
```

### Problema: Docker dice "permission denied"

**Solución:**

```bash
# Agregar usuario al grupo docker
sudo usermod -aG docker $USER

# Reiniciar sesión SSH
exit
ssh usuario@IP
```

### Problema: Los contenedores no inician

**Solución:**

```bash
# Ver logs detallados
docker-compose logs

# Verificar que los puertos no estén en uso
sudo netstat -tulpn | grep -E '9000|9001'

# Reconstruir desde cero
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Problema: El CI/CD falla con "Host key verification failed"

**Solución:**
Verifica que la llave SSH esté correctamente configurada:

```bash
# En el VPS
cat ~/.ssh/authorized_keys
# Debe contener la llave pública
```

### Problema: "Cannot connect to the Docker daemon"

**Solución:**

```bash
# Iniciar Docker
sudo systemctl start docker
sudo systemctl enable docker

# Verificar estado
sudo systemctl status docker
```

## 📊 Comandos Útiles

```bash
# Ver uso de recursos
docker stats

# Ver espacio usado por Docker
docker system df

# Ver IP del servidor
curl ifconfig.me

# Ver uso de CPU y memoria
htop

# Ver logs del sistema
journalctl -xe

# Ver servicios activos
systemctl list-units --type=service --state=running
```

## 📚 Recursos Adicionales

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [GitHub Actions SSH Deploy](https://github.com/marketplace/actions/ssh-deploy)
- [UFW Firewall Guide](https://help.ubuntu.com/community/UFW)

## ✅ Checklist Final

- [ ] VPS con Ubuntu instalado y actualizado
- [ ] Docker y Docker Compose instalados
- [ ] Firewall configurado (puertos 22, 9000, 9001 abiertos)
- [ ] Repositorio clonado en el VPS
- [ ] Par de llaves SSH generado
- [ ] Secretos configurados en GitHub:
  - [ ] VPS_HOST
  - [ ] VPS_USER
  - [ ] VPS_PATH
  - [ ] VPS_SSH_KEY
- [ ] Deployment manual exitoso
- [ ] CI/CD automático probado y funcionando
- [ ] Aplicación accesible desde internet

---

**¡Listo!** Tu calculadora ahora se deploya automáticamente cada vez que hagas push a master. 🎉
