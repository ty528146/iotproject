from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

table_spam = dynamodb.Table('testsetspam')

table_mailtext = dynamodb.Table('usertext')

def lambda_handler(event, context):
    # TODO implement
    username = event["username"]
    # print(username)
    username2 = event["username2"]
    #print(username2)
    responseSpam = []
    responseText = []
    ##############get the spam word from database###################
    try:
        responseSpam = table_spam.query(KeyConditionExpression=Key('username').eq(username))
        print((responseSpam))
    except:
        responseSpam = []
    print("==============================================")
    try:
        responseText = table_mailtext.query(KeyConditionExpression=Key('username2').eq(username2))
        print((responseText))
    except:
        responseText = []    
   
    
    spamword = []
    responselist = []
    spameach = ""
    texteach = ""
    processed = ""
    num = 0
    flag = 0
    # for spam in responseSpam['Items']:
    #     spameach = spam["keyword"]
    #     print(spameach)
        #spamword.append(spam["keyword"])
    for text in responseText['Items']:
        texteach = text['text']
        #print ('texteach'+texteach)
        
        try:
            responseText = table_mailtext.query(KeyConditionExpression=Key('username2').eq(username2)&Key('username').eq(texteach))
            print((responseText)['Items'][0]['text'])
        except:
            responseText = []  
        for spam in responseSpam['Items']:
            spameach = spam["keyword"]
            if(spameach in texteach):
                flag = 1
        print("flag"+str(flag))
        if(flag == 0):
            textlist = texteach.split('/')
            for each in textlist:
                processed = processed + "-"+each
            #responselist.append(texteach)
            responselist.append(processed)
            num += 1
        flag = 0
        processed = ""
    #responseset = set(responselist)
    #num = len(responseset)
    #print(num)
    return {
        'statusCode': 200,
        'body': json.dumps(responselist),
        'emailnum':num
    }
