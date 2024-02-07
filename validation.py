
class Validation:
    def __init__(self):
        pass

    def validateName(self, name):
        if name.replace(' ', '') == '':
            print("Name can't be empty...")
            return False
        return True