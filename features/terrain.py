from lettuce import *
import pymongo

world.conn = pymongo.Connection("localhost")

@before.each_scenario
def clear_databases(scenario):
    databases = ["domain", "ip", "alert", "non80", "leadingin", "newdomain"]
    for db in databases:
        world.conn.drop_database(db)
