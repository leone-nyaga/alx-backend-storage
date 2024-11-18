#!/usr/bin/env python3


def list_all(mongo_collection):
    """
    Lists all documents in a collection.

    Args:
    mongo_collection: The PyMongo collection object.

    Returns:
    A list of all documents in the collection, or an empty list if no documents exist.
    """

    documents = mongo_collection.find()

    return list(documents)
