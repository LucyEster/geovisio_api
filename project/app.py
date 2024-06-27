from flask_openapi3 import OpenAPI, Info, Tag
from typing import Union
from flask import redirect
from urllib.parse import unquote
from sqlalchemy.orm import joinedload

from sqlalchemy.exc import IntegrityError

from model import Session, Coordinate, GeoCatalog
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="GeoVisio API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
coordinate_tag = Tag(name="Coordenada", description="Adição e visualização de coordenadas na base de dados sqlite.")
geo_catalog_tag = Tag(name="Catálogo geográfico", description="Adição e visualização de catálogos geográficos e informações relacionadas à eles na base de dados sqlite.")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.post('/coordinate', tags=[coordinate_tag],
          responses={"200": CoordinateViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_coordinate(form: CoordinateSchema):
    """Adiciona uma nova coordenada à base de dados.

    Retorna uma representação das coordenadas persistidas.
    """
    coordinate = Coordinate(
        latitude=form.latitude,
        longitude=form.longitude)
    logger.debug(f"Adicionando coordenada: '{coordinate.latitude, coordinate.longitude}'")
    try:
        session = Session()
        session.add(coordinate)
        session.commit()
        logger.debug(f"Adicionando coordenada: '{coordinate.latitude, coordinate.longitude}'")
        
        # retorna informação de inserção conforme especificado no schema.
        return view_coordinate(coordinate), 200

    except IntegrityError as e:
        # inicialmente uma mesma coordenada não deve ser cadastrada mais de uma vez
        error_msg = "Coordenada já salva na base!"
        logger.warning(f"Erro ao adicionar coordenada '{coordinate.latitude, coordinate.longitude}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar coordenada!"
        logger.warning(f"Erro ao adicionar coordenada '{coordinate.latitude, coordinate.longitude}', {error_msg}")
        return {"mesage": error_msg}, 400

@app.get('/coordinates', tags=[coordinate_tag],
         responses={"200": ViewCoordinatesSchema, "404": ErrorSchema})
def get_coordinates():
    """Faz a busca por todas as coordenadas cadastradas.

    Retorna uma representação da listagem de coordenadas (sem relação com outras entidades) encontradas na base.
    É uma representação simples de lista de latitudes e longitudes.
    """
    logger.debug(f"Coletando coordenadas ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    coordinates = session.query(Coordinate).all()

    if not coordinates:
        # se não há coordenadas cadastradas
        return {"coordinates": []}, 200
    else:
        logger.debug(f"%d coordenadas encontradas" % len(coordinates))
        # retorna a representação de coordenadas.
        return view_coordinates(coordinates), 200

@app.post('/geo_catalog', tags=[geo_catalog_tag],
          responses={"200": GeoCatalogViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_geo_catalog(form: GeoCatalogSchema):
    """Adiciona um novo catálogo geográfico à base de dados.

    Retorna uma representação do catálogo geográfico que é persistido, 
    embutido na relação com a coordenada relacionada.
    """
    geo_catalog = GeoCatalog(
        title=form.title,
        description=form.description,
        img_source=form.img_source,
        hashtag=form.hashtag
        )
    
    logger.debug(f"Adicionando catálogo geográfico: '{geo_catalog.title, geo_catalog.description}'")
    try:
        session = Session()

        coordinate = session.query(Coordinate).filter(Coordinate.latitude == form.latitude 
                                                      and Coordinate.longitude == form.longitude).first()
        coordinate.add_geo_catalog(geo_catalog)
        session.commit()
        logger.debug(f"Adicionando catálogo geográfico: '{geo_catalog.title, geo_catalog.description}'")
        return view_coordinate(coordinate), 200

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = e
        logger.warning(f"Erro ao adicionar catálogo geográfico '{geo_catalog.title, geo_catalog.description}', {error_msg}")
        return {"mesage": error_msg}, 400

@app.get('/geo_catalogs', tags=[geo_catalog_tag],
         responses={"200": ViewGeoCatalogsSchema, "404": ErrorSchema})
def get_geo_catalogs(query: SearchGeoCatalogSchema):
    """Faz a busca pelos catálogos cadastrados.

    Retorna uma representação da listagem de catálogos geográficos. 
    
    Caso haja parâmetro de busca, fará um filtro com a hashtag apresentada.
    Caso não haja parâmetro, todos os catálogos serão retornados.

    O retorno é completo, contemplando a relação entre coordenada e catálogo.
    """
    logger.debug(f"Coletando geo_catalogs ")

    session = Session()

    # fazendo a busca utilizando join entre Coordinate e Geocatalog
    if query.hashtag:
        geo_catalogs = session.query(Coordinate).join(
            GeoCatalog, Coordinate.geo_catalogs).filter(
            GeoCatalog.hashtag.contains(query.hashtag)).all()
    else:
        geo_catalogs = session.query(Coordinate).options(joinedload(Coordinate.geo_catalogs)).all()

    if not geo_catalogs:
        # se não há informação para retorno
        return {"geo_catalogs": []}, 200
    else:
        logger.debug(f"%d geo_catalogs encontrados" % len(geo_catalogs))
        # retorna a representação dos catálogos
        return show_geo_catalogs(geo_catalogs), 200

@app.delete('/geo_catalog', tags=[geo_catalog_tag],
         responses={"200": ViewGeoCatalogsSchema, "404": ErrorSchema})
def del_geo_catalogs(query: DeleteGeoCatalogSchema):
    """Faz a busca pelos catálogos cadastrados.

    Retorna uma representação da listagem de catálogos geográficos. 
    
    Caso haja parâmetro de busca, fará um filtro com a hashtag apresentada.
    Caso não haja parâmetro, todos os catálogos serão retornados.

    O retorno é completo, contemplando a relação entre coordenada e catálogo.
    """
    logger.debug(f"Coletando geo_catalogs ")

    session = Session()

    # fazendo a busca utilizando join entre Coordinate e Geocatalog
    if query.id:
        geo_catalog = session.query(GeoCatalog).filter(
            GeoCatalog.id == query.id).first()
        

    if not geo_catalog:
        # se não há informação para retorno
        return {"erro": f"não há catálogos com esse identificador (id: %)." % query.id}, 404
    else:
        try:
            session.delete(geo_catalog)
            session.commit()
            logger.debug(" geo_catalog %d removido" %  query.id)
            # retorna a representação dos catálogos
            return {"success": "Removido com sucesso."}, 200
        except Exception as e:
            # caso um erro fora do previsto
            error_msg = e
            logger.warning(f"Erro ao remover catálogo geográfico '{geo_catalog.title, geo_catalog.description}', {error_msg}")
            return {"mesage": error_msg}, 400
    
@app.get('/hashtags', tags=[geo_catalog_tag],
         responses={"200": ViewHashtagsSchema, "404": ErrorSchema})
def get_hashtags():
    """Faz a busca por todas as hashtags cadastradas.

    Retorna uma representação da listagem de hashtags (sem duplicação) encontradas na base.
    """
    logger.debug(f"Coletando hashtags")
    
    session = Session()

    hashtags = []
    for geo_catalog in session.query(GeoCatalog.hashtag).distinct():
        hashtags.append(geo_catalog.hashtag)

    if not hashtags:
        # se não há hashtags cadastradas
        return {"hashtags": []}, 200
    else:
        logger.debug(f"%d hashtags encontrados" % len(hashtags))
        # retorna a representação de hashtags
        return {"hashtags": hashtags}, 200