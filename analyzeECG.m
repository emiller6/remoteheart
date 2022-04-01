function [ml_res] = analyzeECG(ecgsignal)
    %persistent net jetdata;
    %if(isempty(jetdata))
        %jetdata = colourmap(128,class(ecgsignal));
    %end

    % Load trained network
    if(isempty(net))
        %net = coder.loadDeepLearningNetwork('finalNet.mat');
        load('finalNet.mat');
        net = trainedGN;
    end

    image = helperCreateRGBfromTF(signal);

    % Prediction
    [ml_res] = predict(net,image);
end

function image = helperCreateRGBfromTF(data)
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

%% Colourmap
function J = colourmap(m,class)

    n = ceil(m/4);
    u = [(1:1:n)/n ones(1,n-1) (n:-1:1)/n]';
    g = ceil(n/2) - (mod(m,4)==1) + (1:length(u))';
    r = g + n;
    b = g - n;
    r1 = r(r<=128);
    g1 = g(g<=128);
    b1 = b(b >0);
    J = zeros(m,3);
    J(r1,1) = u(1:length(r1));
    J(g1,2) = u(1:length(g1));
    J(b1,3) = u(end-length(b1)+1:end);
    feval = str2func(class);
    J = feval(J);
end
