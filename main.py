import img2img, task


class Sunum:
    def __init__(self):
        self.model = img2img.Img2Img()
        self.template = task.Template()

    def CreateImage(self):
        self.model.generate_image(prompt="latte in red cup",
                             image_path="C:/Users/ksyus/Documents/Yazılımsal Projeler/"
                                        "adCreative.ai iş başvuru case çalışması/"
                                        "coffee-4908764_1280.jpg")

    def CreateTemplate(self):
        ad_template = self.template.create_ad_template()
        self.template.Kaydet(ad_template)
        # todo: kaydediyorsun ama hangi resmi kaydettiğinin farkında değilsin
        # template'e eklenecek resim createImage'den alınmalı. yani ürettiğin resmi kullan.


if __name__ == '__main__':
    sunu = Sunum()
    sunu.CreateImage()
    sunu.CreateTemplate()
    # todo: flask ile ön tarafın isteyeceği şeyleri belirleyeceğiz
    # parametreler belirlendiği zaman fonksiyonları düzenleyeceğiz.
else:
    sunu = Sunum()
    # todo: FLASK.PY oluşturulacak ve imputlar belirlenecek.



