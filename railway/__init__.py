from flask import Flask
app = Flask(__name__)
from railway import routes
# print(type(routes))

