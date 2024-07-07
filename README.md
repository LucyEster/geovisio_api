
# GeoVisio API

  

Esta API tem por princípio realizar a **manipulação de dados** com **base geográfica**.

  

À partir de **coordenadas**, é possível cadastrar itens que são chamados de **catálogos geográficos**.

  

Nesta primeira versão, é possível:

- Cadastrar coordenadas;

- Recuperar uma lista de coordenadas;

- Cadastrar um catálogo geográfico, dada uma coordenada pré-cadastrada;

- Recuperar uma lista de catálogos geográficos;

- Recuperar uma lista de hashtags que foram cadastradas nos catálogos geográficos.



## Qual é a aplicação desta api?

  

Se você possui qualquer tipo de **dado georreferenciado**, é possível utilizar para **associar informações** do seu negócio à essas **coordenadas**.

  

É aplicável às áreas de:

- Agro (mapeamento de safras, escoamento, status de lavouras);

- Petróleo (mapeamento de dados sobre extração e/ou potencial extração);

- Geológico (mapeamento de terreno);

- Biológico (catalogação de fauna, flora, etc.)

- Mobilidade (transportes, pontos de taxi, ônibus, etc.)

- Saúde pública (mapeamento de UBS, ações de vacinação por região)

- Segurança (tático, policial, criminalidade)

- Defesa Civil (Pontos de alagamento, risco de barrancos, etc.)

  

Funciona da seguinte forma:

1. Para cada **coordenada** cadastrada, é possível cadastradar um ou vários **catálogos**.

2. Cada catálogo possui **título, descrição, hashtag, imagem** e estará **associada à uma coordenada**.

3. Dada uma **hashtag**, é possível **filtrar catálogos** que utilizam essa hastag.

  

## Como executar

  

> Para este trabalho foi utilizado o docker e há um arquivo Dockerfile e docker-compose.yml.

  

Para executar a API basta executar na raiz do projeto:

  

```

docker-compose up --build

```


Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.

