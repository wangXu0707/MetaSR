from model import common
import math
import torch.nn as nn
import torch

class Pos2Weight(nn.Module):
    def __init__(self, Cin, kernel_size=3, Cout=3):
        super(Pos2Weight, self).__init__()
        self.Cin = Cin
        self.kernel_size = kernel_size
        self.Cout = Cout
        self.meta_block = nn.Sequential(
            nn.Linear(3, 256),
            nn.ReLU(inplace=True)
        )

    def forward(self, x):
        output = self.meta_block(x)
        return output


def projection_metric(x, inH, inW, scale):
    '''
    :param x: the projection feature map
    :param inH: H of the Input LR image
    :param inW: W of the Input LR image
    :param scale: scale factor for up-sampling
    :return: metric of offset vector and projection pixel coordinate (i,j) of HR image in LR image

    ----
    projection_coord_metrix --- Dimension: outH x outW x 2.
    for pixel (i,j) in HR image ,the projection coordinate is
    x_coordinate = projection_coord_metrix [i,j,:0]
    y_coordinate = projection_coord_metrix [i,j,:1]
    ---

    ---
    offset_vector --- Dimension: (outH x outW) x3
    
    '''
    outH = int(scale * inH)
    outW = int(scale * inW)
    scale_int = int(math.ceil(scale))
    # 大于scale的最小整数

    # projection_pixel_coordinate
    h_p_coord = torch.arange(0, outH, 1).float().mul(1.0 / scale)
    h_p_coord = torch.floor(h_p_coord).int().unsqueeze(1)
    h_p_coord_metrix = h_p_coord.expand(outH, outW).unsqueeze(0).view(outH, outW, -1)

    w_p_coord = torch.arange(0, outW, 1).float().mul(1.0 / scale)
    w_p_coord = torch.floor(w_p_coord).int().unsqueeze(0)
    w_p_coord_metrix = w_p_coord.expand(outH, outW).unsqueeze(0).view(outH, outW, -1)

    projection_coord_metrix = torch.cat([h_p_coord_metrix, w_p_coord_metrix], dim=-1)

    # offset_vector


    return projection_coord_metrix


if __name__ == '__main__':
    projection_metric(x=0, inH=10, inW=5, scale=1.2)
