from connection import SocketClient
import asyncio

class MockGame():
    def __init__(self):
        self.operations = {
            0: self.register,
            1: self.login,
            # 2: self.createroom,
            # 3: self.logout,
            # 4: self.joinroom,
            # 5: self.connectroom,
            # 6: self.listroom,
            # 7: self.sendmessage,
            # 8: self.exitroom
        }

    async def establish_connection(self):
        self.connection = SocketClient()
        await self.connection.connect()

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
        await self.run_choice(io)

    async def run_choice(self, choice: int) -> None:
        await self.operations[choice]()

    async def register(self):
        username = input("what is your username: ")
        password = input("what is your password: ")
        self.userid = await self.connection.register(username, password)
        print("you have registered")
    
    async def login(self):
        username = input("what is your username: ")
        password = input("what is your password: ")
        success = await self.connection.login(username, self.userid, password)
        if success:
            print("succesful login!")
        else:
            print("unsuccesful login!")

    async def start_game(self):
        await game.establish_connection()
        while True:
            await self.get_choice()


if __name__ == "__main__":
    game = MockGame()
    asyncio.run( game.start_game() )