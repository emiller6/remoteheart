function [ml_res] = analyzeECG(ecgsignal)
    %persistent net jetdata;
    %if(isempty(jetdata))
        %jetdata = colourmap(128,class(ecgsignal));
    %end

    % Load trained network
        %net = coder.loadDeepLearningNetwork('finalNet.mat');
    trainedGN = load('finalNet.mat');
    net = trainedGN;

    image = helperCreateRGBfromTF(ecgsignal);

    % Prediction
    [ml_res] = predict(net,image);
end

function im = helperCreateRGBfromTF(data)
%continuous wavelet transform of the ECG signals and generates the scalograms from the wavelet coefficients
  persistent fb
  [~,signalLength] = size(data);

  if isempty(fb)
    fb = cwtfilterbank('SignalLength',signalLength,'VoicesPerOctave',12);
  end

  cfs = abs(fb.wt(data));
  im = ind2rgb(im2uint8(rescale(cfs)),jet(128));
  im = im2uint8(imresize(im,[224 224]));
end
