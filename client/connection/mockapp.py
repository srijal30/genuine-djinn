import sys
from typing import Any, Dict
from connection import SocketClient
import asyncio


async def ainput(string: str) -> str:
    print(string)
    res = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
    return res[0:len(res)-1]


class MockGame():
    def __init__(self):
        self.operations = {
            0: self.register,
            1: self.login,
            2: self.createroom,
            3: self.logout,
            4: self.joinroom,
            5: self.connectroom,
            6: self.listroom,
            7: self.sendmessage,
            8: self.exitroom
        }

    async def establish_connection(self):
        self.connection = SocketClient()
        await self.connection.connect()

    async def start_game(self):
        await self.establish_connection()
        while True:
            await self.get_choice()

    async def get_choice(self) -> None:
        msg = """
        0: register
        1: login
        2: create room
        3: logout
        4: join a room
        5: connect to a room
        6: list rooms
        7: send message
        8: exit a room

        your choice: """
        io = int( await ainput(msg) )
        print()
        await self.run_choice(io)

    async def run_choice(self, choice: int) -> None:
        await self.operations[choice]()

    async def register(self):
        print("REGISTERING:")
        username = await ainput("what is your username: ")
        password = await ainput("what is your password: ")
        tag = await self.connection.register(username, password)
        print(f"your tag is: {tag}")
        print("you have registered")
        print("you are logged in!")
    
    async def login(self):
        print("LOGGIN IN:")
        username = await ainput("what is your username: ")
        password = await ainput("what is your password: ")
        tag = int( await ainput("what is your tag: "))
        success = await self.connection.login(username, tag, password)
        if success:
            print("you are now logged in!")
        else:
            print("login was not a success :(")

    async def logout(self):
        success = await self.connection.logout()
        if success:
            print("you are logged out!")
        else:
            print("log out unsuccessful!")

    async def createroom(self):
        print("CREATING A ROOM:")
        name = await ainput("create a room name: ")
        roominfo = await self.connection.create_room(name)
        self.roomcode = roominfo[0]
        self.roomid = roominfo[1]
        print(f"you have created room named {name}")

    async def joinroom(self):
        print("JOINING A ROOM:")
        code = await ainput("please enter the room code: ")
        self.roomid = await self.connection.join_room(code)
        print(f"you have joined the room with code {code}")

    async def connectroom(self):
        print("CONNECTING TO A ROOM:")
        id = int( await ainput("what is the id of the room you want to join: "))
        success = await self.connection.connect_room(id)
        if success:
            asyncio.create_task(self.connection.receive_messages(self.callback))
            print("you have connected to room and can now send/receive messages")
        else:
            print("connecting to the room was not a success")

    async def listroom(self):
        print("LISTING ALL THE ROOMS YOU HAVE JOINED:")
        rooms = await self.connection.list_rooms()
        for room in rooms:
            print(room)
        print()

    async def sendmessage(self):
        message = await ainput("what is your message: ")
        success = await self.connection.send_message(message)
        if success:
            print("message sent")
        else:
            print("message not sent")

    async def exitroom(self):
        print("EXITING THE ROOM: ")
        success = await self.connection.exit_room()
        if success:
            print("you have left the current room")
        else:
            print("error when leaving room")

    def callback(self, message: Dict[str, Any]):
        display = f"{message['author']['name']}: {message['content']}\n"
        with open("message.log", "a") as file:
            file.write(display)
        print(display)


if __name__ == "__main__":
    game = MockGame()
    asyncio.run( game.start_game() )