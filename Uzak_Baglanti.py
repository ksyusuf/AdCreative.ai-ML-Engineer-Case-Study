import requests
import base64
from PIL import Image
from io import BytesIO

from flask import jsonify


class UzakBaglanti:
    def __init__(self, prompt, image):
        # uzak bilgisayara parametre göndermeme durumu olmaz şimdilik.
        ip_adresi = "192.168.1.199"
        port = "8000"
        genel_adres = "[2a02:4e0:2d98:6f59:5b46:6fc5:9851:19f2]"
        # self.server_url = f"http://{ip_adresi}:{port}/process_image"
        self.server_url = f"http://{genel_adres}:{port}/process_image"
        # malesef genel ip adresli olay çalışmıyor.
        # muhtemelen modem ayarlarını falan yapamadım
        # Uzak bilgisayarın IP adresi ve portunu güncelle

        self.image = image
        self.prompt = prompt

    def postIt(self):
        # with open(self.file_path, "rb") as image_file:
        #     data = base64.b64encode(image_file.read())

        # Dosyayı kaydetmeden okuma işlemi
        with self.image.stream as image_file:
            data = base64.b64encode(image_file.read())

        # im = Image.open(BytesIO(base64.b64decode(data)))
        # im değişkeni kaydedilebilir.
        # im.save('image1.png', 'PNG')

        try:
            response = requests.post(self.server_url, data={'image': data,
                                                            'prompt': self.prompt})
        except Exception as e:
            # Hata durumunda hata mesajını al ve istemciye gönder
            error_message = f"Error: {str(e)}"
            return jsonify({'error': error_message}), 500

        # Sunucu tarafından dönen Base64 kodlanmış işlenmiş resmi çöz
        processed_image_data = base64.b64decode(response.json()['processed_image'])

        # Çözülen veriyi resim dosyasına dönüştür
        processed_image = Image.open(BytesIO(processed_image_data))

        # İşlenmiş resmi göster veya başka bir şekilde işle
        # processed_image.show()

        return processed_image

    def GetIt(self):
        try:
            response = requests.get(self.server_url)
        except Exception as e:
            # Hata durumunda hata mesajını al ve istemciye gönder
            error_message = f"Error: {str(e)}"
            return jsonify({'error': error_message}), 500

        return response.text


if __name__ == '__main__':
    baglanti = UzakBaglanti(None, None)
    baglanti.GetIt()

