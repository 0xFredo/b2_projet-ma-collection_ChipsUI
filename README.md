# Readme temporaire (Branche Frontend)

Suivre les étapes dans l'ordre pour lancer l'application.

---

Installer Node.js et npm (https://nodejs.org/en/download/) si ce n'est pas déjà fait.

```bash
cd web                                           # Se place dans le dossier du frontend
npm create vite@latest . -- --template react-ts  # Initialise Vite avec React et TypeScript 
npm install                                      # Installe les dependances du projet
npm install react-router-dom                     # Installe le routage des pages React
cp .env.example .env                             # Cree la configuration locale a partir du modele
npm run dev                                      # Lance le serveur de developpement Vite
```
