import { useEffect, useState } from "react";
import { api, ErreurApi } from "../services/api";
import type { StatsResponse, Statut } from "../types/api";

const libelles: Record<Statut, string> = {
  a_decouvrir: "À découvrir",
  en_cours: "En cours",
  termine: "Terminées",
};
export default function Stats() {
  const [stats, definirStats] = useState<StatsResponse | null>(null);
  const [chargement, definirChargement] = useState(true);
  const [erreur, definirErreur] = useState<string | null>(null);
  useEffect(() => {
    api
      .statistiques()
      .then(definirStats)
      .catch((cause) =>
        definirErreur(
          cause instanceof ErreurApi
            ? cause.message
            : "Statistiques indisponibles.",
        ),
      )
      .finally(() => definirChargement(false));
  }, []);
  if (chargement)
    return (
      <main className="etat-page">
        <p>On compte les paquets...</p>
      </main>
    );
  if (erreur || !stats)
    return (
      <main className="etat-page">
        <p className="message-erreur">
          {erreur ?? "Aucune statistique disponible."}
        </p>
      </main>
    );
  return (
    <section className="page-standard">
      <span className="surtitre">VOTRE ANNÉE EN CHIPS</span>
      <h1>
        Les chiffres<span className="point">.</span>
      </h1>
      <p className="sous-titre">
        Une vue simple de vos habitudes de dégustation.
      </p>
      <div className="stats-grille">
        <article className="stat-principale">
          <span className="surtitre">TOTAL COLLECTION</span>
          <strong>{stats.total}</strong>
          <p>références dans votre collection</p>
        </article>
        <article className="stat-principale accent-jaune">
          <span className="surtitre">NOTE MOYENNE</span>
          <strong>
            {stats.note_moyenne?.toFixed(1) ?? "—"}
            <small>/ 5</small>
          </strong>
          <p>sur les chips notées</p>
        </article>
      </div>
      <div className="bloc-repartition">
        <div className="section-entete">
          <h2>Répartition des envies</h2>
          <span className="etiquette">{stats.total} au total</span>
        </div>
        {Object.entries(libelles).map(([cle, valeur]) => {
          const nombre = stats.par_statut[cle as Statut] ?? 0;
          const largeur = stats.total
            ? `${(nombre / stats.total) * 100}%`
            : "0%";
          return (
            <div className="barre-stat" key={cle}>
              <div>
                <span>{valeur}</span>
                <strong>{nombre}</strong>
              </div>
              <div className="piste">
                <i style={{ width: largeur }} />
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}
