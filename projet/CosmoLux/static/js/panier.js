// panier.js

// Sauvegarde automatique du panier dans le localStorage
function savePanierToLocalStorage(panier) {
    localStorage.setItem("panier", JSON.stringify(panier))
  }
  
  // Chargement du panier depuis le localStorage
  function loadPanierFromLocalStorage() {
    const panier = localStorage.getItem("panier")
    return panier ? JSON.parse(panier) : []
  }
  
  // Ajout au panier
  function ajouterAuPanier(produitId) {
    const panier = loadPanierFromLocalStorage()
    const produit = panier.find((item) => item.produitId === produitId)
  
    if (produit) {
      produit.quantite++
    } else {
      panier.push({ produitId, quantite: 1 })
    }
  
    savePanierToLocalStorage(panier)
  
    // Mettre à jour le compteur du panier dans la navbar
    updateCartCounter()
  
    return panier
  }
  
  // Mettre à jour la quantité d'un produit
  function miseAJourQuantite(produitId, nouvelleQuantite) {
    const panier = loadPanierFromLocalStorage()
    const produit = panier.find((item) => item.produitId === produitId)
  
    if (produit) {
      produit.quantite = nouvelleQuantite
      savePanierToLocalStorage(panier)
      updateCartCounter()
    }
  
    return panier
  }
  
  // Suppression d'un produit du panier
  function supprimerProduitDuPanier(produitId) {
    let panier = loadPanierFromLocalStorage()
    panier = panier.filter((item) => item.produitId !== produitId)
    savePanierToLocalStorage(panier)
  
    // Mettre à jour le compteur du panier dans la navbar
    updateCartCounter()
  
    return panier
  }
  
  // Calculer le total du panier
  function calculerTotalPanier(panier, produits) {
    let total = 0
  
    panier.forEach((item) => {
      const produit = produits.find((p) => p.id === Number.parseInt(item.produitId))
      if (produit) {
        total += produit.prix * item.quantite
      }
    })
  
    return total
  }
  
  // Mettre à jour le compteur du panier dans la navbar
  function updateCartCounter() {
    const panier = loadPanierFromLocalStorage()
    const totalItems = panier.reduce((total, item) => total + item.quantite, 0)
  
    // Mettre à jour le compteur dans la navbar si l'élément existe
    const cartCounter = document.getElementById("cart-count")
    if (cartCounter) {
      cartCounter.textContent = totalItems
  
      // Ajouter une classe pour l'animation si le compteur n'est pas à zéro
      if (totalItems > 0) {
        cartCounter.classList.add("has-items")
      } else {
        cartCounter.classList.remove("has-items")
      }
    }
  }
  
  // Synchroniser le panier local avec le serveur
  function syncPanierWithServer() {
    const panier = loadPanierFromLocalStorage()
  
    // Envoyer le panier au serveur pour synchronisation
    fetch("/api/sync-panier/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({ panier }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          console.log("Panier synchronisé avec succès")
        }
      })
      .catch((error) => {
        console.error("Erreur lors de la synchronisation du panier:", error)
      })
  }
  
  // Initialiser le panier au chargement de la page
  document.addEventListener("DOMContentLoaded", () => {
    updateCartCounter()
  })
  
  // Fonction utilitaire pour récupérer un cookie
  function getCookie(name) {
    let cookieValue = null
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";")
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim()
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
          break
        }
      }
    }
    return cookieValue
  }
  