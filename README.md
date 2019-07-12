# TestePraticoScraping

## Teste prático de Scrapping
### Target: [www.ibyte.com.br]

#### Objetivos
* Construir um crawler para uma loja online utilizando o Scrapy
* A spider recebe uma palavra para busca e extrai informações de cada produto resultante
* Utilização de form request na busca por produtos
* A spider deve fazer o tratamento de paginação e passar por todas as páginas da pesquisa
* Utilização de xpath na busca por links e na raspagem de dados 
* Utilizar logs para sinalização de ocorrências durante o scraping 
* Persistir os dados no MongoDB

#### Campos utilizados
* url
* código
* nome 
* valor
* valor_antigo 
* descricao
* características {cor, marca, peso, ...} (Alguns produtos não possuem)
* garantia

#### Setup do ambiente
* pip install -r requirements.txt

#### Comandos usados 
* scrapy startproject nome_projeto (para criação do projeto)
* scrapy genspider nome_spider url_target (para criação do spider)

#### Instruções para execução
* Instalar [MongoDB](https://www.mongodb.com/)
* Criar um diretório data/db na raiz do disco (Windows)
* Iniciar o servidor com o mongod.exe (Windows) ou executar o serviço mongod (Linux)
* Seguir para o diretório ibyte/ no terminal do ambiente
* Usar o comando scrapy crawl ibytebot -a pesquisa="palavra" (palavra é o parâmetro para efetuar a pesquisa. Ex. "fone de ouvido")

#### Visualização dos dados
* Instalar [Robomongo(Robo 3T)](https://robomongo.org/download) ou [Mongo Compass](https://www.mongodb.com/products/compass)

#### Estrutura da Spider
* parse 
    * Faz o form request para pesquisa da palavra 
    * Encaminha para a página da pesquisa
* start_scraping
    * Obtém o link de todos os produtos da página 
    * Passa para a proxima página enquanto existir dentro do resultado da pesquisa
    * Encaminha para a página do produto
* produto
    * Acessa o link do produto
    * Retira as informações necessárias
    
#### Opcionais:
* Manipulação de querystrings - Não se mostrou necessário na aplicação
* Utilização de item loaders para carregar informações - Um estudo mais amplo de scrapy.Loaders é necessário para aplicação nesse caso
* Chamadas assíncronas para capturar informações não presentes no HTML (AJAX, etc.) - Não necessário nessa aplicação

#### Tempo utilizado:
* Escolha e estudo do target + Setup do ambiente: +- 1h
* Estudando + Resolvendo bugs: +- 8h
* Desenvolvendo a solução: +- 5h

#### Referências:
* [Scrapy](https://doc.scrapy.org/en/latest/intro/tutorial.html)
* [Xpath](https://doc.scrapy.org/en/xpath-tutorial/topics/xpath-tutorial.html)
* [MongoDB](https://www.mongodb.com/)
* [Robomongo](https://robomongo.org/)
* [Tutorial Pymongo](http://api.mongodb.com/python/current/tutorial.html)
* [Python Web Scraping & Crawling using Scrapy](https://www.youtube.com/playlist?list=PLhTjy8cBISEqkN-5Ku_kXG4QW33sxQo0t)
* [Scrapy with MongoDB](https://realpython.com/web-scraping-with-scrapy-and-mongodb/)
