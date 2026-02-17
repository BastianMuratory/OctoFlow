from .ressource import Resource


class Battery(Resource):
	def __init__(self, resource_id: str, name: str, waterproof: bool, status: int = 0, description: str = ""):
		super().__init__(resource_id, name, status, description)
		self.waterproof = waterproof

	def set_waterproof(self, waterproof: bool) -> None:
		self.waterproof = waterproof

	def get_waterproof(self) -> bool:
		return self.waterproof

	def __str__(self) -> str:
		return (
			f"Battery(ID: {self.resource_id}, Name: {self.name}, "
			f"Waterproof: {self.waterproof}, Status: {self.status}, Description: {self.description})"
		)
