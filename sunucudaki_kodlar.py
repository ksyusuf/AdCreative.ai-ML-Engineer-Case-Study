from io import BytesIO
from PIL import Image
import requests
import time

#### BURASI SUNUCA ÇALIŞACAK
#### RESMİ VE PROMTU ALIP YEREL BİLGİSAYARA GÖNDERECEK VE İŞLENMİŞ RESMİ ALACAK.
#### SADECE STABLE DİFFUSİON İLE RESİM ÜRETME İŞİ YERELDE OLACAK, GERİSİ SUNUCUDA.

server_url = "http://192.168.1.199:8080"  # Bilgisayarınızın IP adresini ve port numarasını KONTROL ET


def bilgisayar_durumu_kontrol():
    try:
        response = requests.get(server_url)

        # Resim içeriğini al
        image_data = response.content

        # Resmi aç ve göster
        received_image = Image.open(BytesIO(image_data))
        received_image.show()

    except requests.ConnectionError:
        print("Bilgisayar kapalı!")

def promt_gonder(promt):
    return 0

def generated_image_al():
    return 0
# todo: bunlar sırayla olursa sıkıntı olmaz diye düşünüyorum.

def resim_gonder(file_path, server_url):
    try:
        with open(file_path, 'rb') as file:
            files = {'file': file}
            response = requests.post(server_url, files=files)
            print(response.content)

        if response.status_code == 200:

            print("Resim başarıyla gönderildi.")
        else:
            print(f"Hata oluştu. Sunucu yanıt kodu: {response.status_code}")

    except FileNotFoundError:
        print("Belirtilen dosya bulunamadı.")
    except requests.ConnectionError:
        print("Sunucuya bağlantı hatası.")

if __name__ == '__main__':
    # while True:
    #     bilgisayar_durumu_kontrol()
    #     time.sleep(60)
    resim_gonder(file_path="C:/Users/ksyus/Documents/Yazılımsal Projeler/adCreative.ai iş başvuru case "
                           "çalışması/AdCreative.ai-ML-Engineer-Case-Study/uploads/coffee-logo.png",
                 server_url=server_url)
    bilgisayar_durumu_kontrol()
