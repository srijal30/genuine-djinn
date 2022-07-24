from connection import SocketClient


class MockGame():
    def __init__(self):
        self.connection = SocketClient()
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

    def get_choice(self) -> None:
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
        """
        io = int( input() )
        self.run_choice(io)

    def run_choice(self, choice: int) -> None:
        self.operations[choice]()

    def register(self):
        username = input("what is your username: ")
        password = input("what is your password: ")
        self.userid = self.connection.register(username, password)
        print("you have registered")
    
    def login(self):
        username = input("what is your username: ")
        password = input("what is your password: ")
        success = self.connection.login(username, self.userid, password)
        if success:
            print("succesful login!")
        else:
            print("unsuccesful login!")

