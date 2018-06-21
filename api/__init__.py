from flask import Flask
from .v1.rides.views import blue_print_rides
from .v1.requests.views import blue_print_requests
app = Flask(__name__)

app.register_blueprint(blue_print_rides)
app.register_blueprint(blue_print_requests)
