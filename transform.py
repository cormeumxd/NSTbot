from PIL import Image
import torch
import torchvision.transforms as transforms

def image_load_transform(path, IMG_SIZE):
  img = Image.open(path)
  loader = transforms.Compose([
      transforms.Resize(IMG_SIZE),
      transforms.CenterCrop(IMG_SIZE),
      transforms.ToTensor(),
      #transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
  ])
  img = loader(img).unsqueeze(0)
  return img.requires_grad_(False)