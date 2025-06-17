// frontend/types/index.ts
export interface Recipe {
  id: number;
  title: string;
  description: string | null;
  created_at: string; // The datetime will come in as a string
  author: {
    id: number;
    username: string;
  };
}