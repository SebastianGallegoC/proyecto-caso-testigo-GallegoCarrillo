# 🚀 GUÍA RÁPIDA: Deployment VPS Ubuntu

**Tiempo estimado**: 15-30 minutos

## ✅ Pre-requisitos

- VPS con Ubuntu (tu IP, usuario, y llave privada SSH)
- Repositorio en GitHub

---

## 📝 PASO A PASO

### 1️⃣ Preparar el VPS (Solo la primera vez)

**Desde tu computadora local**, copia el script de setup al VPS:

```bash
# Reemplaza valores con los tuyos
IP_VPS="123.456.78.90"
USUARIO="ubuntu"
LLAVE_PRIVADA="ruta/a/tu-llave.pem"

# Copiar script
scp -i $LLAVE_PRIVADA setup-vps.sh $USUARIO@$IP_VPS:~/

# Conectar y ejecutar
ssh -i $LLAVE_PRIVADA $USUARIO@$IP_VPS
chmod +x setup-vps.sh
./setup-vps.sh
```

El script instalará Docker, Git, y configurará todo automáticamente.

---

### 2️⃣ Obtener Valores para GitHub Secrets

**Dentro del VPS**, ejecuta esto:

```bash
# Te dará TODOS los valores que necesitas
cd ~/calculadora-app

echo "=========================================="
echo "COPIA ESTOS VALORES A GITHUB SECRETS:"
echo "=========================================="
echo ""
echo "VPS_HOST: $(curl -s ifconfig.me)"
echo "VPS_USER: $(whoami)"
echo "VPS_PATH: $(pwd)"
echo ""
echo "VPS_SSH_KEY (copia TODO desde BEGIN hasta END):"
echo "----------------------------------------"
cat ~/.ssh/github_deploy_key
echo "----------------------------------------"
echo ""
```

---

### 3️⃣ Configurar GitHub Secrets

1. Ve a tu repo en GitHub
2. **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"**
4. Agrega cada secreto:

| Nombre        | Valor                  | Descripción                              |
| ------------- | ---------------------- | ---------------------------------------- |
| `VPS_HOST`    | Tu IP del VPS          | Ej: `123.456.78.90`                      |
| `VPS_USER`    | Usuario SSH            | Ej: `ubuntu`                             |
| `VPS_PATH`    | Ruta de la app         | Ej: `/home/ubuntu/calculadora-app`       |
| `VPS_SSH_KEY` | Llave privada completa | Todo desde `-----BEGIN` hasta `-----END` |

**⚠️ IMPORTANTE**: Para `VPS_SSH_KEY`, copia TODO el contenido incluyendo:

```
-----BEGIN OPENSSH PRIVATE KEY-----
(todas las líneas)
-----END OPENSSH PRIVATE KEY-----
```

---

### 4️⃣ Primer Deployment Manual

**En el VPS**, verifica que todo funciona:

```bash
cd ~/calculadora-app
git pull origin master
docker-compose build --no-cache
docker-compose up -d

# Verificar
docker-compose ps
curl http://localhost:9000/health
```

**Desde tu navegador**:

- Frontend: `http://TU_IP:9001`
- Backend API: `http://TU_IP:9000/docs`

---

### 5️⃣ Activar CI/CD Automático

Desde tu computadora local:

```bash
# Haz un cambio pequeño
git add .
git commit -m "test: Activar CI/CD"
git push origin master
```

Ve a GitHub → pestaña **Actions** para ver el deployment automático.

---

## 🎯 Comandos Útiles en el VPS

```bash
# Ver logs
docker-compose logs -f

# Reiniciar servicios
docker-compose restart

# Detener todo
docker-compose down

# Actualizar manualmente
cd ~/calculadora-app
git pull origin master
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## 🆘 Troubleshooting Rápido

### Error: "Permission denied (publickey)"

```bash
# Verifica que la llave esté en authorized_keys
cat ~/.ssh/authorized_keys
```

### Error: "Cannot connect to Docker daemon"

```bash
# Inicia Docker
sudo systemctl start docker

# Agregar usuario al grupo docker
sudo usermod -aG docker $USER
# Luego sal y vuelve a entrar (exit y ssh de nuevo)
```

### Error: "Port already in use"

```bash
# Ver qué está usando el puerto
sudo netstat -tulpn | grep -E '9000|9001'

# Detener contenedores
docker-compose down
```

---

## 📋 Checklist Final

- [ ] Script `setup-vps.sh` ejecutado en el VPS
- [ ] Docker y Git instalados en el VPS
- [ ] Repositorio clonado en `~/calculadora-app`
- [ ] Secretos configurados en GitHub:
  - [ ] VPS_HOST
  - [ ] VPS_USER
  - [ ] VPS_PATH
  - [ ] VPS_SSH_KEY (completo con BEGIN y END)
- [ ] Deployment manual exitoso
- [ ] Aplicación accesible en `http://TU_IP:9001`
- [ ] Push a GitHub activa deployment automático

---

## 🎉 ¡Listo!

Tu aplicación ahora se deploya automáticamente cada vez que haces push a master.

**URLs de tu app:**

- Frontend: `http://TU_IP_VPS:9001`
- Backend: `http://TU_IP_VPS:9000`
- API Docs: `http://TU_IP_VPS:9000/docs`

Para más detalles, consulta `DEPLOYMENT.md`
