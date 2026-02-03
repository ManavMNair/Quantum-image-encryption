
import numpy as np
def dna_decode(DXi0, DXi1, DXi2, DXi3):
    h,w = DXi0.shape
    img = np.zeros((h,w),dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            binary_pixel = (
                bin(DXi0[i,j])[2:].zfill(2)+
                bin(DXi1[i,j])[2:].zfill(2)+
                bin(DXi2[i,j])[2:].zfill(2)+
                bin(DXi3[i,j])[2:].zfill(2)
            )
            img[i,j]=int(binary_pixel,2)
    return img

# CMedi = dna_decode(DXi0,DXi1,DXi2,DXi3)
def pixel_to_dna_planes(img):
    h, w = img.shape
    DXi0 = np.zeros((h, w), dtype=np.uint8)
    DXi1 = np.zeros((h, w), dtype=np.uint8)
    DXi2 = np.zeros((h, w), dtype=np.uint8)
    DXi3 = np.zeros((h, w), dtype=np.uint8)

    for i in range(h):
        for j in range(w):
            binary_pixel = bin(img[i, j])[2:].zfill(8)

            DXi0[i, j] = int(binary_pixel[0:2], 2)
            DXi1[i, j] = int(binary_pixel[2:4], 2)
            DXi2[i, j] = int(binary_pixel[4:6], 2)
            DXi3[i, j] = int(binary_pixel[6:8], 2)

    return DXi0, DXi1, DXi2, DXi3


def dna_reverse_substitution(DNi0, DNi1, DNi2, DNi3, ksk):
    h, w = DNi0.shape

    for i in range(h):
        for j in range(w):
            for k in range(4):
                key = int(ksk[k % len(ksk)]) % 4

                if k == 0:
                    (DNi0[i, j].astype(np.int16) - key) % 4
                elif k == 1:
                    (DNi1[i, j].astype(np.int16) - key) % 4
                elif k == 2:
                    (DNi2[i, j].astype(np.int16) - key) % 4
                elif k == 3:
                    (DNi3[i, j].astype(np.int16) - key) % 4

    return DNi0, DNi1, DNi2, DNi3


def dna_decrypt(CMedi, DKi0, DKi1, DKi2, DKi3, ksk):

    DXi0, DXi1, DXi2, DXi3 = pixel_to_dna_planes(CMedi)

    # reverse XOR diffusion
    DNi0 = np.bitwise_xor(DXi0, DKi0)
    DNi1 = np.bitwise_xor(DXi1, DKi1)
    DNi2 = np.bitwise_xor(DXi2, DKi2)
    DNi3 = np.bitwise_xor(DXi3, DKi3)

    # reverse DNA substitution
    DNi0, DNi1, DNi2, DNi3 = dna_reverse_substitution(DNi0, DNi1, DNi2, DNi3, ksk)

    # decode to scrambled image
    scrambled_img = dna_decode(DNi0, DNi1, DNi2, DNi3)

    return scrambled_img