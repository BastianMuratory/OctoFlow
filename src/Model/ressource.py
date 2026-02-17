class Resource:
    def __init__(self, resource_id: str, name: str, status: int = 0, description: str = ""):
        self.resource_id = resource_id
        self.name = name
        self.status = status
        self.description = description
    
    def set_id(self, resource_id: str) -> None:
        self.resource_id = resource_id
    
    def set_name(self, name: str) -> None:
        self.name = name
    
    def set_description(self, description: str) -> None:
        self.description = description

    def set_status(self, status: int) -> None:
       self.status = status
    
    def get_id(self) -> str:
        return self.resource_id
    
    def get_name(self) -> str:
        return self.name
    
    def get_description(self) -> str:
        return self.description

    def get_status(self) -> int:
        return self.status
    
    def __str__(self) -> str:
        return f"Resource(ID: {self.resource_id}, Name: {self.name}, Status: {self.status}, Description: {self.description})"