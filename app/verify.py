from starlette.routing import Route
from starlette.applications import Starlette


from . import config
from . import endpoints


routes = [
    Route("/events", endpoint=endpoints.verify, methods=["POST"]),
]

app = Starlette(debug=config.DEBUG, routes=routes)

