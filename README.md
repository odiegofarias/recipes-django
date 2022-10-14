# Blog de receitas

## Sobre
<p>Este projeto foi criado no Curso de Django do Professor Luíz Otávio da Udemy.</p>
<p>
  O projeto é um 'blog' onde as pessoas podem adicionar e compartilhar suas receitas com as demais.
</p>
### Modo se uso
  <p>
    A pessoa não precisa estar logada para visualizar as receitas, mas precisa para publicar uma receita.
    Ao criar a conta e adicionar uma receita ao sistema, ela ficará em "stand-by" aguardando a administração liberar o conteúdo. Após criada, a receita não é publica imediatamente, com isso, a pessoa pode editar ou excluir a sua receita.
  Entretanto, após publicação pela administração, a receita se torna permanente, não podendo ser editada ou excluida pela pessoa criadora, apenas pela administração.
  </p>

## Tecnologias
  <ul>
    <li>Django</li>
    <li>HTML/CSS</li>
    <li>Potsgresql</li>
    <li>Javascript</li>
  </ul>

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
