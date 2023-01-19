#!/usr/bin/env python
# coding: utf-8

# In[3]:


# install pytorch 
#get_ipython().system('pip install --pre torch torchvision torchaudio -f https://download.pytorch.org/whl/nightly/cu102/torch_nightly.html -U')


# In[4]:


# test torch version and CUDA device
# import torch
# print(torch.__version__)
# a = torch.Tensor([1]).cuda()
# print(a)


# In[3]:


# install pycocotools
#get_ipython().system('pip install pycocotools')


# In[4]:


# # mount google drive
# from google.colab import drive
# drive.mount("/content/gdrive")


# In[5]:
if __name__ == '__main__':

    # change to project home directory
    import os
    os.chdir(".../MIRACLE/code/src/ExpandingElements/ImageDetection/object_detect")



    # In[7]:


    import os
    import numpy as np
    import torch
    import torch.nn as nn
    import torchvision
    from torchvision import transforms
    from torchvision.models.detection.faster_rcnn import FastRCNNPredictor


    # In[8]:


    # from custom_dataset_mscoco import myOwnDataset
    # import utils
    # from engine import train_one_epoch, evaluate


    # In[9]:


    import pprint
    pp = pprint.PrettyPrinter()
    import json


    # In[10]:


    # path to data and annotation
    # data_dir = 'data'
    # annotation = 'data/result.json'


    # In[11]:


    # input transformations

    import transforms as T

    def get_transform(train):
        transforms = []
        transforms.append(T.ToTensor())
        if train:
            transforms.append(T.RandomHorizontalFlip(0.5))
        return T.Compose(transforms)

    # normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std= [0.229, 0.224, 0.225])

    # train_transform = transforms.Compose([
    #   transforms.Resize(227),
    #   transforms.CenterCrop(227),
    #   transforms.ToTensor(),
    #   normalize
    #  ])

    # validation_transform = transforms.Compose([
    #   transforms.ToTensor()
    #  ])

    # test_transform = transforms.Compose([
    #   transforms.ToTensor()
    #  ])

    # create dataset
    dataset_train = myOwnDataset(root=data_dir,
                              annotation=annotation,
                              transforms=get_transform(train=True)
                              )
    dataset_validation = myOwnDataset(root=data_dir,
                              annotation=annotation,
                              transforms=get_transform(train=False)
                              )

    dataset_test = myOwnDataset(root=data_dir,
                              annotation=annotation,
                              transforms=get_transform(train=False)
                              )
    

    # In[34]:


    # split the dataset in train, validation and test set

    # indices = torch.randperm(len(dataset_train)).tolist()
    # dataset_train = torch.utils.data.Subset(dataset_train, indices[:-64])
    # print(len(dataset_train))
    # dataset_validation = torch.utils.data.Subset(dataset_validation, indices[-64:-1])
    # print(len(dataset_validation))
    # dataset_test = torch.utils.data.Subset(dataset_test, indices[-1:])
    # print(len(dataset_test))

    validSize = int(len(dataset_train) * 0.84)
    trainSize = int(len(dataset_train) * 0.15)
    testSize = int(len(dataset_train) - (trainSize + validSize))
    indices = torch.randperm(len(dataset_train)).tolist()

    print("SPLITTING")

    dataset_train = torch.utils.data.Subset(dataset_train, indices[:trainSize * -1])
    print(len(dataset_train))

    dataset_validation = torch.utils.data.Subset(dataset_validation, indices[trainSize * -1:testSize * -1])
    print(len(dataset_validation))

    dataset_test = torch.utils.data.Subset(dataset_test, indices[testSize * -1:])
    print(len(dataset_test))


    # In[35]:


    # define training, validation and test data loaders
    data_loader_train = torch.utils.data.DataLoader(
        dataset_train, batch_size=1, shuffle=True, num_workers=1,
        collate_fn=utils.collate_fn)

    data_loader_validation = torch.utils.data.DataLoader(
        dataset_validation, batch_size=1, shuffle=False, num_workers=1,
        collate_fn=utils.collate_fn)

    data_loader_test = torch.utils.data.DataLoader(
        dataset_test, batch_size=1, shuffle=False, num_workers=1,
        collate_fn=utils.collate_fn)


    # In[36]:


    # select device (whether GPU or CPU)
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


    # In[37]:


    # # DataLoader is iterable over Dataset
    # # check image_id, labels, box dimentions
    # for imgs, annotations in data_loader:
    #     print('image_id: ', annotations[0]['image_id'])
    #     print('labels: ', annotations[0]['labels'])
    #     print('boxes: ', annotations[0]['boxes'])
    #     print('-----------------------------------------')


    # In[38]:


    def get_model_instance(num_classes):
        # load a model instance pre-trained on COCO
        model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
        # print(model)
        # get number of input features for the classifier
        in_features = model.roi_heads.box_predictor.cls_score.in_features
        
        # replace the pre-trained head with a new one
        model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
        return model


    # 

    # In[39]:


    # load model
    num_classes = 6
    # get the model using our helper function
    model = get_model_instance(num_classes)


    # In[40]:


    # move model to the right device
    model.to(device)


    # In[41]:


    # construct an optimizer
    params = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.SGD(params, lr=0.005, momentum=0.9, weight_decay=0.0005)
    # optimizer = torch.optim.Adam(params, lr=0.005, weight_decay=0.0005)
    # and a learning rate scheduler
    lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=100, gamma=0.1)


    # In[42]:


    # let's train it for 10 epochs
    num_epochs = 1


    # In[43]:

    print("================= TRAIN and VALIDATION ===========================")
    for epoch in range(num_epochs):
        # train for one epoch, printing every 10 iterations
        print("HERE")
        train_one_epoch(model, optimizer, data_loader_train, device, epoch, print_freq=10)
        # update the learning rate
        lr_scheduler.step()
        # evaluate on the test dataset
        evaluate(model, data_loader_validation, device=device)
    print("That's it!")


    # In[ ]:


    torch.save(model.state_dict(), 'chkpnt1.pth')


    # In[44]:


    model = torchvision.models.detection.fasterrcnn_resnet50_fpn()


    # In[45]:


    in_features = model.roi_heads.box_predictor.cls_score.in_features


    # In[46]:


    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)


    # In[47]:


    model.load_state_dict(torch.load('chkpnt1.pth'))


    # In[48]:


    model.eval()

    print("DONE TRAINING")
    # # In[50]:


    # print("================= INFERENCE ===========================")
    # with torch.no_grad():
    #     correct = 0
    #     total = 0
    #     inference_result = {}
    #     for images, labels in data_loader_test:
    #         print("-------batch------------")
    #         # pp.pprint(labels)
    #         outputs = model(images)
    #         # pp.pprint(outputs)
    #         # print("boxes")
    #         # pp.pprint(outputs[0]["boxes"][0].numpy().tolist())
    #         boxes = outputs[0]["boxes"][0].numpy().tolist()
    #         # # # pp.pprint(boxes)
    #         # print("labels")
    #         labels = outputs[0]["labels"][0].numpy().tolist()
    #         # # pp.pprint(labels)
    #         # print("scores")
    #         scores = outputs[0]["scores"][0].numpy().tolist()
    #         # # pp.pprint(scores)
    #         # populate JSON
    #         inference_result["boxes"] = boxes
    #         inference_result["labels"] = labels
    #         inference_result["scores"] = scores

    #         pp.pprint(inference_result)
    #         break


    # # In[51]:


    # # write inference result
    # with open('./inference_result.json', 'w') as fp:
    #   json.dump(inference_result, fp)

