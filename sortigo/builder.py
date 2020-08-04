from PIL import Image, ImageDraw

import cv2

from . separator import Separator
from . sorting import Sorting, BubbleSemiSort

def build_frame(divider:Separator):
    buffer_image = Image.new('RGBA', ( divider.image_width, divider.image_height ), (0, 0, 0, 0))
    draw = ImageDraw.Draw(buffer_image)
    for x in range(buffer_image.width):
        for y in range(buffer_image.height):
            sector_indexes = divider.detect_sector(x, y)
            sector_indexes['x'] -= 1
            sector_indexes['y'] -= 1
            current_sector = dict(x=divider.row_arrays[sector_indexes['y']][sector_indexes['x']], y=sector_indexes['y'])
            local_coords = divider.get_local_coords(x, y)
            draw.point((x, y), divider.get_selected_pixel(current_sector, local_coords) )
    
    return buffer_image

def build_animation(image_path:str, settings:dict, video_name:str, extention:str):
    sep = Separator(image_path, image_settings)
    
    algorithm = None
    if settings['algorithm'] == "Bubble":
        algorithm = BubbleSemiSort()
    else:
        raise 
    steps = []
    for row in sep.row_arrays:
        algorithm.set_array(row)     
        steps.append( algorithm.get_all_iterations )