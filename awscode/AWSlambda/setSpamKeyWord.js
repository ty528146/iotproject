const AWS = require('aws-sdk');
const dynamodb = new AWS.DynamoDB({region: 'us-west-2', apiVersion: '2012-08-10'});
//const cisp = new AWS.CognitoIdentityServiceProvider({apiVersion:'2016-04-18'});
AWS.config.update({
  region: "us-west-2"
});

var docClient = new AWS.DynamoDB.DocumentClient();

var table = "testsetspam";
exports.handler = (event, context, callback) => {
    //const accessToken = event.accessToken;

    const type = event.type;
    
    const params = {"TableName":"testsetspam"};
    if(type==="delete"){
        console.log("delete")
            var params2 = {
            TableName:table,
            Key:{
                "username":event.username,
                "keyword":event.keyword
            }
        };
        console.log("Attempting a conditional delete...");
        docClient.delete(params2, function(err, data,data2) {
            if (err) {
                console.error("Unable to delete item. Error JSON:", JSON.stringify(err, null, 2));
            } else {
                console.log("DeleteItem succeeded:", JSON.stringify(data, null, 2));
                data2 = {statusCode: 200,
        body: JSON.stringify('delete successfully!'),
    };
                callback(null,data2);
            }
});
    }else if(type ==="set"){
        // const cispParams = {
        //     "AccessToken":accessToken
        // };
        const params = {
        Item:{
        "keyword":{
            S:event.keyword//"user_id"+Math.random()
        },
        "username":{
            S:event.username
        }
    },
    TableName:"testsetspam"}
    dynamodb.putItem(params,function(err,data){
        data = {statusCode: 200,
        body: JSON.stringify('insert and set spam successfully!'),
    };
        if(err){
            console.log(err);
            callback(err);
        }else{
            console.log(data);
            callback(null,data);
        }
    });
       
       
    }else{
        callback("input should only be single or all");
    }
};

