
################################################################################
# Helper and utility functions
# 
# Code and images by Aaron Penne
# https://github.com/aaronpenne/generative_art
#
# Released under the MIT license (https://opensource.org/licenses/MIT)
################################################################################

import os
import logging
import sys
from datetime import datetime
import ConfigParser

from setup_logging import log

class ConfigUtils(object):
    def cast_dict(self, dictionary):
        """
        Tries to convert the values in a dict to int, then float
        """
        for key in dictionary:
            try:
                dictionary[key] = int(dictionary[key])
            except:
                try:
                    dictionary[key] = float(dictionary[key])
                except:
                    pass
        return dictionary

    def config_to_dict(self, config_path, config_section='default'):
        """
        Grabs section from config file and converts it to a dict
        """
        config = ConfigParser.ConfigParser()
        config.read(config_path)
        section_list = config.items(config_section)
        log.info('Args pulled from config file:')
        for pair in section_list:
            log.info('  {}: {}'.format(pair[0], pair[1]))
        section_dict = dict(section_list)
        section_dict = self.cast_dict(section_dict)
        return section_dict


class OpsUtils(object):
    def __init__(self, script_path, seed=1138):
        self.script_path = script_path
        self.script_name = os.path.basename(script_path)
        self.script_dir = os.path.dirname(script_path)
        self.sketch_name = os.path.splitext(self.script_name)[0]
        self.seed = seed
        self.timestamp = self.get_timestamp_string()

    def print_seed(self):
        log.info(self.seed)

    def get_timestamp_string(self):
        timestamp = datetime.now()
        timestamp = timestamp.strftime('%Y%m%d_%H%M%S')
        return timestamp

    def get_filename(self, counter):
        filename = '{}_{}_{}_{:03d}.png'.format(self.sketch_name, self.seed, self.timestamp, counter)
        return filename

    def make_dir(self, path):
        try:
            os.makedirs(path)
        except OSError:
            if not os.path.isdir(path):
                raise

    def save_graphic(self, pg, path, counter):
        self.make_dir(path)
        output_file = self.get_filename(counter)
        output_path = os.path.join(path, output_file)
        pg.save(output_path)
        log.info('Saved to {}'.format(output_path))

        


class DrawUtils(OpsUtils):
    def __init__(self, script_path, width, height, seed=1138):
        super(DrawUtils, self).__init__(script_path, seed)  # Calls init from inherited class to get those variables first
        log.info(self.timestamp)
        self.width = width
        self.height = height

    def draw_test(self, pg, num_circles): 
        for i in range(num_circles):
            pg.fill(random(255),50,50,10)
            pg.ellipse(random(pg.width),random(pg.height),random(pg.width*0.2),random(pg.height*0.2))


    def circle_point(self, cx, cy, rx, ry, a):
        """
        Translates polar coords to cartesian
        """
        x = cx + rx * cos(a)
        y = cy + ry * sin(a)
        return x, y
        
    def noise_loop(self, a, r, min_val, max_val, x_c, y_c):
        """
        Samples 2D Perlin noise in a circle to make smooth noise loops
        Adapted from https://github.com/CodingTrain/website/blob/master/CodingChallenges/CC_136_Polar_Noise_Loop_2/P5/noiseLoop.js
        """
        xoff = map(cos(a), -1, 1, x_c, x_c + 2*r)
        yoff = map(sin(a), -1, 1, y_c, y_c + 2*r)
        r = noise(xoff, yoff)
        return map(r, 0, 1, min_val, max_val)

    def frange(self, start, end=None, increment=None):
        """
        Adapted from http://code.activestate.com/recipes/66472
        """
        if end == None:
            end = start + 0.0
            start = 0.0
        if increment == None:
            increment = 1.0
        L = []
        while 1:
            next = start + len(L) * increment
            if increment > 0 and next >= end:
                break
            elif increment < 0 and next <= end:
                break
            L.append(next)
        return L
