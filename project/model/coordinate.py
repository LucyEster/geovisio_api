from sqlalchemy import Column, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base, GeoCatalog


class Coordinate(Base):
    __tablename__ = 'coordinates'

    id = Column("id_coordinate", Integer, primary_key=True)
    longitude = Column(Float(9,6))
    latitude = Column(Float(9,6))
    created_at = Column(DateTime, default=datetime.now())

    # Definindo relacionamento com os catálogos geográficos. Uma coordenada pode ter N catálogos.
    geo_catalogs = relationship("GeoCatalog")

    def __init__(self, longitude:float, latitude:float,
                 created_at:Union[DateTime, None] = None):
        """
        Cria uma coordenada

        Arguments:
            longitude: longitude da coordenada.
            latitude: latitude da coordenada.
            created_at: data de criação.
        """
        self.longitude = longitude
        self.latitude = latitude

        # se não for informada, será o data exata da inserção no banco
        if created_at:
            self.created_at = created_at

    def add_geo_catalog(self, geo_catalog: GeoCatalog):
        """ Adiciona um novo catálogo a coordenada.
        """
        self.geo_catalogs.append(geo_catalog)
