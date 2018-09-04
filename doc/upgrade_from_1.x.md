Guide of Upgrade from 1.x to 2.x
---------------------------------------

If you have Pinry installed by srouce code, it's easy for
you to upgrade from 1.x to 2.x, just follow these steps.

At first you should checkout the old branch.

```bash
# it is not required if you are currently the old version
git checkout 1.x version

# install and enter the shell
pipenv install 
pipenv shell

# Upgrade to lastest version of django-images

pip install -U git+https://github.com/mirumee/django-images.git
python manage.py makemigrations
python manage.py migrate --fake-initial

# clean action
pip uninstall django-images

# It will ask if you want to remove an extra file named like
# Uninstalling django-images-0.4.3:
# -------------------------------------------
#  Would remove:
#    /path_to_your_python_packages/django_images-0.4.3.dist-info/*
#    /path_to_your_python_packages/django_images/*
#  Would not remove (might be manually added):
#    /path_to_your_python_packages/django_images/migrations/0002_auto_20180826_0845.py
# Proceed (y/n)? 
# ------------------------------------------
# Please remove the file it by hand if possible (this operation is optional)
rm /path_to_your_python_packages/django_images/migrations/0002_auto_20180826_0845.py

# exit pipenv's virtualenv
exit
```

Ant then you should checkout to version 2.x (our current master) 

```bash
# If you are not the lastest version ,just call "git pull --rebase"
# to upgrade to lastest version of Pinry (2.x)
git checkout master
make install
make migrate

# Try to run as development server
make serve

# If no error occurs, just enjoy it

```

And now, you can just run your server in the way you like.
