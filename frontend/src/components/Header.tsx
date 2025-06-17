// frontend/src/components/Header.tsx

"use client";

import Link from "next/link";
import { useAuth } from "@/context/AuthContext";

export default function Header() {
  // 1. Get the new 'isLoading' state from our hook
  const { isAuthenticated, isLoading, logout } = useAuth();

  return (
    <header className="bg-white shadow-md">
      <nav className="container mx-auto px-6 py-3 flex justify-between items-center">
        <Link href="/" className="text-2xl font-bold text-gray-800">
          RecipeApp
        </Link>

        <div className="flex items-center space-x-4">
          {/* 2. If it's loading, render nothing (or a spinner) to avoid the mismatch */}
          {isLoading ? (
            <div className="h-10 w-24"></div> // A placeholder to prevent layout shift
          ) : isAuthenticated ? (
            <div className="flex items-center space-x-4">
              <Link
                href="/add-recipe"
                className="text-gray-800 hover:text-blue-500"
              >
                Add Recipe
              </Link>
              <button
                onClick={logout}
                className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
              >
                Logout
              </button>
            </div>
          ) : (
            <>
              <Link href="/login" className="text-gray-800 hover:text-blue-500">
                Login
              </Link>
              <Link
                href="/signup"
                className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded ml-4"
              >
                Sign Up
              </Link>
            </>
          )}
        </div>
      </nav>
    </header>
  );
}
