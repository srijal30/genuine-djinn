from app import ChatApp
import asyncio
import threading


async def message_sender(app):
    for i in range(10):
        await asyncio.sleep(1)
        app.receive_message({'author': {'name': 'sender'}, 'content': f'testing {i}'})


if __name__ == "__main__":
    application = ChatApp()
    routine = message_sender(application)
    t = threading.Thread( target=asyncio.run, args=(routine,) )
    t.start()
    application.mainloop()
