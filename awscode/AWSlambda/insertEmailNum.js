const AWS = require('aws-sdk');
const dynamodb = new AWS.DynamoDB({region: 'us-west-2', apiVersion: '2012-08-10'});
exports.handler = (event, context, callback) => {
    // TODO implement
    console.log(event);
    const params = {
        Item:{
        "username":{
            S:event.username//"user_id"+Math.random()
        },
        "emailNum":{
            N:event.emailNum
        }
    },
    TableName:"csee4764"}
    dynamodb.putItem(params,function(err,data){
        data = {statusCode: 200,
        body: JSON.stringify('Hello from Lambda!'),
    };
        if(err){
            console.log(err);
            callback(err);
        }else{
            console.log(data);
            callback(null,data);
        }
    });
        

};
