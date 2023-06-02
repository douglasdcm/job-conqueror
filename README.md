# Introdução
Este projeto utiliza um crawler assíncrono e genérico para buscar por vagas em diferentes sites de empresas.

# Começando
Antes de começar a contribuir com o projeto, veja o nosso [Código de Conduta](https://github.com/douglasdcm/job-conqueror/blob/main/CODE_OF_CONDUCT.md).

# Adicionando empresas
Se você quiser adicionar mais empresas ao projeto é bem simples. Em poucos minutos você consegue fazer isso. Veja o exemplo abaixo:
![Exemplo](https://github.com/douglasdcm/job-conqueror/blob/main/static/images/add-locator-example.jpg?raw=true)

- Faça um fork deste projeto e clone o seu repositório 
- Adicione o link de vagas da empresa no arquivo [companies_data.csv](https://github.com/douglasdcm/job-conqueror/blob/main/src/crawler/companies_data.csv)
- Adicione o Xpath 'locator' do link das vagas. O Selenium usa isso para descobrir as vagas da empresa. Veja os exemplos que estão no arquivo.
- Adicione `Y` no terceiro campo do csv. Isso indica que o link está habilitado para a próxima coleta de dados.
- Submeta sua Merge Request para este projeto

# Atualizando o código fonte
Para atualizar o código fonte, ative seu ambiente virtual e instale as dependências
```
python3.7 -m venv env
source venv/bin/activate
pip install -r requirements.txt
pip install -r test-requirements.txt
sudo mkdir -p /webapp/logs
sudo cp ./src/resources/basic_page.html /webapp
chmod -R 777 /webapp
```
Instale o Docker e Docker Compose e suba os containers.
```
sudo docker compose up -d
```
Copie o arquivo ".env_template" para ".env" e adicione dados de teste no banco de dados
```
python add_fake_data_to_databse.py
```
Agora você pode mexer no código à vontade.

# Rodando os testes

Verifique a versão do seu navegador Chrome e baixe o webdriver correto pelo [link](https://chromedriver.chromium.org/downloads)
- Inicialize o container do postgres manualmente (esse processo será melhorado no futuro)
```
sudo docker compose up -d
```
- Rode os testes.
Atenção: os teste não funcionais demoram mais de uma hora para terminar. Melhor deixar pra rodar quando necessário. Por enquanto, execute os testes funcionais para validar seu setup.
```
python -m pytest -m functional
```
ou com tox
```
tox
```
ou com os utilitários
```
./utils/run_functional.sh
```

## Testes não funcionais
Para executar os testes de performance (estes demoram mais de 1h)
```
./utils/run_non_functional.sh
```
Para testes do comandos no terminal

```
./utils/cProfile/run_perfomance_test_cli.sh
```
Os resultados da execução serão abertos no navegador
<br>
References about snakeviz
- https://jiffyclub.github.io/snakeviz/
- https://docs.python.org/3/library/profile.html#module-cProfile

# Debug

```
$ docker exec -it postgres psql -U postgres

# Ver número de conexões no banco de dados
postgres=# select count(*) from pg_stat_activity;

# Contar o número de registros coletados
postgres=# select count(*) from positions;
```
- Logs da aplicação
```
tail -f /webapp/logs/crawlers.log
```

# Contribuindo
Ajude este projeto a crescer adicionando novas empresas ou adicionando os 'locators' das empresas que estão pendentes.<br>
Pull requests são bem-vindas. Para mudanças grandes crie uma issue para discutirmos o que está sendo modificado. Adicione os testes apropriados.

Dê uma estrelinha se você gostou deste projeto :)