import asyncio
import json
from typing import Any

from loguru import logger
from redis.asyncio import Redis

from product_fusion_backend.core import email_service


class RedisService:
    @staticmethod
    async def connect() -> Redis:
        return Redis(
            host="localhost",
            port=6379,
            db=0,
        )

    @classmethod
    async def insert(cls, email: str, data: dict[str, Any], queue: bool = False) -> None:
        redis_client: Redis = await cls.connect()
        data["status"] = "queued"
        await redis_client.hset(
            f"email:{email}",
            mapping=data,
        )
        if queue:
            await cls.publish(data)

    @classmethod
    async def update(cls, email: str) -> None:
        redis_client: Redis = await cls.connect()
        await redis_client.hset(f"email:{email}", "status", "sent")

    @classmethod
    async def delete(cls, name: str) -> int:
        redis_client: Redis = await cls.connect()
        return await redis_client.hdel(f"email:{name}")

    @classmethod
    async def get(cls, email: str) -> dict[str, Any]:
        redis_client: Redis = await cls.connect()
        return await redis_client.hgetall(f"email:{email}")

    @classmethod
    async def publish(cls, data: dict[str, Any]) -> None:
        redis_client: Redis = await cls.connect()
        await redis_client.publish(
            "email-channel",
            json.dumps(data),
        )

    @classmethod
    async def subscribe(cls, channel: str) -> None:
        redis_client: Redis = await cls.connect()
        subscriber = redis_client.pubsub()
        await subscriber.subscribe(channel)
        logger.info(f"Subscribed to channel: {channel}")
        try:
            async for message in subscriber.listen():
                if message.get("type") == "message":
                    logger.info("Received message")
                    data = json.loads(message["data"])
                    if data:
                        logger.info(f"Sending email to: {data['email']}")
                        sent = await email_service.send_email(
                            data["email"],
                            data["subject"],
                            data["body"],
                        )
                        if sent:
                            logger.info("Email sent successfully.")
                            await cls.update(data["email"])
        except asyncio.CancelledError:
            logger.info("Subscription task was cancelled, shutting down subscription.")
            await subscriber.unsubscribe(channel)
        finally:
            await redis_client.close()

    @classmethod
    async def start_subscriber(cls, channel: str) -> None:
        cls.subscriber_task = asyncio.create_task(cls.subscribe(channel))

    @classmethod
    async def stop_subscriber(cls) -> None:
        if cls.subscriber_task:
            cls.subscriber_task.cancel()
            try:
                await cls.subscriber_task
            except asyncio.CancelledError:
                logger.info("Subscriber task cancelled successfully.")


redis_service = RedisService()
