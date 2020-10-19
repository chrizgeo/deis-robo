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

load 'E:\LEARN\S3\DEIS\Labs\lab4\Lab_Students(1)\Lab_Students\ProblemNo3\IMU_Vals'
fs=100;
dt=1/fs;
% subtracting noise from the values
accReadings=accReadings-AccelerometerNoiseMPU9250;
gyroReadings=gyroReadings-GyroscopeNoiseMPU9250;

h=figure('Name','Acceleration & Gyro Readings');
set(h,'units','normalized','outerposition',[0 0 1 1]);
subplot(311);
plot(accReadings(:,1));hold on;
plot(gyroReadings(:,1),'r');
legend('Acc','Gyro','Location','SouthEast','fontsize',14)

subplot(312);
plot(accReadings(:,2));hold on;
plot(gyroReadings(:,2),'r');
legend('Acc','Gyro','Location','SouthEast','fontsize',14)

subplot(313);
plot(accReadings(:,3));hold on;
plot(gyroReadings(:,3),'r');
legend('Acc','Gyro','Location','SouthEast','fontsize',14)

% the values of p,q, and r
GyroPQR(:,1)=gyroReadings(:,1);
GyroPQR(:,2)=gyroReadings(:,2);
GyroPQR(:,3)=gyroReadings(:,3);

% the values of Gyro are the angular rate of Gyro but not the Euler angles.
% Therefore, we change it to Euler angles

for kk=1:length(GyroPQR)
    if(kk==1)
        prevPhi=0;
        prevTheta=0;
        prevPsi=0;
    end
    
    sinPhi=sin(prevPhi);
    cosPhi=cos(prevPhi);
    
    cosTheta=cos(prevTheta);
    tanTheta=tan(prevTheta);
    
    GyroEulerPhiThetaPsi(kk,1)=prevPhi+dt*(GyroPQR(kk,1)+GyroPQR(kk,2)*sinPhi*tanTheta+GyroPQR(kk,3)*cosPhi*tanTheta);
    GyroEulerPhiThetaPsi(kk,2)=prevTheta+dt*(            GyroPQR(kk,2)*cosPhi         -GyroPQR(kk,3)*sinPhi);
    GyroEulerPhiThetaPsi(kk,3)=prevPsi+dt*(              GyroPQR(kk,2)*sinPhi/cosTheta+GyroPQR(kk,3)*cosPhi/cosTheta);
    
    clear sinPhi;clear cosPhi;clear cosTheta;clear tanTheta;
    
    prevPhi=GyroEulerPhiThetaPsi(kk,1);
    prevTheta=GyroEulerPhiThetaPsi(kk,2);
    prevPsi=GyroEulerPhiThetaPsi(kk,3);
end
clear prevPhi;clear prevTheta;clear prevPsi;clear kk;

% Acceleration
AccXYZ(:,1)=accReadings(:,1);
AccXYZ(:,2)=accReadings(:,2);
AccXYZ(:,3)=accReadings(:,3);

% acceleration data is the measure fx,fy and fz accelerations in which
% gravitation acceleration is also included/

g=9.8;
for kk=1:length(AccXYZ)
    AccPhiTheta(kk,2)=asin(AccXYZ(kk,1)/g);
    AccPhiTheta(kk,1)=asin(-AccXYZ(kk,2)/(g*cos(AccPhiTheta(kk,2))));
end
%%
%%%%%%%%%%%%%%%%%%%%%%%%% Kalman Filtering %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
H = eye(4);

%%%%%%%%%%%%%%%%%%% CHOOSE RIGHT VALUES
Q = 0.001*eye(4);
R = 50*eye(4);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for k=1:length(GyroPQR)
    %% getting Gyro data
    p = GyroPQR(k,1);
    q = GyroPQR(k,2);
    r = GyroPQR(k,3);
    
    A = eye(4) + dt*1/2*[ 0  -p  -q  -r;p   0   r  -q;q  -r   0   p...
        ;r   q  -p   0];
    
    % getting acceleration data
    phi=AccPhiTheta(k,1);
    theta=AccPhiTheta(k,2);
    psi=0;
    %% Euler to quaternion    
    
    sinPhi   = sin(phi/2);    cosPhi   = cos(phi/2);
    sinTheta = sin(theta/2);  cosTheta = cos(theta/2);
    sinPsi   = sin(psi/2);    cosPsi   = cos(psi/2);
    
    z = real([ cosPhi*cosTheta*cosPsi + sinPhi*sinTheta*sinPsi;
        sinPhi*cosTheta*cosPsi - cosPhi*sinTheta*sinPsi;
        cosPhi*sinTheta*cosPsi + sinPhi*cosTheta*sinPsi;
        cosPhi*cosTheta*sinPsi - sinPhi*sinTheta*cosPsi;
        ]);
    %%
    if(k==1)
        x = [1 0 0 0]';
        P = 1*eye(4);
    end
    
    
    xp = A*x;
    Pp = A*P*A' + Q;
    
    K = Pp*H'*inv(H*Pp*H' + R);
    
    x = xp + K*(z - H*xp);     % x = [ q1 q2 q3 q4 ]
    P = Pp - K*H*Pp;
    
    phi_Fused   =  atan2( 2*(x(3)*x(4) + x(1)*x(2)), 1 - 2*(x(2)^2 + x(3)^2) );
    theta_Fused = -asin(  2*(x(2)*x(4) - x(1)*x(3)) );
    psi_Fused   =  atan2( 2*(x(2)*x(3) + x(1)*x(4)), 1 - 2*(x(3)^2 + x(4)^2) );
    
    EulerSaved(k, :) = [ phi_Fused theta_Fused psi_Fused ];
    clear phi_Fused,clear theta_Fused;clear psi_Fused;
end
EulerSaved=EulerSaved.*180/pi;

t = 0:dt:length(GyroEulerPhiThetaPsi)*dt-dt;

h=figure('Name','Acceleration & Gyro Readings with Sensor fusion');
set(h,'units','normalized','outerposition',[0 0 1 1]);

subplot(311);
plot(accReadings(:,1));hold on;
plot(gyroReadings(:,1),'r');hold on;
plot(EulerSaved(:,1),'g');
legend('Acc','Gyro','acc-Gyro fused','Location','SouthEast','fontsize',12)

subplot(312);
plot(accReadings(:,2));hold on;
plot(gyroReadings(:,2),'r');hold on;
plot(EulerSaved(:,2),'g');
legend('Acc','Gyro','acc-Gyro fused','Location','SouthEast','fontsize',12)

subplot(313);
plot(accReadings(:,3));hold on;
plot(gyroReadings(:,3),'r');hold on;
plot(EulerSaved(:,3),'g');
legend('Acc','Gyro','acc-Gyro fused','Location','SouthEast','fontsize',12);


h = figure('Name','Gyro Euler angles EKF');

subplot(311);
set(h,'units','normalized','outerposition',[0 0 1 1]);
plot(t,GyroEulerPhiThetaPsi(:,1).*180/pi);hold on;
plot(t,EulerSaved(:,1),'r');
legend('Gyro','acc-Gyro fused','Location','SouthEast','fontsize',12);

subplot(312);
set(h,'units','normalized','outerposition',[0 0 1 1]);
plot(t,GyroEulerPhiThetaPsi(:,2).*180/pi);hold on;
plot(t,EulerSaved(:,2),'r');
legend('Gyro','acc-Gyro fused','Location','SouthEast','fontsize',12);

subplot(313);
set(h,'units','normalized','outerposition',[0 0 1 1]);
plot(t,GyroEulerPhiThetaPsi(:,3).*180/pi);hold on;
plot(t,EulerSaved(:,3),'r');
legend('Gyro','acc-Gyro fused','Location','SouthEast','fontsize',12);



