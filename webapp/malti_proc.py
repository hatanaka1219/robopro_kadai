from flask import Flask, render_template, request, redirect, url_for, send_from_directory,flash
import numpy as np
import cv2
from image_proc import fil_proc as fp
from image_proc import hsv
import os
app = Flask(__name__)
app.secret_key = 'hogehoge'

scale = "color"
@app.route('/')
def index():
    return render_template('index_mp.html')

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.route('/upload', methods=['POST'])
def upload():
    print("upload")
    if request.files['image']:
        # 画像として読み込み
        stream = request.files['image'].stream
        img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
        img_raw = cv2.imdecode(img_array, 1)
        if request.form['color'] == "gs":
            scale = "gs"
            print("gray scale")
            img = cv2.cvtColor(img_raw, cv2.COLOR_RGB2GRAY)
        else:
            scale = "color"
            print("full color")
            img = img_raw
        cv2.imwrite("./static/images/raw.png",img)
        flash('アップロードに成功しました',"success")
        return render_template('index_mp.html')
    else:
        print("read error")
        flash('ファイルが選択されていません',"failed")
        return render_template('index_mp.html')

@app.route('/amazonz', methods=['POST'])
def amazonzfilter():
    print("amazonzfilter")
    # 画像として読み込み
    s_magnification = 0.4
    v_magnification = 0.9
    #stream = request.files['image'].stream
    #img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
    #img_raw = cv2.imdecode(img_array, 1)
    img_raw = img = cv2.imread("./static/images/raw.png")
    img_hsv = cv2.cvtColor(img_raw, cv2.COLOR_BGR2HSV)
    img_hsv[:,:,(1)] = img_hsv[:,:,(1)]*s_magnification
    img_hsv[:,:,(2)] = img_hsv[:,:,(2)]*v_magnification
    img_bgr = cv2.cvtColor(img_hsv,cv2.COLOR_HSV2BGR)
    cv2.imwrite("./static/images/out/proc.png",img_bgr)
    return render_template('index_mp.html')



@app.route('/sendtext', methods=['POST'])
def getarray():
    in_figure = "static/images/raw.png"
    img = cv2.imread(in_figure)
    filter_33=np.zeros([3,3])
    #cv2.imshow("gray",img)
    print(filter_33)
    #print("post form---------------------------------------------------------------")
    #array = request.form["1"]
    print(type("1"))
    for i in range(3):
        for j in range(3):
            l = "arr"+str(3*i+j)
            filter_33[i,j] = request.form[l]
            print(l,request.form[l],type(float(request.form[l])))
    k =float(request.form["numk"])
    k = np.array(k)
    kanel = np.array(filter_33)

    print(kanel/k)

    # index.html をレンダリングする
    h_magnification = float(request.form["h"])
    s_magnification = float(request.form["s"])
    v_magnification = float(request.form["v"])
    img_fil = fp(img,kanel/k)
    if scale != "gs":
        img_out = hsv(img_fil,h_magnification,s_magnification,v_magnification)
    else:
        img_out = img_fil
    cv2.imwrite("./static/images/out/proc.png",img_out)
    print("end save")
    return render_template('index_mp.html')


if __name__ == '__main__':
    app.debug = True
    finit = np.ones([10,10])
    finit *= 255
    cv2.imwrite("./static/images/raw.png",finit)
    cv2.imwrite("./static/images/out/proc.png",finit)
    app.run(host='0.0.0.0')
