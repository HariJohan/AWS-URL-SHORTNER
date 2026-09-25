import json
import boto3
from datetime import datetime, timezone

dynamodb = boto3.resource("dynamodb")

url_table = dynamodb.Table("URLShortenerTable")
analytics_table = dynamodb.Table("URLClickAnalyticsTable")


def cors_response(status_code, body):

    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "GET,OPTIONS"
        },
        "body": json.dumps(body)
    }


def lambda_handler(event, context):

    try:

        path_parameters = event.get(
            "pathParameters"
        ) or {}

        code = path_parameters.get("code")

        if not code:
            return cors_response(
                400,
                {"error": "code is required"}
            )

        # Find URL
        result = url_table.get_item(
            Key={
                "code": code
            }
        )

        if "Item" not in result:

            return cors_response(
                404,
                {"error": "Short URL not found"}
            )

        item = result["Item"]

        target_url = item["target_url"]

        # Update click count atomically
        url_table.update_item(
            Key={
                "code": code
            },
            UpdateExpression="SET click_count = click_count + :one",
            ExpressionAttributeValues={
                ":one": 1
            }
        )

        # Get request information
        headers = event.get("headers") or {}

        user_agent = (
            headers.get("User-Agent")
            or headers.get("user-agent")
            or "Unknown"
        )

        request_context = (
            event.get("requestContext")
            or {}
        )

        identity = (
            request_context.get("identity")
            or {}
        )

        ip_address = (
            identity.get("sourceIp")
            or "Unknown"
        )

        timestamp = datetime.now(
            timezone.utc
        ).isoformat()

        # Store click analytics
        analytics_table.put_item(
            Item={
                "code": code,
                "timestamp": timestamp,
                "ip_address": ip_address,
                "user_agent": user_agent
            }
        )

        # Redirect
        return {
            "statusCode": 302,
            "headers": {
                "Location": target_url,
                "Access-Control-Allow-Origin": "*"
            },
            "body": ""
        }

    except Exception as e:

        print("ERROR:", str(e))

        return cors_response(
            500,
            {
                "error": "Internal server error"
            }
        )
