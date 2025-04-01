
def reload(func):
    def wrapper():
        print("Reloading the Weapon...")
        func()
    return wrapper

def select(func):
    def wrapper():
        print("Selecting the Weapon...")
        func()
        
    return wrapper

@select
@reload
def fire():
    print("Firing started!!!")

fire()