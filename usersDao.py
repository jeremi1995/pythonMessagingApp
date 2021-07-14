import yaml

class UsersDao:
    def __init__(self):
        self.write_lock = False
    
    def acquire_lock(self):
        while self.write_lock:
            continue
        self.write_lock = True
    
    def release_lock(self):
        # Release the write lock
        self.write_lock = False

    def rewriteFile(self, fileObject):
        # Open and write to file
        with open("database/conversations.yaml", "w") as rC:
            rC.write(yaml.dump(fileObject))

    def authenticate(self, params):
        # 0: User found
        # 1: username or password incorrect
        with open("database/users.yaml", "r") as usersFile:
            users = yaml.load(usersFile.read())
            for user in users:
                if user["username"] == params["username"] and user["password"] == params["password"]:
                    return 0
        return 1

    def userExists(self, params):
        # 0: user exists
        # 1: user doesn't exist
        with open("database/users.yaml", "r") as usersFile:
            users = yaml.load(usersFile.read())
            for user in users:
                if user["username"] == params["username"]:
                    return 0
        return 1

    def signUp(self, params):
        # 0: Sign up successful
        # 1: User already exists
        retVal = 0

        self.acquire_lock()
        
        # Look for the users in users.json:
        with open("database/users.yaml", "r") as usersFile:
            users = yaml.load(usersFile.read())
            for user in users:
                if user["username"] == params["username"]:
                    retVal = 1
                    break
        
        if (retVal == 0):
            with open("database/users.yaml", "a") as usersFile:
                usersFile.write(yaml.dump([{"username": params["username"], "password": params["password"]}]))

        self.release_lock()

        return retVal
