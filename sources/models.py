# coding=UTF-8
from py2neo import Graph, Node, Relationship
from passlib.hash import bcrypt
from datetime import datetime
import uuid
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

graph = Graph()

class User:

    def __init__(self, username):
        self.username = username

    def find(self):
        user = graph.find_one("User", "username", self.username)
        return user

    def register(self, name, surname, age, password):
        if not self.find():
            user = Node("User", username=self.username, name=name, surname=surname, age=age, password=bcrypt.encrypt(password))
            graph.create(user)
            return True

        return False

    def verify_password(self, password):
        user = self.find()

        if not user:
            return False

        return bcrypt.verify(password, user["password"])

    def add_shop(self, shopname, work, buy):
        user = self.find()

        shop = graph.merge_one("Shop", "name", shopname)
        graph.create(shop)
        if work:
            relation = Relationship(user, "WORKS_IN", shop)
            graph.create_unique(relation)
        if buy:
            relation = Relationship(user, "BUYS_IN", shop)
            graph.create_unique(relation)

    def my_work_shops(self):
        query = """
            MATCH (u:User)-[:WORKS_IN]->(s:Shop) 
            WHERE u.username={user} 
            RETURN s
            ORDER BY s.name ASC
            """
        return graph.cypher.execute(query, user=self.username)

    def my_buy_shops(self):
        query = """
            MATCH (u:User)-[:BUYS_IN]->(s:Shop) 
            WHERE u.username={user} 
            RETURN s
            ORDER BY s.name ASC
            """
        return graph.cypher.execute(query, user=self.username)

    def add_to_my_list(self, shop, work, buy):
        user = self.find()
        foundshop = graph.find_one("Shop", "name", shop)
        if work:
            relation = Relationship(user, "WORKS_IN", foundshop)
            graph.create_unique(relation)
        if buy:
            relation = Relationship(user, "BUYS_IN", foundshop)
            graph.create_unique(relation)

def get_shops():
    query = """
    MATCH (s:Shop) 
    RETURN s
    ORDER BY s.name ASC
    """
    return graph.cypher.execute(query)

def get_workers(shop):
    query = """
    MATCH (u:User)-[:WORKS_IN]->(s:Shop) 
    WHERE s.name={shop}
    RETURN u
    ORDER BY u.surname ASC
    """
    return graph.cypher.execute(query, shop=shop)

def get_clients(shop):
    query = """
    MATCH (u:User)-[:BUYS_IN]->(s:Shop) 
    WHERE s.name={shop}
    RETURN u
    ORDER BY u.surname ASC
    """
    return graph.cypher.execute(query, shop=shop)





