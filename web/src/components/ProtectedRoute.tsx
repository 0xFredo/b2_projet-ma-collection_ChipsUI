import { Navigate, Outlet } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function ProtectedRoute() {
	const { token, chargement } = useAuth()
	if (chargement) return <main className="etat-page"><p>Vérification de la session...</p></main>
	return token ? <Outlet /> : <Navigate to="/login" replace />
}
