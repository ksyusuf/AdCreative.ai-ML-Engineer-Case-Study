import os
import requests
import base64
from PIL import Image
from io import BytesIO


class UzakBaglanti:
    def __init__(self, prompt, image):
        # uzak bilgisayara parametre göndermeme durumu olmaz şimdilik.
        ip_adresi = "192.168.1.199"
        port = "8000"
        self.server_url = f"http://{ip_adresi}:{port}/process_image"
        # Uzak bilgisayarın IP adresi ve portunu güncelle

        image.save(os.path.join("uploads", image.filename))
        # kodlarım dosya yolu ile çalıştığı için
        # gelen resimleri önce kaydettim sonra yollarını aldım

        self.file_path = os.path.join("uploads", image.filename)
        self.prompt = prompt

    def postIt(self):
        with open(self.file_path, "rb") as image_file:
            data = base64.b64encode(image_file.read())

        # im = Image.open(BytesIO(base64.b64decode(data)))
        # im değişkeni kaydedilebilir.
        # im.save('image1.png', 'PNG')

        response = requests.post(self.server_url, data={'image': data,
                                                        'prompt': self.prompt})

        # Sunucu tarafından dönen Base64 kodlanmış işlenmiş resmi çöz
        processed_image_data = base64.b64decode(response.json()['processed_image'])

        # Çözülen veriyi resim dosyasına dönüştür
        processed_image = Image.open(BytesIO(processed_image_data))

        # İşlenmiş resmi göster veya başka bir şekilde işle
        # processed_image.show()

        return processed_image
