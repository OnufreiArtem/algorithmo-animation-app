from PIL import Image, ImageDraw

import cv2

from . separator import Separator
from . sorting import Sorting, BubbleSemiSort
from . exceptions import UnknownAlgorithmException

def build_frame(divider:Separator):
    buffer_image = Image.new('RGBA', ( divider.image_width, divider.image_height ), (0, 0, 0, 0))
    #print(divider.row_arrays)
    for sector_y in range(len(divider.row_arrays)):
        for sector_x in range(divider.columns):
            #print( "column {0} row {1} ".format(divider.row_arrays[sector_y][sector_x], sector_y) )
            sector = divider.get_sector(sector_y,divider.row_arrays[sector_y][sector_x])
            #print(sector)
            buffer_image.paste(sector['region'], (sector_x*divider.sector_width, sector_y*divider.sector_width, (sector_x+1)*divider.sector_width, (sector_y+1)*divider.sector_width))

    return buffer_image

def build_animation(image_path:str, settings:dict, video_name:str, extention:str):
    import time

    start_time = time.time()
    sep = Separator(image_path, settings)

    out = cv2.VideoWriter(video_name + '.' + extention, cv2.VideoWriter_fourcc(*'DIVX'), 15, (sep.image_width, sep.image_height))

    algorithm = None
    if settings['algorithm'] == "Bubble":
        algorithm = BubbleSemiSort()
    else:
        raise UnknownAlgorithmException("Unknown or undefined type of algorithm was specified") 
    
    steps = []
    
    for row in sep.row_arrays:
        steps.append(algorithm.get_all_iterations(row))


    import os

    i = 0
    for phase in range(len(steps[0])):
        for row in range(len(sep.row_arrays)):
            sep.row_arrays[row] = steps[row][phase]
        frame = build_frame(sep)
        filepath = 'frames/frame_{0}.png'.format(i)
        frame.save(filepath, "PNG")
        out.write( cv2.imread(filepath) )
        os.remove(filepath)
        i+=1

    out.release()

    print('It took ' + str(time.time() - start_time))
