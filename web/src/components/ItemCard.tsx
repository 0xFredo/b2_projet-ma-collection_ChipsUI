import { Link } from "react-router-dom";
import type { Item } from "../types/api";

export default function ItemCard({
  item,
  ajouter,
}: {
  item: Item;
  ajouter?: (item: Item) => void;
}) {
  return (
    <article className="carte-item">
      <div className="item-image">
        {item.image_url ? (
          <img src={item.image_url} alt={item.titre} />
        ) : (
          <span>✳</span>
        )}
      </div>
      <div className="corps-item">
        <span className="etiquette">{item.categorie}</span>
        <h3>{item.titre}</h3>
        <p>{item.description}</p>
        <div className="meta-item">
          <span>{item.annee}</span>
          <Link to={`/items/${item.id}`}>Voir la fiche →</Link>
        </div>
        {ajouter && (
          <button
            className="bouton bouton-secondaire bouton-large"
            onClick={() => ajouter(item)}
          >
            + Ajouter à ma collection
          </button>
        )}
      </div>
    </article>
  );
}
