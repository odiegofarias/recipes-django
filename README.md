# Blog de receitas

## Instalação

Primeiro passo é clonar o repositório:

```sh
$ git clone git@github.com:odiegofarias/recipes-django.git
$ cd recipes-django
```

Crie seu ambiente virtual para instalar as dependências necessárias e o ative:
```sh
$ python -m venv .venv
$ .venv\scripts\activate
```

Então, instale as depedências:

```sh
(.venv)$ pip install -r requirements.txt
```
Note que: o .venv na frente do prompt indica que o terminal está operando com seu ambiente virtual.

Assim que o `pip` terminar de baixar as dependências:
```sh
(env)$ cd project
(env)$ python manage.py runserver
```
E navegue para`http://127.0.0.1:8000/`.
