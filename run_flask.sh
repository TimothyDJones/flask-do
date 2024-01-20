#/bin/sh
# https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3

# export FLASK_APP=hello
export FLASK_APP=app
export FLASK_ENV=development
flask run -h "0.0.0.0" -p 5555
