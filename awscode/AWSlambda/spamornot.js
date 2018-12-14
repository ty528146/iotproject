const AWS = require('aws-sdk');
const dynamodb = new AWS.DynamoDB({region: 'us-west-2', apiVersion: '2012-08-10'});
//const cisp = new AWS.CognitoIdentityServiceProvider({apiVersion:'2016-04-18'});

exports.handler = (event, context, callback) => {
    //const accessToken = event.accessToken;

    const type = event.type;
    
    const params = {"TableName":"usertext"};
    
     const response = {
         statusCode: 200,
         body: JSON.stringify('Hello from Lambda!'),
     };
    const response2 = {
        statusCode: 200,
        body: JSON.stringify('this is all'),
    };
    const response3 = {
        statusCode: 200,
        body: JSON.stringify('this is for single'),
    };
    if(type==="all"){
        dynamodb.scan(params,function(err,data){
        if(err){
            console.log(err);
            callback(err);
        }else{
            console.log(data);
            const items = data.Items.map(
                (dataField) =>{//+ convert string to integer
                    return {emailNum:data.Item.text.N};
                }
                );
            //data = {statusCode: 200,
            //body: items};//JSON.stringify(data)};
            callback(null,items); //callback(null,items);//callback(null,data);
        }
    });
    }else if(type ==="single"){
        // const cispParams = {
        //     "AccessToken":accessToken
        // };
        
         const params = {
            Key:{
                "username":
                {S:event.username
                }
            },
            TableName:"usertext"
        };
        dynamodb.getItem(params,function(err,data){
            if(err){
                console.log(err);
                callback(err);
            }else{
                console.log(data);
                callback(null,{text:data.Item.text.S});//this is very crucial must match front end 
                //array of single item// data);//{age:+data.Age.N,height:+data.Height.N,income:+data.Income.N]});
            }
    });
       
    }else{
        callback("input should only be single or all");
    }
};

