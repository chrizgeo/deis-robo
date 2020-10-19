function [AccPhiTheta]=Acc_PhiTheta(accReadings,AccelerometerNoiseMPU9250)

% subtracting noise from the values
accReadings=accReadings-AccelerometerNoiseMPU9250;

AccXYZ(:,1)=accReadings(:,1);
AccXYZ(:,2)=accReadings(:,2);
AccXYZ(:,3)=accReadings(:,3);

g=9.8;
for kk=1:length(AccXYZ)
    AccPhiTheta(kk,2)=asin(AccXYZ(kk,1)/g);
    AccPhiTheta(kk,1)=asin(-AccXYZ(kk,2)/(g*cos(AccPhiTheta(kk,2))));
end
end