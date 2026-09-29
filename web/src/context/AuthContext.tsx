/* eslint-disable react-refresh/only-export-components */
import { createContext, useContext, useEffect, useState, type ReactNode } from 'react'
import type { User } from '../types/api'
import { api, ErreurApi } from '../services/api'
import { useLocalStorage } from '../hooks/useLocalStorage'

interface AuthContextValue {
	token: string | null
	utilisateur: User | null
	chargement: boolean
	erreur: string | null
	connexion: (email: string, motDePasse: string) => Promise<void>
	inscription: (email: string, motDePasse: string) => Promise<void>
	deconnexion: () => void
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
	const [token, definirToken] = useLocalStorage<string | null>('token', null)
	const [utilisateur, definirUtilisateur] = useState<User | null>(null)
	const [chargement, definirChargement] = useState(Boolean(token))
	const [erreur, definirErreur] = useState<string | null>(null)

	useEffect(() => {
		if (!token) return
		let verificationActive = true
		const tokenVerifie = token
		api.utilisateurCourant().then(utilisateur => {
			if (verificationActive) definirUtilisateur(utilisateur)
		}).catch(() => {
			if (verificationActive && window.localStorage.getItem('token') === JSON.stringify(tokenVerifie)) {
				definirToken(null); definirUtilisateur(null)
			}
		}).finally(() => {
			if (verificationActive) definirChargement(false)
		})
		return () => { verificationActive = false }
	}, [token, definirToken])

	const connexion = async (email: string, motDePasse: string) => {
		definirErreur(null)
		try {
			const resultat = await api.connecter({ email, password: motDePasse })
			definirToken(resultat.access_token)
			definirUtilisateur(await api.utilisateurCourant())
		} catch (cause) { definirErreur(cause instanceof ErreurApi ? cause.message : 'Connexion impossible.'); throw cause }
	}

	const inscription = async (email: string, motDePasse: string) => {
		definirErreur(null)
		try { await api.inscrire({ email, password: motDePasse }); await connexion(email, motDePasse) }
		catch (cause) { definirErreur(cause instanceof ErreurApi ? cause.message : 'Inscription impossible.'); throw cause }
	}

	const deconnexion = () => { definirToken(null); definirUtilisateur(null) }
	return <AuthContext.Provider value={{ token, utilisateur, chargement, erreur, connexion, inscription, deconnexion }}>{children}</AuthContext.Provider>
}

export function useAuth(): AuthContextValue {
	const contexte = useContext(AuthContext)
	if (!contexte) throw new Error('useAuth doit être utilisé dans AuthProvider')
	return contexte
}
