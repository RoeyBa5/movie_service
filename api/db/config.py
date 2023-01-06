class MongoConfig:
    def __init__(self, host: str, db_name: str, collection_name: str):
        self.host = host
        self.db_name = db_name
        self.collection_name = collection_name
