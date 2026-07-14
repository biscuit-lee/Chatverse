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
    <div className="flex-1 ml-97 p-8 w-1/2 flex items-center justify-center min-h-screen">
      <form onSubmit={handleSubmit} className="flex flex-col gap-4 w-80">
        <h1 className="text-2xl font-bold text-center">
          {isRegister ? "Create Account" : "Login"}
        </h1>

        <input
          type="text"
          name="username"
          placeholder="Username"
          autoComplete="off"
          autoCorrect="off"
          autoCapitalize="off"
          spellCheck={false}
          className="border rounded-lg px-4 py-2 outline-none focus:ring-2 focus:ring-blue-300"
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          autoComplete="new-password"
          autoCorrect="off"
          autoCapitalize="off"
          spellCheck={false}
          className="border rounded-lg px-4 py-2 outline-none focus:ring-2 focus:ring-blue-300"
        />

        {loginError && <p className="text-red-500 text-sm">{loginError}</p>}

        <button className="bg-blue-500 text-white rounded-lg py-2 hover:bg-blue-600 transition-colors">
          {isRegister ? "Register" : "Login"}
        </button>

        <p
          onClick={() => setIsRegister(!isRegister)}
          className="text-sm text-center text-blue-500 cursor-pointer hover:underline"
        >
          {isRegister
            ? "Already have an account? Login"
            : "Don't have an account? Register"}
        </p>
      </form>
    </div>
  );
}
