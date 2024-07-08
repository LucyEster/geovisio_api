from pydantic import BaseModel, Base64Bytes, Base64UrlBytes 
from typing import Optional, List
from model.geo_catalog import GeoCatalog
from model.coordinate import Coordinate
from base64 import b64encode
from json import dumps


class GeoCatalogSchema(BaseModel):
    """ Define como um novo catálogo a ser inserido deve ser representado
    """
    title: str = "Title Example"
    description: str = "This is an example of description of a geographic catalog."
    img_source: Base64UrlBytes = b'VGhpcyBpcyB0aGUgd2F5'
    hashtag: str = "#example"
    latitude: float = -23.3528444
    longitude: float = -44.7228947
    name: str = "example"
    contact: str = "exampple"
    city: str = "example"
    region: str = "example"
    country: str = "example"


class SearchGeoCatalogSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base na hashtag associada.
    """
    hashtag: Optional[str] = None
    region: Optional[str] = None

class DeleteGeoCatalogSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a remoção. Que será
        feita apenas com base no id associado.
    """
    id: Optional[int] = None


class ViewGeoCatalogsSchema(BaseModel):
    """ Define como uma listagem de catálogos geográficos será retornada.
    """
    geo_catalogs:List[GeoCatalogSchema]

class ViewHashtagsSchema(BaseModel):
    """ Define como uma listagem de hashtags será retornada.
    """
    hashtags:List[str]

def show_geo_catalogs(geo_catalogs_with_coordinate: List[Coordinate]):
    """ Retorna uma representação dos catálogos seguindo o schema definido em
        GeoCatalog.
    """
    result = []
    for coordinate in geo_catalogs_with_coordinate:
        for geo_catalog in coordinate.geo_catalogs:
            result.append({
                "id": int(geo_catalog.id),
                "title": str(geo_catalog.title),
                "name": str(coordinate.name),
                "contact": str(coordinate.contact),
                "city": str(coordinate.city),
                "region": str(coordinate.region),
                "country": str(coordinate.country),
                "description": str(geo_catalog.description),
                "hashtag": str(geo_catalog.hashtag),
                "created_at": str(geo_catalog.created_at),
                "img_source": b64encode(geo_catalog.img_source).decode('utf-8'),
                "longitude": float(coordinate.longitude),
                "latitude": float(coordinate.latitude) 
            })
    return {"geo_catalogs": result}


class GeoCatalogViewSchema(BaseModel):
    """ Define como um catálogo geográfico será retornado: informações + coordenadas.
    """
    id: int = 1
    title: str = "Title Example"
    description: str = "This is an example of description of a geographic catalog."
    img_source: Base64UrlBytes = b'VGhpcyBpcyB0aGUgd2F5'
    hashtag: str = "#example"


def show_geo_catalog(geo_catalog: GeoCatalog):
    """ Retorna uma representação do catálogo geográfico seguindo schema definido em
        GeoCatalogViewSchema.
    """
    return {
        "id": geo_catalog.id,
        "title": geo_catalog.title,
        "description": geo_catalog.description,
        "hashtag": geo_catalog.hashtag
    }
