from flask import Flask
from flask_cors import CORS
from flask import Flask, jsonify, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import pandas as pd
import recommand
import os
import json
import time

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'csv', 'txt', 'pdf', 'png', 'jpg', 'jpeg', }
dp = recommand.myrecommend()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def cleanFolder():
    folders = ["static/uploads", "html"]
    basepath = os.path.dirname(__file__)  # 当前文件所在路径
    for path in folders:
        files = os.listdir(os.path.join(basepath, path))
        files.sort()
        if len(files) > 10:
            for one in files[10:]:
                if one[0] != '.':
                    os.remove(os.path.join(basepath, path, one))

def getCharts(myfile):
    dp.read_csv(myfile)
    # choose one from three ranking function
    # dp.learning_to_rank()
    # dp.partial_order()
    # dp.diversified_ranking()
    dp.ranking()
    # output functions
    # can use several different methods at the same time

    # dp.to_single_html()
    # dp.to_single_json()
    # dp.to_multiple_htmls()
    # dp.to_list()
    # dp.to_print_out()
    # dp.to_multiple_jsons()
    # dp.show_visualizations().render_notebook()
    tmp_list =  dp.to_list()
    list = []
    rows = len(tmp_list)
    if (rows <= 0):
        for item in tmp_list:
            list.append(json.loads(item))
    else:
        index = 0
        for item in tmp_list:
            if(index < 20):
                list.append(json.loads(item))
                index += 1
            else:
                break
    list.clear()
    for item in tmp_list:
        list.append(json.loads(item))
    return jsonify(list)

@app.route('/api')
def hello_world():
    return 'This is the api.'

@app.route('/api/getcharts', methods=['POST'])
def getcharts():
    f = request.files['file']
    cols = request.form.get('cols')
    if not cols:
        cols = [] # No cols specified
    basepath = os.path.dirname(__file__)  # 当前文件所在路径
    upload_path = os.path.join(basepath, 'static/uploads', str(int(time.time())) + secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
    f.save(upload_path)

    # Delete columns
    cols = list(map(lambda n: int(n), cols.split(',')))
    if len(cols) > 0:
        # 如果限制了只读取 csv 中的几列
        df = pd.read_csv(upload_path)
        columns_to_delete = []
        for i in range(len(df.columns)):
            if cols.count(i) == 0:
                columns_to_delete.append(df.columns[i])
        for c in columns_to_delete:
            df.drop(c, axis=1, inplace=True)
    df.to_csv(upload_path, index=False)
    result = getCharts(upload_path)

    cleanFolder()
    return result


if __name__ == "__main__":
    app.run(debug=True)
