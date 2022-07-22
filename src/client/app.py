import websockets

DOMAIN = "ws://localhost:5000"
ROUTE = "/ws/"
URL = DOMAIN + ROUTE


async def login(username: str, password: str) -> None:
    """Wrapper function that sends login request to server"""
    async with websockets.connect(URL) as ws:
        await ws.recv()
        pass


# Register
async def register(username: str, password: str) -> None:
    """Wrapper function that sends register request to server"""
    async with websockets.connect(URL) as ws:
        await ws.recv()
        pass


# Send Message


# Receive Messages
