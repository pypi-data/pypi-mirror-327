# API Gateway & DynamoDB Utility Library

## Overview  
This library provides utility functions to interact with **AWS API Gateway** and **DynamoDB**. It enables secure API communication for **fetching and upserting data** via API Gateway, ensuring robust error handling, logging, and authentication using an **API Key**.

## Features  
- ✅ **Fetch Data** from DynamoDB via API Gateway  
- ✅ **Upsert Data** (Insert/Update) into DynamoDB  
- ✅ **Secure API Access** using API Key  
- ✅ **Robust Logging & Error Handling**  
- ✅ **Optimized JSON Response Handling**  
- ✅ **Support for Private Repository Deployment**  

---

## Installation  

### **Prerequisites**
Ensure you have **Python 3.8+** installed.

Install the required dependencies:
```bash
pip install requests
pip install api_gateway_dynamodb 
```

Usage - Read Data

```python

 from api_gateway_dynamodb import get_data_from_api_gateway_dynamodb

# API Gateway Endpoint URL
api_url = "https://your-api-gateway-url.com/get-data"

# Example Parameters
database_table_name = "customer"
partition_key = "customer_id"
partition_key_value = "123456"
api_key = "your-api-key-here"

# Fetch data
response = get_data_from_api_gateway_dynamodb(api_url, 
                                              database_table_name, 
                                              partition_key, 
                                              partition_key_value, 
                                              api_key)

print(response)  # Output: JSON response with data from DynamoDB
```
Usage - Insert / Update data

```python

from api_gateway_dynamodb import upsert_data_via_api_gateway_dynamodb

# API Gateway Endpoint URL
api_url = "https://your-api-gateway-url.com/upsert-data"

# Example Data Payload
payload = {
    "id_number": "123456",
    "name": "John",
    "surname": "Doe",
    "title": "Mr"
}

# Upsert Parameters
method_name = "insert"
table_name = "customer"
partition_key = "id_number"
api_key = "your-api-key-here"

# Insert or Update Data
response = upsert_data_via_api_gateway_dynamodb(payload, method_name, table_name, partition_key, api_key, api_url)

print(response)  # Output: JSON response confirming the operation


```