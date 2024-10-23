import requests
import gradio as gr
import colorsys

def season(color1, color2, color3, color4):
    colors = [color1, color2, color3, color4]
    season = {'Spring': 0, 'Summer': 0, 'Autumn': 0, 'Winter': 0, 'Transitional': 0}

    for color in colors:
        col = color[5:-1]
        col = col.split(', ')

        r, g, b, a = col

        h, l, s = colorsys.rgb_to_hls(int(float(r))/255, int(float(g))/255, int(float(b))/255)
        hue_degrees = h * 360

        if hue_degrees < 90 or hue_degrees > 270:
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
    
    return most_common_seasons[0]


def generate_palette(color1, color2, color3, color4):
    base_url = "https://www.thecolorapi.com/scheme"
    
    init_palette = []
    fin_palette = []
    
    colors = [color1, color2, color3, color4]
    print(colors)
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

    
    # for color in colors:
    #     params1 = {
    #         "rgb": color, 
    #         "mode": "triad",        #color scheme mode - analogic, monochrome, triad, etc.
    #         "count": 3                 
    #     }
    #     params2 = {
    #         "rgb": color, 
    #         "mode": "monochrome-light",        #color scheme mode - analogic, monochrome, triad, etc.
    #         "count": 1                 
    #     }
    #     params3 = {
    #         "rgb": color, 
    #         "mode": "quad",        #color scheme mode - analogic, monochrome, triad, etc.
    #         "count": 6                 
    #     }
    #     params4 = {
    #         "rgb": color, 
    #         "mode": "monochrome-dark",        #color scheme mode - analogic, monochrome, triad, etc.
    #         "count": 1                 
    #     }


    #     response = requests.get(base_url, params=params1)
    #     data = response.json()
    #     palette_result += [color_data['rgb']['value'] for color_data in data['colors']]
    #     print(palette_result)

    #     response2 = requests.get(base_url, params=params2)
    #     data2 = response2.json()
    #     palette_result += [color_data['rgb']['value'] for color_data in data2['colors']]

    #     response3 = requests.get(base_url, params=params3)
    #     data3 = response3.json()
    #     palette_result += [color_data['rgb']['value'] for color_data in data3['colors']]

    #     response4 = requests.get(base_url, params=params4)
    #     data4 = response4.json()
    #     palette_result += [color_data['rgb']['value'] for color_data in data4['colors']]

    fin_palette = list(set(fin_palette))
    return fin_palette

def process_rgba(val):
    val = val[5:-1]
    print(val)
    val = val.split(', ')
    r, g, b, a = val
    return f'rgb({int(float(r))},{int(float(g))},{int(float(b))})'


#gradio prep
def gradio_interface(color1, color2, color3, color4):
    palette = generate_palette(color1, color2, color3, color4)
    seasons = season(color1, color2, color3, color4)
    
    output_html = "<h3>Generated Palettes:</h3>"

    output_html += "<div style='display: grid; grid-template-columns: repeat(5, 50px); grid-gap: 5px;'>"
    
    for color in palette:
        # output_html += f"<h4>Base Color: {color}</h4><div style='display:flex;'>"
        output_html += f"<div style='background-color:{color}; width:50px; height:50px;'></div>"
    
    output_html += "</div>"

    output_html += seasons
    
    return output_html


#gradio interface
gradio_app = gr.Interface(
    fn=gradio_interface, 
    inputs=[
        gr.ColorPicker(label="Color 1"), 
        gr.ColorPicker(label="Color 2"), 
        gr.ColorPicker(label="Color 3"), 
        gr.ColorPicker(label="Color 4")
    ], 
    outputs=gr.HTML(label="Generated Color Palettes"),
    title="Color Palette Generator",
    description="input four colors to generate a palette for each using The Color API."
)

gradio_app.launch()
