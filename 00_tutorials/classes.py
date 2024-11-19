class Dog:
    static_var=15

    def __init__(self, name):
        self.name = name

    def __del__(self): 
        print(f"deconstructing {self}")

    def printDog(self):
        print(f"{self.name}-{self.static_var}")

dog = Dog("Test")
doggo = Dog("tseT")

dog.printDog()
doggo.printDog()
