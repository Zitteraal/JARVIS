from PIL import Image, ImageDraw
import math

# 256x256 Master-Größe
size = 256
img = Image.new("RGBA", (size, size), "#0B1011") # Deep Graphite Hintergrund
draw = ImageDraw.Draw(img)

center_x, center_y = size // 2, size // 2
radius = 80
node_radius = 12
color = "#B7F36B" # Signal Lime

# Zeichne die Verbindungslinien (Netzwerk)
for i in range(6):
    angle = math.radians(i * 60)
    end_x = center_x + radius * math.cos(angle)
    end_y = center_y + radius * math.sin(angle)
    draw.line((center_x, center_y, end_x, end_y), fill=color, width=4)

# Zeichne die äußeren Knoten
for i in range(6):
    angle = math.radians(i * 60)
    end_x = center_x + radius * math.cos(angle)
    end_y = center_y + radius * math.sin(angle)
    draw.ellipse((end_x - node_radius, end_y - node_radius, end_x + node_radius, end_y + node_radius), fill=color)

# Zeichne den zentralen Knoten (etwas größer)
center_radius = 18
draw.ellipse((center_x - center_radius, center_y - center_radius, center_x + center_radius, center_y + center_radius), fill=color)

# Speichere als PNG und ICO
img.save("assets/evox_app_icon.png")
# Erstelle eine echte Multi-Size-ICO für Windows
img.save("assets/evox_app_icon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])

print("EVOX Icons erfolgreich generiert in 'assets/'")