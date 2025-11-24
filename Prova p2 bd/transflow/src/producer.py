import uuid
from src.faststream_wrapper import faststream
from src.models.corrida_model import CorridaEvento

EXCHANGE = 'transflow_exchange'
ROUTING_KEY = 'corrida_finalizada'

async def publish_corrida(payload: dict) -> dict:
    payload['id_corrida'] = payload.get('id_corrida') or str(uuid.uuid4())
    corrida = CorridaEvento(**payload)
    await faststream.publish(EXCHANGE, ROUTING_KEY, corrida.dict())
    return corrida.dict()
