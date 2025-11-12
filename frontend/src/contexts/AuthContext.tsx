/**
 * Authentication Context
 * Manages global authentication state
 */

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { api } from '@/lib/api';
import { useRouter } from 'next/router';

interface User {
  id: string;
  email: string;
  full_name: string;
  role: 'free' | 'starter' | 'pro' | 'enterprise';
  is_active: boolean;
  is_verified: boolean;
  videos_generated_this_month: number;
  videos_generated_total: number;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string, fullName: string) => Promise<void>;
  logout: () => void;
  refetchUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  // Fetch user on mount if authenticated
  useEffect(() => {
    const fetchUser = async () => {
      if (api.auth.isAuthenticated()) {
        try {
          const userData = await api.auth.getCurrentUser();
          setUser(userData);
        } catch (error) {
          console.error('Failed to fetch user:', error);
          // Clear invalid tokens
          api.auth.logout();
        }
      }
      setLoading(false);
    };

    fetchUser();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      await api.auth.login(email, password);
      const userData = await api.auth.getCurrentUser();
      setUser(userData);
      router.push('/dashboard');
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Login failed');
    }
  };

  const signup = async (email: string, password: string, fullName: string) => {
    try {
      await api.auth.signup(email, password, fullName);
      // Auto-login after signup
      await login(email, password);
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Signup failed');
    }
  };

  const logout = () => {
    api.auth.logout();
    setUser(null);
    router.push('/login');
  };

  const refetchUser = async () => {
    try {
      const userData = await api.auth.getCurrentUser();
      setUser(userData);
    } catch (error) {
      console.error('Failed to refetch user:', error);
    }
  };

  const value: AuthContextType = {
    user,
    loading,
    isAuthenticated: !!user,
    login,
    signup,
    logout,
    refetchUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
