import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function ProtectedRoute() {
  const { token, chargement } = useAuth();
  const emplacement = useLocation();
  if (chargement)
    return (
      <main className="etat-page">
        <p>Vérification de la session...</p>
      </main>
    );
  if (token) return <Outlet />;

  const destination = `${emplacement.pathname}${emplacement.search}${emplacement.hash}`;
  return (
    <Navigate
      to="/login"
      replace
      state={{
        destination,
        message:
          "Connectez-vous pour continuer.",
      }}
    />
  );
}
