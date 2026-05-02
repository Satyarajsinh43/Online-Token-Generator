import React from "react";
import { SignIn } from "@clerk/clerk-react";
import "./Login.css";

const Login = () => {
  return (
    <div className="login-page">
      <div className="container" style={{ display: 'flex', justifyContent: 'center', marginTop: '50px', marginBottom: '50px' }}>
        <SignIn 
          signUpUrl="/register" 
          forceRedirectUrl="/role-redirect" 
          appearance={{
            elements: {
              footer: { display: 'none' }
            }
          }}
        />
      </div>
    </div>
  );
};

export default Login;
