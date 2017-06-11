from sqlalchemy import Column, Integer, String, DateTime

from model.base import Base


class BusRoute(Base):
    __tablename__ = "bus_routes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    route_id = Column(Integer, unique=True, nullable=False)
    route_name = Column(String, nullable=False)
    route_type = Column(Integer, nullable=False)
    first_station_name = Column(String)
    last_station_name = Column(String)
    first_bus_time = Column(DateTime)
    last_bus_time = Column(DateTime)
    term = Column(Integer)

    def as_dict(self):
        return {
            'route_id': self.route_id,
            'route_name': self.route_name,
            'route_type': self.route_type,
            'first_station_name': self.first_station_name,
            'last_station_name': self.last_station_name,
            'first_bus_time': self.first_bus_time,
            'last_bus_time': self.last_bus_time,
            'term': self.term,
        }
