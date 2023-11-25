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

        import os
        import socket

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

        response = requests.post(self.server_url, data={'image': data,
                                                        'prompt': self.prompt})

        # Sunucu tarafından dönen Base64 kodlanmış işlenmiş resmi çöz
        processed_image_data = base64.b64decode(response.json()['processed_image'])

        # Çözülen veriyi resim dosyasına dönüştür
        processed_image = Image.open(BytesIO(processed_image_data))

        # İşlenmiş resmi göster veya başka bir şekilde işle
        # processed_image.show()

        return processed_image
