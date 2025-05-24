import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import random
import io
import base64

st.set_page_config(page_title="Birthday Cake", layout="centered")
st.title("🎂 Happy Birthday Animation!")

name = st.text_input("Enter the birthday person's name:", "")

def add_audio(file_path):
    with open(file_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
        st.markdown(f"""
        <audio autoplay loop>
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """, unsafe_allow_html=True)

def generate_frame(name, frame_num):
    width, height = 600, 400
    img = Image.new("RGB", (width, height), (10, 10, 30))
    draw = ImageDraw.Draw(img)

    cake_top = height // 2
    draw.rectangle([(200, cake_top), (400, cake_top + 100)], fill=(255, 192, 203))
    draw.rectangle([(220, cake_top - 30), (380, cake_top)], fill=(255, 165, 0))

    for i in range(5):
        x = 240 + i * 30
        draw.rectangle([(x, cake_top - 50), (x + 10, cake_top - 30)], fill=(255, 255, 255))
        flame_color = (255, random.randint(100, 255), 0)
        draw.ellipse([(x - 2, cake_top - 60), (x + 12, cake_top - 45)], fill=flame_color)

    for _ in range(25):
        star_x = random.randint(0, width)
        star_y = random.randint(0, cake_top - 60)
        star_color = (255, 255, random.randint(150, 255))
        draw.ellipse([(star_x, star_y), (star_x + 3, star_y + 3)], fill=star_color)

    if name:
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        draw.text((width // 2 - 100, cake_top + 120), f"Happy Birthday, {name}!", font=font, fill=(255, 255, 0))
        draw.text((width // 2 - 120, cake_top + 150), "🎉 Wishing you joy and laughter! 🎉", font=font, fill=(255, 255, 255))

    return img

def generate_gif(name):
    frames = []
    for i in range(15):  # 15 frames
        frame = generate_frame(name, i)
        frames.append(frame)

    gif_io = io.BytesIO()
    frames[0].save(gif_io, format='GIF', save_all=True, append_images=frames[1:], duration=150, loop=0)
    gif_io.seek(0)
    return gif_io

if name:
    gif = generate_gif(name)
    add_audio("happy_birthday.mp3")
    st.image(gif, caption="🎂 Ameen's Birthday Cake!", use_container_width=True)


    st.download_button("🎁 Download Birthday Card", gif, file_name=f"{name}_birthday.gif", mime="image/gif")
else:
    st.info("Enter a name to generate a birthday animation.")
