class Gopal:
    def __init__(self, itGatter):
           self.func=itGatter

    def __call__(self, *args):
        return self.func(*args)

@Gopal
def gopal1():
    return "Hi"

print(gopal1())