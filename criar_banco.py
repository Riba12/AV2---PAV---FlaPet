from main import app
from src.entities.Base import db
from src.entities.Agendamento import Agendamento
from src.entities.Animal import Animal
from src.entities.Cliente import Cliente
from src.entities.Servico import Servico
from src.entities.Especie import Especie
from src.entities.Raca import Raca
from sqlalchemy import inspect


with app.app_context():


    print("DEBUG: Tentando obter a versão do PGSQL...")
    db.session.execute(db.text("SELECT version();")).scalar()
    print("DEBUG: Conexão bem-sucedida. Executando DDL...")
    search_path_atual = db.session.execute(db.text("SHOW search_path;")).scalar()
    print(f"DEBUG: search_path atual da conexão: {search_path_atual}")
    
    db.drop_all()
    db.metadata.create_all(db.engine)
    db.session.commit()
        
    print("DEBUG: Schema criado com sucesso.")

    inspector = inspect(db.engine)
    tabelas_criadas = inspector.get_table_names()
    if 'cliente' in [t.lower() for t in tabelas_criadas]:
            print(f"DEBUG: Tabelas criadas: {tabelas_criadas}")
            print("\n✅ BANCO DE DADOS INICIALIZADO COM SUCESSO!")
            print("As tabelas foram criadas no seu banco Neon.")
    else:
            print("\n❌ FALHA AO CRIAR TABELAS.")
            print("O comando foi executado, mas as tabelas principais não foram detectadas no servidor Neon. Verifique se a URI no .env está 100% correta, sem erros de senha ou host.")