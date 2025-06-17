// frontend/app/page.tsx

export const dynamic = 'force-dynamic';
import Link from 'next/link'; // 1. Import the Link component
import { Recipe } from "@/types"; // Import our new Recipe type

// This async function fetches the data from our FastAPI backend
async function getRecipes(): Promise<Recipe[]> {
  // We fetch data from the GET /recipes endpoint
  const res = await fetch('http://127.0.0.1:8000/recipes/', { cache: 'no-store' });

  // Recommendation: handle errors
  if (!res.ok) {
    // This will activate the closest `error.js` Error Boundary
    throw new Error('Failed to fetch data');
  }

  return res.json();
}

// The main page component is now an async function
export default async function HomePage() {
  const recipes = await getRecipes();

  return (
    <main className="p-4 sm:p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl sm:text-4xl font-bold text-gray-800">Recipe Feed</h1>
        <Link href="/signup" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          Sign Up
        </Link>
      </div>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {recipes.map((recipe) => (
          // We use the recipe's id as the key for each element in the list
          <Link href={`/recipe/${recipe.id}`} key={recipe.id}>
            <div className="border rounded-lg p-4 shadow-sm bg-white h-full hover:shadow-md transition-shadow duration-200 cursor-pointer">
              <h2 className="text-xl font-semibold text-gray-900 mb-2">{recipe.title}</h2>
              <p className="text-gray-600 mb-3">{recipe.description}</p>
              <p className="text-sm text-gray-500">by {recipe.author.username}</p>
            </div>
          </Link>
        ))}
      </div>
    </main>
  );
}