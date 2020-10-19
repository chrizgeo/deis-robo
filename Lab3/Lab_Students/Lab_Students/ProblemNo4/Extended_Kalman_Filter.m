function [phi theta psi] = Extended_Kalman_Filter (AccPhiTheta,GyroPQR,dt,k)
    H = [ 1 0 0; 0 1 0 ];
    Q = [ 0.0001 0 0; 0 0.0001 0; 0 0 0.1 ];
    R = [ 6 0; 0 6 ];
 
        p = GyroPQR(1,1);
        q = GyroPQR(1,2);
        r = GyroPQR(1,3);
        
        accPhi = AccPhiTheta(1,1);
        accTheta = AccPhiTheta(1,2);
        
        x = [1 0 0 ]';
        P = 1*eye(3);
        
        A = eye(3) + dt*1/2*[ q*cos(accPhi)*tan(accTheta)-r*sin(accPhi)*tan(accTheta)    q*sin(accPhi)*sec(accTheta)^2+r*cos(accPhi)*tan(accTheta)^2   0;...
            -q*sin(accPhi)-r*cos(accPhi)   0   0;...
            q*cos(accPhi)*sec(accTheta)-r*sin(accPhi)*sec(accTheta)  q*sin(accPhi)*sec(accTheta)*tan(accTheta)+r*cos(accPhi)*sec(accTheta)*tan(accTheta)   0];

        % getting acceleration data
        phi=AccPhiTheta(1,1);
        theta=AccPhiTheta(1,2);
        psi=0;
        %% Euler to quaternion    

        sinPhi   = sin(phi);    cosPhi   = cos(phi);
        sinTheta = sin(theta);  tanTheta = tan(theta);
        secTheta = sec(theta);
        z = real([phi theta ]);
        %%
      


        xp = A*x;
        Pp = A*P*A' + Q;

        K = Pp*H'*inv(H*Pp*H' + R);

        x = xp + K*(z - H*xp);     % x = [ q1 q2 q3 q4 ]
        P = Pp - K*H*Pp;

        phi_Fused   =  atan2( 2*(x(3)*x(4) + x(1)*x(2)), 1 - 2*(x(2)^2 + x(3)^2) );
        theta_Fused = -asin(  2*(x(2)*x(4) - x(1)*x(3)) );
        psi_Fused   =  atan2( 2*(x(2)*x(3) + x(1)*x(4)), 1 - 2*(x(3)^2 + x(4)^2) );

        phi = phi_Fused;
        theta = theta_Fused;
        psi = psi_Fused;
        clear phi_Fused,clear theta_Fused;clear psi_Fused;
