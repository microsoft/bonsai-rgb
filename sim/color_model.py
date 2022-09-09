import numpy as np

class ColorModel:
    def __init__(self, config):
        # config = {'C':0, 'M':0, 'Y':0, 'K':0, 'R': 0, 'G': 0, 'B': 0}
        self.target_CMYK = np.array([config['C'],
                                     config['M'], 
                                     config['Y'],
                                     config['K']])
        self.RGB = np.array([config['R'], config['G'], config['B']])

    def color_step(self, action):
        """
        Actions are d_Red, d_Green, d_Blue
        """
        RGB_deltas = np.array([action['delta_red'],action['delta_green'], action['delta_blue']])
        self.RGB += RGB_deltas
        self.RGB = np.rint(self.RGB).astype(int)
        self.RGB = np.clip(self.RGB, 0, 255)

    def rgb_to_cmyk(self, rgb):
        """
        Simplified version of RGB to CMYK conversion, assumes RGB and CMYK scales to be 255 and 100
        """
        if np.array_equal(rgb, [0, 0, 0]):
            return np.array([0, 0, 0, 100])
        cmy = 1 - rgb / 255
        k = cmy.min()
        cmy = (cmy - k) / (1 - k)
        cmyk = np.append(cmy, k)
        cmyk *= 100
        cmyk = np.rint(cmyk).astype(int)
        return cmyk

    def cmyk_deltas(self, cmyk1, cmyk2):
        """
        Extremely simple deltas between CMYK values: MAE and absolute diffs
        """
        deltas = cmyk1-cmyk2
        #deltas = np.append(np.absolute(cmyk1-cmyk2).mean(), deltas)
        return deltas

    def delta_error(self, deltas):
        # doesn't work
        predicted_cmyk = self.rgb_to_cmyk(self.RGB)
        deltas = self.cmyk_deltas(self.target_CMYK, predicted_cmyk)
        return deltas.mean().item()

    @property
    def state(self):
        predicted_cmyk = self.rgb_to_cmyk(self.RGB)
        deltas = self.cmyk_deltas(self.target_CMYK, predicted_cmyk)
        return {
            'sim_halted': 0,
            'target_C': self.target_CMYK[0].item(),     # TODO: why item()? 
            'target_M': self.target_CMYK[1].item(),
            'target_Y': self.target_CMYK[2].item(),
            'target_K': self.target_CMYK[3].item(),
            'Mean_Absolute_Error': deltas.mean().item(),
            'delta1': deltas[0].item(),
            'delta2': deltas[1].item(),
            'delta3': deltas[2].item(),
            'delta4': deltas[3].item(),
            'current_red': self.RGB[0].item(),
            'current_green': self.RGB[1].item(),
            'current_blue': self.RGB[2].item(),
        }


