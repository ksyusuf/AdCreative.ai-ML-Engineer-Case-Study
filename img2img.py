from PIL import Image
import os
from diffusers import StableDiffusionImg2ImgPipeline


def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1
    while os.path.exists(path):
        path = filename + " (" + str(counter) + ")" + extension
        counter += 1
    return path


class Img2Img:
    def __init__(self):
        self.model_path = os.getenv("SDV5_MODEL_PATH")
        self.save_path = os.path.join("C:/Users/ksyus/Documents/Yazılımsal Projeler/adCreative.ai iş başvuru case "
                                      "çalışması", "SDV5_OUTPUT")
        if not os.path.exists(self.save_path):
            os.mkdir(self.save_path)
        # modeli oluşturalım
        self.pipe = StableDiffusionImg2ImgPipeline.from_pretrained(self.model_path)
        self.pipe = self.pipe.to('cpu')

    def generate_image(self, prompt, image_path, strength=0.75, guidance_scale=7.5):
        init_image = Image.open(image_path).convert("RGB")
        init_image = init_image.resize((512, 512))

        print("Resim oluşturuluyor...")
        generated_image = self.pipe(prompt=prompt,
                                    image=init_image,
                                    strength=strength,
                                    guidance_scale=guidance_scale).images[0]

        # oluşan resmi benzersiz bir isim ile kaydedelim
        output_path = uniquify(
            os.path.join(self.save_path, (prompt[:25] + "...") if len(prompt) > 25 else prompt) + ".png")
        print(output_path)
        generated_image.save(output_path)
        return generated_image


if __name__ == '__main__':
    image_pipeline = Img2Img()
    image_pipeline.generate_image(prompt="latte in red cup",
                                  image_path="C:/Users/ksyus/Documents/Yazılımsal Projeler/adCreative.ai iş başvuru "
                                             "case çalışması/coffee-4908764_1280.jpg")
else:
    image_pipeline = Img2Img()
