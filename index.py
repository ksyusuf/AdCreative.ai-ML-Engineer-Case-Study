import base64
from io import BytesIO

from flask import Flask, render_template, request
import os
import main

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    # Formdan gelen verileri al
    image = request.files['image']
    promt = request.form['promt']
    logo = request.files['logo']
    color = request.form['color']
    punchline = request.form['punchline']
    button_text = request.form['button_text']

    # Verileri işle (örneğin, resmi işle ve yeni bir resim oluştur)
    # Bu kısmı ihtiyacınıza göre özelleştirebilirsiniz.
    print("resim oluşturma başladı.")
    print("image: ", image)
    print("promt: ", promt)
    print("logo: ", logo)
    print("color: ", color)
    print("punchline: ", punchline)
    print("button_text: ", button_text)
    generated_image = main.sunu.CreateImage(prompt=promt, image=image)

    # Örneğin, yüklenen resmi 'uploads' klasörüne kaydet
    generated_image.save(os.path.join(app.config['UPLOAD_FOLDER'], "uretilmis_resim.jpg"))

    # Sonucun bulunduğu yolu belirt
    result_image_path = os.path.join(app.config['UPLOAD_FOLDER'], "uretilmis_resim.jpg")

    generate_template = main.sunu.CreateTemplate(generated_image=result_image_path,
                                                 logo_path=logo,
                                                 punchline=punchline,
                                                 button_text=button_text,
                                                 button_punchline_color=color)
    print("generated_image:", generate_template)  # Bu satır eklenmiş
    # Resmi base64 formatına dönüştür
    img_buffer = BytesIO()
    generate_template.save(img_buffer, format="JPEG")
    img_str = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

    # Şablona sonucun yolunu ve diğer verileri gönder
    return render_template('index.html', result_image=img_str)


if __name__ == '__main__':
    app.run(debug=True)
