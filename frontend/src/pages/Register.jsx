import React from "react";
import { SignUp } from "@clerk/clerk-react";
import "./Register.css";

const Register = () => {
  return (
    <div className="register-page">
      <div className="container" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: '50px', marginBottom: '50px' }}>
        <SignUp 
          signInUrl="/login" 
          forceRedirectUrl="/role-redirect" 
          appearance={{
            elements: {
              footer: { display: 'none' },
              formFieldRow__password: "custom-password-row"
            }
          }}
        />
      </div>
    </div>
  );
};

export default Register;
