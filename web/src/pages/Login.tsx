import { useState, type FormEvent } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Login() {
  const { connexion, erreur } = useAuth(); const naviguer = useNavigate(); const emplacement = useLocation()
  const [email, definirEmail] = useState(''); const [motDePasse, definirMotDePasse] = useState(''); const [envoi, definirEnvoi] = useState(false)
  const soumettre = async (evenement: FormEvent) => { evenement.preventDefault(); definirEnvoi(true); try { await connexion(email, motDePasse); naviguer(emplacement.state?.destination ?? '/') } catch { /* erreur affichée par le contexte */ } finally { definirEnvoi(false) } }
  return <section className="auth-page"><div className="auth-intro"><span className="surtitre">BIENVENUE CHEZ CHIPSUI</span><h1>Retrouvez votre sélection.</h1><p>Votre étagère personnelle, vos envies du moment, vos prochaines découvertes.</p></div><form className="formulaire" onSubmit={soumettre}><span className="surtitre">CONNEXION</span><h2>Ouvrir sa collection</h2><label>Email<input type="email" value={email} onChange={e => definirEmail(e.target.value)} required /></label><label>Mot de passe<input type="password" value={motDePasse} onChange={e => definirMotDePasse(e.target.value)} required /></label>{erreur && <p className="message-erreur">{erreur}</p>}<button className="bouton bouton-primaire bouton-large" disabled={envoi}>{envoi ? 'Connexion...' : 'Se connecter'}</button><p className="aide-formulaire">Pas encore de compte ? <Link to="/register">Créer un compte</Link></p></form></section>
}
