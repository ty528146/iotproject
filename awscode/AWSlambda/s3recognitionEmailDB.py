import json
import boto3
import time
import json

from botocore.exceptions import ClientError
bucket='csee4764'

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
  <p>This email was sent with
    <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
    <a href='https://aws.amazon.com/sdk-for-python/'>
      I am king of hello world</a>.</p>
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
def send_email(msg,image):
    BODY_HTML = """<html>
    <head></head>
    <body>
      <h1>Amazon SES Test (SDK for Python)</h1>
      <p>This email was sent with
        <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
        <a href='https://s3.amazonaws.com/csee4764/"""+image+"""'>
          check your email click this link to see the picture of your mail -- the content of your mail cover is """+ msg+"""</a>.</p>
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


#photo=''
AWS_REGION = "us-east-1"
#client=boto3.client('rekognition',region_name=AWS_REGION)

def lambda_handler(event, context):
    #global text_result
    print event
    time.sleep(3)
    client=boto3.client('rekognition',region_name=AWS_REGION)
    try:
        photo = str(event['Records'][0]['s3']['object']['key'])
    except:
        photo = "no photo coming"
    #photo = "csee4764.jpeg"
    print photo
    try:
        response=client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':photo}})
        textDetections=response['TextDetections']
        output = "text:"
        for text in textDetections:
                #print 'Detected text:' + text['DetectedText']
                each = text['DetectedText']
                if(len(each)<20 and len(each)>3 and 'lll' not in each and '.' not in each and ','not in each and 'iil' not in each and 'ill' not in each and not any(c.isdigit() for c in each)):
                    output = output+"--"+each
    except:
        output = "no data identified"
    aim = photo[:-5]
    print "photoname is hhhhhhhh"+aim
    print "output is hhhhhhhhhhhh"+output
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('usertext')
    response = table.put_item(
    Item={
        'username': photo[:-5],
        'text': output,
        'username2':photo[0:5]
    }
)
######this is to send email###########
    
    send_email(output,photo)
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps(output)
    }
