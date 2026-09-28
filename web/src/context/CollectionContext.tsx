/* eslint-disable react-refresh/only-export-components */
import { createContext, useContext, useState, type ReactNode } from 'react'
import type { CollectionEntry } from '../types/api'

interface CollectionContextValue {
  collection: CollectionEntry[]
  definirCollection: (collection: CollectionEntry[]) => void
}

const CollectionContext = createContext<CollectionContextValue | undefined>(undefined)

export function CollectionProvider({ children }: { children: ReactNode }) {
  const [collection, definirCollection] = useState<CollectionEntry[]>([])

  return <CollectionContext.Provider value={{ collection, definirCollection }}>{children}</CollectionContext.Provider>
}

export function useCollection(): CollectionContextValue {
  const contexte = useContext(CollectionContext)
  if (!contexte) throw new Error('useCollection doit être utilisé dans CollectionProvider')
  return contexte
}
