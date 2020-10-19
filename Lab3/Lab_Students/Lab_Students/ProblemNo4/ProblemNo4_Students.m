%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%                    Sensor Fusion Lab, Problem No 3
%
% Prepared by: Orand, Abbas
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Data was collected from an IMU9250. The sampling rate was set to 100 Hz.
% First, the IMU was placed at rest. Then, the IMU was moved along its 
% x-axis between almost 40 % and -40 degrees for more than 10 times 
% followed by a short rest. More than 10 more times the same movement was
% repeated. After a short rest, the IMU was moved along its y-axis between
% almost -25 and 25 degrees for two sets of ten-times. There was a short
% rest between the two sets.

clear
clc
close all


% GyroscopeNoise and AccelerometerNoise is determined from datasheet.
GyroscopeNoiseMPU9250 = 3.0462e-06; % GyroscopeNoise (variance value) in units of rad/s
AccelerometerNoiseMPU9250 = 0.0061; % AccelerometerNoise(variance value)in units of m/s^2

load 'E:\LEARN\S3\DEIS\Labs\lab4\Lab_Students(1)\Lab_Students\ProblemNo4\IMU_Vals'
fs=100;
dt=1/fs;
% subtracting noise from the values
accReadings=accReadings-AccelerometerNoiseMPU9250;
gyroReadings=gyroReadings-GyroscopeNoiseMPU9250;


% The Gyro values used for sensor fusion
% the values of p,q, and r
GyroPQR(:,1)=gyroReadings(:,1);
GyroPQR(:,2)=gyroReadings(:,2);
GyroPQR(:,3)=gyroReadings(:,3);

% The Gyro values used for comparing the Gyro Euler results with the fused
% data, observing the drift
[GyroEulerPhiThetaPsi]=Gyro_pqr(GyroPQR,dt);

% Acceleration
[AccPhiTheta]=Acc_PhiTheta(accReadings,AccelerometerNoiseMPU9250);


%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Extended Kalman Filtering
for k=1:length(GyroPQR)
    
    % getting Gyro data
    p = GyroPQR(k,1);
    q = GyroPQR(k,2);
    r = GyroPQR(k,3);
    
    % getting the accelerometer values    
    phi=AccPhiTheta(k,1);
    theta=AccPhiTheta(k,2);
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% EKF function%%%%%%%%%%%%%%%%%%%%%%%
    
    [phi theta psi] = Extended_Kalman_Filter([phi theta],[p q r],dt,k);
    
    EulerSaved(k, :) = [ phi theta psi ];
end
EulerSaved=EulerSaved.*180/pi;

t = 0:dt:length(GyroEulerPhiThetaPsi)*dt-dt;
h=figure('Name','GyroEulerAngles EKF');
set(h,'units','normalized','outerposition',[0 0 1 1]);

subplot(121);plot(t,GyroEulerPhiThetaPsi(:,1).*180/pi);hold on; % Roll
plot(t, EulerSaved(:,1),'r')
ylim([-75 75]);set(gca,'fontsize',40);title('Roll');
legend('Gyro Angles','Gyro&Acc Fused');

subplot(122);plot(t,GyroEulerPhiThetaPsi(:,2).*180/pi);hold on; % Pitch
plot(t, EulerSaved(:,2),'r')
ylim([-75 75]);set(gca,'fontsize',40);title('Pitch');


[ax1,h1]=suplabel('t (s)');
[ax2,h2]=suplabel('angle (deg)','y');
set(h1,'FontSize',40)
set(h2,'FontSize',40)




