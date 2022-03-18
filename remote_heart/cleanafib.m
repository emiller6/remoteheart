
recs = ["04015" "04043" "04048" "04126" "04746" "04908" "04936" "05091" "05121" "05261" "06426" "06453" "06995" "07162" "07859" "07879" "07910" "08215" "08219" "08378" "08405" "08434" "08455"];
afib = zeros(2*length(recs),65536);
y = 0;
for i=1:length(recs)
    tmp = matfile(strcat('afib/',convertStringsToChars(recs(i)),'m.mat')).val;
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
    lbls = [lbls;"AFIB"];
end

save('afib.mat','afib');
