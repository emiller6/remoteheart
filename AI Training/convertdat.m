
fid = fopen('ptb-xl/RECORDS');
loc = fgetl(fid);
while ischar(loc)
    if ~contains(loc,'records100')
        wfdb2mat(strcat('ptb-xl/',loc))
    end
    loc = fgetl(fid);
end
fclose(fid);