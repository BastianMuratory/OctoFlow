from .ressource import Resource


class Drone(Resource):
	def __init__(
		self,
		resource_id: str,
		name: str,
		waterproof: bool,
		ip: str,
		ir: bool,
		mesh: str,
		status: int = 0,
		description: str = ""
	):
		super().__init__(resource_id, name, status, description)
		self.waterproof = waterproof
		self.ip = ip
		self.ir = ir
		self.mesh = mesh

	def set_waterproof(self, waterproof: bool) -> None:
		self.waterproof = waterproof

	def get_waterproof(self) -> bool:
		return self.waterproof

	def set_ip(self, ip: str) -> None:
		self.ip = ip

	def get_ip(self) -> str:
		return self.ip

	def set_ir(self, ir: bool) -> None:
		self.ir = ir

	def get_ir(self) -> bool:
		return self.ir

	def set_mesh(self, mesh: str) -> None:
		self.mesh = mesh

	def get_mesh(self) -> str:
		return self.mesh

	def __str__(self) -> str:
		return (
			f"Drone(ID: {self.resource_id}, Name: {self.name}, "
			f"Waterproof: {self.waterproof}, IP: {self.ip}, "
			f"IR: {self.ir}, Mesh: {self.mesh}, Status: {self.status}, Description: {self.description})"
		)
