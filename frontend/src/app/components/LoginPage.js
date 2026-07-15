"use client";
import { useState } from "react";
import { useAuth } from "../lib/AuthContext";

export default function LoginPage() {
  const [loginError, setLoginError] = useState("");
  const [isRegister, setIsRegister] = useState(false);
  const { login, register } = useAuth();

  async function handleSubmit(event) {
    event.preventDefault();
    setLoginError("");

    const formData = new FormData(event.currentTarget);
    const username = formData.get("username");
    const password = formData.get("password");

    try {
      if (isRegister) {
        await register(username, password);
        await login(username, password);
      } else {
        await login(username, password);
      }
    } catch (err) {
      if (err.status === 401 || err.status === 403) {
        setLoginError("Wrong password/username");
      } else if (err.status === 409 || err.message?.includes("Taken")) {
        setLoginError("Username already taken");
      } else {
        setLoginError("Something went wrong");
      }
    }
  }

  return (
    <div className="min-h-screen bg-background flex items-center justify-center px-4">
      <div className="w-full max-w-sm">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-text-primary">Chatverse</h1>
          <p className="text-text-secondary mt-2 text-[15px]">
            {isRegister ? "Create your account" : "Welcome back"}
          </p>
        </div>

        <form
          onSubmit={handleSubmit}
          className="bg-surface border border-border rounded-2xl p-8 shadow-sm"
        >
          <div className="flex flex-col gap-5">
            <div>
              <label className="block text-sm font-medium text-text-primary mb-1.5">
                Username
              </label>
              <input
                type="text"
                name="username"
                placeholder="Enter your username"
                autoComplete="off"
                autoCorrect="off"
                autoCapitalize="off"
                spellCheck={false}
                className="w-full bg-background border border-border rounded-xl px-4 py-3 text-[15px] text-text-primary placeholder:text-text-secondary outline-none focus:border-accent focus:ring-1 focus:ring-accent transition-all duration-200"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-text-primary mb-1.5">
                Password
              </label>
              <input
                type="password"
                name="password"
                placeholder="Enter your password"
                autoComplete="new-password"
                autoCorrect="off"
                autoCapitalize="off"
                spellCheck={false}
                className="w-full bg-background border border-border rounded-xl px-4 py-3 text-[15px] text-text-primary placeholder:text-text-secondary outline-none focus:border-accent focus:ring-1 focus:ring-accent transition-all duration-200"
              />
            </div>

            {loginError && (
              <p className="text-danger text-sm font-medium">{loginError}</p>
            )}

            <button
              type="submit"
              className="w-full bg-accent text-white font-bold py-3 rounded-xl hover:bg-accent-hover transition-colors duration-200 text-[15px] mt-1 cursor-pointer"
            >
              {isRegister ? "Create account" : "Sign in"}
            </button>
          </div>
        </form>

        <p
          onClick={() => {
            setIsRegister(!isRegister);
            setLoginError("");
          }}
          className="text-sm text-center text-accent cursor-pointer hover:underline mt-6"
        >
          {isRegister
            ? "Already have an account? Sign in"
            : "Don't have an account? Sign up"}
        </p>
      </div>
    </div>
  );
}
