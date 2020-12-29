import os

class User:
    # Constructor
    def __init__(self, UserName, Age):
        self._UserName = UserName
        self._Age = Age
    # Get UserName
    def GetUserInfo(self):
        return self._UserName, self._Age

def main():
    u1 = User("Luan", 20)
    print(u1.GetUserInfo())


if __name__ == '__main__':main()
