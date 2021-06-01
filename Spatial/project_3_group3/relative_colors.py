import numpy as np
from PIL import Image
import os
from multiprocessing import Pool
""" 
A script that transforms regular rgb images to relative rgb images.
"""

def transform2relative(dir):
    for image in os.listdir(dir):
        im = Image.open(f"{dir}/{image}")
        if image.split(".")[-1] == "jpg":
            im = im.transpose(method=Image.ROTATE_270)
        mat = np.asarray(im)
        rel_mat = transform_image(mat)
        outdir = f"./model2_easy_xtra_rel/{dir.split('/')[-1]}/{image}"
        Image.fromarray(rel_mat).save(outdir)
        print(outdir)


def transform_image(mat):
    height, width = mat.shape[:2]
    rel_mat = np.zeros_like(mat)
    for m in range(height):
        for n in range(width):
            rel_mat[m,n,:] = relative_color(mat[m,n,:].astype(float))
    return rel_mat

            
def relative_color(rbg):
    sum = np.sum(rbg)
    if sum > 0:
        rel = 255 * (rbg / np.sum(rbg))
        return rel.astype(int)
    else:
        return np.zeros_like(rbg)

    
def main():
    workers = 4
    directory = "./model2_easy_xtra"
    directories = [f"{directory}/{dir}" for dir in os.listdir(directory)]
    with Pool(processes = workers) as pool:
        pool.map(transform2relative, 
            [dir for dir in directories])


if __name__=="__main__":
    main()


    
        


