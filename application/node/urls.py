from .views import *
from presentation.view import View


View.get("/request/file",file_server)
View.post("/discovery",sync_nodes)