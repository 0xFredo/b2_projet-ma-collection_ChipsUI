# ADR 0002 — Utilisation de Tailwind pour le formattage du site

## Statut

Refusé

## Contexte

Dans le cadre du projet (Frontend React 18 + TypeScript avec Vite), les contraintes techniques imposent de créer une interface soignée, responsive (lisible en largeur 375 px minimum) et d'interdire les librairies de composants UI prêts à l'emploi (telles que MUI, Chakra UI ou Bootstrap). Le sujet laissait néanmoins le choix entre **CSS pur**, **CSS Modules** ou **Tailwind CSS** pour la mise en forme.

Il était nécessaire de trancher sur la stratégie de stylisation afin d'assurer la cohérence visuelle de l'application et la facilité de maintenance du code par l'équipe.

## Décision

Nous avons décidé d'utiliser du ***CSS pur*** (avec d'éventuels fichiers .css structurés par composants ou variables globales) et d'écarter l'utilisation de Tailwind CSS.

Raisons du choix :
- Maîtrise et contrôle total du CSS : Le CSS pur permet un contrôle direct et granulaire sur chaque propriété, évitant l'abstraction ou la surcharge imposée par les classes utilitaires.
- Absence de dépendances et de configuration supplémentaires : Évite d'ajouter Tailwind CSS ainsi que ses outils de build (PostCSS, Autoprefixer, etc.) au projet Vite, simplifiant ainsi la configuration du bundler et les dépendances npm.
- Identité visuelle unique et personnalisée : Cela encourage la création d'un design sur-mesure plus personnel sans tomber dans le design typique généré par défaut par Tailwind.
- Apprentissage et consolidation des bases : Renforce la maîtrise du CSS natif (Flexbox, Grid, variables CSS, Media Queries pour le responsive à 375 px).

## Conséquences

|                Positives                |               Négatives               |
| --------------------------------------- | ------------------------------------- |
| Contrôle total sur le formatage du site | Fichier CSS de plus de 650 lignes     |
| Présentation plus personnelle           | Long à réaliser                       |
| Utilisation facile de variables natives | Répétition du code CSS à surveiller   |
| Bundle plus léger au niveau de Vite     | Risque de conflits de noms de classes |