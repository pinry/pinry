# Developing Pinry

Pinry currently has two major requirements:

- Python 3.6+
- Node 10+

For minor requirements you need two have installed two package managers that
are not the defaults for these languages:

- Python, pipenv
- Node, yarn

To install these is pretty simple, you can just run:

    cd pinry
    pip install pipenv
    npm install -g yarn

After that you can install this project with:

    pipenv install --dev
    cd pinry-spa; yarn install

You will need to run two separate items as of right now, the SPA and the
backend:

    pipenv run python manage.py migrate
    pipenv run python manage.py runserver

And from another terminal:

    cd pinry-spa; yarn serve
