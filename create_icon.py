#!/usr/bin/env python3
"""
Create Windows ICO file for VisoLingua
"""

from PIL import Image, ImageDraw
import os

def create_app_icon():
    """Create a simple VisoLingua icon in ICO format"""
    
    # Icon sizes for Windows ICO
    sizes = [16, 32, 48, 64, 128, 256]
    images = []
    
    for size in sizes:
        # Create image with transparent background
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Colors
        bg_color = (230, 50, 50, 255)      # Red background
        text_color = (255, 255, 255, 255)  # White text
        border_color = (180, 30, 30, 255)  # Darker red border
        
        # Calculate sizes based on icon size
        border_width = max(1, size // 32)
        corner_radius = size // 8
        
        # Draw background with rounded rectangle effect
        draw.rectangle([border_width, border_width, size-border_width, size-border_width], 
                      fill=bg_color, outline=border_color, width=border_width)
        
        # Add "VL" text for VisoLingua
        if size >= 16:
            font_size = size // 3
            try:
                # Try to use a better font if available
                from PIL import ImageFont
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                # Fallback to default font
                font = None
            
            text = "VL"
            if size >= 48:
                text = "VL"
            
            # Get text size
            if font:
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
            else:
                text_width = len(text) * (font_size // 2)
                text_height = font_size
            
            # Center text
            x = (size - text_width) // 2
            y = (size - text_height) // 2
            
            draw.text((x, y), text, fill=text_color, font=font)
        
        # Add small translation symbol for larger icons
        if size >= 64:
            # Draw small arrow or translation symbol
            arrow_size = size // 8
            arrow_x = size - arrow_size * 2
            arrow_y = size - arrow_size * 2
            
            # Simple arrow: →
            draw.polygon([
                (arrow_x, arrow_y + arrow_size//2),
                (arrow_x + arrow_size//2, arrow_y),
                (arrow_x + arrow_size//2, arrow_y + arrow_size//4),
                (arrow_x + arrow_size, arrow_y + arrow_size//4),
                (arrow_x + arrow_size, arrow_y + arrow_size*3//4),
                (arrow_x + arrow_size//2, arrow_y + arrow_size*3//4),
                (arrow_x + arrow_size//2, arrow_y + arrow_size)
            ], fill=(255, 255, 255, 200))
        
        images.append(img)
        print(f"Created {size}x{size} icon")
    
    # Save as ICO file
    ico_path = "assets/icons/app.ico"
    os.makedirs(os.path.dirname(ico_path), exist_ok=True)
    
    # Save ICO with all sizes
    images[0].save(ico_path, format='ICO', sizes=[(img.width, img.height) for img in images])
    
    print(f"✓ ICO file created: {ico_path}")
    print(f"📏 Sizes included: {[f'{img.width}x{img.height}' for img in images]}")
    
    # Also create a PNG version for preview
    png_path = "assets/icons/app.png"
    images[-1].save(png_path, format='PNG')
    print(f"✓ PNG preview created: {png_path}")
    
    return ico_path

def test_icon():
    """Test if the created icon is valid"""
    ico_path = "assets/icons/app.ico"
    
    try:
        # Try to open the ICO file
        with Image.open(ico_path) as img:
            print(f"✓ ICO file is valid")
            print(f"   Format: {img.format}")
            print(f"   Size: {img.size}")
            print(f"   Mode: {img.mode}")
            
        return True
    except Exception as e:
        print(f"X ICO file test failed: {e}")
        return False

if __name__ == "__main__":
    print("Creating VisoLingua Windows Icon...")
    print("=" * 50)
    
    try:
        ico_path = create_app_icon()
        
        if test_icon():
            print("\n🎉 Icon creation successful!")
            print(f"You can now use: {ico_path}")
            print("\nTo rebuild the exe with the new icon:")
            print("  python build_exe.py")
        else:
            print("\nX Icon creation failed!")
            
    except Exception as e:
        print(f"X Error creating icon: {e}")
        print("\nAlternative: Create ICO file manually:")
        print("1. Create PNG images (16x16, 32x32, 48x48, 256x256)")
        print("2. Convert to ICO online: https://convertio.co/png-ico/")
        print("3. Save as assets/icons/app.ico")