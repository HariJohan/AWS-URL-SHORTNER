import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("URLShortenerTable")


def decimal_to_int(obj):
    if isinstance(obj, Decimal):
        return int(obj)
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "GET,OPTIONS"
        },
        "body": json.dumps(body, default=decimal_to_int)
    }


def lambda_handler(event, context):
    try:
        result = table.scan()
        items = result.get("Items", [])

        return response(
            200,
            {
                "count": len(items),
                "links": items
            }
        )

    except Exception as e:
        print("ERROR:", str(e))
        return response(
            500,
            {
                "error": "Internal server error"
            }
        )