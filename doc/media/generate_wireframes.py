from PIL import Image, ImageDraw, ImageFont
import os

out_dir = os.path.dirname(__file__)

font = ImageFont.load_default()

# Dashboard mock
w, h = 1000, 600
img = Image.new("RGB", (w, h), "white")
d = ImageDraw.Draw(img)

# Header
d.rectangle([(0,0),(w,70)], fill=(30,30,30))
d.text((20,20), "Gaia — Project Dashboard (mock)", fill="white", font=font)

# Status columns
cols = ["To Do", "In Progress", "Done"]
col_w = (w-80)//3
for i, col in enumerate(cols):
    x = 20 + i*(col_w+20)
    d.rectangle([(x,100),(x+col_w,520)], outline=(0,0,0), width=2)
    d.text((x+10,110), col, fill=(0,0,0), font=font)
    # sample cards
    for j in range(4):
        card_y = 140 + j*80
        d.rectangle([(x+10, card_y),(x+col_w-10, card_y+60)], outline=(120,120,120), width=1)
        d.text((x+20, card_y+10), f"ISSUE-{i+1}{j+1}: Example task title", fill=(0,0,0), font=font)

img.save(os.path.join(out_dir, "dashboard-mock.png"), "PNG")

# Telegram flow mock
w2, h2 = 1000, 300
img2 = Image.new("RGB", (w2, h2), "white")
d2 = ImageDraw.Draw(img2)

# Boxes
d2.rectangle([(50,70),(250,200)], outline=(0,0,0), width=2)
d2.text((70,90), "Telegram Bot", fill=(0,0,0), font=font)

d2.rectangle([(380,40),(620,120)], outline=(0,0,0), width=2)
d2.text((400,60), "Orchestrator", fill=(0,0,0), font=font)

d2.rectangle([(750,70),(950,200)], outline=(0,0,0), width=2)
d2.text((770,90), "Issue Tracker", fill=(0,0,0), font=font)

# Arrows / labels
d2.line([(250,130),(380,80)], fill=(0,0,0), width=2)
d2.text((300,100), "creates ->", fill=(0,0,0), font=font)

d2.line([(620,80),(750,130)], fill=(0,0,0), width=2)
d2.text((660,100), "calls CLI/API ->", fill=(0,0,0), font=font)

img2.save(os.path.join(out_dir, "telegram-flow.png"), "PNG")

print("Wireframes written:")
print(os.path.join(out_dir, "dashboard-mock.png"))
print(os.path.join(out_dir, "telegram-flow.png"))
