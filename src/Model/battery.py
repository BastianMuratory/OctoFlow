from .ressource import Resource
from dataclasses import dataclass

@dataclass
class Battery(Resource):
	waterproof: bool
	serial_number: str

	def __str__(self) -> str:
		return (
			f"Battery(ID: {self.id}, Name: {self.name}, "
			f"Waterproof: {self.waterproof}, Status: {self.status}, Description: {self.description})"
		)
