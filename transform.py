from PIL import Image
import torch
import torchvision.transforms as transforms
import io

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

def tensor_to_image(tensor):
  tensor = transforms.ToPILImage()(tensor)
  image_buffer = io.BytesIO()
  tensor.save(image_buffer, format='JPEG')
  image_buffer.seek(0)
  return image_buffer