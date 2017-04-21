from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class PersonModel(Base):
	__tablename__ = 'person'
	person_id = Column(Integer, primary_key=True)
	name = Column(String(200), nullable=False)
	role = Column(String(50))
	office_space = Column(String(50), ForeignKey('room.name'))
	living_space = Column(String(50), ForeignKey('room.name'))

class RoomModel(Base):
	__tablename__ = 'room'
	id = Column(Integer, primary_key=True)
	name = Column(String(200))
	room_type = Column(String(50))
	people = relationship("PersonModel", foreign_keys=[PersonModel.office_space])
	people = relationship("PersonModel", foreign_keys=[PersonModel.living_space])

