import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { api, ErreurApi } from "../services/api";
import type { Item } from "../types/api";
import { useAuth } from "../context/AuthContext";

export default function ItemDetail() {
  const { token } = useAuth();
  const naviguer = useNavigate();
  const { itemId } = useParams();
  const [item, definirItem] = useState<Item | null>(null);
  const [erreur, definirErreur] = useState<string | null>(null);
  const [message, definirMessage] = useState<string | null>(null);
  const [erreurAjout, definirErreurAjout] = useState<string | null>(null);
  const [ajoutEnCours, definirAjoutEnCours] = useState(false);
  useEffect(() => {
    if (itemId)
      api
        .item(Number(itemId))
        .then(definirItem)
        .catch((cause) =>
          definirErreur(
            cause instanceof ErreurApi ? cause.message : "Fiche indisponible.",
          ),
        );
  }, [itemId]);

  const ajouter = async () => {
    if (!item) return;
    if (!token) {
      naviguer("/login", { state: { destination: `/items/${item.id}` } });
      return;
    }

    definirAjoutEnCours(true);
    definirMessage(null);
    definirErreurAjout(null);
    try {
      await api.ajouterCollection({ item_id: item.id, statut: "a_decouvrir" });
      definirMessage("Cet élément a rejoint votre collection.");
    } catch (cause) {
      definirErreurAjout(
        cause instanceof ErreurApi ? cause.message : "Ajout impossible.",
      );
    } finally {
      definirAjoutEnCours(false);
    }
  };
  if (erreur)
    return (
      <main className="etat-page">
        <p className="message-erreur">{erreur}</p>
        <Link to="/" className="bouton bouton-secondaire">
          Retour au catalogue
        </Link>
      </main>
    );
  if (!item)
    return (
      <main className="etat-page">
        <p>On ouvre la fiche...</p>
      </main>
    );
  return (
    <section className="detail-item">
      <Link to="/" className="lien-texte">
        ← Retour au catalogue
      </Link>
      <div className="detail-corps">
        <div className="item-image item-image--detail">
          {item.image_url ? <img src={item.image_url} alt={item.titre} /> : "✳"}
        </div>
        <div>
          <span className="etiquette">{item.categorie}</span>
          <h1>{item.titre}</h1>
          <span className="annee">{item.annee}</span>
          <p>{item.description}</p>
          <button
            className="bouton bouton-primaire"
            onClick={ajouter}
            disabled={ajoutEnCours}
          >
            {ajoutEnCours ? "Ajout..." : "Ajouter à ma collection"}
          </button>
          {message && <p className="message-succes">{message}</p>}
          {erreurAjout && <p className="message-erreur">{erreurAjout}</p>}
        </div>
      </div>
    </section>
  );
}
