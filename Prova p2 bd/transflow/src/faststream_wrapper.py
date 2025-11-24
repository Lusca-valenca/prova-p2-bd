import asyncio
from aio_pika import connect_robust, Message, ExchangeType
import os
import json

RABBIT_URL = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@rabbitmq:5672/')

class FastStreamClient:
    def __init__(self):
        self._conn = None
        self._channel = None

    async def connect(self):
        if self._conn is None:
            self._conn = await connect_robust(RABBIT_URL)
            self._channel = await self._conn.channel()

    async def publish(self, exchange_name: str, routing_key: str, payload: dict):
        await self.connect()
        exchange = await self._channel.declare_exchange(exchange_name, ExchangeType.DIRECT, durable=True)
        msg = Message(json.dumps(payload).encode())
        await exchange.publish(msg, routing_key=routing_key)

    async def consume(self, queue_name: str, exchange_name: str, routing_key: str, callback):
        await self.connect()
        exchange = await self._channel.declare_exchange(exchange_name, ExchangeType.DIRECT, durable=True)
        queue = await self._channel.declare_queue(queue_name, durable=True)
        await queue.bind(exchange, routing_key)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    body = message.body.decode()
                    payload = json.loads(body)
                    await callback(payload)

faststream = FastStreamClient()
