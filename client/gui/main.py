import asyncio

from app import ChatApp


def start_app() -> None:
    """Start the app."""
    # create loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # create application
    application = ChatApp(loop)

    # run application forever
    application.update_loop()
    loop.run_forever()


if __name__ == "__main__":
    start_app()
