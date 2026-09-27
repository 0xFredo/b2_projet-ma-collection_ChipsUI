import { useEffect, useState } from 'react'

export function useDebounce<T>(valeur: T, delai: number): T {
  const [valeurDebitee, setValeurDebitee] = useState(valeur)

  useEffect(() => {
    const identifiant = window.setTimeout(() => setValeurDebitee(valeur), delai)
    return () => window.clearTimeout(identifiant)
  }, [valeur, delai])

  return valeurDebitee
}
