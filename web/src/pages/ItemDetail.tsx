import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { api, ErreurApi } from '../services/api'
import type { Item } from '../types/api'

export default function ItemDetail() {
  const { itemId } = useParams(); const [item, definirItem] = useState<Item | null>(null); const [erreur, definirErreur] = useState<string | null>(null)
  useEffect(() => { if (itemId) api.item(Number(itemId)).then(definirItem).catch(cause => definirErreur(cause instanceof ErreurApi ? cause.message : 'Fiche indisponible.')) }, [itemId])
  if (erreur) return <main className="etat-page"><p className="message-erreur">{erreur}</p><Link to="/" className="bouton bouton-secondaire">Retour au catalogue</Link></main>
  if (!item) return <main className="etat-page"><p>On ouvre la fiche...</p></main>
  return <section className="detail-item"><Link to="/" className="lien-texte">← Retour au catalogue</Link><div className="detail-corps"><div className="detail-image">{item.image_url ? <img src={item.image_url} alt={item.titre} /> : '✳'}</div><div><span className="etiquette">{item.categorie}</span><h1>{item.titre}</h1><span className="annee">{item.annee}</span><p>{item.description}</p><button className="bouton bouton-primaire">Ajouter à ma collection</button></div></div></section>
}
