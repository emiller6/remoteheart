%%AFib Classification
%%Sampling rate is 128 Hz, each record has 65,536 samples

%%Based on https://www.mathworks.com/help/wavelet/ug/classify-time-series-using-wavelet-analysis-and-deep-learning.html?searchHighlight=ecg%20machine%20learning&s_tid=srchtitle_ecg%20machine%20learning_24
load('github_repo/ECGData/ECGData.mat');
%load('afib.mat');
%lbls = [];
%for j=1:2*length(recs)
    %lbls = [lbls;"AFIB"];
%end

ECGData.Data = [ECGData.Data; afib];
ECGData.Labels = [ECGData.Labels; lbls];
%if ~exist('github_repo/ECGData/data', 'dir')
helperCreateECGDirectories(ECGData, 'github_repo/ECGData', 'data');
%end
helperPlotReps(ECGData)

%Time-Frequency Representations
helperCreateRGBfromTF(ECGData, 'github_repo/ECGData', 'data');

%Separate Training and Testing Data
all_imgs = imageDatastore('github_repo/ECGData/data','IncludeSubfolders',true,'LabelSource','foldernames');
rng default
[imgsTrain,imgsValidation] = splitEachLabel(all_imgs,0.8,'randomized');

%GoogLeNet
net = googlenet;
layer_graph = layerGraph(net);
numberOfLayers = numel(layer_graph.Layers);
newDropoutLayer = dropoutLayer(0.6,'Name','new_Dropout');
layer_graph = replaceLayer(layer_graph,'pool5-drop_7x7_s1',newDropoutLayer);
numClasses = numel(categories(imgsTrain.Labels));
newConnectedLayer = fullyConnectedLayer(numClasses,'Name','new_fc','WeightLearnRateFactor',5,'BiasLearnRateFactor',5);
layer_graph = replaceLayer(layer_graph,'loss3-classifier',newConnectedLayer);
newClassLayer = classificationLayer('Name','new_classoutput');
layer_graph = replaceLayer(layer_graph,'output',newClassLayer);

%Train GoogLeNet
options = trainingOptions('sgdm',...
    'MiniBatchSize',15,...
    'MaxEpochs',20,...
    'InitialLearnRate',1e-4,...
    'ValidationData',imgsValidation,...
    'ValidationFrequency',10,...
    'Verbose',1,...
    'ExecutionEnvironment','cpu',...
    'Plots','training-progress');
rng default
trainedGN = trainNetwork(imgsTrain,layer_graph,options);

%Evaluate GoogLeNet
[YPred,probs] = classify(trainedGN,imgsValidation);
accuracy = mean(YPred==imgsValidation.Labels);
disp(['GoogLeNet Accuracy: ',num2str(100*accuracy),'%'])

%SqueezeNet
sqz = squeezenet;
squeeze_graph = layerGraph(sqz);
tmpLayer = squeeze_graph.Layers(end-5);
newDropoutLayer = dropoutLayer(0.6,'Name','new_dropout');
squeeze_graph = replaceLayer(squeeze_graph,tmpLayer.Name,newDropoutLayer);
numClasses = numel(categories(imgsTrain.Labels));
tmpLayer = squeeze_graph.Layers(end-4);
newLearnableLayer = convolution2dLayer(1,numClasses, ...
        'Name','new_conv', ...
        'WeightLearnRateFactor',10, ...
        'BiasLearnRateFactor',10);
squeeze_graph = replaceLayer(squeeze_graph,tmpLayer.Name,newLearnableLayer);
tmpLayer = squeeze_graph.Layers(end);
newClassLayer = classificationLayer('Name','new_classoutput');
squeeze_graph = replaceLayer(squeeze_graph,tmpLayer.Name,newClassLayer);

%Resize Data Images
augimgsTrain = augmentedImageDatastore([227 227],imgsTrain);
augimgsValidation = augmentedImageDatastore([227 227],imgsValidation);

%Train Squeezenet
ilr = 3e-4;
miniBatchSize = 10;
maxEpochs = 15;
valFreq = floor(numel(augimgsTrain.Files)/miniBatchSize);
opts = trainingOptions('sgdm',...
    'MiniBatchSize',miniBatchSize,...
    'MaxEpochs',maxEpochs,...
    'InitialLearnRate',ilr,...
    'ValidationData',augimgsValidation,...
    'ValidationFrequency',valFreq,...
    'Verbose',1,...
    'ExecutionEnvironment','cpu',...
    'Plots','training-progress');

rng default
trainedSN = trainNetwork(augimgsTrain,squeeze_graph,opts);

%Evaluate Squeezenet
[YPred,probs] = classify(trainedSN,augimgsValidation);
accuracy = mean(YPred==imgsValidation.Labels);
disp(['SqueezeNet Accuracy: ',num2str(100*accuracy),'%'])
