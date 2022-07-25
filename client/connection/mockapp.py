from typing import Any, Dict
from connection import SocketClient
import asyncio

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
        self.userid = 0

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
        io = int( input(msg) )
        print()
        await self.run_choice(io)

    async def run_choice(self, choice: int) -> None:
        await self.operations[choice]()

    async def register(self):
        print("REGISTERING:")
        username = input("what is your username: ")
        password = input("what is your password: ")
        self.userid = await self.connection.register(username, password)
        print("THE TYPE OF THE TAG:", type(self.userid))
        print("you have registered")
    
    async def login(self):
        print("LOGGIN IN:")
        username = input("what is your username: ")
        password = input("what is your password: ")
        success = await self.connection.login(username, self.userid, password)
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
        name = input("create a room name: ")
        roominfo = await self.connection.create_room(name)
        self.roomcode = roominfo[0]
        self.roomid = roominfo[1]
        print(f"you have created room named {name}")

    async def joinroom(self):
        print("JOINING A ROOM:")
        code = input("please enter the room code: ")
        self.roomid = await self.connection.join_room()
        print(f"you have joined the room with code {code}")

    async def connectroom(self):
        print("CONNECTING TO A ROOM:")
        success = await self.connection.connect_room(self.roomid)
        if success:
            self.connection.start_receive_messages(self.print_message)
            print("you have connected to room and can now send/receive messages")
        else:
            print("connecting to the room was not a success")

    async def listroom(self):
        print("LISTING ALL THE ROOMS YOU HAVE JOINED:")
        rooms = await self.connection.list_rooms()
        for room in rooms:
            print(room)
            print(rooms[room])
        print()

    async def sendmessage(self):
        message = input(">>>: ")
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

    def print_message(self, user: Dict[str, Any]):
        print( f"{user['username']}" )


if __name__ == "__main__":
    game = MockGame()
    asyncio.run( game.start_game() )