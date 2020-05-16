from __future__ import division
from __future__ import print_function
import os, time, scipy.io, shutil
import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import glob
import re
import cv2
from PIL import Image

from CBDNetUtils import hwc_to_chw, chw_to_hwc
from CBDNetModel import CBDNet

#typeChoice = ['all', 'real', 'synthetic']

def processUsingCBD(imagePath, typeChoice):

    checkpoint_dir = './checkpoint/' + typeChoice + '/'

    model_info = torch.load(checkpoint_dir + 'checkpoint.pth.tar', map_location='cpu')
    print('==> loading existing model:', checkpoint_dir + 'checkpoint.pth.tar')
    model = CBDNet()

    model.load_state_dict(model_info['state_dict'])
    model.eval()

    with torch.no_grad():
        original_noisy_img = cv2.imread(imagePath)
        if original_noisy_img.shape[0] > 512 or original_noisy_img.shape[1] > 512:
            scale_percent = 512 / max(original_noisy_img.shape[1], original_noisy_img.shape[0])
            width = int(original_noisy_img.shape[1] * scale_percent)
            height = int(original_noisy_img.shape[0] * scale_percent)
            dim = (width, height)
            noisy_img = cv2.resize(original_noisy_img, dim)
            print("DOWNSCALED FROM ", original_noisy_img.shape, " TO ", noisy_img.shape, ' with scale factor of ', scale_percent)
        noisy_img = noisy_img[:,:,::-1] / 255.0
        noisy_img = np.array(noisy_img).astype('float32')

        temp_noisy_img_chw = hwc_to_chw(noisy_img)
        print('here')
        input_var = torch.from_numpy(temp_noisy_img_chw.copy()).type(torch.FloatTensor).unsqueeze(0)
        _, output = model(input_var)

        output_np = output.squeeze().cpu().detach().numpy()
        output_np = chw_to_hwc(np.clip(output_np, 0, 1))
        #output_np = np.resize(output_np, (noisy_img[0],noisy_img[1]))
        #concated = np.concatenate((temp_noisy_img, output_np), axis=1) * 255
        denoised = (output_np*255).astype(np.uint8)
        denoised = Image.fromarray(denoised)
        
    return denoised