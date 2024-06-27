from pydantic import BaseModel
from typing import Optional, List
from model.coordinate import Coordinate

from schemas import GeoCatalogSchema


class CoordinateSchema(BaseModel):
    """ Define como uma nova coordenada a ser inserida deve ser representada
    """
    latitude: float = -23.3528444
    longitude: float = -44.7228947


class ViewCoordinatesSchema(BaseModel):
    """ Define como uma listagem de coordenadas será retornada.
    """
    coordinate:List[CoordinateSchema]


def view_coordinates(coordinates: List[Coordinate]):
    """ Retorna uma representação do da coordenada seguindo o schema definido em
        CoordinateViewSchema.
    """
    result = []
    for coordinate in coordinates:
        result.append({
            "latitude": float(coordinate.latitude),
            "longitude": float(coordinate.longitude),
            "created_at": str(coordinate.created_at)
        })
    return {"coordinates": result}

class CoordinateViewSchema(BaseModel):
    """ Define como uma coordenada será retornada: coordenada + catálogos.
    """
    id: int = 1
    latitude: float = -23.3528444
    longitude: float = -44.7228947
    geo_catalogs:List[GeoCatalogSchema]

class CoordinateDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    latitude: float
    longitude: float

def view_coordinate(coordinate: Coordinate):
    """ Retorna uma representação da coordenada seguindo o schema definido em
        CoordinateViewSchema.
    """
    return {
        "id": coordinate.id,
        "latitude": coordinate.latitude,
        "longitude": coordinate.longitude,
        "total_catalogs": len(coordinate.geo_catalogs),
        "geo_catalogs": [{"title": gc.title,
                          "description": gc.description,
                          "hashtag": gc.hashtag,
                          "created_at": gc.created_at
                          } for gc in coordinate.geo_catalogs]
    }
