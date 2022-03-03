fid = fopen('training2017/RECORDS');
loc = fgetl(fid);
recs = [];
while ischar(loc)
    recs = [recs; loc];
    loc = fgetl(fid);
end
fclose(fid);

afib = {};
y = 0;
for i=1:length(recs)
     [time, signal, Fs, siginfo] = rdmat(strcat('training2017/',convertStringsToChars(recs(i,:)),'.mat')).val;
     tmp = signal;
     tmp(1,:) = tmp(1,:)./1000;
     afib = {afib; tmp};
end


save('afib_lstm.mat','afib')
