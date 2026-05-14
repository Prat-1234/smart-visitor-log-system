import boto3
import json
from datetime import datetime

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("VisitorLogs")

SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:353625676485:visitor-alerts"

def lambda_handler(event, context):

    # Handle CORS preflight request
    if event.get("httpMethod") == "OPTIONS":
        return cors_response(200, "OK")

    try:
        # Parse incoming form data
        raw_body = event.get("body", "{}")
        body = json.loads(raw_body) if isinstance(raw_body, str) else raw_body

        visitor_id  = body.get("visitorId", "")
        name        = body.get("name", "")
        email       = body.get("email", "")
        phone       = body.get("phone", "")
        purpose     = body.get("purpose", "")
        host        = body.get("host", "")
        timestamp   = body.get("timestamp", datetime.now().strftime("%d/%m/%Y, %I:%M:%S %p"))

        # Basic validation
        if not all([visitor_id, name, email, phone, purpose, host]):
            return cors_response(400, {"error": "Missing required fields"})

        # Duplicate check — same email today
        today = datetime.now().strftime("%Y-%m-%d")
        existing = table.query(
            IndexName="email-date-index",
            KeyConditionExpression="email = :e AND #d = :d",
            ExpressionAttributeNames={"#d": "date"},
            ExpressionAttributeValues={":e": email, ":d": today}
        )
        if existing["Count"] > 0:
            return cors_response(409, {"error": "Visitor already checked in today"})

        # Save to DynamoDB
        table.put_item(Item={
            "visitorId":  visitor_id,
            "name":       name,
            "email":      email,
            "phone":      phone,
            "purpose":    purpose,
            "host":       host,
            "timestamp":  timestamp,
            "date":       datetime.now().strftime("%Y-%m-%d")
        })

        print(f"Visitor logged: {visitor_id} | {name} | {purpose}")

        # Send SNS alert
        sns = boto3.client("sns", region_name="us-east-1")
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="🏢 New Visitor Check-in!",
            Message=f"New visitor has checked in!\n\nVisitor ID: {visitor_id}\nName: {name}\nEmail: {email}\nPhone: {phone}\nPurpose: {purpose}\nVisiting: {host}\nTime: {timestamp}"
        )
        print(f"SNS alert sent for {visitor_id}")

        return cors_response(200, {
            "message": "Visitor logged successfully",
            "visitorId": visitor_id
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return cors_response(500, {"error": "Internal server error"})


def cors_response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "POST, OPTIONS"
        },
        "body": json.dumps(body)
    }
