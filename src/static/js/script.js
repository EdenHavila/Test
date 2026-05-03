const burgerBtn = document.querySelector(".burger-menu");
const menu = document.querySelector("#vertical-menu");
const overlay = document.querySelector(".overlay");
const MenuItems = document.querySelectorAll(".menu-item");
const SubMenuItems = document.querySelectorAll(".sub-item");


const open_modal = document.querySelector(".new_request");
const modal = document.querySelector("#myModal");
const close_modal = document.querySelector(".close");


burgerBtn.addEventListener("click", (e) => {
  // console.log("hello")
  menu.classList.toggle("active");
});

overlay.addEventListener("click", (e) => {
  menu.classList.remove("active");
});

MenuItems.forEach((menu) => {
  menu.addEventListener("click", (e) => {
    // Retirer la classe "active" de tous les éléments de menu
    MenuItems.forEach((item) => {
      item.classList.remove("active");
    });

    // Ajouter la classe "active" seulement à l'élément de menu cliqué
    menu.classList.add("active");
  });
});

SubMenuItems.forEach((sub) => {
  sub.addEventListener("click", (e) => {
    SubMenuItems.forEach((item) => {
      item.classList.remove("active");
    });
    sub.classList.add("active");
  });
});



open_modal.addEventListener("click", (e) => {
  modal.classList.add("active");
});

close_modal.addEventListener("click", (e) => {
  modal.classList.remove("active");
})

modal.addEventListener("click", (e) => {
  if (e.target.id === "myModal") {
    modal.classList.remove("active");
  }
})

/**
 * ✅ APPROCHE VANILLA JS (ACTUELLEMENT ACTIVE)
 * 
 * Fonction globale appelée depuis les templates via onclick="resetFilters('context')"
 * 
 * RÔLE:
 * - Réinitialise tous les <select> de la filter-bar en mettant value = ''
 * - Réinitialise les inputs de type date
 * - Réinitialise la barre de recherche identifiée par #search-{context}
 * - Déclenche HTMX pour recharger la liste avec les filtres vides
 * 
 * AVANTAGES:
 * ✅ Fonction unique définie une seule fois
 * ✅ Templates courts et propres (1 ligne: onclick="...")
 * ✅ Facile à maintenir (un seul endroit à modifier)
 * 
 * INCONVÉNIENTS:
 * ❌ Fonction dans le scope global (pollution du namespace)
 * ❌ Incompatible avec les modules ES6 (type="module")
 * ❌ Moins moderne/déclaratif qu'Alpine
 * 
 * PRÉREQUIS:
 * - <script src="script.js"> doit être chargé SANS type="module"
 * - Dans base.html: <script src="{% static 'js/script.js' %}" defer></script>
 */
function resetFilters(context) {
  // Réinitialiser tous les selects de la filter-bar
  const filterBar = document.querySelector('.filter-bar');
  if (filterBar) {
    const selects = filterBar.querySelectorAll('select');
    selects.forEach(select => {
      select.value = '';
    });
    
    // Réinitialiser aussi les inputs de type date
    const dateInputs = filterBar.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
      input.value = '';
    });
  }

  // Réinitialiser la barre de recherche
  const searchInput = document.querySelector(`#search-${context}`);
  if (searchInput) {
    searchInput.value = '';
  }

  // Déclencher le rechargement de la liste via HTMX
  const triggerElement = filterBar?.querySelector('select') || searchInput;
  if (triggerElement && typeof htmx !== 'undefined') {
    htmx.trigger(triggerElement, 'change');
  } else {
    // Fallback : recharger la page si htmx n'est pas disponible
    window.location.reload();
  }
}

/**
 * ⭕ APPROCHE ALPINE.JS (DÉSACTIVÉE - CODE COMMENTÉ)
 * 
 * Alternative moderne utilisant Alpine.js avec x-data et @click
 * 
 * RÔLE:
 * - Même comportement que la fonction Vanilla ci-dessus
 * - Définition locale dans chaque template via x-data="{...}"
 * 
 * AVANTAGES:
 * ✅ Pas de pollution du scope global
 * ✅ Compatible avec les modules ES6
 * ✅ Syntaxe moderne et déclarative
 * ✅ Scope isolé par composant
 * 
 * INCONVÉNIENTS:
 * ❌ Code répété dans chaque template (~15 lignes)
 * ❌ Plus verbeux dans les templates
 * ❌ Nécessite Alpine.js chargé
 * 
 * POUR ACTIVER CETTE APPROCHE:
 * 1. Dans les templates, décommenter le bloc x-data="{...}" 
 * 2. Remplacer onclick="resetFilters('context')" par @click="resetFilters()"
 * 3. Optionnellement, commenter la fonction resetFilters() Vanilla ci-dessus
 * 
 * EXEMPLE DE CODE À UTILISER DANS LES TEMPLATES:
 * 
 * <div class="filter-bar" x-data="{
 *   resetFilters() {
 *     document.querySelectorAll('.filter-bar select').forEach(el => el.value = '');
 *     const searchInput = document.querySelector('#search-catalogue');
 *     if (searchInput) searchInput.value = '';
 *     const firstSelect = document.querySelector('.filter-bar select');
 *     if (firstSelect && typeof htmx !== 'undefined') {
 *       htmx.trigger(firstSelect, 'change');
 *     }
 *   }
 * }">
 *   <button @click="resetFilters()">Reset</button>
 * </div>
 */

/**
 * Fonction pour préserver les valeurs des filtres après navigation HTMX
 */
document.body.addEventListener('htmx:afterSwap', function(event) {
  // Si le swap est dans le content-wrapper, on peut initialiser les listeners
  if (event.target.id === 'content-wrapper') {
    // Réattacher les événements du burger menu si nécessaire
    const newBurgerBtn = document.querySelector(".burger-menu");
    if (newBurgerBtn) {
      newBurgerBtn.addEventListener("click", (e) => {
        const menu = document.querySelector("#vertical-menu");
        if (menu) {
          menu.classList.toggle("active");
        }
      });
    }
  }
});
