import os
import requests
import base64
from PIL import Image
from io import BytesIO

"""
BURASI SUNUCA ÇALIŞACAK
RESMİ VE PROMTU ALIP YEREL BİLGİSAYARA GÖNDERECEK VE İŞLENMİŞ RESMİ ALACAK.
SADECE STABLE DİFFUSİON İLE RESİM ÜRETME İŞİ YERELDE OLACAK, GERİSİ SUNUCUDA.
isteği sunucu yapar. yerel bilgisayar karşılar.
sunucu yerel bilgisayara post işlemi yapar. promt + image --->>> return generated_image
"""


class UzakBaglanti:
    def __init__(self, prompt, image, server_url):
        # uzak bilgisayara da parametre göndermeme durumu olmaz ya.
        self.server_url = server_url  # Uzak bilgisayarın IP adresi ve portunu güncelle

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
