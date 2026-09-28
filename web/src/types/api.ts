// 1. Union littérale obligatoire pour le statut
export type Statut = "a_decouvrir" | "en_cours" | "termine";

// 2. Types Utilisateur & Auth
export interface User {
  id: number;
  email: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

// 3. Type Item (Catalogue)
// Adapte les champs specifiques a ton univers si besoin (ex: studio, plateforme...)
export interface Item {
  id: number;
  titre: string;
  categorie: string;
  description: string;
  annee: number;
  image_url: string;
  [key: string]: unknown; // Pour accepter d'autres champs specifiques sans utiliser 'any'
}

// 4. Reponse paginée pour le catalogue
export interface PaginatedItems {
  total: number;
  page: number;
  limit: number;
  results: Item[];
}

// 5. Type Entry (Collection personnelle avec Item imbriqué)
export interface CollectionEntry {
  id: number;
  statut: Statut;
  note?: number | null;
  commentaire?: string | null;
  date_ajout: string;
  item: Item;
}

// 6. DTOs pour les requêtes (Payloads)
export interface CreateEntryPayload {
  item_id: number;
  statut: Statut;
  note?: number;
  commentaire?: string;
}

export interface UpdateEntryPayload {
  statut?: Statut;
  note?: number;
  commentaire?: string;
}

// 7. Statistiques
export interface StatsResponse {
  total: number;
  par_statut: Record<Statut, number>;
  note_moyenne: number | null;
}

// 8. Format d'erreur imposé par l'API
export interface ApiErrorDetail {
  code: number;
  message: string;
}

export interface ApiErrorResponse {
  erreur: ApiErrorDetail;
}