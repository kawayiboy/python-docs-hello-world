# -*- coding: UTF-8 -*-
import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory
from flask import send_file
from PIL import Image, ImageFilter
import numpy as np

UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#http://flask.pocoo.org/docs/0.12/patterns/fileuploads/

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    im = Image.open(filename)
    im2 = im.filter(ImageFilter.BLUR)
    im2.save(filename)
    # return send_from_directory(app.config['UPLOAD_FOLDER'],
    #                            filename)
    return redirect(url_for('line_file',
                                    filename=filename))

def image_linestyle(filename,depths=10):
    a = np.asarray(Image.open(filename).convert('L')).astype('float')
    depth = depths  # 深度的取值范围(0-100)，标准取10
    grad = np.gradient(a)  # 取图像灰度的梯度值
    grad_x, grad_y = grad  # 分别取横纵图像梯度值
    grad_x = grad_x * depth / 100.#对grad_x值进行归一化
    grad_y = grad_y * depth / 100.#对grad_y值进行归一化
    A = np.sqrt(grad_x ** 2 + grad_y ** 2 + 1.)
    uni_x = grad_x / A
    uni_y = grad_y / A
    uni_z = 1. / A
    vec_el = np.pi / 2.2  # 光源的俯视角度，弧度值
    vec_az = np.pi / 4.  # 光源的方位角度，弧度值
    dx = np.cos(vec_el) * np.cos(vec_az)  # 光源对x 轴的影响
    dy = np.cos(vec_el) * np.sin(vec_az)  # 光源对y 轴的影响
    dz = np.sin(vec_el)  # 光源对z 轴的影响
    b = 255 * (dx * uni_x + dy * uni_y + dz * uni_z)  # 光源归一化
    b = b.clip(0, 255)
    im = Image.fromarray(b.astype('uint8'))  # 重构图像
    return im

@app.route('/line/<filename>')
def line_file(filename):
    newfilename = 'line_'+filename
    if not os.path.exists(newfilename):
        im = image_linestyle(filename)
        im.save(newfilename)
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               newfilename)

#https://stackoverflow.com/questions/7877282/how-to-send-image-generated-by-pil-to-browser
# @app.route('/path')
# def view_method():
#     response = send_file(tempFileObj, as_attachment=True, attachment_filename='myfile.jpg')
#     return response

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)