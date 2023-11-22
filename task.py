from PIL import Image
import os
from PIL import ImageDraw, ImageFont


def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1
    while os.path.exists(path):
        path = filename + " (" + str(counter) + ")" + extension
        counter += 1
    return path


class Template:
    def __init__(self):
        # İlgili inputları tanımlayın
        self.image_path = (
            "C:/Users/ksyus/Documents/Yazılımsal Projeler/adCreative.ai iş başvuru case çalışması/SDV5_OUTPUT/"
            "latte in purple cup.png")
        # todo: mesela image_patch dışarıdan alınacak şekilde güncellenmeli.
        self.logo_path = ("C:/Users/ksyus/Documents/Yazılımsal Projeler/adCreative.ai iş başvuru case "
                          "çalışması/"
                          "coffee-logo.png")
        self.punchline = "Kahve dünyasının bir numarası\nSipariş için dokunun"
        self.button_text = "Sipariş   >"
        self.button_punchline_color = "#007bff"  # Örnek renk kodu
        self.SAVE_PATH = ("C:/Users/ksyus/Documents/Yazılımsal Projeler/adCreative.ai iş başvuru case "
                          "çalışması/templateler/"
                          "kahve")

        # Kaynak resmi açın
        self.generated_image = Image.open(self.image_path)

    def create_ad_template(self):
        # Reklam şablonunu oluşturmak için yeni bir görüntü oluşturun
        ad_template = Image.new("RGB", (800, 800), "white")
    
        # Logo ekleyin
        logo = Image.open(self.logo_path).convert("RGBA").resize((200, 100))
        logo_position = ((ad_template.width - logo.width) // 2, 30)
        ad_template.paste(logo, logo_position, logo)
    
        # Oluşturulan görseli ortaya ekleyin
        self.generated_image = self.generated_image.resize((384, 384))
        image_position = ((ad_template.width - self.generated_image.width) // 2, logo_position[1] + logo.height + 20)
        ad_template.paste(self.generated_image, image_position)
    
        # Punchline'ı ekleyin
        # https://fonts.google.com/specimen/Playfair+Display
        draw = ImageDraw.Draw(ad_template)
        # Fontu seç
        font_path = ('C:/Users/ksyus/Documents/Yazılımsal Projeler/adCreative.ai iş başvuru case '
                     'çalışması/Playfair_Display/PlayfairDisplay-ExtraBold.ttf')
        font_size = 44
        font = ImageFont.truetype(font_path, font_size)
    
        # Metni ortadan \n kaçış dizesine göre böl
        lines = self.punchline.split('\n')
    
        # İlk satırın boyutlarını ölç
        text_width, text_height = draw.textbbox((0, 0), lines[0], font=font)[2:]
    
        # İlk satırı resme ekle
        x1 = (ad_template.width - text_width) / 2
        y1 = image_position[1] + self.generated_image.height + 25 # üstteki resimden 25px aşağı yerleştiriyoruz.
        draw.text((x1, y1), lines[0], fill=self.button_punchline_color, font=font)
    
        # Eğer ikinci satır varsa, onu da resme ekle
        if len(lines) > 1:
            # İkinci satırın boyutlarını ölç
            text_width, text_height = draw.textbbox((0, 0), lines[1], font=font)[2:]
    
            # İkinci satırı resme ekle
            x2 = (ad_template.width - text_width) / 2
            y2 = y1 + text_height + 10  # 10 piksel boşluk bırak
            draw.text((x2, y2), lines[1], fill=self.button_punchline_color, font=font)
    
        # Button'u ekle
        def rounded_rectangle(draw, position, size, radius=25, fill="white", outline=None):
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
            font_button = ImageFont.truetype(font_path, font_size_button)  # İlgili fontu kullanabilirsin
    
            # Yazıyı butonun içine yerleştirin
            text_width_button, text_height_button = draw_button.textbbox((0, 0), self.button_text, font=font_button)[2:]
            x_button = x + (width - text_width_button) // 2  # Butonun ortasına yerleştirmek için
            y_button = y + (height - text_height_button) // 2  # Butonun ortasına yerleştirmek için
            draw_button.text((x_button, y_button), self.button_text, fill="white", font=font_button)
    
        button_width = 200
        button_height = 50
        draw_button = ImageDraw.Draw(ad_template)
    
        # # Butonun konumunu belirleyin ve resme ekleyin
        button_position = ((ad_template.width - button_width) // 2, ad_template.height - button_height - 30)
    
        # Butonu ovalleştir ve renk ve konumu belirle
        rounded_rectangle(draw_button, button_position, (button_width, button_height), radius=15, fill=self.button_punchline_color)
    
        return ad_template

    def Kaydet(self, ad_template):
        # Reklam template'ini kaydedin
        ad_template.save(uniquify(template.SAVE_PATH + "_template.png"))
    

if __name__ == '__main__':
    template = Template()
    ad_template = template.create_ad_template()
    template.Kaydet(ad_template)
else:
    template = Template()

