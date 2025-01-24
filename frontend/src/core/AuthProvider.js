import React, { createContext, useContext } from "react";
import AuthService from "../services/auth";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  return (
    <AuthContext.Provider value={AuthService}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom Hook to Access AuthService
export const useAuth = () => {
  return useContext(AuthContext);
};
