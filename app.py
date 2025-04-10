from flask import Flask, render_template, request, url_for, send_file ,after_this_request
from rembg import remove
import random
import time
import os

app = Flask(__name__)

upload = "upload"
output = "output"
time = 300 #5min

os.makedirs(upload, exist_ok=True)
os.makedirs(output, exist_ok=True)


def check_and_delete_file(file_path):
    if os.path.exists(file_path):
        if os.path.isfile(file_path):
            os.remove(file_path)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        upload_image = request.files['image']
        file_name = f"{random.randint(1000, 9999)}.{upload_image.filename.split('.')[-1]}"
        upload_path = os.path.join(upload, file_name)
        upload_image.save(upload_path)


        with open(upload_path, "rb") as input_file:
            input_data = input_file.read()
            output_data = remove(input_data)


        output_filename = f"output_{file_name}"
        output_file_path = os.path.join(output, output_filename)
        with open(output_file_path, "wb") as output_file:
            output_file.write(output_data)
            check_and_delete_file(f"upload/{file_name}")


        return render_template("index.html", output_image=output_filename)

    return render_template("index.html")


@app.route('/download/<filename>')
def download(filename):
    file_path = os.path.join(output, filename)



    return send_file(file_path, as_attachment=True)


import threading

def clear_output_folder():
    while True:
        time.sleep(300)
        for file_name in os.listdir(output):
            file_path = os.path.join(output, file_name)
            if os.path.isfile(file_path):
                try:
                    print("file have remove")
                    os.remove(file_path)
                except Exception:
                    pass

threading.Thread(target=clear_output_folder, daemon=True).start()

if __name__ == "__main__":
    app.run(debug=True)