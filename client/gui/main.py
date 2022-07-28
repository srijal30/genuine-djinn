import asyncio

from app import ChatApp

if __name__ == "__main__":
    # create loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # create application
    application = ChatApp(loop)

    application.update_loop()
    loop.run_forever()
