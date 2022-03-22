recs = [];
fid = fopen('physionet.org/files/ptb-xl/1.0.1/RECORDS');
loc = fgetl(fid);
while ischar(loc)
    if ~contains(loc,'records100')
        recs = [recs; loc];
    end
    loc = fgetl(fid);
end
fclose(fid);
mi = [] %zeros(12*length(recs),65536);
y = 0;
for i=1:length(recs)
    [time, signal, Fs, siginfo] = rdmat(strcat('mi_matfiles/',convertStringsToChars(recs(i,:)),'m'));
    tmp = signal;
    for x=1:12
        y = y+1;
        tmp_2 = resample(tmp(x,:),128,Fs);
        mi(y,:) = tmp_2(1:65536);
    end
end

labels_file = fopen('physionet.org/files/ptb-xl/1.0.1/ptbxl_database.csv');
lbls = [];
loc = fgetl(labels_file);
while ischar(loc)
  start_idx = strfind(loc, '{');
  end_idx = strfind(loc, '}');
  codes = loc(start_idx+1:end_idx);
  if contains(codes, 'NORM') && codes(strfind(codes, 'NORM')+6) ~= 0
    lbls = [lbls;"N"]
  else
    if contains(codes, 'MI') && codes(strfind(codes, 'MI')+4) ~= 0
      lbls = [lbls;"MI"]
    else
      lbls = [lbls;"O"]
    end
  end
  loc = fgetl(labels_file);
end

lbls_2 = [];
for j=1:12*length(recs)
    lbls_2 = [lbls_2;"O"];
end

data = mi;
labels = lbls;
save('MI_data.mat','data');
save('MI_labels.mat','labels');
