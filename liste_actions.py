'''Ce module contient les dictionnaires des commandes pouvant être envoyées au capteur et le format des images pouvant être capturées.
À chaque commande est associé la valeur hexadécimale qui doit être envoyée à l'Arduino afin qu'il effectue les modifications ou les actions.'''
dic_actions = {"320x240": b'\x00', "640x480": b'\x01', "1024x768": b'\x02', "1280x960": b'\x03',
               "1600x1200": b'\x04', "2048x1536": b'\x05', "2592x1944": b'\x06', "capture": b'\x10',
               "JPEG": b'\x11', "RAW": b'\x12', "captureRAW": b'\x13', "stream": b'\x20', "streamStop": b'\x21', "captureBMP": b'\x30', "BMP": b'\x31',
               "Advanced_AWB": b'\x40', "Simple_AWB": b'\x41', "Manual_day": b'\x42', "Manual_A": b'\x43', "Manual_cwf": b'\x44', "Manual_cloudy": b'\x45', "AWB_off": b'\x46',
               "Saturation4": b'\x50', "Saturation3": b'\x51', "Saturation2": b'\x52', "Saturation1": b'\x53', "Saturation0": b'\x54',
               "Saturation_1": b'\x55', "Saturation_2": b'\x56', "Saturation_3": b'\x57', "Saturation_4": b'\x58',
               "Brightness4": b'\x60', "Brightness3": b'\x61', "Brightness2": b'\x62', "Brightness1": b'\x63', "Brightness0": b'\x64',
               "Brightness_1": b'\x65', "Brightness_2": b'\x66', "Brightness_3": b'\x67', "Brightness_4": b'\x68',
               "Contrast4": b'\x70', "Contrast3": b'\x71', "Contrast2": b'\x72', "Contrast1": b'\x73', "Contrast0": b'\x74',
               "Contrast_1": b'\x75', "Contrast_2": b'\x76', "Contrast_3": b'\x77', "Contrast_4": b'\x78',
               "degree_180": b'\x80', "degree_150": b'\x81', "degree_120": b'\x82', "degree_90": b'\x83', "degree_60": b'\x84', "degree_30": b'\x85',
               "degree0": b'\x86', "degree30": b'\x87', "degree60": b'\x88', "degree90": b'\x89', "degree120": b'\x8a', "degree150": b'\x8b',
               "No Effect": b'\x90', "BW": b'\x91', "Bluish": b'\x92', "Sepia": b'\x93', "Reddish": b'\x94', "Greenish": b'\x95', "Negative": b'\x96',
               "Exposure_1.7EV": b'\xA0', "Exposure_1.3EV": b'\xA1', "Exposure_1EV": b'\xA2', "Exposure_0.7EV": b'\xA3', "Exposure_0.3EV": b'\xA4',
               "Exposure_default": b'\xA5', "Exposure0.7EV": b'\xA6', "Exposure1EV": b'\xA7', "Exposure1.3EV": b'\xA8', "Exposure1.7EV": b'\xA9',
               "Auto_Sharpness_default": b'\xB0', "Auto_Sharpness_1": b'\xB1', "Auto_Sharpness_2": b'\xB2',
               "Manual_Sharpnessoff": b'\xB3', "Manual_Sharpness1": b'\xB4', "Manual_Sharpness2": b'\xB5', "Manual_Sharpness3": b'\xB6', "Manual_Sharpness4": b'\xB7', "Manual_Sharpness5": b'\xB8',
               "Mirror": b'\xC0', "Flip": b'\xC1', "Mirror_Flip": b'\xC2', "Normal": b'\xC3',
               "High": b'\xD0', "Default": b'\xD1', "Low": b'\xD2',
               "Color_bar": b'\xE0', "Color_square": b'\xE1', "BW_square": b'\xE2', "DLI": b'\xE3'}
dic_formats = {"JPEG": '.jpg', "BMP": '.bmp', "RAW": '.raw'}
