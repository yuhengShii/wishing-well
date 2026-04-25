export interface Wish {
  id: number;
  title: string;
  description?: string;
  category?: string;
  priority: number;
  status: WishStatus;
  vote_count: number;
  contact?: string;
  created_at: string;
  updated_at?: string;
}

export type WishStatus = "pending" | "approved" | "implemented" | "rejected";

export interface WishForm {
  title: string;
  description?: string;
  category?: string;
  contact?: string;
}

export interface WishFilters {
  category?: string;
  status?: WishStatus;
}
