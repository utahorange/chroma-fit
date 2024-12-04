import requests
import gradio as gr
import colorsys
from colorsys import rgb_to_hsv
import re
import random
import numpy as np

def parse_rgb_string(rgb_string):
    rgb_values = re.findall(r'\d+', rgb_string)
    return tuple(map(int, rgb_values))

def rgb_tuple_to_string(rgb_tuple):
    return f'rgb({rgb_tuple[0]}, {rgb_tuple[1]}, {rgb_tuple[2]})'

def sort_by_hue(rgb_colors_str):
    rgb_colors = [parse_rgb_string(c) for c in rgb_colors_str]
    sorted_colors = sorted(rgb_colors, key=lambda rgb: rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255))
    return [rgb_tuple_to_string(rgb) for rgb in sorted_colors]

def brightness(rgb):
    return 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]

def filter_black_white(rgb_colors_str, black_threshold=20, white_threshold=235):
    rgb_colors = [parse_rgb_string(c) for c in rgb_colors_str]
    
    filtered_colors = [ #anything too close to black or white
        rgb for rgb in rgb_colors
        if black_threshold < brightness(rgb) < white_threshold
    ]
    
    return [rgb_tuple_to_string(rgb) for rgb in filtered_colors]

def is_too_dark(h, s, l, threshold=0.2):
    return l < threshold or l > 0.9

def remove_too_dark(colors, threshold=0.2):
    """
    Removes colors that are too dark based on the lightness in HSL color space.
    
    :param colors: List of RGB colors to check.
    :param threshold: Lightness threshold below which the color is considered too dark.
    :return: List of colors that are not too close to black.
    """
    filtered_colors = []
    
    for color in colors:
        r, g, b = parse_rgb_string(color)
        # Convert RGB to HLS
        h, s, l = colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0)
        h = h * 360  # Convert hue to degrees (0 to 360)
        
        # If the color is not too close to black, keep it
        if not is_too_dark(h, s, l, threshold):
            filtered_colors.append(color)
    
    return filtered_colors



def color_distance(c1, c2):
    """
    Computes the Euclidean distance between two colors in the RGB space.
    The smaller the distance, the more similar the colors are.
    """
    print(c1,c2)
    return np.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2 + (c1[2] - c2[2]) ** 2)


def remove_similar_colors(colors, threshold=30):
    """
    Removes colors that are too similar based on a distance threshold.
    The function returns a list of unique colors that are sufficiently different from each other.
    
    :param colors: List of colors (each color is a tuple of RGB values)
    :param threshold: Minimum distance between colors to consider them different
    """
    unique_colors = [colors[0]] if len(colors) > 0 else []

    for color in colors:
        # Check if the color is too similar to any already in the list
        if all(color_distance(parse_rgb_string(color), parse_rgb_string(other)) > threshold for other in unique_colors):
            unique_colors.append(color)
    
    return unique_colors


def season(colors):
    # colors = [color1, color2, color3]
    colors = list(colors)
    season = {'Spring': 0, 'Summer': 0, 'Autumn': 0, 'Winter': 0, 'Transitional': 0}

    for color in colors:
        r, g, b = parse_rgb_string(color)[0], parse_rgb_string(color)[1], parse_rgb_string(color)[2]

        h, l, s = colorsys.rgb_to_hls(int(float(r))/255, int(float(g))/255, int(float(b))/255)
        hue_degrees = h * 360
        print("hue", "light", hue_degrees, l)

        if hue_degrees < 90:
            temperature = 'Warm'
        else:
            temperature = 'Cold'

        if l > 0.75:
            if temperature == 'Warm':
                season['Spring'] += 1
            else:
                season['Summer'] += 1
        elif l > 0.52:
            if temperature == 'Warm':
                season['Spring'] += 2
            else:
                season['Summer'] += 2
        elif l < 0.25:
            if temperature == 'Warm':
                season['Autumn'] += 1
            else:
                season['Winter'] += 1
        elif l < 0.48:
            if temperature == 'Warm':
                season['Autumn'] += 2
            else:
                season['Winter'] += 2
        else:
            season['Transitional'] += 1

    print(season)

    max_count = max(season.values())
    most_common_seasons = [key for key, value in season.items() if value == max_count]
    
    return most_common_seasons[random.randint(0, len(most_common_seasons)-1)]


def generate_palette(color1, color2, color3):
    base_url = "https://www.thecolorapi.com/scheme"
    
    init_palette = []
    fin_palette = []
    
    colors = [color1, color2, color3]
    colors = [process_rgba(color) for color in colors]

    for color in colors:
        params = {
            "rgb": color, 
            "mode": "quad",        #color scheme mode - analogic, monochrome, triad, etc.
            "count": 4                 
        }
        params2 = {
            "rgb": color, 
            "mode": "triad",        #color scheme mode - analogic, monochrome, triad, etc.
            "count": 3
        }

        response = requests.get(base_url, params=params)
        data = response.json()
        init_palette += [color_data['rgb']['value'] for color_data in data['colors']]
        
        response = requests.get(base_url, params=params2)
        data = response.json()
        init_palette += [color_data['rgb']['value'] for color_data in data['colors']]

    for color in init_palette:
        params = {
            "rgb": color, 
            "mode": "monochrome",        #color scheme mode - analogic, monochrome, triad, etc.
            "count": 2     
        }
        response = requests.get(base_url, params=params)
        data = response.json()
        fin_palette += [color_data['rgb']['value'] for color_data in data['colors']]


    fin_palette = list(set(fin_palette))
    fin_palette = filter_black_white(fin_palette)
    fin_palette = remove_too_dark(fin_palette)
    fin_palette = remove_similar_colors(fin_palette, threshold=50)
    fin_palette = sort_by_hue(fin_palette)

    return fin_palette

def process_rgba(val):
    r, g, b = val[0], val[1], val[2]
    return f'rgb({int(float(r))},{int(float(g))},{int(float(b))})'


# #gradio prep
def gradio_interface(color1, color2, color3):
    palette = generate_palette(color1, color2, color3)
    seasons = season(palette)
    
    output_html = "<h3>Generated Palettes:</h3>"

    output_html += "<div style='display: grid; grid-template-columns: repeat(5, 50px); grid-gap: 5px;'>"
    
    for color in palette:
        # output_html += f"<h4>Base Color: {color}</h4><div style='display:flex;'>"
        output_html += f"<div style='background-color:{color}; width:50px; height:50px;'></div>"
    
    output_html += "</div>"

    output_html += seasons
    
    return output_html


# #gradio interface
# gradio_app = gr.Interface(
#     fn=gradio_interface, 
#     inputs=[
#         gr.ColorPicker(label="Color 1"), 
#         gr.ColorPicker(label="Color 2"), 
#         gr.ColorPicker(label="Color 3"), 
#     ], 
#     outputs=gr.HTML(label="Generated Color Palettes"),
#     title="Color Palette Generator",
#     description="input three colors to generate a palette for each using The Color API."
# )

# gradio_app.launch()
