import redis.asyncio as redis
from typing import Optional
from domain.repositories import ICacheRepository
from config.settings import settings

class RedisCacheRepository(ICacheRepository):
    def __init__(self):
        self.redis_client = redis.from_url(settings.redis_url)
    
    async def get(self, key: str) -> Optional[str]:
        try:
            value = await self.redis_client.get(key)
            return value.decode('utf-8') if value else None
        except Exception as e:
            print(f"Redis get error: {e}")
            return None
    
    async def set(self, key: str, value: str, ttl: int = 3600) -> bool:
        try:
            await self.redis_client.setex(key, ttl, value)
            return True
        except Exception as e:
            print(f"Redis set error: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        try:
            result = await self.redis_client.delete(key)
            return result > 0
        except Exception as e:
            print(f"Redis delete error: {e}")
            return False
