motosucata-django
=================

Website / Catalogo desarrollado en Django

Instalación y Uso
-----------------

1. Clone el proyecto

    ``` sh
    $ git clone https://github.com/laborautonomo/motosucata-django.git
    $ cd motosucata-django
    ``` 

2. Crear y activar el [vitualenv](http://pypi.python.org/pypi/virtualenv)

    ``` sh
    $ virtualenv venv
    $ source venv/bin/activate
    ``` 

3. Bajar y hacer la instalación de los requerimientos con [pip](http://pypi.python.org/pypi/pip)

    ``` sh
    $ pip install -r requirements.txt
    ```

4. Configurar el proyecto en lo archivo `motosucata/settings.py`

5. Sincroniza la base de datos: `$ python manage.py syncdb`

6. Recoger los archivos estáticos: `$ python manage.py collectstatic`

7. Finalmente, ejecute `$ python manage.py runserver`


Referencias
-----------

* [Django documentation](https://docs.djangoproject.com/en/1.6/)
* [Getting Started with Django on Heroku](https://devcenter.heroku.com/articles/getting-started-with-django)