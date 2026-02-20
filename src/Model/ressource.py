from dataclasses import dataclass

@dataclass
class Resource:
    id:int
    name:str
    status:int
    description:str
    
    def __str__(self) -> str:
        return f"Resource(ID: {self.id}, Name: {self.name}, Status: {self.status}, Description: {self.description})"