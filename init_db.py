from app.database.database import Base, engine
from app.models.user_model import User

# Criar todas as tabelas
Base.metadata.create_all(bind=engine)
print("✅ Tabelas criadas com sucesso no banco de dados!")
