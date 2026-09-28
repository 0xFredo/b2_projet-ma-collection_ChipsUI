import type {
	ApiErrorResponse, AuthResponse, CollectionEntry, CreateEntryPayload, Item, PaginatedItems, StatsResponse, UpdateEntryPayload, User,
} from '../types/api'

const BASE_URL = 'http://localhost:8000'

export class ErreurApi extends Error {
	code: number

	constructor(message: string, code = 500) {
		super(message)
		this.name = 'ErreurApi'
		this.code = code
	}
}

function estErreurApi(valeur: unknown): valeur is ApiErrorResponse {
	if (typeof valeur !== 'object' || valeur === null || !('erreur' in valeur)) return false
	const erreur = valeur.erreur
	return typeof erreur === 'object' && erreur !== null && 'message' in erreur && typeof erreur.message === 'string'
}

async function requete<T>(chemin: string, options: RequestInit = {}): Promise<T> {
	const token = window.localStorage.getItem('token')
	const entetes = new Headers(options.headers)
	entetes.set('Content-Type', 'application/json')
	if (token) entetes.set('Authorization', `Bearer ${token}`)

	const reponse = await fetch(`${BASE_URL}${chemin}`, { ...options, headers: entetes })
	if (reponse.status === 204) return undefined as T
	const corps: unknown = await reponse.json().catch(() => undefined)
	if (!reponse.ok) {
		if (estErreurApi(corps)) throw new ErreurApi(corps.erreur.message, corps.erreur.code)
		throw new ErreurApi('Une erreur est survenue.', reponse.status)
	}
	return corps as T
}

export const api = {
	inscrire: (donnees: { email: string; password: string }) => requete<User>('/auth/register', { method: 'POST', body: JSON.stringify(donnees) }),
	connecter: (donnees: { email: string; password: string }) => requete<AuthResponse>('/auth/login', { method: 'POST', body: JSON.stringify(donnees) }),
	utilisateurCourant: () => requete<User>('/auth/me'),
	listerItems: (parametres: { q?: string; categorie?: string; page?: number; limit?: number }) => {
		const recherche = new URLSearchParams()
		Object.entries(parametres).forEach(([cle, valeur]) => valeur !== undefined && recherche.set(cle, String(valeur)))
		return requete<PaginatedItems>(`/items?${recherche.toString()}`)
	},
	item: (id: number) => requete<Item>(`/items/${id}`),
	listerCollection: (statut?: string, tri?: string) => {
		const recherche = new URLSearchParams()
		if (statut) recherche.set('statut', statut)
		if (tri) recherche.set('tri', tri)
		return requete<CollectionEntry[]>(`/me/collection?${recherche.toString()}`)
	},
	ajouterCollection: (donnees: CreateEntryPayload) => requete<CollectionEntry>('/me/collection', { method: 'POST', body: JSON.stringify(donnees) }),
	modifierCollection: (id: number, donnees: UpdateEntryPayload) => requete<CollectionEntry>(`/me/collection/${id}`, { method: 'PATCH', body: JSON.stringify(donnees) }),
	supprimerCollection: (id: number) => requete<void>(`/me/collection/${id}`, { method: 'DELETE' }),
	statistiques: () => requete<StatsResponse>('/me/stats'),
}
