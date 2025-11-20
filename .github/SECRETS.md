# GitHub Actions Secrets Configuration Guide

Este archivo contiene instrucciones para configurar los secretos necesarios en GitHub Actions.

## 🔐 Secretos Requeridos

### Para VPS Ubuntu (REQUERIDO - Deployment automático)

Estos secretos son **OBLIGATORIOS** para que el deployment automático al VPS funcione.

#### `VPS_HOST`

- **Descripción**: IP pública o dominio de tu VPS Ubuntu
- **Cómo obtenerlo**:
  1. Conéctate a tu VPS por SSH
  2. Ejecuta: `curl ifconfig.me`
  3. Copia la IP que aparece
- **Ejemplo**: `123.456.78.90` o `calculadora.tudominio.com`

#### `VPS_USER`

- **Descripción**: Usuario SSH para conectarse al VPS
- **Cómo obtenerlo**:
  1. Conéctate a tu VPS
  2. Ejecuta: `whoami`
  3. Copia el nombre de usuario
- **Ejemplo**: `ubuntu`, `root`, o tu usuario personalizado

#### `VPS_PATH`

- **Descripción**: Ruta completa (absoluta) donde está la aplicación en el VPS
- **Cómo obtenerlo**:
  1. Conéctate a tu VPS
  2. Navega al directorio de la app: `cd ~/calculadora-app`
  3. Ejecuta: `pwd`
  4. Copia la ruta completa
- **Ejemplo**: `/home/ubuntu/calculadora-app`

#### `VPS_SSH_KEY`

- **Descripción**: Llave privada SSH para autenticación sin password
- **Cómo obtenerlo**:
  1. Conéctate a tu VPS
  2. Genera una llave (si no tienes):
     ```bash
     ssh-keygen -t rsa -b 4096 -C "deploy-key" -f ~/.ssh/github_deploy_key -N ""
     ```
  3. Agrega la llave pública a authorized_keys:
     ```bash
     cat ~/.ssh/github_deploy_key.pub >> ~/.ssh/authorized_keys
     chmod 600 ~/.ssh/authorized_keys
     ```
  4. Muestra la llave privada:
     ```bash
     cat ~/.ssh/github_deploy_key
     ```
  5. Copia TODO el contenido (incluyendo BEGIN y END)
- **Formato**:
  ```
  -----BEGIN OPENSSH PRIVATE KEY-----
  b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABlwAAAAdzc2gtcn
  NhAAAAAwEAAQAAAYEAx... (múltiples líneas)
  -----END OPENSSH PRIVATE KEY-----
  ```
- ⚠️ **MUY IMPORTANTE**:
  - Copia TODO el contenido, desde `-----BEGIN` hasta `-----END`
  - Incluye todas las líneas intermedias
  - NO agregues espacios ni saltos de línea extra

### Resumen Rápido - Secretos VPS

Ejecuta estos comandos en tu VPS para obtener todos los valores:

```bash
# 1. VPS_HOST
echo "VPS_HOST: $(curl -s ifconfig.me)"

# 2. VPS_USER
echo "VPS_USER: $(whoami)"

# 3. VPS_PATH (estando en el directorio de la app)
cd ~/calculadora-app
echo "VPS_PATH: $(pwd)"

# 4. VPS_SSH_KEY (genera primero si no existe)
ssh-keygen -t rsa -b 4096 -C "deploy-key" -f ~/.ssh/github_deploy_key -N ""
cat ~/.ssh/github_deploy_key.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
echo "VPS_SSH_KEY (copia todo lo siguiente):"
cat ~/.ssh/github_deploy_key
```

---

### Para Codecov (Opcional - Reportes de cobertura)

**CODECOV_TOKEN**

- Descripción: Token para subir reportes de cobertura a Codecov
- Cómo obtenerlo:
  1. Ve a https://codecov.io/
  2. Inicia sesión con GitHub
  3. Agrega tu repositorio
  4. Copia el token desde Settings → General
- Ejemplo: `a1b2c3d4-e5f6-7890-abcd-ef1234567890`

### Para Docker Hub (Opcional - Solo si quieres publicar imágenes)

**DOCKER_USERNAME**

- Descripción: Tu nombre de usuario de Docker Hub
- Cómo obtenerlo: Es tu username en https://hub.docker.com/
- Ejemplo: `juanperez`

**DOCKER_PASSWORD**

- Descripción: Token de acceso de Docker Hub (NO uses tu password)
- Cómo obtenerlo:
  1. Ve a https://hub.docker.com/settings/security
  2. Click en "New Access Token"
  3. Dale un nombre descriptivo (ej: "GitHub Actions CI/CD")
  4. Selecciona permisos: Read, Write, Delete
  5. Copia el token generado (solo se muestra una vez)
- Ejemplo: `dckr_pat_AbCdEfGhIjKlMnOpQrStUvWx`

### Para AWS (Opcional - Deployment en AWS)

**AWS_ACCESS_KEY_ID**

- Descripción: ID de clave de acceso de AWS IAM
- Cómo obtenerlo:
  1. Ve a AWS Console → IAM
  2. Users → Tu usuario → Security credentials
  3. Create access key → Command Line Interface (CLI)
  4. Copia el Access key ID
- Ejemplo: `AKIAIOSFODNN7EXAMPLE`

**AWS_SECRET_ACCESS_KEY**

- Descripción: Clave secreta de acceso de AWS
- Cómo obtenerlo: Se muestra junto con el Access Key ID (una sola vez)
- Ejemplo: `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`

**AWS_REGION**

- Descripción: Región de AWS donde deployar
- Ejemplo: `us-east-1`

### Para Google Cloud (Opcional - Deployment en GCP)

**GCP_PROJECT_ID**

- Descripción: ID de tu proyecto en Google Cloud
- Cómo obtenerlo: Google Cloud Console → Dashboard → Project info
- Ejemplo: `mi-proyecto-12345`

**GCP_SA_KEY**

- Descripción: Service Account Key en formato JSON
- Cómo obtenerlo:
  1. Google Cloud Console → IAM & Admin → Service Accounts
  2. Create Service Account
  3. Grant permissions (Cloud Run Admin, etc.)
  4. Create Key → JSON
  5. Copia todo el contenido del archivo JSON
- Ejemplo: `{"type": "service_account", "project_id": "...", ...}`

### Para Kubernetes (Opcional - Deployment en K8s)

**KUBE_CONFIG**

- Descripción: Contenido del archivo kubeconfig en base64
- Cómo obtenerlo:
  ```bash
  cat ~/.kube/config | base64
  ```
- Ejemplo: `YXBpVmVyc2lvbjogdjEKY2x1c3RlcnM6Ci0gY2x1c3Rlcj...`

## 📝 Cómo Agregar Secretos en GitHub

### Método 1: Desde la interfaz web

1. Ve a tu repositorio en GitHub
2. Click en `Settings` (Configuración)
3. En el menú lateral, click en `Secrets and variables` → `Actions`
4. Click en el botón verde `New repository secret`
5. Ingresa:
   - **Name**: El nombre del secreto (ej: `DOCKER_USERNAME`)
   - **Secret**: El valor del secreto
6. Click en `Add secret`

### Método 2: Usando GitHub CLI

```bash
# Instalar GitHub CLI
# Windows: choco install gh
# Mac: brew install gh
# Linux: sudo apt install gh

# Autenticarse
gh auth login

# Agregar secretos
gh secret set DOCKER_USERNAME -b"tu-usuario-docker"
gh secret set DOCKER_PASSWORD -b"tu-token-docker"
gh secret set CODECOV_TOKEN -b"tu-token-codecov"
```

### Método 3: Usando la API de GitHub

```bash
# Requiere un token personal de GitHub con permisos repo
curl -X PUT \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: token YOUR_GITHUB_TOKEN" \
  https://api.github.com/repos/OWNER/REPO/actions/secrets/SECRET_NAME \
  -d '{"encrypted_value":"BASE64_ENCRYPTED_VALUE","key_id":"KEY_ID"}'
```

## ✅ Verificar Secretos Configurados

1. Ve a Settings → Secrets and variables → Actions
2. Verás una lista de todos los secretos configurados
3. No podrás ver los valores, solo los nombres
4. Puedes actualizar o eliminar secretos desde aquí

## 🔒 Mejores Prácticas de Seguridad

### ✅ DO (Hacer)

- ✅ Usa tokens en lugar de passwords
- ✅ Crea tokens con el mínimo privilegio necesario
- ✅ Rota los tokens regularmente (cada 3-6 meses)
- ✅ Usa secretos de entorno cuando sea posible
- ✅ Elimina secretos que ya no uses
- ✅ Documenta qué secretos usa cada workflow

### ❌ DON'T (No hacer)

- ❌ Nunca hagas commit de secretos en el código
- ❌ No uses passwords directamente (usa tokens)
- ❌ No compartas secretos entre múltiples workflows innecesariamente
- ❌ No uses secretos en logs o outputs
- ❌ No des permisos excesivos a los tokens

## 🧪 Probar sin Secretos

Si quieres probar el pipeline sin configurar todos los secretos:

### Opción 1: Comentar jobs que requieren secretos

En `.github/workflows/ci-cd.yml`:

```yaml
# deploy:
#   name: Deploy to Production
#   runs-on: ubuntu-latest
#   # ... resto del job comentado
```

### Opción 2: Usar condicionales

```yaml
deploy:
  name: Deploy to Production
  runs-on: ubuntu-latest
  if: ${{ secrets.DOCKER_USERNAME != '' }} # Solo ejecuta si el secreto existe
  steps:
    # ...
```

### Opción 3: Modo dry-run

Agrega una variable de entorno:

```yaml
env:
  DRY_RUN: true

- name: Deploy
  if: env.DRY_RUN != 'true'
  run: |
    # deployment steps
```

## 🔄 Actualizar Secretos

### Rotar un token

1. Genera un nuevo token en la plataforma (Docker Hub, AWS, etc.)
2. Ve a Settings → Secrets and variables → Actions
3. Click en el secreto que quieres actualizar
4. Click en "Update secret"
5. Pega el nuevo valor
6. Click en "Update secret"
7. **Revoca el token anterior** en la plataforma original

### Estrategia de rotación

```
1. Crear nuevo token → 2. Actualizar secreto en GitHub →
3. Probar workflow → 4. Revocar token anterior
```

## 📋 Checklist de Configuración

### Para CI/CD Básico (sin deployment)

- [ ] Repositorio creado en GitHub
- [ ] Código pusheado
- [ ] Workflow file en `.github/workflows/ci-cd.yml`
- [ ] ✅ No requiere secretos adicionales

### Para CI/CD con Coverage

- [ ] Cuenta en Codecov creada
- [ ] Repositorio agregado en Codecov
- [ ] `CODECOV_TOKEN` configurado en GitHub

### Para CI/CD con Docker Hub

- [ ] Cuenta en Docker Hub creada
- [ ] Access token generado
- [ ] `DOCKER_USERNAME` configurado
- [ ] `DOCKER_PASSWORD` configurado

### Para CI/CD con AWS

- [ ] Cuenta en AWS creada
- [ ] IAM user con permisos adecuados
- [ ] Access key creado
- [ ] `AWS_ACCESS_KEY_ID` configurado
- [ ] `AWS_SECRET_ACCESS_KEY` configurado
- [ ] `AWS_REGION` configurado

## 🆘 Troubleshooting

### Error: "Secret not found"

**Problema**: El workflow no encuentra un secreto

**Solución**:

1. Verifica que el nombre del secreto sea exactamente igual (case-sensitive)
2. Asegúrate de haber guardado el secreto
3. El secreto debe estar en "Repository secrets", no en "Environment secrets"

### Error: "Bad credentials" en Docker Hub

**Problema**: Falla el login a Docker Hub

**Solución**:

1. Verifica que `DOCKER_USERNAME` sea correcto
2. Asegúrate de usar un **access token**, no tu password
3. El token debe tener permisos Read, Write, Delete
4. Regenera el token si es necesario

### Error: "Codecov upload failed"

**Problema**: No se puede subir el reporte a Codecov

**Solución**:

1. Verifica que el token sea correcto
2. Asegúrate que el repositorio esté agregado en Codecov
3. El token debe ser un "Repository Upload Token"
4. Si falla, el workflow continuará (es opcional)

## 📚 Recursos Adicionales

- [GitHub Actions Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Docker Hub Access Tokens](https://docs.docker.com/docker-hub/access-tokens/)
- [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [Codecov Documentation](https://docs.codecov.com/docs)

## 📞 Ayuda

Si tienes problemas configurando los secretos:

1. Revisa los logs del workflow en la pestaña Actions
2. Verifica que el nombre del secreto sea correcto
3. Asegúrate de tener permisos de admin en el repositorio
4. Consulta la documentación oficial de la plataforma

---

**Nota**: Este es un archivo de documentación. Los valores de los secretos NUNCA deben estar en archivos versionados en Git.
