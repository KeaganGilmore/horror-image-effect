from PIL import Image, ImageEnhance, ImageOps, ImageDraw
import random

def create_horror_effect(image_path, output_path):
    # Load the image
    img = Image.open(image_path)

    # Extend to landscape if square
    width, height = img.size
    if width == height:
        new_width = int(height * 1.5)  # Extend to landscape
        new_img = Image.new("RGB", (new_width, height), "white")
        offset = (new_width - width) // 2
        new_img.paste(img, (offset, 0))
        img = new_img

    # Convert to grayscale with subtle color tones
    img = img.convert("L").convert("RGB")
    enhancer = ImageEnhance.Color(img)
    color_tone_factor = random.uniform(0.1, 0.3)  # Subtle color highlights
    img = enhancer.enhance(color_tone_factor)

    # Apply random brightness and contrast adjustments
    brightness_enhancer = ImageEnhance.Brightness(img)
    contrast_enhancer = ImageEnhance.Contrast(img)
    img = brightness_enhancer.enhance(random.uniform(0.4, 0.7))
    img = contrast_enhancer.enhance(random.uniform(0.6, 1.0))

    # Add a vignette effect
    vignette = Image.new("L", img.size, 0)
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            distance_to_center = ((x - img.size[0] / 2) ** 2 + (y - img.size[1] / 2) ** 2) ** 0.5
            vignette.putpixel((x, y), int(255 - (distance_to_center / max(img.size) * 255)))
    vignette = vignette.resize(img.size)
    img = Image.composite(img, ImageOps.colorize(vignette, "black", "black"), vignette)

    # Add distortion effect
    pixels = img.load()
    for i in range(0, img.size[0], random.randint(10, 20)):
        if random.random() < 0.3:
            box = (i, 0, i + random.randint(5, 15), img.size[1])
            slice = img.crop(box)
            img.paste(slice, (i + random.randint(-10, 10), 0))

    # Add squiggles to simulate melting effect
    draw = ImageDraw.Draw(img)
    for _ in range(random.randint(10, 20)):
        start_x = random.randint(0, img.size[0])
        start_y = random.randint(0, img.size[1] // 2)
        end_x = start_x + random.randint(-50, 50)
        end_y = start_y + random.randint(50, 150)
        draw.line([(start_x, start_y), (end_x, end_y)], fill="black", width=random.randint(1, 3))

    # Save the output
    img.save(output_path)

# Test the function with test.png
create_horror_effect("test.png", "horror_test_output.png")

print("Horror effect applied and saved as horror_test_output.png!")
