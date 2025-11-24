import asyncio
from src.faststream_wrapper import faststream
from src.database.redis_client import incr_saldo_atomic
from src.database.mongo_client import corridas_collection

EXCHANGE = 'transflow_exchange'
QUEUE = 'corrida_finalizada_queue'
ROUTING_KEY = 'corrida_finalizada'

async def process_corrida_event(payload: dict):
    motorista_nome = payload['motorista']['nome']
    valor = float(payload['valor_corrida'])

    novo_saldo = await incr_saldo_atomic(motorista_nome, valor)

    filtro = { 'id_corrida': payload['id_corrida'] }
    doc = { **payload, 'saldo_motorista_apos': novo_saldo }

    await corridas_collection.update_one(filtro, {'$set': doc}, upsert=True)
    print(f"Processado evento corrida {payload['id_corrida']} -> novo saldo {novo_saldo}")

async def start_consumer():
    await faststream.consume(QUEUE, EXCHANGE, ROUTING_KEY, process_corrida_event)

if __name__ == '__main__':
    asyncio.run(start_consumer())
