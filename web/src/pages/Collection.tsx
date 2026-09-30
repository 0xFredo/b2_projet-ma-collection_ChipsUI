import { useCallback, useEffect, useState } from "react";
import { api, ErreurApi } from "../services/api";
import type { CollectionEntry, Statut } from "../types/api";

const libelles: Record<Statut, string> = {
  a_decouvrir: "À découvrir",
  en_cours: "En cours",
  termine: "Terminées",
};
export default function Collection() {
  const [entrees, definirEntrees] = useState<CollectionEntry[]>([]);
  const [statut, definirStatut] = useState("");
  const [tri, definirTri] = useState("date");
  const [chargement, definirChargement] = useState(true);
  const [erreur, definirErreur] = useState<string | null>(null);
  const charger = useCallback(() => {
    void Promise.resolve()
      .then(() => {
        definirChargement(true);
        return api.listerCollection(statut || undefined, tri);
      })
      .then(definirEntrees)
      .catch((cause) =>
        definirErreur(
          cause instanceof ErreurApi
            ? cause.message
            : "Collection indisponible.",
        ),
      )
      .finally(() => definirChargement(false));
  }, [statut, tri]);
  useEffect(() => {
    charger();
  }, [charger]);
  const supprimer = async (id: number) => {
    try {
      await api.supprimerCollection(id);
      definirEntrees(entrees.filter((entree) => entree.id !== id));
    } catch (cause) {
      definirErreur(
        cause instanceof ErreurApi ? cause.message : "Suppression impossible.",
      );
    }
  };
  const modifier = async (
    entree: CollectionEntry,
    nouveauStatut: Statut,
    nouvelleNote: number | null,
  ) => {
    try {
      const miseAJour = await api.modifierCollection(entree.id, {
        statut: nouveauStatut,
        ...(nouvelleNote ? { note: nouvelleNote } : {}),
      });
      definirEntrees(
        entrees.map((element) =>
          element.id === entree.id ? miseAJour : element,
        ),
      );
    } catch (cause) {
      definirErreur(
        cause instanceof ErreurApi ? cause.message : "Modification impossible.",
      );
    }
  };
  return (
    <section className="page-standard">
      <div className="section-entete">
        <div>
          <span className="surtitre">MON ESPACE</span>
          <h1>
            Ma collection<span className="point">.</span>
          </h1>
          <p className="sous-titre">
            Vos découvertes, vos envies, votre rythme.
          </p>
        </div>
        <div className="compteur">
          <strong>{entrees.length}</strong>
          <span>
            paquets
            <br />
            conservés
          </span>
        </div>
      </div>
      <div className="filtres">
        <select value={statut} onChange={(e) => definirStatut(e.target.value)}>
          <option value="">Tous les statuts</option>
          {Object.entries(libelles).map(([cle, valeur]) => (
            <option key={cle} value={cle}>
              {valeur}
            </option>
          ))}
        </select>
        <select value={tri} onChange={(e) => definirTri(e.target.value)}>
          <option value="date">Plus récentes</option>
          <option value="note">Mieux notées</option>
        </select>
      </div>
      {chargement ? (
        <div className="etat-page">
          <p>On trie vos paquets...</p>
        </div>
      ) : erreur ? (
        <div className="etat-page">
          <p className="message-erreur">{erreur}</p>
          <button className="bouton bouton-secondaire" onClick={charger}>
            Réessayer
          </button>
        </div>
      ) : !entrees.length ? (
        <div className="etat-page vide-collection">
          <span>✳</span>
          <h2>Votre collection est encore vide.</h2>
          <p>Parcourez le catalogue et gardez les chips qui vous font envie.</p>
        </div>
      ) : (
        <div className="liste-collection">
          {entrees.map((entree) => (
            <article className="ligne-collection" key={entree.id}>
              <div className="item-image item-image--mini">
                {entree.item.image_url ? (
                  <img src={entree.item.image_url} alt="" />
                ) : (
                  "✳"
                )}
              </div>
              <div className="ligne-infos">
                <span className="etiquette">{libelles[entree.statut]}</span>
                <h2>{entree.item.titre}</h2>
                <p>
                  {entree.commentaire || "Aucun commentaire pour le moment."}
                </p>
                <select
                  value={entree.statut}
                  onChange={(e) =>
                    modifier(
                      entree,
                      e.target.value as Statut,
                      entree.note ?? null,
                    )
                  }
                >
                  <option value="a_decouvrir">À découvrir</option>
                  <option value="en_cours">En cours</option>
                  <option value="termine">Terminée</option>
                </select>
              </div>
              <div className="ligne-note">
                {entree.note
                  ? `${"★".repeat(entree.note)}${"☆".repeat(5 - entree.note)}`
                  : "Non notée"}
                <select
                  aria-label="Note"
                  value={entree.note ?? ""}
                  onChange={(e) =>
                    modifier(
                      entree,
                      entree.statut,
                      e.target.value ? Number(e.target.value) : null,
                    )
                  }
                >
                  <option value="">Noter</option>
                  {[1, 2, 3, 4, 5].map((note) => (
                    <option key={note} value={note}>
                      {note} / 5
                    </option>
                  ))}
                </select>
                <button
                  className="bouton bouton-danger"
                  onClick={() => supprimer(entree.id)}
                >
                  Supprimer
                </button>
              </div>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}
