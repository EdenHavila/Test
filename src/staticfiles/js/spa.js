/*$(document).ready(function () {
  function loadPage(url, addToHistory = true) {
    $.ajax({
      url: url,
      headers: { 'X-Requested-With': 'XMLHttpRequest' },
      success: function (data) {
        $('#content-wrapper').html(data);
        if (addToHistory) {
          history.pushState(null, '', url);
        }
      },
      error: function () {
        $('#content-wrapper').html('<p>Erreur de chargement.</p>');
      }
    });
  }

  $(document).on('click', '.spa-link', function (e) {
    e.preventDefault();
    const url = $(this).attr('href');
    loadPage(url);
  });

  // Gérer le bouton retour
  window.onpopstate = function () {
    loadPage(location.pathname, false);
  };
});
*/


$(document).ready(function () {
  function showLoader() {
    $('#loader').fadeIn(150);
  }

  function hideLoader() {
    $('#loader').fadeOut(150);
  }

  function loadPage(url, addToHistory = true) {
    showLoader();

    // Effet fade out du contenu actuel
    $('#content-wrapper').fadeOut(200, function () {
      $.ajax({
        url: url,
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
        success: function (data) {
          $('#content-wrapper').html(data).fadeIn(200);
          if (addToHistory) {
            history.pushState(null, '', url);
          }
        },
        error: function () {
          $('#content-wrapper').html('<p style="color:red;">Erreur de chargement. Veuillez réessayer.</p>').fadeIn(200);
        },
        complete: function () {
          hideLoader();
        }
      });
    });
  }

  $(document).on('click', '.spa-link', function (e) {
    e.preventDefault();
    const url = $(this).attr('href');
    loadPage(url);
  });

  window.onpopstate = function () {
    loadPage(location.pathname, false);
  };
});
