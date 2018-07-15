import csv
import os

from django.shortcuts import render
from neo4j.v1 import GraphDatabase, basic_auth

base_dir= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Create your views here.
"""change according to the IP in which Neo4j server is running, by default it is set to local system"""
# driver = GraphDatabase.driver("bolt://10.141.63.61:7687", auth=basic_auth("neo4j", "password"))
driver = GraphDatabase.driver("bolt://127.0.0.1:7687", auth=basic_auth("neo4j", "password"))


def home(request):
    session = driver.session()
    if request.method=="POST":
        print(request.POST['sex'])
        x = "MATCH (n:adult_data) where n.sex=\"" + request.POST['sex'] + "\" and n.race=\"" + request.POST['race'] + "\" and n.relation=\"" + request.POST['relationship'] + "\" " \
            "RETURN n.age as age,n.workclass as workclass,  n.fnlweight as fnlweight, n.education as education,  " \
            "n.education_num as education_num, n.marital_status as marital_status, n.occupation as occupation, n.relation as relation," \
            " n.race as race, n.sex as sex, n.capital_gain as capital_gain, n.capital_loss as capital_loss, n.hours_per_week as hours_per_week," \
            " n.native_country as native_country, n.salary as salary limit 25"
        complete_data = session.run(x)
        column_list = []
        for i in complete_data:
            column_list = i.keys()
            break
        print(column_list)

        dict = {}
        list_list = []
        for i in complete_data:
            list = []
            for a in i:
                list.append(a)
            list_list.append(list)
    else:
        x="MATCH (n:adult_data)  RETURN n.sex as sex, count(n.sex) as frequency ORDER BY n.sex"
        sex_count=session.run(x)
        column_list = ['sex','frequency']
        csvfile = open(os.path.join(base_dir, 'webapp/static/data/sex_result_count.csv'), 'w', newline='')
        writer = csv.writer(csvfile)
        writer.writerow(column_list)

        for i in sex_count:
            print(i)
            val = []
            for keys in column_list:
                val.append(i[keys])
            writer.writerow(val)
        csvfile.close()

        x="MATCH (n:adult_data)  RETURN n.relation as label, count(n.relation) as value ORDER BY n.relation"
        relationship_count=session.run(x)
        column_list = ['label','value']
        csvfile = open(os.path.join(base_dir, 'webapp/static/data/relation_result_count.csv'), 'w', newline='')
        writer = csv.writer(csvfile)
        writer.writerow(column_list)

        for i in relationship_count:
            val = []
            for keys in column_list:
                val.append(i[keys])
            writer.writerow(val)
        csvfile.close()

        x="MATCH (n:adult_data) where n.sex=\"" + "Male\""+" and n.race=\""+"White\""+" and n.relation=\""+"Husband\""+" " \
          "RETURN n.age as age,n.workclass as workclass,  n.fnlweight as fnlweight, n.education as education,  " \
          "n.education_num as education_num, n.marital_status as marital_status, n.occupation as occupation, n.relation as relation," \
          " n.race as race, n.sex as sex, n.capital_gain as capital_gain, n.capital_loss as capital_loss, n.hours_per_week as hours_per_week," \
          " n.native_country as native_country, n.salary as salary limit 50"
        complete_data=session.run(x)
        column_list = []
        for i in complete_data:
            column_list = i.keys()
            break
        print(column_list)

        dict={}
        list_list=[]
        for i in complete_data:
            list = []
            for a in i:
                list.append(a)
            list_list.append(list)
    session.close()
    return render(request,"webapp/home.html",{'list_list':list_list,'column_list':column_list})
