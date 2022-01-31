recs = [];
fid = fopen('ptb-xl/RECORDS');
loc = fgetl(fid);
while ischar(loc)
    if ~contains(loc,'records100')
        recs = [recs; loc];
    end
    loc = fgetl(fid);
end
fclose(fid);
mi = zeros(2*length(recs),65536);
y = 0;
for i=1:length(recs)
    tmp = matfile(strcat('mi/',convertStringsToChars(recs(i)),'m.mat')).val;
    for x=1:2
        y = y+1;
        %ADC conversion --- ensure this is correct for 16+24 format (24 =
        %byte offset) and 12-bit resolution
        tmp(x,:) = tmp(x,:)./200;
        tmp_2 = resample(tmp(x,:),128,250);
        afib(y,:) = tmp_2(1:65536);
    end
end

lbls = [];
for j=1:2*length(recs)
    lbls = [lbls;"MI"];
end

save('mi.mat','mi');
