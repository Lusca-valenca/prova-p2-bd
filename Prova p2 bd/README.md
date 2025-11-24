1. Instalar as Dependências
pip install -r requirements.txt

Exemplo de conteúdo do arquivo requirements.txt:
```
fastapi
uvicorn
faststream[rabbit]
pymongo
redis
pydantic
```

Variáveis de Ambiente Necessárias

Crie um arquivo .env na raiz do projeto com as seguintes configurações:
```
# Configurações do RabbitMQ ou Kafka
BROKER_HOST=rabbitmq
BROKER_PORT=5672
BROKER_USER=guest
BROKER_PASS=guest

# Configurações do MongoDB
MONGO_URI=mongodb://mongo:27017
MONGO_DB=transflow_db

# Configurações do Redis
REDIS_HOST=redis
REDIS_PORT=6379
```
Execução com Docker
```
docker compose up --build
```

Este comando iniciará automaticamente:

  A API principal (FastAPI)

  O consumidor FastStream (RabbitMQ/Kafka)

  O MongoDB (para armazenar corridas)

  O Redis (para armazenar saldo dos motoristas)

  O RabbitMQ (ou Kafka) para mensageria

Acesse:

  API FastAPI: http://localhost:8000/docs

  Painel RabbitMQ: http://localhost:15672

  Usuário: guest | Senha: guest

Instruções de Uso e Testes:
  Criar uma corrida
```
POST http://localhost:8000/corridas/
{
  "id_corrida": "12345",
  "motorista": "Rodrigo",
  "passageiro": "Carla",
  "valor": 25.50,
  "status": "concluida"
}
```
 Consultar todas as corridas
```
GET http://localhost:8000/corridas/
```
  Consultar saldo de um motorista
```
GET http://localhost:8000/saldo/Lucas
```
  Verificação no RabbitMQ

Acesse http://localhost:15672
 e observe:

  Fila: corridas

  Ready: mensagens aguardando processamento

  Unacked: mensagens sendo processadas

  Acked: mensagens confirmadas

Se o Ready = 0, significa que as mensagens foram consumidas com sucesso.
