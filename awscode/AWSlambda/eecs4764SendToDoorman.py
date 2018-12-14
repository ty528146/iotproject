import json

import boto3
from botocore.exceptions import ClientError

print('Loading function')

# Replace sender@example.com with your "From" address. # This address must be verified with Amazon SES. 
SENDER = "tyb528146@outlook.com"
# Replace recipient@example.com with a "To" address. If your account # is still in the sandbox, this address must be verified.
RECIPIENT = "qz2343@columbia.edu"#"tyb528146@outlook.com"
# Specify a configuration set. If you do not want to use a configuration # set, comment the following variable, and the
# ConfigurationSetName=CONFIGURATION_SET argument below. CONFIGURATION_SET = "ConfigSet"
# If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES. AWS_REGION = "us-west-2"
CONFIGURATION_SET = "ConfigSet"
# If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES. 
AWS_REGION = "us-east-1"
# The subject line for the email.
SUBJECT = "Amazon SES Test (SDK for Python)"
# The email body for recipients with non-HTML email clients.

BODY_HTML = """<html>
<head></head>
<body>
  <h1>Amazon SES Test (SDK for Python)</h1>
  <p>This email was sent  from user """+ "username" +"""Dear officer,
  This email is to remind you that some emails have been delivered to the wrong user.
  Kind regards,
  """+"molly"+"""
    <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
    <a href='https://aws.amazon.com/sdk-for-python/'>
      </a>.</p>
</body>
</html>
"""

# The email body for recipients with non-HTML email clients.
BODY_TEXT = ("Amazon SES Test (Python)\r\n"
             "I am king of hello world."
            )
# The HTML body of the email.

# The character encoding for the email.
CHARSET = "UTF-8"
# Create a new SES resource and specify a region.

client = boto3.client('ses',region_name=AWS_REGION)
# Try to send the email.
def send_email(msg,username):
    BODY_HTML = """<html>
    <head></head>
    <body>
      <h1>Amazon SES Test (SDK for Python)</h1>
      <p>This email was sent  from user """+ username +"""<p>Dear officer,</p>
  <p>This email is to remind you that some emails have been delivered to the wrong user.</p>
  <p>Kind regards,</p>
  """+"""<p>"""+username+"""</p>"""+"""
    <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
    <a href='https://aws.amazon.com/sdk-for-python/'>
      </a>.</p>
    </body>
    </html>
    """
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    "qz2343@columbia.edu"# "tyb528146@outlook.com"
                ],
}, Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
           # ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

def lambda_handler(event, context):
    #username = event['username']
    username = "user1"
    #print(event['username'])
    msg = "hhh"
    send_email(msg,username)
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('send email successfully!')
    }
