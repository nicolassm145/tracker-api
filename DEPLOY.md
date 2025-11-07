# 🚀 Guia de Deploy - Backend + Banco de Dados na Nuvem

## 📋 Visão Geral
- **Banco de Dados:** Neon PostgreSQL (Gratuito)
- **Backend API:** Render (Gratuito)

---

## PARTE 1️⃣: Configurar o Banco de Dados (Neon)

### Passo 1: Criar conta no Neon
1. Acesse: https://neon.tech/
2. Clique em **"Sign Up"** e faça login com GitHub
3. Após o login, clique em **"Create a project"**

### Passo 2: Configurar o projeto
1. **Project name:** tracker-api-db (ou qualquer nome)
2. **Region:** Escolha o mais próximo (ex: US East - Ohio)
3. **PostgreSQL version:** 16 (ou mais recente)
4. Clique em **"Create Project"**

### Passo 3: Copiar a Connection String
1. Na dashboard do projeto, você verá a **Connection String**
2. Copie a string que começa com `postgresql://`
3. Ela será algo como:
   ```
   postgresql://usuario:senha@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```
4. **GUARDE ESSA STRING!** Vamos usar no próximo passo

---

## PARTE 2️⃣: Fazer Deploy do Backend (Render)

### Passo 1: Preparar o repositório Git
No seu terminal PowerShell, execute:

```powershell
# Inicializar git (se ainda não fez)
git init

# Adicionar todos os arquivos
git add .

# Fazer commit
git commit -m "Preparar para deploy"

# Criar repositório no GitHub e fazer push
# (Vá em github.com, crie um novo repositório "tracker-api")
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/tracker-api.git
git push -u origin main
```

### Passo 2: Criar conta no Render
1. Acesse: https://render.com/
2. Clique em **"Get Started"** e faça login com GitHub
3. Autorize o Render a acessar seus repositórios

### Passo 3: Criar Web Service
1. No dashboard do Render, clique em **"New +"** → **"Web Service"**
2. Conecte o repositório **tracker-api**
3. Configure:
   - **Name:** tracker-api
   - **Region:** Oregon (US West) ou mais próximo
   - **Branch:** main
   - **Root Directory:** (deixe vazio)
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** Free

### Passo 4: Adicionar Variáveis de Ambiente
Na seção **"Environment Variables"**, clique em **"Add Environment Variable"** e adicione:

```
DATABASE_URL = sua_connection_string_do_neon_aqui
SECRET_KEY = sua_chave_secreta (use o token gerado antes)
STEAM_API_KEY = sua_steam_key
PSN_API_KEY = sua_psn_key (ou deixe vazio)
XBOX_API_KEY = sua_xbox_key (ou deixe vazio)
IGDB_CLIENT_ID = seu_client_id
TWITCH_CLIENT_SECRET = seu_client_secret
IGDB_ACCESS_TOKEN = seu_access_token
```

### Passo 5: Deploy!
1. Clique em **"Create Web Service"**
2. Aguarde o build (pode levar 5-10 minutos)
3. Quando terminar, você verá a URL da sua API:
   ```
   https://tracker-api-xxxx.onrender.com
   ```

---

## PARTE 3️⃣: Inicializar o Banco de Dados

### Opção A: Criar tabelas via código Python
Crie um arquivo `init_db.py` na raiz do projeto:

```python
from app.database.database import Base, engine
from app.models.user_model import User

# Criar todas as tabelas
Base.metadata.create_all(bind=engine)
print("✅ Tabelas criadas com sucesso!")
```

Execute localmente apontando para o banco Neon:
```powershell
python init_db.py
```

### Opção B: Via SQL direto no Neon
1. No dashboard do Neon, vá em **"SQL Editor"**
2. Execute os comandos SQL para criar suas tabelas

---

## ✅ PARTE 4️⃣: Testar a API

### Teste local da conexão com Neon:
1. Atualize seu `.env` local com a DATABASE_URL do Neon
2. Rode localmente: `python run.py`
3. Acesse: http://127.0.0.1:8000/docs

### Teste a API em produção:
1. Acesse: `https://sua-api.onrender.com/docs`
2. Teste os endpoints

---

## 🔧 PARTE 5️⃣: Configurações Extras (Importante!)

### Habilitar CORS para o Frontend
Edite `app/main.py` e adicione:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique o domínio do frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📝 Checklist Final

- [ ] Banco de dados Neon criado e connection string copiada
- [ ] Código commitado e pushed para GitHub
- [ ] Web Service criado no Render
- [ ] Variáveis de ambiente configuradas no Render
- [ ] Deploy concluído com sucesso
- [ ] Tabelas do banco criadas
- [ ] API testada e funcionando
- [ ] CORS configurado

---

## 🆘 Problemas Comuns

### Build falha no Render:
- Verifique se o `requirements.txt` está correto
- Veja os logs de build no Render

### Erro de conexão com banco:
- Verifique se a DATABASE_URL está correta
- Certifique-se de incluir `?sslmode=require` no final da string

### API não responde:
- Verifique os logs no Render
- Certifique-se que todas as variáveis de ambiente estão configuradas

---

## 🎯 Próximos Passos

Depois que a API estiver funcionando:
1. Anote a URL da API do Render
2. Use essa URL no seu frontend para fazer as requisições
3. No frontend, substitua `http://localhost:8000` pela URL do Render

**URL da API será algo como:**
```
https://tracker-api-xxxx.onrender.com
```
