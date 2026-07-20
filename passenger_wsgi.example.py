# If ASGI supported, use the ASGI application instead of WSGI
# from src.main import app as application

#####
# If runnig uvicorn, use the following command:
# uvicorn passenger_wsgi:application --host

#####
# If only WSGI is supported, use the WSGI application
# from a2wsgi import ASGIMiddleware

# from src.main import app

# application = ASGIMiddleware(app)  # type: ignore[arg-type]

#####
## Example wsgi bootstrap code for cpanel
# import imp
# import os
# import sys

# sys.path.insert(0, os.path.dirname(__file__))

# wsgi = imp.load_source("wsgi", "passenger_wsgi.py")
# application = wsgi.application


#####
## If only WSGI is supported, use the WSGI application
import os
import sys

# Add your application directory to the system path
sys.path.insert(0, os.path.dirname(__file__))

# Import your FastAPI instance (assuming your main script is main.py and app instance is named app)
# Import the ASGI-to-WSGI middleware
from a2wsgi import ASGIMiddleware

from main import app

# Wrap the FastAPI app to make it WSGI-compliant
application = ASGIMiddleware(app)
