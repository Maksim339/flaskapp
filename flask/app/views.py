from app import app
from flask import request, jsonify, Blueprint, Flask
import os
from PIL import Image
from pdf2image import convert_from_path
import json
from flask_cors import CORS, cross_origin

CORS(app, resources={r"/upload": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
from datetime import timedelta

ALLOWED_EXTENSIONS = set(['png', 'PNG', 'JPG', 'jpg', 'PDF', 'pdf', 'JPEG', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# set static cache
app.send_file_max_age_default = timedelta(seconds=1)


def clean_response(text_list):
    clean_list = []
    one_string_list = []
    for string in text_list:
        if string.find('73d15fc8') == -1:
            one_string_list.append(string)
        else:
            clean_list.append(" ".join(one_string_list))
            one_string_list = []
    return clean_list


def _parse_by_position(path):
    open_json = open(path)
    data_json = json.load(open_json)
    response = []
    for _ in data_json["DocumentMetadata"]:
        for a in data_json["Blocks"]:
            if a["BlockType"] == "LINE":
                response.append(a["Text"])
    return clean_response(response)


def cropp(im):
    areas = {}
    i = 0
    while i < 100:
        y0, x0 = request.form.get(f"areas[{i}][top]"), request.form.get(f"areas[{i}][left]")
        if x0 and y0:
            y1, x1 = int(y0) + int(request.form.get(f"areas[{i}][height]")), int(x0) \
                     + int(request.form.get(f"areas[{i}][width]"))
            areas[i] = x0, y0, x1, y1
            im_crop = im.crop((int(x0), int(y0), int(x1), int(y1)))
            im_crop.save(f"images/area{i}.jpg")
            i += 1
        else:
            break


def add_background(w, h):
    fds = os.listdir('images')
    hash_pic = Image.open('hash_key.png')
    fds.sort()
    i = 10
    background = Image.new('RGB', (w * 2, h * 3), (255, 255, 255))
    for im in fds:
        img = Image.open(f'images/{im}')
        offset = 100, i
        background.paste(img, offset)
        i += img.size[1] + 20
        offset = 100, i
        background.paste(hash_pic, offset)
        background.save('background.jpg')
        i += hash_pic.size[1] + 20
        os.remove(f'images/{im}')



@app.post('/upload')
@cross_origin(origin='*', headers=['content-type'])
def upload():
    f = request.files["files[0][file]"]
    filename = request.form.get("files[0][name]")

    if not (f and allowed_file(filename)):
        return jsonify({"error": 1001, "   msg": "Only .png, .jpg, .pdf"})
    else:
        width = request.form.get("files[0][width]")
        height = request.form.get("files[0][height]")
        w, h = int(width), int(height)
        if filename.rsplit('.', 1)[1] == "PDF" or filename.rsplit('.', 1)[1] == "pdf":
            f.save("content.pdf")
            images = convert_from_path('content.pdf')
            for i in range(len(images)):
                images[i] = images[i].resize((w, h))
                cropp(images[i])
            os.remove('content.pdf')
        else:
            im = Image.open(f)
            im = im.resize((w, h))
            im = im.convert('RGB')
            cropp(im)
        add_background(w, h)
        path_to_image = "background.jpg"
        try:
            os.system(
                f'amazon-textract --input-document'
                f' "{path_to_image}" --pretty-print-table-format csv > test.json')
        except Exception as e:
            os.system('echo ошибка')
            print(e, 'ошибка')
        ans = _parse_by_position('test.json')
        ans_msg = {filename: ans}

        return ans_msg

#
# if __name__ == '__main__':
#     app.run(host='0.0.0.0')

