motosucata-django
=================

Website / Catalogo desenvolvido com Django

Uso e Instalação
----------------

1. Clone o projeto

    ``` sh
    $ git clone https://github.com/laborautonomo/motosucata-django.git
    $ cd motosucata-django
    ``` 

2. Crie e ative o [vitualenv](http://pypi.python.org/pypi/virtualenv)

    ``` sh
    $ virtualenv venv
    $ source venv/bin/activate
    ``` 

3. Baixe e instale os requerimentos utilizando [pip](http://pypi.python.org/pypi/pip)

    ``` sh
    $ pip install -r requirements.txt
    ```

4. Configure o projeto no arquivo `motosucata/settings.py`

5. Syncronize a base de dados: `$ python manage.py syncdb`

6. Colete os arquivos estáticos: `$ python manage.py collectstatic`


Referências
-----------

* [Django documentation](https://docs.djangoproject.com/en/1.6/)
* [Getting Started with Django on Heroku](https://devcenter.heroku.com/articles/getting-started-with-django)