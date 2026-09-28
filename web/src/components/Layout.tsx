import { Link, NavLink, Outlet } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Layout() {
  const { token, utilisateur, deconnexion } = useAuth()
  return <div className="application">
    <header className="barre">
      <Link to="/" className="marque"><span className="marque-symbole">✳</span><span>ChipsUI<br /><small>CHIPS COLLECTION</small></span></Link>
      <nav className="navigation" aria-label="Navigation principale">
        <NavLink to="/" end>Catalogue</NavLink>
        {token && <><NavLink to="/collection">Ma collection</NavLink><NavLink to="/stats">Statistiques</NavLink></>}
      </nav>
      <div className="actions">
        {token ? <><span className="profil">{utilisateur?.email}</span><button className="bouton bouton-discret" onClick={deconnexion}>Quitter</button></> : <><Link className="lien-connexion" to="/login">Se connecter</Link><Link className="bouton bouton-primaire" to="/register">S'inscrire</Link></>}
      </div>
    </header>
    <main className="contenu"><Outlet /></main>
    <footer className="pied"><span>CHIPSUI / MA COLLECTION</span><span>Une collection bien assaisonnée.</span></footer>
  </div>
}
