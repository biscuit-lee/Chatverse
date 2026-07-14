"use client";

import { createContext, useContext, useState, useEffect } from "react";
import { api } from "./api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("token");
    const username = localStorage.getItem("username");
    const id = localStorage.getItem("userId");
    if (token && username && id) {
      setUser({ token, username, id: Number(id) });
    }
    setLoading(false);
  }, []);

  async function login(username, password) {
    const res = await api.login(username, password);
    localStorage.setItem("token", res.token);
    localStorage.setItem("username", res.username);
    localStorage.setItem("userId", String(res.id));
    setUser({ token: res.token, username: res.username, id: res.id });
    return res;
  }

  async function register(username, password) {
    const res = await api.register(username, password);
    return res;
  }

  function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    localStorage.removeItem("userId");
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
