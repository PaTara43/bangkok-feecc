from pymongo import MongoClient, DESCENDING, ReturnDocument
import json

with open('config.json') as config_file:
    config = json.load(config_file)


class MongoDBUtil:
    def __init__(self, uri: str, db_name: str, collection_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def add_item(self, item: dict) -> str:
        """
        Add a single item to the MongoDB collection.

        Args:
            item (dict): The item to be added to the collection.

        Returns:
            str: The ID of the inserted item.
        """
        result = self.collection.insert_one(item)
        return str(result.inserted_id)

    def get_latest_item(self) -> str:
        """
        Retrieve the latest item from the specified collection.

        Returns: latest item ID
        """
        latest_item = self.collection.find_one(sort=[('_id', DESCENDING)])
        return latest_item

    def modify_item(self, item, update_fields):
        """
        Modify an item in the specified collection.

        :param item: The ID of the item to modify.
        :param update_fields: A dictionary of fields to update.
        :return: The modified document or None if not found.
        """
        result = self.collection.find_one_and_update(
            {'_id': item["_id"]},
            {'$set': update_fields},
            return_document=ReturnDocument.AFTER
        )
        return result

    def get_esp_data(self) -> list:
        """
        Get all items from the MongoDB collection and return them as a dictionary.

        Returns:
            dict: A dictionary containing all items in the collection.
        """
        items = list(self.collection.find())
        # Convert ObjectId to string for JSON serialization
        items_list = [{**item, "_id": str(item["_id"])} for item in items]
        timestamps = [item.get('timestamp', None) for item in items_list]
        humidities = [item.get('humidity', None) for item in items_list]
        temperatures = [item.get('temperature', None) for item in items_list]
        address = items_list[-1].get('address', None)

        return [address, {"Timestamps": timestamps, "Humidities": humidities, "Temperatures": temperatures}]

    def remove_all_items(self) -> None:
        """
        Remove all items from the MongoDB collection.

        Returns:
            None
        """
        self.collection.delete_many({})

# Example usage (commented out):
if __name__ == "__main__":
    mongo_util = MongoDBUtil(config['mongo_connection_uri'], config['database_name'], "esp_data")
    # print(mongo_util.add_item({"timestamp": "16:51", "humidity": 13, "temperature": 13, "address": "123"}))
    print(mongo_util.get_esp_data())
    item = mongo_util.get_latest_item()
    print(item)
    mongo_util.modify_item(item, {"address": "321", "humidity": 21, "temperature": 21})
    print(mongo_util.get_esp_data())
    # mongo_util.remove_all_items()