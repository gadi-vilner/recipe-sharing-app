// frontend/src/context/AuthContext.tsx

"use client";

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';

// Define the shape of the context data
interface AuthContextType {
  isAuthenticated: boolean;
  isLoading: boolean; // To track if we've checked for a token yet
  token: string | null;
  login: (token: string) => void;
  logout: () => void;
}

// Create the context with an initial undefined value
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Define the AuthProvider component
export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true); // 2. Start in a loading state

  // On initial load, check if a token exists in localStorage
  useEffect(() => {
    try {
      const storedToken = localStorage.getItem('accessToken');
      if (storedToken) {
        setToken(storedToken);
      }
    } catch (error) {
      console.error("Could not access local storage", error);
    } finally {
      // 3. After checking, set loading to false
      setIsLoading(false);
    }
  }, []);

  const login = (newToken: string) => {
    localStorage.setItem('accessToken', newToken);
    setToken(newToken);
  };

  const logout = () => {
    localStorage.removeItem('accessToken');
    setToken(null);
  };

  // Determine if the user is authenticated based on the presence of a token
  const isAuthenticated = !!token;

  return (
    // 4. Provide the new 'isLoading' state to the context
    <AuthContext.Provider value={{ isAuthenticated, isLoading, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// Create a custom hook for easy access to the context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};