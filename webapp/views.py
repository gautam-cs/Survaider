from django.shortcuts import render
from neo4j.v1 import GraphDatabase, basic_auth

# Create your views here.
"""change according to the IP in which Neo4j server is running, by default it is set to local system"""
# driver = GraphDatabase.driver("bolt://10.141.63.61:7687", auth=basic_auth("neo4j", "password"))
driver = GraphDatabase.driver("bolt://127.0.0.1:7687", auth=basic_auth("neo4j", "password"))


def home(request):
    session=driver.session()
    x="MATCH (n:adult_data)  RETURN n.sex as sex, count(n.sex) as frequency ORDER BY n.sex"
    sex_count=session.run(x)
    dict={}
    for i in sex_count:
        dict.update({i[0]:i[1]})
    print(dict)


    x="MATCH (n:adult_data)  RETURN n.relation as relation, count(n.relation) as frequency ORDER BY n.relation LIMIT 25"
    relationship_count=session.run(x)
    dict = {}
    for i in relationship_count:
        dict.update({i[0]: i[1]})
    print(dict)

    # x="MATCH (n:adult_data) RETURN n"
    # complete_data=session.run(x)
    # for i in complete_data:
    #     print(i)
    session.close()
    return render(request,"webapp/index.html",{'Male_count':8, 'Female_count':5,
                                               'complete_data':5})
