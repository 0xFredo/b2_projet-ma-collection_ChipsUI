import { Link } from "react-router-dom";

export default function NotFound() {
  return (
    <section className="page-standard">
      <span className="surtitre">ERREUR 404</span>
      <h1>Cette page s&apos;est perdue.</h1>
      <p className="sous-titre">
        Oups, cette page est tombée du sachet.
      </p>
      <Link className="bouton bouton-primaire" to="/">
        Retour au catalogue
      </Link>
    </section>
  );
}
