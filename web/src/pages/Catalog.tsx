import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import ItemCard from "../components/ItemCard";
import { api, ErreurApi } from "../services/api";
import type { Item, PaginatedItems } from "../types/api";
import { useDebounce } from "../hooks/useDebounce";

export default function Catalog() {
  const naviguer = useNavigate();
  const [recherche, definirRecherche] = useState("");
  const rechercheDebitee = useDebounce(recherche, 400);
  const [categorie, definirCategorie] = useState("");
  const [page, definirPage] = useState(1);
  const [donnees, definirDonnees] = useState<PaginatedItems | null>(null);
  const [chargement, definirChargement] = useState(true);
  const [erreur, definirErreur] = useState<string | null>(null);
  const [ajout, definirAjout] = useState<string | null>(null);
  const [categories, definirCategories] = useState<string[]>([]);
  useEffect(() => {
    let requeteActive = true;
    void Promise.resolve()
      .then(() => {
        definirChargement(true);
        definirErreur(null);
        return api.listerItems({
          q: rechercheDebitee || undefined,
          categorie: categorie || undefined,
          page,
          limit: 12,
        });
      })
      .then((resultat) => {
        if (requeteActive) definirDonnees(resultat);
      })
      .catch((cause) =>
        requeteActive &&
        definirErreur(
          cause instanceof ErreurApi
            ? cause.message
            : "Catalogue indisponible.",
        ),
      )
      .finally(() => {
        if (requeteActive) definirChargement(false);
      });
    return () => {
      requeteActive = false;
    };
  }, [rechercheDebitee, categorie, page]);
  useEffect(() => {
    void api
      .listerItems({ page: 1, limit: 50 })
      .then((resultat) => {
        definirCategories(
          Array.from(
            new Set(resultat.results.map((item) => item.categorie)),
          ),
        );
      })
      .catch(() => undefined);
  }, []);
  const ajouter = async (item: Item) => {
    if (!window.localStorage.getItem("token")) {
      naviguer("/login");
      return;
    }
    try {
      await api.ajouterCollection({ item_id: item.id, statut: "a_decouvrir" });
      definirAjout(`${item.titre} rejoint votre collection.`);
    } catch (cause) {
      definirAjout(
        cause instanceof ErreurApi ? cause.message : "Ajout impossible.",
      );
    }
    window.setTimeout(() => definirAjout(null), 3000);
  };
  const pages = donnees ? Math.ceil(donnees.total / donnees.limit) : 0;
  return (
    <>
      <section className="hero-catalogue">
        <div>
          <span className="surtitre">LE CATALOGUE CHIPSUI</span>
          <h1>
            Une collection qui
            <br />
            <em>craque</em> sous la dent.
          </h1>
          <p>
            Explorez les pépites salées, gardez vos favorites et composez votre
            prochaine dégustation.
          </p>
        </div>
        <div className="hero-chip">
          ✳
          <small>
            CHIP
            <br />
            INDEX
          </small>
        </div>
      </section>
      <section className="catalogue-section">
        <div className="section-entete">
          <div>
            <span className="surtitre">{donnees?.total ?? "—"} RÉFÉRENCES</span>
            <h2>Les chips du moment</h2>
          </div>
          <Link className="lien-texte" to="/collection">
            Voir ma collection →
          </Link>
        </div>
        <div className="filtres">
          <label className="recherche">
            <span>⌕</span>
            <input
              placeholder="Rechercher une chips..."
              value={recherche}
              onChange={(e) => {
                definirRecherche(e.target.value);
                definirPage(1);
              }}
            />
          </label>
          <select
            value={categorie}
            onChange={(e) => {
              definirCategorie(e.target.value);
              definirPage(1);
            }}
          >
            <option value="">Toutes les catégories</option>
            {categories.map((valeur) => (
              <option key={valeur} value={valeur}>
                {valeur}
              </option>
            ))}
          </select>
        </div>
        {ajout && <p className="message-succes">{ajout}</p>}
        {chargement ? (
          <div className="etat-page">
            <p>On ouvre les paquets...</p>
          </div>
        ) : erreur ? (
          <div className="etat-page">
            <p className="message-erreur">{erreur}</p>
            <button
              className="bouton bouton-secondaire"
              onClick={() => definirPage(page)}
            >
              Réessayer
            </button>
          </div>
        ) : !donnees?.results.length ? (
          <div className="etat-page">
            <p>Aucune chips ne correspond à votre recherche.</p>
          </div>
        ) : (
          <>
            <div className="grille-items">
              {donnees.results.map((item) => (
                <ItemCard key={item.id} item={item} ajouter={ajouter} />
              ))}
            </div>
            <div className="pagination">
              <button
                className="bouton bouton-discret"
                disabled={page <= 1}
                onClick={() => definirPage(page - 1)}
              >
                ←
              </button>
              <span>
                Page {page} / {pages}
              </span>
              <button
                className="bouton bouton-discret"
                disabled={page >= pages}
                onClick={() => definirPage(page + 1)}
              >
                →
              </button>
            </div>
          </>
        )}
      </section>
    </>
  );
}
