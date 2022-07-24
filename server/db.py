from prisma import Prisma

# db should be in this file to stop circular dependency issues

db = Prisma()

SYSTEM_NAME: str = "_SYSTEM"


async def make_system():
    """Initalizes the system user."""
    system = await db.user.find_unique({"id": 0})

    if system:
        return

    await db.user.create(
        {
            "id": 0,
            "name": SYSTEM_NAME,
            "password": "null",
            "tag": 0,
        }
    )
