import torch
import torchvision.transforms as transforms
from PIL import Image
import torch.nn as nn
import torchvision.models as models
import torch.optim as optim
from torchvision.utils import save_image
from transform import image_load_transform

import numpy as np


class NeuralStyleTransform():
  def __init__(self, content_image, style_image):
    self.cnn = models.vgg19(pretrained=True).to(device).eval().features[:35].requires_grad_(False)
    self.content_layers = {19}
    self.style_layers = {0, 5, 10, 19, 28, 34}
    self.content_image = content_image
    self.style_image = style_image


  def content_loss(self, input_img, content_img):
    return torch.mean((input_img - content_img)**2)

  def gram_matrix(self, tensor):
    batch_size, channel, h, w = tensor.shape
    features = tensor.view(channel, h*w)
    G = torch.mm(features, features.t())
    return G

  def style_loss(self, input_img, style_img):
    G_input = self.gram_matrix(input_img)
    G_style = self.gram_matrix(style_img)
    return ((G_input - G_style)**2).mean()

  def get_features(self, img, layers):
    x = img
    features = {}
    for num, layer in enumerate(self.cnn.eval()):
      x = layer(x)
      if num in layers:
        features[num] = x
    return features

  #useless
  def denormalize(self, tensor):
    mean = torch.tensor([0.485, 0.456, 0.406]).to(device)
    std = torch.tensor([0.229, 0.224, 0.225]).to(device)
    tensor = tensor * std[:, None, None] + mean[:, None, None]
    tensor = torch.clamp(tensor, 0, 1)
    return tensor

  def transform(self, epochs=101, alpha=10, betta=1000, learning_rate=3e-2):
    input_image = self.content_image.clone().requires_grad_(True)
    optimizer = optim.Adam([input_image], lr=learning_rate)
    content_features = self.get_features(self.content_image, self.content_layers)
    style_features = self.get_features(self.style_image, self.style_layers)
    for epoch in range(epochs):
      optimizer.zero_grad()
      content_loss = style_loss = 0
      input_features = self.get_features(input_image, self.content_layers.union(self.style_layers))
      for key in input_features:
        if key in self.content_layers:
          content_loss += self.content_loss(input_features[key], content_features[key])
        if key in self.style_layers:
          style_loss += self.style_loss(input_features[key], style_features[key])/len(self.style_layers)
      total_loss = alpha*content_loss + betta*style_loss
      total_loss.backward()
      optimizer.step()
      #if epoch % 50 == 0:
        #img_show(self.style_image.cpu(), input_image.cpu().detach())
        #plt.show()
    return input_image.detach().clamp(0, 1)