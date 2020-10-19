clear
clc
close all

% insert the address for the file location
load 'E:\LEARN\S3\DEIS\Labs\lab4\Lab_Students(1)\Lab_Students\ProblemNo2\Signal'

plot(ts,Signal,'k'); hold on;
set(gca,'fontsize',30);
xlabel('t (s)'); ylabel('Amplitude (V)');

Ts=0.001;
A = 1;
H = 1;
% What shoud Q and R be
Q = cov(Signal); 
R = 0.5; 
%
for kk=1:length(Signal)
    if(kk==1)
        x = 0.5;
        P = 1;        
    end
    z = Signal(kk,1); 
    xp = A*x; 
    Pp = A*P*A' + Q; 
    K = Pp*H'*inv(H*Pp*H' + R); 
    x = xp + K*(z - H*xp); 
    P = Pp - K*H*Pp; 
    volt(kk,1) = x; 
end
plot(ts,volt,'r','linewidth',1.5);
legend('Signal','Kalman Filtered','Location','SouthWest')
legend boxoff

