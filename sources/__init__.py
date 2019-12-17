from .views import app
from .models import graph

graph.cypher.execute("CREATE CONSTRAINT ON (s:Shop) ASSERT s.name IS UNIQUE")
graph.cypher.execute("CREATE CONSTRAINT ON (u:User) ASSERT u.username IS UNIQUE")