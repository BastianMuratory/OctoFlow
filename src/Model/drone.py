from .ressource import Resource
from dataclasses import dataclass

@dataclass
class Drone(Resource):
	ip: str
	radio_type: str
	mesh: str
	bandwidth: str
	encryption: str
	encryption_key: str
	ir: str
	banane: bool
	serial_number: str
	controller_support: str
	controller_sd_card: str
	encoder: str
	encoder_sd_card: str
	antenna_coax: str
	waterproof: bool

	def __str__(self) -> str:
		return (
			f"Drone(ID: {self.id}, Name: {self.name}, "
			f"Waterproof: {self.waterproof}, IP: {self.ip}, "
			f"IR: {self.ir}, Mesh: {self.mesh}, Status: {self.status}, Description: {self.description})"
		)
