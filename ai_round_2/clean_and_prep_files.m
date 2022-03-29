
list = ['afdb/1.0.0/', 'chfdb/1.0.0/', 'cudb/1.0.0/', 'nsrdb/1.0.0/', 'stdb/1.0.0/', 'svdb/1.0.0/'];
num_recs = [2, 2, 1, 2, 2, 2];
label = ['AFIB','CHF', 'VT', 'NSR', 'ST', 'SVA'];
ecg_data = [];
ecg_labels = [];

for i = 1:length(list)
  list(i) = strcat('physionet.org/files/', list(i))
  prepData(list(i));
  strcat('prepped ',list(i))
  [d, l] = cleanData(list(i), num_recs(i), label(i));
  ecg_data = [ecg_data; d];
  ecg_labels = [ecg_labels; l];
  size(ecg_data)
  strcat('cleaned ',list(i))
end
save('ecg_data.mat', 'ecg_data', 'ecg_labels')

function [] = prepData(datafiles_loc)
  fid = fopen(strcat(datafiles_loc,'RECORDS'));
  loc = fgetl(fid);
  while ischar(loc)
      wfdb2mat(strcat(datafiles_loc,loc))
      loc = fgetl(fid);
  end
  fclose(fid);
end

function [data, labels] = cleanData(datafiles_loc, num_per_rec, label)
  recs = [];
  fid = fopen(strcat(datafiles_loc,'RECORDS'));
  loc = fgetl(fid);
  data = [];
  labels = [];
  while ischar(loc)
      [time, signal, Fs, siginfo] = rdmat(strcat(loc,'m'));
      tmp = signal';
      for x=1:num_per_rec
          tmp_2 = resample(tmp(x,:),128,Fs);
          data = [data; tmp_2(1:65000)];
          labels = [labels; label];
      end
      loc = fgetl(fid);
  end
  fclose(fid);
end
