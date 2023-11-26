from io import BytesIO

from PIL import Image
import os
from PIL import ImageDraw, ImageFont


def uniquify(path):
    """kaydedilen dosyaların isimlerini benzersiz yapar."""
    filename, extension = os.path.splitext(path)
    counter = 1
    while os.path.exists(path):
        path = filename + " (" + str(counter) + ")" + extension
        counter += 1
    return path


class Template:
    def create_ad_template(self, generated_image, logo, punchline, button_text, button_punchline_color):
        # Kaynak resmi açın
        # generated_image = Image.open(generated_image)
        # image.open fonksiyonu resmi string olarak alır.
        print("template'e gelen resim türü:\n", type(generated_image))
        print(generated_image)
        background = Image.new("RGB", (generated_image.width, generated_image.height), "blue")
        background.paste(generated_image, (0, 0))  # İkinci argüman, yapıştırma konumunu belirtir

        # Reklam şablonunu oluşturmak için yeni bir görüntü oluşturun
        ad_template = Image.new("RGB", (800, 800), "white")

        # Logo ekleyin
        logo = Image.open(logo).convert("RGBA").resize((200, 100))
        logo_position = ((ad_template.width - logo.width) // 2, 30)
        ad_template.paste(logo, logo_position, logo)

        # Oluşturulan görseli ortaya ekleyin
        generated_image = generated_image.resize((384, 384))
        image_position = ((ad_template.width - generated_image.width) // 2, logo_position[1] + logo.height + 20)
        ad_template.paste(generated_image, image_position)

        # Punchline'ı ekleyin
        draw = ImageDraw.Draw(ad_template)
        # Fontu seç
        # Scriptin bulunduğu klasörün yolu
        script_folder = os.path.dirname(os.path.abspath(__file__))
        # Font dosyasının tam yolu
        font_path = os.path.join(script_folder,
                                 'Yazi-Font',
                                 'PlayfairDisplay-ExtraBold.ttf')
        font_size = 44
        font = ImageFont.truetype(font_path, font_size)

        # Metni \n kaçış dizesine göre böl
        lines = punchline.split('\n')

        # İlk satırın boyutlarını ölç
        text_width, text_height = draw.textbbox((0, 0), lines[0], font=font)[2:]

        # İlk satırı resme ekle
        x1 = (ad_template.width - text_width) / 2
        y1 = image_position[1] + generated_image.height + 25  # üstteki resimden 25px aşağı yerleştiriyoruz.
        draw.text((x1, y1), lines[0], fill=button_punchline_color, font=font)

        # Eğer ikinci satır varsa, onu da resme ekle
        if len(lines) > 1:
            # İkinci satırın boyutlarını ölç
            text_width, text_height = draw.textbbox((0, 0), lines[1], font=font)[2:]

            # İkinci satırı resme ekle
            x2 = (ad_template.width - text_width) / 2
            y2 = y1 + text_height + 10  # 10 piksel boşluk bırak
            draw.text((x2, y2), lines[1], fill=button_punchline_color, font=font)

        def rounded_rectangle(draw, position, size, radius=25, fill="white", outline=None):
            """butonun kenarlarını yuvarlar."""
            x, y = position
            width, height = size
            draw.pieslice([x, y, x + 2 * radius, y + 2 * radius], 180, 270, fill=fill, outline=outline)
            draw.pieslice([x + width - 2 * radius, y, x + width, y + 2 * radius], 270, 360, fill=fill, outline=outline)
            draw.pieslice([x, y + height - 2 * radius, x + 2 * radius, y + height], 90, 180, fill=fill, outline=outline)
            draw.pieslice([x + width - 2 * radius, y + height - 2 * radius, x + width, y + height], 0, 90, fill=fill,
                          outline=outline)
            draw.rectangle([x + radius, y, x + width - radius, y + height], fill=fill, outline=outline)
            draw.rectangle([x, y + radius, x + width, y + height - radius], fill=fill, outline=outline)

            # Butonun içine yazı ekleyin
            font_size_button = 20
            font_button = ImageFont.truetype(font_path, font_size_button)  # punchline'ın fontu

            # Yazıyı butonun içine yerleştirin
            text_width_button, text_height_button = draw_button.textbbox((0, 0), button_text, font=font_button)[2:]
            x_button = x + (width - text_width_button) // 2  # Butonun ortasına yerleştirmek için
            y_button = y + (height - text_height_button) // 2  # Butonun ortasına yerleştirmek için
            draw_button.text((x_button, y_button), button_text, fill="white", font=font_button)

        # Button'u ekle
        button_width = 200
        button_height = 50
        draw_button = ImageDraw.Draw(ad_template)

        # Butonun konumunu belirleyin ve resme ekleyin
        button_position = ((ad_template.width - button_width) // 2, ad_template.height - button_height - 30)

        # Butonu ovalleştir ve renk ve konumu belirle
        rounded_rectangle(draw_button, button_position, (button_width, button_height), radius=15,
                          fill=button_punchline_color)
        # todo: resmin de kenarları yuvarlatılacak.
        # todo: template'in kenarlarında borderline olacak

        return ad_template



    def Kaydet(self, ad_template):
        """oluşturulan template'i bir üst dizinde templates klasörüne kaydeder."""
        # Bulunulan dizinin bir üst dizini
        parent_directory = os.path.dirname(os.getcwd())

        # "templates" klasörünü oluştur
        templates_folder = os.path.join(parent_directory, "templates")
        os.makedirs(templates_folder, exist_ok=True)

        # Reklam template'ini kaydet
        template_path = uniquify(os.path.join(templates_folder, "ad_template.png"))
        ad_template.save(template_path)

        # Kaydedilen dosyanın yolunu return et. İleride lazım olabilir.
        return template_path


if __name__ == '__main__':
    template = Template()

    # İlgili inputları tanımlayın
    image_path = "../SDV5_OUTPUT/latte in purple cup.png"
    logo_path = "../coffee-logo2.png"
    punchline = "bu kahve masası\nha ri ka"
    button_text = "Sipariş   >"
    button_punchline_color = "#007bff"  # Örnek renk kodu

    processed_image = Image.open(image_path)
    # artık gelen resim yol olarak değil de direkt resim olarak fonksiyona verilecek.

    ad_template = template.create_ad_template(processed_image,
                                              logo_path,
                                              punchline,
                                              button_text,
                                              button_punchline_color)
    template.Kaydet(ad_template)
else:
    print("Task dışarıdan çalıştırıldı.")
    template = Template()
