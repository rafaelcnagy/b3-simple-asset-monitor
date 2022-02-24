# b3-simple-asset-monitor
A django project made as a technical test for Inoa Sistemas


# Descrição do desafio
O objetivo do sistema é auxiliar um investidor nas suas decisões de comprar/vender ativos. Para tal, ele deve registrar periodicamente a cotação atual de ativos da B3 e também avisar, via e-mail, caso haja oportunidade de negociação.

Os seguintes requisitos funcionais são necessários:

- Obter periodicamente as cotações de alguma fonte pública qualquer e armazená-las, em uma periodicidade configurável, para consulta posterior
- Expor uma interface web para permitir consultar os preços armazenados, configurar os ativos a serem monitorados e parametrizar os túneis de preço de cada ativo
- Enviar e-mail para o investidor sugerindo Compra sempre que o preço de um ativo monitorado cruzar o seu limite inferior, e sugerindo Venda sempre que o preço de um ativo monitorado cruzar o seu limite superior


# Requisitos
- python 3.8
- poetry


# Instalação
Para a instação do ambiente de execução, você deve executar alguns comandos no terminal.

Primeiro vamos instalar o ambiente virtual:
```
poetry install
```

Copiamos o arquivo de configurações:
```
cp .env.ini .env
```

> Edite o arquivo `.env`, adicionando dados como as API keys da [HG brasil](https://hgbrasil.com/) e o e-mail que será remetente da aplicação (deve ser gmail), junto com sua [senha de app](https://support.google.com/mail/answer/185833).

Então, devemos criar as migrations e executá-las, através desses dois comandos:
```
poetry run python manage.py makemigrations
poetry run python manage.py migrate
```

Finalmente, devemos baixar os arquivos estáticos:
```
poetry run python manage.py collectstatic
```


# Execução
Por padrão, o servidor vai ser executado no localhost, usando a porta 8000.

Execute o comando no terminal:
```
poetry run python manage.py runserver
```
