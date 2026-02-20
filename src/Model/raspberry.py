from .ressource import Resource
from dataclasses import dataclass

@dataclass
class Raspberry(Resource):
	ip: str

	def __str__(self) -> str:
		return (
			f"Raspberry(ID: {self.id}, Name: {self.name}, "
			f"IP: {self.ip}, Status: {self.status}, Description: {self.description})"
		)
