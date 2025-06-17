// frontend/src/app/add-recipe/page.tsx

"use client";

import { useState, FormEvent, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";

export default function AddRecipePage() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState<string | null>(null);
  
  // Get auth state and router from our hooks
  const { isAuthenticated, isLoading, token } = useAuth();
  const router = useRouter();

  // This effect protects the route on the client-side
  useEffect(() => {
    // If the context is done loading and the user is not authenticated, redirect them
    if (!isLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isLoading, isAuthenticated, router]);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);

    // Don't submit if we don't have a token
    if (!token) {
      setError("You must be logged in to create a recipe.");
      return;
    }

    try {
      const res = await fetch('http://127.0.0.1:8000/recipes/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // This is the crucial part: sending our auth token to the backend
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ title, description }),
      });

      if (!res.ok) {
        const errorData = await res.json();
        // Use the error detail from the backend if available
        throw new Error(errorData.detail || 'Failed to submit recipe');
      }
      
      // On successful creation, show a confirmation and redirect
      alert('Recipe created successfully!');
      router.push('/'); // Redirect to the home page feed

    } catch (error) {
      if (error instanceof Error) {
        setError(error.message);
      } else {
        setError('An unexpected error occurred');
      }
    }
  };

  // While the auth context is loading, we can show a placeholder to prevent flicker
  if (isLoading) {
    return <p className="text-center mt-10">Loading...</p>;
  }
  
  // If we've finished loading and the user is NOT authenticated, render nothing.
  // The useEffect hook above will handle redirecting them away.
  if (!isAuthenticated) {
    return null; 
  }

  // If authenticated, show the form
  return (
    <div className="flex justify-center items-center mt-10">
      <form onSubmit={handleSubmit} className="bg-white p-8 rounded-lg shadow-md w-full max-w-2xl">
        <h1 className="text-2xl font-bold mb-6 text-center">Add a New Recipe</h1>
        
        {error && <p className="text-red-500 text-center mb-4">{error}</p>}
        
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="title">
            Recipe Title
          </label>
          <input
            id="title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            required
          />
        </div>
        
        <div className="mb-6">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="description">
            Description
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 h-32 leading-tight focus:outline-none focus:shadow-outline"
          />
        </div>

        <div className="flex items-center justify-center">
          <button
            type="submit"
            className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full"
          >
            Submit Recipe
          </button>
        </div>
      </form>
    </div>
  );
}