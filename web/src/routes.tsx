/* Système de routes avec React Router (ex: les routes /, /collection, /stats, /login, etc.) comme demandé dans le sujet. */

import './styles.css'

import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import { AuthProvider } from './context/AuthContext';
import { CollectionProvider } from './context/CollectionContext';

import Login from './pages/Login';
import Register from './pages/Register';
import Catalog from './pages/Catalog';
import Collection from './pages/Collection';
import Stats from './pages/Stats';
import ItemDetail from './pages/ItemDetail';
import ProtectedRoute from './components/ProtectedRoute';

export default function AppRoutes() {
  return (
    <BrowserRouter>
      <AuthProvider><CollectionProvider><Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Catalog />} />
          <Route path="/items/:itemId" element={<ItemDetail />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route element={<ProtectedRoute />}>
            <Route path="/collection" element={<Collection />} />
            <Route path="/stats" element={<Stats />} />
          </Route>
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes></CollectionProvider></AuthProvider>
    </BrowserRouter>
  );
}
