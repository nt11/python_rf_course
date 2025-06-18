% fAmp = pa(G, OIP3, P1dB, Psat)
pa_attributes = { ...
    struct('sn','SN1234','G',21.1,'OIP3',23.2,'P1dB',14.3), ...
    struct('sn','SN4321','G',22.8,'OIP3',25.5,'P1dB',16.0), ...
    struct('sn','SN2222','G',23.7,'OIP3',26.1,'P1dB',17.5), ...
    struct('sn','SN3333','G',23.4,'OIP3',25.9,'P1dB',19.4), ...
    struct('sn','SN4444','G',22.5,'OIP3',28.1,'P1dB',20.1)};

Freq =  [1500,2000,2500]; % MHz
p_in =          (-15:3)'; % dBm

% Each power amplifier is a file with name as the SN and testest for the frequencies
for k = 1:length(pa_attributes)

    G       = pa_attributes{k}.G;
    OIP3    = pa_attributes{k}.OIP3;
    P1dB    = pa_attributes{k}.P1dB;
    % Open text file for writing PA data. Name of file is the SN. Delete if it exists
    if exist([pa_attributes{k}.sn '.txt'],'file')
        delete([pa_attributes{k}.sn '.txt']);
    end

    T = table;
    for f = Freq
        fAmp    = pa('G',G,'OIP3',OIP3,'P1dB',P1dB);
        p_out   = db10(fAmp(sqrt(lin10(p_in)/1000*50)).^2/50*1000);
        p_out   = round((p_out + randn(size(p_out))/20)*100)/100;
        F       = f*ones(size(p_in));
        t       = table(p_in,p_out,F);
        % Append table
        T = [T;t];
        % Drop Gain and P1dB for higher frequency
        G       = G     - rand*2;
        P1dB    = P1dB  - rand  ;
    end
    % Write the table to the file
    writetable(T,[pa_attributes{k}.sn '.txt']);
end
