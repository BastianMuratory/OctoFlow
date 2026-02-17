from .ressource import Resource


class Raspberry(Resource):
	def __init__(self, resource_id: str, name: str, ip: str, status: int = 0, description: str = ""):
		super().__init__(resource_id, name, status, description)
		self.ip = ip

	def set_ip(self, ip: str) -> None:
		self.ip = ip

	def get_ip(self) -> str:
		return self.ip

	def __str__(self) -> str:
		return (
			f"Raspberry(ID: {self.resource_id}, Name: {self.name}, "
			f"IP: {self.ip}, Status: {self.status}, Description: {self.description})"
		)
