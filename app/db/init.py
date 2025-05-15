from tortoise import Tortoise
from app.config import settings

async def init_db():
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={"models": ["app.models.user", "app.models.notification"]}
    )
    await Tortoise.generate_schemas()
