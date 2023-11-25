# import img2img
import Template
from Uzak_Baglanti import UzakBaglanti


class Sunum:
    def __init__(self):
        # self.model = img2img.Img2Img()
        # uzak bilgisayarda çalıştıracağımız için bunu kullanmayacağız.
        self.template = Template.Template()

    def CreateImage(self, prompt="latte in red cup",
                    image='../AdCreative.ai-ML-Engineer-Case-Study/uploads/coffee-5495609_1280.jpg'):
        # bu noktada uzak bilgisayarla bağlantı kurma işlemini gerçekleştirsin.
        generate_image = (UzakBaglanti(prompt=prompt,
                                       image=image)
                          .postIt())

        # üretilmiş resmi geri döndürür.
        return generate_image

    def CreateTemplate(self, generated_image='../AdCreative.ai-ML-Engineer-Case-Study/uploads/latte in purple cup.png',
                       logo_path="../uploads/coffee-logo.png",
                       punchline="Kahve dünyasının bir numarası/nSipariş için dokunun",
                       button_text="Sipariş   >",
                       button_punchline_color="#007bff"):
        ad_template = self.template.create_ad_template(generated_image,
                                                       logo_path,
                                                       punchline,
                                                       button_text,
                                                       button_punchline_color)
        return_patch = self.template.Kaydet(ad_template=ad_template)
        return ad_template


if __name__ == '__main__':
    sunu = Sunum()
    sunu.CreateImage()
    sunu.CreateTemplate()
else:
    sunu = Sunum()
