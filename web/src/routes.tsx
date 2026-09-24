/* Système de routes avec React Router (ex: les routes /, /collection, /stats, /login, etc.) comme demandé dans le sujet. */

import './styles.css'

import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

import Login from './pages/Login';
import Register from './pages/Register';
import Catalog from './pages/Catalog';
import Collection from './pages/Collection';
import Stats from './pages/Stats';
import ProtectedRoute from './components/ProtectedRoute';

export default function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<h1>Catalogue</h1>} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
