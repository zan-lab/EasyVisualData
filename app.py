from random import randrange
import os
from flask import Flask, render_template, json, make_response, send_file, send_from_directory
from flask import flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from Graph import *
import ExcelParse as ep
from common import *
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'xls','xlsx'}

#初始化工作
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 路由大军
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload",methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return Res(code=-1,msg="No file part")
    file = request.files['file']

    if file.filename == '':
        return Res(code=-1,msg='No selected file')
    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return Res({"filename":file.filename})

@app.route("/checktablename/<filename>/<tablename>",methods=['GET'])
def checktable(filename,tablename):
    return checkTableName(filename,tablename)

@app.route("/gettablename/<filename>",methods=['GET'])
def gettable(filename):
    return getTableName(filename)

@app.route("/rendertable",methods=["POST"])
def rendertable():
    strdata=list(request.form.to_dict().keys())[0]
    jsondata=json.loads(strdata)
    #创建对象并处理空数据
    graph=Graph(jsondata)
    resdict=graph.render()
    return resdict

@app.route("/downloads/<filename>",methods=['GET'])
def downloads(filename):
    directory = os.path.abspath('./downloads')  # 规定目录
    return send_from_directory(directory, filename, as_attachment=True)

#自带函数
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#程序主入口
if __name__ == "__main__":

    app.config['JSON_AS_ASCII'] = False
    app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"
    app.run()