import json
import boto3
import hashlib
from datetime import datetime, timezone

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("URLShortenerTable")


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "POST,OPTIONS"
        },
        "body": json.dumps(body)
    }


def lambda_handler(event, context):

    try:
        body = json.loads(event.get("body") or "{}")

        target_url = body.get("target_url")

        if not target_url:
            return response(
                400,
                {"error": "target_url is required"}
            )

        if not (
            target_url.startswith("http://")
            or target_url.startswith("https://")
        ):
            return response(
                400,
                {"error": "URL must start with http:// or https://"}
            )

        # Generate a 6-character short code
        short_code = hashlib.sha256(
            target_url.encode()
        ).hexdigest()[:6]

        created_at = datetime.now(
            timezone.utc
        ).isoformat()

        table.put_item(
            Item={
                "code": short_code,
                "target_url": target_url,
                "created_at": created_at,
                "click_count": 0
            }
        )

        return response(
            201,
            {
                "code": short_code,
                "target_url": target_url,
                "created_at": created_at
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