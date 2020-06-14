if __name__ == '__main__':
    from create_db import emptyCollections, getClient
    client = getClient()
    db = client.restaurant_data
    emptyCollections(db)