import gdown

url = "https://drive.google.com/drive/u/0/folders/1f1GxaU8RbP6-AWGfgFYxGjH2u-vGLQEG"
output = "fcn8s_from_caffe.npz"

gdown.download_folder(url, quiet=True, use_cookies=False)


print('Folder downloaded successfully.')


############################################################################################################