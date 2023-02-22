#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# install pytorch 
# !pip install --pre torch torchvision torchaudio -f https://download.pytorch.org/whl/nightly/cu102/torch_nightly.html -U


# In[4]:
from PIL import Image
from torchvision import transforms
import os
import numpy as np
import torch
import torch.nn as nn
import torchvision
from torchvision import datasets, transforms, models
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
os.environ["TOKENIZERS_PARALLELISM"] = "false"


def objectDetect(imagePath):


	img = Image.open(imagePath).convert('RGB')

	tfms = transforms.Compose([
				transforms.Resize(227),
				transforms.ToTensor(),
				transforms.Normalize([0.485, 0.456, 0.406],
                              		[0.229, 0.224, 0.225]),
				transforms.CenterCrop(227)
				])

	img_tensor = tfms(img).to('cpu').unsqueeze(0)

	model = torchvision.models.detection.fasterrcnn_resnet50_fpn()
	in_features = model.roi_heads.box_predictor.cls_score.in_features
	num_classes = 6

	model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)

	model.load_state_dict(torch.load('./Code/detectors/Motor/model.pth'))
	model.eval()
	
	output = model(img_tensor)

	scores = output[0]['scores']
	labels = output[0]['labels']
	labelDict = {0: "x", 1:"left", 2:"right", 3:"down", 4:"ham", 5:"check",}
	if len(scores) > 0 and len(labels) > 0:
		scores = output[0]['scores'][0].item()
		labels = output[0]['labels'][0].item()
		if scores > 0.5:
			return(["closable", labelDict[labels]])

	else:
		return(["Not closable"])















