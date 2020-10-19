function [GyroEulerPhiThetaPsi]=Gyro_pqr(GyroPQR,dt)


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