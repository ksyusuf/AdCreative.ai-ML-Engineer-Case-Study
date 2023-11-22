from PIL import Image
import os
from diffusers import StableDiffusionImg2ImgPipeline

SDV5_MODEL_PATH = os.getenv("SDV5_MODEL_PATH")
SAVE_PATH = os.path.join("C:/Users/ksyus/Documents/Yazılımsal Projeler/adCreative.ai iş başvuru case çalışması",
                         "SDV5_OUTPUT")

if not os.path.exists(SAVE_PATH):
    os.mkdir(SAVE_PATH)


def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + " (" + str(counter) + ")" + extension
        counter += 1

    return path


# img2img modelini eğitelim
print("model oluşturuluyor...")
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(SDV5_MODEL_PATH)
pipe = pipe.to('cpu')

prompt = "latte in purple cup"

print(f"Characters in prompt: {len(prompt)}, limit: 200")

# kaynak resmimizi alalım ve yeniden boyutlandıralım.
dosya_yolu = "C:/Users/ksyus/Documents/Yazılımsal Projeler/adCreative.ai iş başvuru case çalışması/coffee-5495609_1280.jpg"
init_image = Image.open(dosya_yolu).convert("RGB")
init_image = init_image.resize((512, 512))

# modelimize promtu verip resmimizi oluşturalım.
print("resim oluşturuluyor...")
# todo: bu parametrelerle oynayarak projeyi geliştireceğiz.
image = pipe(prompt=prompt, image=init_image, strength=0.75, guidance_scale=7.5).images[0]

# çıktıyı benzersiz isimle kaydet.
image_path = uniquify(os.path.join(SAVE_PATH, (prompt[:25] + "...") if len(prompt) > 25 else prompt) + ".png")
print(image_path)

image.save(image_path)

