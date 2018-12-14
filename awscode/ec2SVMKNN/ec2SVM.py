from flask import Flask,render_template,flash,url_for,redirect,request,jsonify
from flask_pymongo import PyMongo
from sklearn import svm,neighbors
from sklearn.externals import joblib
import json
#from content_management import 
app = Flask(__name__)#is an object main app help determine the route
######
a = {"a":1,"b":2,"c":3,"d":4,"e":5,"f":6,"g":7,"h":8,"i":9,"j":10,"k":11,"l":12,"m":13,"n":14,"o":15,"p":16,"q":17,"r":18,"s":19,"t":20,"u":21,"v":22,"w":23,"x":24,"y":25,"z":26}
def changeString(str1):
    c = ""
    for i in str1:
        if i in a:
            c += str(a[i])
        else:
            c += str(0)
    return c
def splitStringToNParts(n,str1):
    result = []
    print str1
    resultstr = []
    for i in range(0,n):
        each = str1[i*((len(str1)/n)):(i+1)*(len(str1)/n)]
        result.append(int(each))
    return result, resultstr

app.config['MONGO_DBNAME']= 'myiotdb'
app.config['MONGO_URI']= 'mongodb://localhost:27017/myiotdb'
mongo= PyMongo(app)
@app.route('/insert',methods = ['GET','POST'])
def insert():
        error = None
        coo = mongo.db.mailtext
        #if request.method == "GET":
                #return render_template("dogs2.html")
        try:
                if request.method == "POST":
                        '''
                        data= request.get_json()
                        #e)
                        xcol = data['xcol']
                        ycol = data['ycol']
'''
                        xcol=request.json["emailtext"]
                        ycol=request.json['label']
                        #print ycol
                        print xcol
                        coo.insert({'emailtext': xcol,'label':ycol})
                #        return jsonify({'result':'sucess post'})#username#render_template("dogs3.html")

                       # return jsonify({'result':'sucess post'+ycol})
                        return jsonify({'result':'sucess post'+ycol})
#                       return '200ok'+str(xcol)
                else:
                        error = "err"

                return jsonify({'result':'sucess get'})

        except Exception as e:
                return str(e)
@app.route('/')
def index():
        return "this is an home page"


@app.route('/predict',methods = ['GET','POST'])
def predict():
        error = None
        #coo = mongo.db.coo
        #if request.method == "GET":
                #return render_template("dogs2.html")
        try:
                if request.method == "POST":
                        data= request.get_json()
                        #e)
                        str2 = data['emailtext']
                       # aim1 =  ''.join(str(ord(c)) for c in s1)
                        print str2
                        result, resultstr= splitStringToNParts(12,changeString(str2))
                        print result
                        xcol = result
                        ycol = data['label']
                        xcol = (xcol)
                        print xcol
                        #xcol = xcol
                        filename = 'finalized_model.sav'
                        loaded_model = joblib.load(filename)
                        prediction = loaded_model.predict([xcol])
                        print prediction
                        return jsonify({'the prediction is':str(prediction),'the real is':str(eval(ycol))})#str(type(eval(xcol)))#jsonify({'result':'sucess post'+ycol})
                else:
                        error = "err"
                return jsonify({'result':'sucess get'})

        except Exception as e:
                return "there is error"+str(e)
@app.route('/train')
def train():
#this place change the database
        coo = mongo.db.mailtext
        X_col = []
        Y_col = []
        for each in coo.find():
        #<type 'unicode'>,      X_col.append(type(each['xcol']))
                 str2 = each['emailtext']
                 result,resultstr= splitStringToNParts(12,changeString(str2))
                 X_col.append(result)
                #X_col.append((each['xcol']))

        #X_col.append(json.loads(each)['xcol'])
                 Y_col.append(int(each['label']))
        print X_col
        print Y_col
        clf = svm.LinearSVC()
        clf.fit(X_col, Y_col)
        filename = 'finalized_model.sav'
        joblib.dump(clf, filename)
        return str(X_col)

if __name__ == "__main__":
        app.run(debug=True,host='0.0.0.0',port=80)