from PIL import Image, ImageDraw, ImageFont
import random
import os

# Buat direktori untuk menyimpan gambar jika belum ada
output_dir = 'abc'
os.makedirs(output_dir, exist_ok=True)

# Fungsi untuk menghasilkan gambar acak
def generate_image(filename, width=800, height=600):
    # Buat gambar baru dengan warna latar belakang acak
    image = Image.new('RGB', (width, height), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    draw = ImageDraw.Draw(image)
    
    # Tambahkan teks acak ke gambar
    text = f"Image {filename}"
    font = ImageFont.load_default()
    textbbox = draw.textbbox((0, 0), text, font=font)
    textwidth = textbbox[2] - textbbox[0]
    textheight = textbbox[3] - textbbox[1]
    x = (width - textwidth) / 2
    y = (height - textheight) / 2
    draw.text((x, y), text, font=font, fill=(255, 255, 255))
    
    # Simpan gambar
    image.save(os.path.join(output_dir, filename))

# Hasilkan 100 gambar
for i in range(1, 101):
    filename = f'image_{i:03}.jpg'
    generate_image(filename)

print("100 images have been successfully generated in the 'abc' directory.")
