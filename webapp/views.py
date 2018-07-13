from django.shortcuts import render
from neo4j.v1 import GraphDatabase, basic_auth

# Create your views here.
"""change according to the IP in which Neo4j server is running, by default it is set to local system"""
# driver = GraphDatabase.driver("bolt://10.141.63.61:7687", auth=basic_auth("neo4j", "password"))
driver = GraphDatabase.driver("bolt://127.0.0.1:7687", auth=basic_auth("neo4j", "password"))


def home(request):
    session=driver.session()
    x="MATCH (n:adult_data)where n.sex='Male' and n.age='40' RETURN n LIMIT 25"
    result = session.run(x)
    print(result)
    for i in result:
        print(i)
    return render(request,"webapp/index.html",{'data': result})
