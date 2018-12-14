const AWS = require('aws-sdk');
const dynamodb = new AWS.DynamoDB({region: 'us-west-2', apiVersion: '2012-08-10'});
exports.handler = (event, context, callback) => {
    // TODO implement
    
    var params2 = {
    TableName : "usertext",
   KeyConditionExpression: 'username2 = :i',
      ExpressionAttributeValues: {
        ':i': { "S": "user1" }
      }
};

dynamodb.query(params2, function(err, data) {
    if (err) {
        console.log("Unable to query. Error:", JSON.stringify(err, null, 2));
    } else {
        console.log("Query succeeded.");
        data.Items.forEach(function(item) {
            console.log(" -", item.username.S + ": " + item.username.S
            );
            
            const params = {
        Key:{"username2":
            {
            S:"user1"//"sakjdflafasf123"//can appear at most once
            },
            "username":
            {
            S:item.username.S//"*"//"sakjdflafasf123"//can appear at most once
            }
        },
        TableName:"usertext"
    };
    dynamodb.deleteItem(params,function(err,data){
        if(err){
            console.log(err);
            callback(err);
        }else{
            console.log(data);
            data = {statusCode:200,
                body:data
            }
            callback(null,data);
        }
    });
            
        });
    }
});
    
    
    
};
