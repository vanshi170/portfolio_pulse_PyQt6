import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

def create_gradient_background(size):
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    center_x, center_y = size[0] // 2, size[1] // 2
    max_radius = int(math.sqrt(center_x**2 + center_y**2))
    
    for r in range(max_radius, 0, -1):
        # Interpolate between blue (#3b82f6) and cyan (#06b6d4)
        progress = r / max_radius
        red = int(59 * progress + 6 * (1 - progress))
        green = int(130 * progress + 182 * (1 - progress))
        blue = int(246 * progress + 212 * (1 - progress))
        alpha = int(255 * (1 - progress**2)) # Fade out towards edge
        
        draw.ellipse(
            [center_x - r, center_y - r, center_x + r, center_y + r],
            fill=(red, green, blue, alpha)
        )
    return img

def draw_candlestick(draw, x, y, width, height, is_up=True):
    x, y, width, height = int(x), int(y), int(width), int(height)
    color = (34, 197, 94, 255) if is_up else (239, 68, 68, 255) # Green vs Red
    
    # Draw wick
    wick_x = x + width // 2
    draw.line([(wick_x, y), (wick_x, y + height)], fill=color, width=max(1, width//4))
    
    # Draw body
    body_height = height // 2
    body_y = y + (height // 4) if is_up else y + (height // 4)
    draw.rectangle([x, body_y, x + width, body_y + body_height], fill=color)

def generate_logo(size, filename):
    img = create_gradient_background(size)
    draw = ImageDraw.Draw(img)
    
    w, h = size
    
    # Draw candlesticks
    draw_candlestick(draw, w*0.3, h*0.4, w*0.1, h*0.4, is_up=True)
    draw_candlestick(draw, w*0.5, h*0.2, w*0.1, h*0.5, is_up=False)
    draw_candlestick(draw, w*0.7, h*0.3, w*0.1, h*0.6, is_up=True)
    
    # Draw trend line
    points = [
        (int(w*0.2), int(h*0.8)),
        (int(w*0.35), int(h*0.6)),
        (int(w*0.55), int(h*0.7)),
        (int(w*0.75), int(h*0.4)),
        (int(w*0.9), int(h*0.2))
    ]
    draw.line(points, fill=(255, 255, 255, 255), width=max(2, int(w*0.03)), joint="curve")
    
    # Draw points on trend line
    for px, py in points:
        r = int(w*0.03)
        draw.ellipse([px-r, py-r, px+r, py+r], fill=(255, 255, 255, 255))
        
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    img.save(filename)
    print(f"Generated {filename}")
    return img

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    generated_dir = os.path.join(base_dir, "generated")
    os.makedirs(generated_dir, exist_ok=True)
    
    # App icon (needs 256x256)
    ico_img = generate_logo((256, 256), os.path.join(generated_dir, "app_icon.png"))
    ico_img.save(os.path.join(generated_dir, "app_icon.ico"), format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (32, 32)])
    print(f"Generated {os.path.join(generated_dir, 'app_icon.ico')}")
    
    # Splash Logo (bigger, maybe 800x800)
    generate_logo((800, 800), os.path.join(generated_dir, "splash_logo.png"))
    
    # Standard Logo
    generate_logo((512, 512), os.path.join(generated_dir, "logo.png"))

if __name__ == "__main__":
    main()
