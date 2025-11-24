import os
import asyncio
from fastapi import FastAPI, HTTPException
from typing import List
import uvicorn

from src.producer import publish_corrida
from src.database.redis_client import get_saldo
from src.database.mongo_client import corridas_collection
from src.models.corrida_model import CorridaEvento

app = FastAPI(title='TransFlow API')

class CorridaIn(CorridaEvento):
    pass

@app.post('/corridas')
async def post_corrida(c: CorridaIn):
    payload = c.dict()
    try:
        published = await publish_corrida(payload)
        return { 'status': 'published', 'corrida': published }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/corridas', response_model=List[CorridaEvento])
async def get_corridas():
    docs = []
    cursor = corridas_collection.find()
    async for d in cursor:
        d.pop('_id', None)
        docs.append(d)
    return docs

@app.get('/corridas/{forma_pagamento}', response_model=List[CorridaEvento])
async def get_corridas_por_pagamento(forma_pagamento: str):
    docs = []
    cursor = corridas_collection.find({ 'forma_pagamento': forma_pagamento })
    async for d in cursor:
        d.pop('_id', None)
        docs.append(d)
    return docs

@app.get('/saldo/{motorista}')
async def saldo_motorista(motorista: str):
    s = await get_saldo(motorista)
    return { 'motorista': motorista, 'saldo': s }

if __name__ == '__main__':
    if os.getenv('START_CONSUMER', '0') == '1':
        from src.consumer import start_consumer
        import threading
        t = threading.Thread(target=lambda: asyncio.run(start_consumer()), daemon=True)
        t.start()
    uvicorn.run('src.main:app', host='0.0.0.0', port=8000)
