from .ressource import Resource
from dataclasses import dataclass

@dataclass
class GCS(Resource):
	ip: str
	radio_type: str
	api_port: str
	waterproof: bool

	def __str__(self) -> str:
		return (
			f"GCS(ID: {self.id}, Name: {self.name}, "
			f"Waterproof: {self.waterproof}, IP: {self.ip}, "
			f"API: {self.api}, Status: {self.status}, Description: {self.description})"
		)
