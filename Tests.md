### **1. Test du flux d'Authentification (`/auth`)** ✅

1. **`POST /auth/register`** : Crée un compte utilisateur (ex: `test@example.com` / `password123`) $\rightarrow$ Vérifie la réponse **`201 Created`**. ✅
    
2. **`POST /auth/register`** (Doublon) : Re-teste avec le même email $\rightarrow$ Vérifie que tu obtiens bien une erreur **`409 Conflict`**. ✅
    
3. **Se connecter via Swagger** : Clique sur le bouton vert **Authorize** en haut à droite, entre ton email et ton mot de passe, puis valide. ✅
    
4. **`GET /auth/me`** : Exécute la route $\rightarrow$ Vérifie la réponse **`200 OK`** avec l'ID et l'email. ✅
    

### **2. Test du Catalogue Public (`/items`)** ✅

1. **`GET /items`** : Exécute sans paramètre $\rightarrow$ Vérifie que le JSON renvoie la structure `{ "total": ..., "page": 1, "limit": 12, "results": [...] }`. ✅
    
2. **`GET /items` avec filtres** : ✅
    
    - Teste le filtre `categorie`.
        
    - Teste la recherche `q` avec une lettre/mot présent dans le titre de ton item de test.
        
3. **`GET /items/1`** : Récupère l'item par son ID $\rightarrow$ Vérifie le statut **`200 OK`**. ✅
    
4. **`GET /items/999`** : Teste avec un ID inexistant $\rightarrow$ Vérifie le statut **`404 Not Found`** et le format d'erreur maison `{"erreur": {"code": 404, "message": "..."}}`. ✅
    

### **3. Test de la Collection Personnelle (`/me`)**

1. **`POST /me/collection`** : Ajoute l'item `1` dans ta collection avec :
    
    JSON
    
    ```
    {
      "item_id": 1,
      "statut": "en_cours",
      "note": 4,
      "commentaire": "Super début !"
    }
    ```
    
    $\rightarrow$ Vérifie le statut **`201 Created`** et que l'objet `item` est bien imbriqué dans la réponse. ✅
    
1. **`POST /me/collection`** (Doublon) : Essaie d'ajouter une deuxième fois l'item `1` $\rightarrow$ Vérifie le retour **`409 Conflict`**. ✅
    
2. **`GET /me/collection`** : Exécute pour voir la liste de tes entrées.
    
3. **`PATCH /me/collection/1`** : Modifie le statut en `"termine"` et la note à `5` $\rightarrow$ Vérifie le statut **`200 OK`**.
    
4. **`GET /me/stats`** : Exécute la route $\rightarrow$ Vérifie le format de la réponse avec la clé **`par_statut`** :
    
    JSON
    
    ````
    {
      "total": 1,
      "par_statut": {
        "a_decouvrir": 0,
        "en_cours": 0,
        "termine": 1
      },
      "note_moyenne": 5.0
    }
    ```[cite: 7]
    ````
    
5. **`DELETE /me/collection/1`** : Supprime l'entrée $\rightarrow$ Vérifie le code **`204 No Content`**