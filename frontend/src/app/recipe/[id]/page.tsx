// frontend/src/app/recipe/[id]/page.tsx

import { Recipe } from "@/types";

// This async function fetches a single recipe by its ID
async function getRecipeById(id: string): Promise<Recipe> {
  const res = await fetch(`http://127.0.0.1:8000/recipes/${id}`, { cache: 'no-store' });
  if (!res.ok) {
    throw new Error('Failed to fetch recipe');
  }
  return res.json();
}

// This is the component for the detail page
// It receives 'params' which contains the dynamic route parameters (e.g., { id: '1' })
export default async function RecipeDetailPage({ params }: { params: { id: string } }) {
  const recipe = await getRecipeById(params.id);

  return (
    <article className="max-w-4xl mx-auto p-4 sm:p-8">
      <h1 className="text-4xl font-extrabold text-gray-900 mb-2">{recipe.title}</h1>
      <p className="text-lg text-gray-600 mb-6">by {recipe.author.username}</p>

      <div className="prose lg:prose-xl">
        <p>{recipe.description}</p>
      </div>

      {/* We can add ingredients and instructions here later */}
    </article>
  );
}