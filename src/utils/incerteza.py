class varFC:
    def __init__(self, name:str, value:bool, fc:float):
        self.name = name
        self.value = value
        self.fc = fc
    
    def get_name(self) -> str:
        return self.name
    
    def to_string(self):
        return  f'{self.name}: {self.value} (FC = {self.fc})'

    def set_fc(self, value:float):
        self.fc = value
