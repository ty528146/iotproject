const AWS = require('aws-sdk');
const dynamodb = new AWS.DynamoDB({region: 'us-west-2', apiVersion: '2012-08-10'});
exports.handler = (event, context, callback) => {
    // TODO implement
    console.log(event);
    const params = {
        Item:{
        
        "Board":{
            S:event.board
        },
        
        "location":{
            S:event.locationtwo
        }
        
    },
    TableName:"location"}
    dynamodb.putItem(params,function(err,data){
        data = {statusCode: 200,
        body: JSON.stringify('locationsent!'),
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
