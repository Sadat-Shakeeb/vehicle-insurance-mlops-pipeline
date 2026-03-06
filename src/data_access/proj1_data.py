import os
import sys
import pymongo
import certifi

from pandas import DataFrame

from src.exception import MyException
from src.logger import logging
from src.constants import DATABASE_NAME, MONGODB_URL_KEY

# Load the certificate authority file to avoid timeout errors when connecting to MongoDB
ca = certifi.where()

class MongoDBClient:
    """
    MongoDBClient is responsible for establishing a connection to the MongoDB database.

    Attributes:
    ----------
    client : MongoClient
        A shared MongoClient instance for the class.
    database : Database
        The specific database instance that MongoDBClient connects to.

    Methods:
    -------
    __init__(database_name: str) -> None
        Initializes the MongoDB connection using the given database name.
    """

    client = None  # Shared MongoClient instance across all MongoDBClient instances

    def __init__(self, database_name: str = DATABASE_NAME) -> None:
        """
        Initializes a connection to the MongoDB database. If no existing connection is found, it establishes a new one.

        Parameters:
        ----------
        database_name : str, optional
            Name of the MongoDB database to connect to. Default is set by DATABASE_NAME constant.

        Raises:
        ------
        MyException
            If there is an issue connecting to MongoDB or if the environment variable for the MongoDB URL is not set.
        """
        try:
            # Check if a MongoDB client connection has already been established; if not, create a new one
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY)  # Retrieve MongoDB URL from environment variables
                if mongo_db_url is None:
                    raise Exception(f"Environment variable '{MONGODB_URL_KEY}' is not set.")
                
                # Establish a new MongoDB client connection
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
                
            # Use the shared MongoClient for this instance
            self.client = MongoDBClient.client
            self.database = self.client[database_name]  # Connect to the specified database
            self.database_name = database_name
            logging.info("MongoDB connection successful.")
            
        except Exception as e:
            # Raise a custom exception with traceback details if connection fails
            raise MyException(e, sys)


class Proj1Data:
    """Utility class for accessing project data stored in MongoDB.

    Provides convenience methods used by other components (e.g. DataIngestion) to
    export collections as pandas DataFrames.
    """

    def __init__(self, database_name: str = DATABASE_NAME) -> None:
        try:
            self.client = MongoDBClient(database_name=database_name)
            self.database = self.client.database
        except Exception as e:
            raise MyException(e, sys)

    def export_collection_as_dataframe(self, collection_name: str) -> DataFrame:
        """Fetches all documents from the specified collection and returns a DataFrame.

        Parameters
        ----------
        collection_name : str
            Name of the MongoDB collection to read from.

        Returns
        -------
        pandas.DataFrame
            DataFrame containing the documents from the collection. If the
            collection is empty, an empty DataFrame is returned. The special
            MongoDB ``_id`` field is dropped automatically since it isn't part
            of the original dataset.
        """
        try:
            logging.info(f"Exporting collection '{collection_name}' to DataFrame.")
            collection = self.database[collection_name]
            records = list(collection.find({}))
            df = DataFrame(records)
            # MongoDB documents always include an ``_id`` field; remove it
            # unless the caller explicitly needs it.
            if '_id' in df.columns:
                logging.debug("Dropping automatic '_id' column from DataFrame.")
                df = df.drop(columns=['_id'])
            logging.info(f"Loaded {len(df)} records from collection '{collection_name}'.")
            return df
        except Exception as e:
            raise MyException(e, sys)
