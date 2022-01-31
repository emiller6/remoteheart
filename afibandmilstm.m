%Based on https://www.mathworks.com/help/signal/ug/classify-ecg-signals-using-long-short-term-memory-networks.html

%%AFib Classification
%Load data


%Compare Visuals
normal = Signals{1};
aFib = Signals{4};

subplot(2,1,1)
plot(normal)
title('Normal Rhythm')
xlim([4000,5200])
ylabel('Amplitude (mV)')

subplot(2,1,2)
plot(aFib)
title('Atrial Fibrillation')
xlim([4000,5200])
xlabel('Samples')
ylabel('Amplitude (mV)')

%Prep and Split Raw Data
[Signals,Labels] = segmentSignals(Signals,Labels);
summary(Labels)
afibs = Signals(Labels=='A');
afibl = Labels(Labels=='A');
normals = Signals(Labels=='N');
normall = Labels(Labels=='N');
[trainIndA,~,testIndA] = dividerand(718,0.9,0.0,0.1);
[trainIndN,~,testIndN] = dividerand(4937,0.9,0.0,0.1);

XTrainA = afibs(trainIndA);
YTrainA = afibl(trainIndA);
XTrainN = normals(trainIndN);
YTrainN = normall(trainIndN);

XTestA = afibs(testIndA);
YTestA = afibl(testIndA);
XTestN = normals(testIndN);
YTestN = normall(testIndN);

%Duplicate AFIB signals to prevent assumption of Normal
XTrain = [repmat(XTrainA(1:634),7,1); XTrainN(1:4438)];
YTrain = [repmat(YTrainA(1:634),7,1); YTrainN(1:4438)];

XTest = [repmat(XTestA(1:70),7,1); XTestN(1:490)];
YTest = [repmat(YTestA(1:70),7,1); YTestN(1:490);];

%Define and train LSTM Network - potentially decrease minibatchsize or
%initiallearnrate to improve accuracy
layers = [ ...
    sequenceInputLayer(1)
    bilstmLayer(100,'OutputMode','last')
    fullyConnectedLayer(2)
    softmaxLayer
    classificationLayer
    ];
options = trainingOptions('adam', ...
    'MaxEpochs',10, ...
    'MiniBatchSize', 100, ...
    'InitialLearnRate', 0.005, ...
    'SequenceLength', 1000, ...
    'GradientThreshold', 1, ...
    'ExecutionEnvironment',"auto",...
    'plots','training-progress', ...
    'Verbose',true);
net = trainNetwork(XTrain,YTrain,layers,options);

%Assess Accuracy
trainPred = classify(net,XTrain,'SequenceLength',1000);
LSTMAccuracyTrain = sum(trainPred == YTrain)/numel(YTrain)*100
figure
confusionchart(YTrain,trainPred,'ColumnSummary','column-normalized',...
              'RowSummary','row-normalized','Title','Confusion Chart for LSTM');
          
testPred = classify(net,XTest,'SequenceLength',1000);
LSTMAccuracyTest = sum(testPred == YTest)/numel(YTest)*100
figure
confusionchart(YTest,testPred,'ColumnSummary','column-normalized',...
              'RowSummary','row-normalized','Title','Confusion Chart for LSTM');

%Feature Extraction and Standardization
instfreqTrain = cellfun(@(x)instfreq(x,fs)',XTrain,'UniformOutput',false);
instfreqTest = cellfun(@(x)instfreq(x,fs)',XTest,'UniformOutput',false);
pentropyTrain = cellfun(@(x)pentropy(x,fs)',XTrain,'UniformOutput',false);
pentropyTest = cellfun(@(x)pentropy(x,fs)',XTest,'UniformOutput',false);
XTrain2 = cellfun(@(x,y)[x;y],instfreqTrain,pentropyTrain,'UniformOutput',false);
XTest2 = cellfun(@(x,y)[x;y],instfreqTest,pentropyTest,'UniformOutput',false);
XV = [XTrain2{:}];
mu = mean(XV,2);
sg = std(XV,[],2);

XTrainSD = XTrain2;
XTrainSD = cellfun(@(x)(x-mu)./sg,XTrainSD,'UniformOutput',false);

XTestSD = XTest2;
XTestSD = cellfun(@(x)(x-mu)./sg,XTestSD,'UniformOutput',false);

%Modify and Train Architecture
layers = [ ...
    sequenceInputLayer(2)
    bilstmLayer(100,'OutputMode','last')
    fullyConnectedLayer(2)
    softmaxLayer
    classificationLayer
    ];

options = trainingOptions('adam', ...
    'MaxEpochs',30, ...
    'MiniBatchSize', 100, ...
    'InitialLearnRate', 0.005, ...
    'GradientThreshold', 1, ...
    'ExecutionEnvironment',"auto",...
    'plots','training-progress', ...
    'Verbose',false);
net2 = trainNetwork(XTrainSD,YTrain,layers,options);

%Evaluate Accuracy
trainPred2 = classify(net2,XTrainSD);
LSTMAccuracyTrain = sum(trainPred2 == YTrain)/numel(YTrain)*100
figure
confusionchart(YTrain,trainPred2,'ColumnSummary','column-normalized',...
              'RowSummary','row-normalized','Title','Confusion Chart for LSTM');
testPred2 = classify(net2,XTestSD);
LSTMAccuracyTest = sum(testPred2 == YTest)/numel(YTest)*100
figure
confusionchart(YTest,testPred2,'ColumnSummary','column-normalized',...
              'RowSummary','row-normalized','Title','Confusion Chart for LSTM');

%%MI Classification
