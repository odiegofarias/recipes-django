# Blog de receitas

<h4>Sobre</h4>
<p>Este projeto foi criado no Curso de Django do Professor Luíz Otávio da Udemy.</p>
<p>
  O projeto basicamente é um 'blog' onde as pessoas podem adicionar e compartilhar suas receitas com os demais usuários
  
</p>

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
