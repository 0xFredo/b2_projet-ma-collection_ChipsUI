import { useCallback, useState } from 'react'

export function useLocalStorage<T>(cle: string, valeurInitiale: T): [T, (valeur: T) => void] {
	const [valeur, definirValeur] = useState<T>(() => {
		const stockee = window.localStorage.getItem(cle)
		if (!stockee) return valeurInitiale
		try {
			return JSON.parse(stockee) as T
		} catch {
			return valeurInitiale
		}
	})

	const enregistrer = useCallback((nouvelleValeur: T) => {
		definirValeur(nouvelleValeur)
		window.localStorage.setItem(cle, JSON.stringify(nouvelleValeur))
	}, [cle])

	return [valeur, enregistrer]
}
