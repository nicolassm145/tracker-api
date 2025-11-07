# Comandos para corrigir o deploy

## Execute no terminal:

```powershell
git add .
git commit -m "Fix: Force Python 3.11.6 and update psycopg2"
git push origin main
```

## Se ainda não funcionar no Render:

### Opção 1: Limpar Build Cache no Render
1. Vá nas configurações do seu Web Service no Render
2. Clique em "Manual Deploy" → "Clear build cache & deploy"

### Opção 2: Configurar Python Version nas Settings do Render
1. No dashboard do Render, vá em Settings
2. Procure por "Environment"
3. Adicione uma variável de ambiente:
   - Key: `PYTHON_VERSION`
   - Value: `3.11.6`
4. Clique em "Save Changes"
5. Faça um novo deploy

### Opção 3: Especificar no Build Command
No Render, mude o Build Command para:
```
./build.sh
```

E certifique-se que o Start Command é:
```
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## O que foi alterado:
✅ runtime.txt → python-3.11.6
✅ .python-version → 3.11.6 (novo arquivo)
✅ psycopg2-binary → 2.9.10 (mais recente)
✅ build.sh → adiciona limpeza de cache
✅ sqlalchemy → 2.0.35

## Verificar depois do deploy:
Acesse: https://sua-api.onrender.com/docs
