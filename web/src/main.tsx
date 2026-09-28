/* Enveloppement de l'application dans les Contexts (AuthContext, CollectionContext) et le routeur (BrowserRouter). */

import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './styles.css'
import Routes from './routes.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Routes />
  </StrictMode>,
)