from .ressource import Resource


class GCS(Resource):
	def __init__(
		self,
		resource_id: str,
		name: str,
		waterproof: bool,
		ip: str,
		api: str,
		status: int = 0,
		description: str = ""
	):
		super().__init__(resource_id, name, status, description)
		self.waterproof = waterproof
		self.ip = ip
		self.api = api

	def set_waterproof(self, waterproof: bool) -> None:
		self.waterproof = waterproof

	def get_waterproof(self) -> bool:
		return self.waterproof

	def set_ip(self, ip: str) -> None:
		self.ip = ip

	def get_ip(self) -> str:
		return self.ip

	def set_api(self, api: str) -> None:
		self.api = api

	def get_api(self) -> str:
		return self.api

	def __str__(self) -> str:
		return (
			f"GCS(ID: {self.resource_id}, Name: {self.name}, "
			f"Waterproof: {self.waterproof}, IP: {self.ip}, "
			f"API: {self.api}, Status: {self.status}, Description: {self.description})"
		)
