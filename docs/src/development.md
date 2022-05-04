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


## Testing

We have many tests built into Pinry to ensure that changes don't break
anything. If you are live dangerously and have cutting edge new Pinry
features first you can use our master branch for your own instance. We
recommend using our tags/versions though.

To run Pinry's tests inside the Pinry repo run:

    pipenv run python manage.py test

# Docker

Follow the steps below to install Pinry locally or on any server. This
process installs the minimal requirements to run Pinry. For development
requirements and procedures, see testing above.

Current docker configuration will just mount source code directory to
docker app directory and run any codes existed in current git branch,
you may also add "local_settings.py" to customize settings without
changing settings file in `pinry/settings`.

- Install the requirements:
    - Docker
    - Docker Compose

- Set any custom configuration options you need and run


    cp docker-compose.example.yml docker-compose.yml  
    # edit docker-compose.yml and change the secret-key,  
    # don't forget to backup this config file.  
    # You should build frontend first  
    docker-compose up build_frontend  
    # then start the backend server  
    docker-compose up -d web


- If you want to run Pinry with current user in docker


    ./start_docker_with_current_user.sh [-d]


- Bootstrap the database(optional)


    docker-compose exec web python3 manage.py migrate --settings=pinry.settings.docker



**Note** : No static file server configured, your should configure nginx or other server to serve
static files from `./static`(as path `/static`) and `./pinry-spa/dist` (as html root `/`)
