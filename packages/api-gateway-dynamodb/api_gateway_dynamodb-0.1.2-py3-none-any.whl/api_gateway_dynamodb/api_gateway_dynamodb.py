import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def get_data_from_api_gateway_dynamodb(api_url: str,
                                       database_table_name: str,
                                       partition_key: str,
                                       partition_key_value: str,
                                       api_key: str) -> dict:
    """
    Fetch data from an API Gateway endpoint that retrieves data from a DynamoDB table.

    Parameters:
        api_url (str): The API Gateway endpoint URL.
        database_table_name (str): The name of the DynamoDB table to query.
        partition_key (str): The partition key column name to retrieve data.
        partition_key_value (str): The partition key value to retrieve data.
        api_key (str): The API key for authentication.

    Returns:
        dict: The JSON response containing the requested data.
    """
    try:
        logging.info(
            f"Fetching data from API: {api_url} | Table: {database_table_name} | Partition Key: {partition_key_value}")
        response = requests.get(url=api_url, headers={"x-api-key": api_key},
                                params={
                                    "database_table_name": database_table_name,
                                    "partition_key": partition_key,
                                    "partition_key_value": partition_key_value,
                                })
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)

        data = response.json().get('body', {})
        logging.info(f"Data successfully retrieved: {data}")
        return data

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from API Gateway: {e}")
        return {"error": "Failed to fetch data from API Gateway"}

    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON response: {e}")
        return {"error": "Invalid JSON response received"}


def upsert_data_via_api_gateway_dynamodb(payload: dict,
                                         method_name: str,
                                         table_name: str,
                                         partition_key: str,
                                         api_key: str,
                                         api_url: str) -> dict:
    """
    Upsert (insert or update) data via API Gateway into a DynamoDB table.

    Parameters:
        payload (dict): The data to be inserted or updated.
        method_name (str): The API method name (e.g., "insert", "update").
        table_name (str): The name of the DynamoDB table.
        partition_key (str): The partition key value for data upsert.
        api_key (str): The API key for authentication.
        api_url (str): The API Gateway endpoint URL.

    Returns:
        dict: The JSON response from the API Gateway.
    """
    headers = {
        'Accept': 'application/json',
        'x-api-key': api_key,
        'table_name': table_name,
        'partition_key': partition_key,
        'method_name': method_name
    }

    try:
        logging.info(f"Sending data to API: {api_url} | Table: {table_name} | Partition Key: {partition_key}")
        response = requests.post(url=api_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)

        response_body = response.json().get('body', {})
        if isinstance(response_body, str):  # Ensure it's parsed properly
            response_body = json.loads(response_body)

        logging.info(f"Data successfully upserted: {response_body}")
        return response_body

    except requests.exceptions.RequestException as e:
        logging.error(f"Error sending data to API Gateway: {e}")
        return {"error": "Failed to send data to API Gateway"}

    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON response: {e}")
        return {"error": "Invalid JSON response received"}
