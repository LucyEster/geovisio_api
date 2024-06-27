from sqlalchemy import *
from datetime import datetime
from typing import Union
from sqlalchemy.orm import relationship

from  model import Base


class GeoCatalog(Base):
    __tablename__ = 'geo_catalogs'

    id = Column("id_geo_catalog",Integer, primary_key=True)
    title = Column(String(144))
    description = Column(String(3000))
    img_source = Column(BLOB, nullable=True)
    hashtag = Column(String(40))
    created_at = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o catálogo geográfico e uma coordenada.
    # Aqui está sendo definido a coluna 'coordenada' que vai guardar
    # a referencia a coordenada, a chave estrangeira que relaciona
    # uma coordenada a um catálogo geográfico.
    coordinate_id = Column(Integer, ForeignKey("coordinates.id_coordinate"), nullable=False)

    def __init__(self, title:str,
                 description:str,
                 img_source:LargeBinary,
                 hashtag:str,
                 created_at:Union[DateTime, None] = None):
        """
        Cria um catálogo geográfico.

        Arguments:
            title: título de um catálogo geográfico.
            description: descrição de um catálogo geográfico.
            hashtag: chave para acesso ao catálogo.
            img_source: imagem vinculada ao catálogo.
            created_at: data de inserção da informação geográfica.
        """
        self.title = title
        self.description = description
        self.img_source = img_source
        self.hashtag = hashtag

        if created_at:
            self.created_at = created_at

