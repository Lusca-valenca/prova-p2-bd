
## Como subir (com Docker)
1. Rode:
   ```
   docker-compose up --build
   ```
2. A API estará em `http://localhost:8000/docs`. Dashboard do RabbitMQ: `http://localhost:15672` (guest/guest).

## Endpoints
- POST /corridas
- GET /corridas
- GET /corridas/{forma_pagamento}
- GET /saldo/{motorista}

## Exemplo payload POST /corridas
{
  "passageiro": { "nome": "João", "telefone": "99999-1111" },
  "motorista": { "nome": "Carla", "nota": 4.8 },
  "origem": "Centro",
  "destino": "Inoã",
  "valor_corrida": 35.50,
  "forma_pagamento": "DigitalCoin"
}

