from src import create_app

app = create_app()

# o sistema nao aceita CPF nao valido e nao unico 
# o sistema nao aceita agendamento em horarios ja ocupados
# o sistema nao aceita cadastro de animal sem cliente associado
# o sistema nao deixa deletar cliente com animais cadastrados