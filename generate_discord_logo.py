from PIL import Image, ImageDraw
import math

# 512x512 für die Discord Rich Presence Assets
size = 512
img = Image.new("RGBA", (size, size), "#0B1011") 
draw = ImageDraw.Draw(img)

center_x, center_y = size // 2, size // 2
radius = 160
node_radius = 24
color = "#B7F36B" 

for i in range(6):
    angle = math.radians(i * 60)
    end_x = center_x + radius * math.cos(angle)
    end_y = center_y + radius * math.sin(angle)
    draw.line((center_x, center_y, end_x, end_y), fill=color, width=8)

for i in range(6):
    angle = math.radians(i * 60)
    end_x = center_x + radius * math.cos(angle)
    end_y = center_y + radius * math.sin(angle)
    draw.ellipse((end_x - node_radius, end_y - node_radius, end_x + node_radius, end_y + node_radius), fill=color)

center_radius = 36
draw.ellipse((center_x - center_radius, center_y - center_radius, center_x + center_radius, center_y + center_radius), fill=color)

img.save("assets/evox_discord_logo.png")
print("Quadratisches Logo (512x512) generiert!")