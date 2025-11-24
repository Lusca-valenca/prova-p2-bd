import os
import redis.asyncio as redis

REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

async def get_saldo(motorista: str) -> float:
    key = f"saldo:{motorista.lower()}"
    val = await redis_client.get(key)
    return float(val) if val is not None else 0.0

async def incr_saldo_atomic(motorista: str, valor: float) -> float:
    key = f"saldo:{motorista.lower()}"
    async with redis_client.pipeline() as pipe:
        while True:
            try:
                await pipe.watch(key)
                current = await pipe.get(key)
                current_f = float(current) if current is not None else 0.0
                new = current_f + float(valor)
                pipe.multi()
                pipe.set(key, new)
                await pipe.execute()
                return new
            except redis.WatchError:
                continue
            finally:
                try:
                    await pipe.reset()
                except Exception:
                    pass
