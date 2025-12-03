# Tracker API

API REST para rastreamento de jogos e conquistas entre múltiplas plataformas (Steam, PlayStation, Xbox e IGDB). 

## Sobre o Projeto

O Tracker API é uma aplicação backend que permite aos usuários rastrear seus jogos e conquistas em diferentes plataformas de gaming. A API integra com múltiplos serviços:

- **Steam**: Jogos, conquistas, estatísticas
- **PlayStation Network**: Perfil, troféus
- **Xbox**: XUID, conquistas, jogos
- **IGDB**: Base de dados de jogos, lançamentos, trending

##  Tecnologias

- **[FastAPI](https://fastapi.tiangolo.com/)** - Framework web moderno e rápido
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - ORM Python
- **[PostgreSQL](https://www.postgresql.org/)** - Banco de dados relacional
- **[Pydantic](https://docs.pydantic.dev/)** - Validação de dados
- **[JWT](https://jwt.io/)** - Autenticação via tokens
- **[Uvicorn](https://www.uvicorn.org/)** - Servidor ASGI

## Estrutura do Projeto

```
tracker-api/
├── app/
│   ├── config.py              # Configurações e variáveis de ambiente
│   ├── main.py                # Aplicação principal FastAPI
│   ├── database/
│   │   └── database.py        # Configuração do SQLAlchemy
│   ├── models/
│   │   └── user_model.py      # Modelos de banco de dados
│   ├── routes/
│   │   ├── user_routes.py     # Endpoints de autenticação
│   │   ├── steam_routes.py    # Endpoints Steam
│   │   ├── playstation_routes.py  # Endpoints PSN
│   │   ├── xbox_routes.py     # Endpoints Xbox
│   │   └── igdb_routes.py     # Endpoints IGDB
│   ├── schemas/
│   │   └── user_schema.py     # Schemas Pydantic
│   ├── services/
│   │   ├── user_service.py    # Lógica de negócio de usuários
│   │   ├── steam_service.py   # Integração Steam API
│   │   ├── playstation_service.py  # Integração PSN API
│   │   ├── xbox_service.py    # Integração Xbox API
│   │   └── igdb_service.py    # Integração IGDB API
│   └── utils/
│       └── security.py        # JWT, hashing de senhas
├── .env                       # Variáveis de ambiente (não commitar)
├── .env.example               # Template de variáveis de ambiente
├── requirements.txt           # Dependências Python
├── runtime.txt                # Versão Python para deploy
├── build.sh                   # Script de build para Render
├── run.py                     # Script para rodar localmente
├── init_db.py                 # Script para inicializar banco
└── get_igdb_token.py          # Gerar token IGDB
```

## 🔧 Instalação e Configuração

### Pré-requisitos

- Python 3.11+
- PostgreSQL 14+
- Git

### 1. Clone o repositório

```bash
git clone https://github.com/nicolassm145/tracker-api.git
cd tracker-api
```

### 2. Crie e ative o ambiente virtual

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Copie o arquivo `.env.example` para `.env` e preencha com suas credenciais:

```bash
cp .env.example .env
```

Edite o arquivo `.env`:

```env
# Database
DATABASE_URL=postgresql://usuario:senha@localhost:5432/tracker_db

# Security
SECRET_KEY=sua_chave_secreta_super_segura

# Steam API
STEAM_API_KEY=sua_steam_api_key

# PlayStation Network API
PSN_API_KEY=sua_psn_api_key

# Xbox API
XBOX_API_KEY=sua_xbox_api_key

# IGDB (Twitch) API
IGDB_CLIENT_ID=seu_igdb_client_id
TWITCH_CLIENT_SECRET=seu_twitch_client_secret
IGDB_ACCESS_TOKEN=seu_igdb_access_token
```

### 5. Configure o banco de dados

**Criar banco PostgreSQL:**

```bash
createdb tracker_db
```

**Inicializar tabelas:**

```bash
python init_db.py
```

### 6. Execute a aplicação

```bash
python run.py
```

A API estará disponível em: `http://localhost:8000`

Documentação interativa: `http://localhost:8000/docs`

##  Como Obter as API Keys

### Steam API Key

1. Acesse: https://steamcommunity.com/dev/apikey
2. Faça login e registre sua aplicação
3. Copie a API Key gerada

### IGDB (Twitch) API

1. Acesse: https://dev.twitch.tv/console/apps
2. Crie uma nova aplicação
3. Copie o **Client ID** e **Client Secret**
4. Execute: `python get_igdb_token.py` para gerar o token

### PlayStation Network

- Use a biblioteca PSNAWP (já incluída)
- Configure sua PSN API Key

### Xbox

- Registre uma aplicação no Azure AD ou use serviços como OpenXBL

### Secret Key (JWT)

Gere uma chave segura:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Endpoints Principais

### Autenticação

- `POST /users/register` - Criar nova conta
- `POST /users/login` - Login (retorna JWT token)
- `GET /users/me` - Dados do usuário autenticado

### Steam

- `GET /steam/profile/{steam_id}` - Perfil do usuário
- `GET /steam/games/{steam_id}` - Lista de jogos
- `GET /steam/achievements/{steam_id}/{app_id}` - Conquistas de um jogo

### PlayStation

- `GET /playstation/profile/{online_id}` - Perfil PSN

### Xbox

- `GET /xbox/xuid/{gamertag}` - Obter XUID
- `GET /xbox/achievements/{xuid}` - Conquistas do usuário

### IGDB

- `GET /igdb/games/search` - Buscar jogos
- `GET /igdb/games/trending` - Jogos em alta
- `GET /igdb/games/upcoming` - Próximos lançamentos

##  Deploy

### Render (Recomendado)

1. Faça push do código para o GitHub
2. Crie uma conta no [Render](https://render.com/)
3. Crie um novo **Web Service**
4. Conecte seu repositório GitHub
5. Configure as variáveis de ambiente
6. Deploy automático!

### Banco de Dados: Neon PostgreSQL

1. Crie conta no [Neon](https://neon.tech/)
2. Crie um novo projeto
3. Copie a connection string
4. Configure no Render como variável `DATABASE_URL`

##  Testes

Acesse a documentação interativa em `/docs` para testar todos os endpoints:

```
https://sua-api.onrender.com/docs
```

##  Licença

Este projeto está sob a licença MIT.

##  Autores

- **Nicolas** - [nicolassm145](https://github.com/nicolassm145)
- **Pedro** - [IamPedrin](https://github.com/IamPedrin)

