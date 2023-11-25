import base64
from io import BytesIO
from flask import Flask, render_template, request
import main
import os
import socket

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
# daha sonra bu yapı değiştirilip yüklenen ve oluşturulan
# resimler farklı klasörlere kaydedilebilir.


@app.route('/')
def index():

    def get_ip_address():
        # Socket oluştur
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            # Google'ın DNS sunucusuna bağlan
            s.connect(('8.8.8.8', 80))
            ip_address = s.getsockname()[0]
        except socket.error:
            ip_address = '127.0.0.1'  # Eğer bağlantı kurulamazsa varsayılan IP adresi

        finally:
            s.close()

        return ip_address

    def get_port():
        port = int(os.environ.get('PORT', 8000))
        return port

    ip_address = get_ip_address()
    port = get_port()

    print(f"Sunucu IP adresi: {ip_address}")
    print(f"Kullanılan port: {port}")
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    # todo: bu yapının ajax ile yapılması daha iyi olur.
    # daha kullanıcı dostu olur.

    # Formdan gelen verileri al
    image = request.files['image']
    promt = request.form['promt']
    logo = request.files['logo']
    color = request.form['color']
    punchline = request.form['punchline']
    button_text = request.form['button_text']

    # verilern parametreler ile stable diffusion ile resim oluşturuluyor.
    generated_image = main.sunu.CreateImage(prompt=promt, image=image)
    print("generated_image tipi: ", generated_image)

    ### -----------------
    # # üretilmiş resmi 'uploads' klasörüne kaydet.
    # generated_image.save(os.path.join(app.config['UPLOAD_FOLDER'], "uretilmis_resim.jpg"))
    #
    # # üretilmiş resmin bulunduğu yolu al.
    # result_image_path = os.path.join(app.config['UPLOAD_FOLDER'], "uretilmis_resim.jpg")
    # bu metotları iptal ettim çünkü sunucu içerisinde kayıt yapamıyorum
    ### -----------------

    # üretilmiş resmi klasörden çekip template oluşturmaya başla.
    generate_template = main.sunu.CreateTemplate(generated_image=generated_image,
                                                 logo_path=logo,
                                                 punchline=punchline,
                                                 button_text=button_text,
                                                 button_punchline_color=color)
    # Resmi ön tarafa gönderebilmek için base64 formatına dönüştür
    img_buffer = BytesIO()
    generate_template.save(img_buffer, format="JPEG")
    img_str = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

    # template'i ön tarafa gönder ve karşıla.
    return render_template('index.html', result_image=img_str)


if __name__ == '__main__':
    app.run(debug=True)
