// Google Analytics 4 — Revista ECYS, Edición XXIX.
// Cargado desde los HTML de 29Edicion; no afecta la página principal ni otras ediciones.
(function () {
  'use strict';
  const measurementId = 'G-K17PR81E0J';

  // Evita instalar por segunda vez la misma etiqueta si el script se repite.
  if (document.querySelector('script[src="https://www.googletagmanager.com/gtag/js?id=' + measurementId + '"]')) {
    return;
  }
  const script = document.createElement('script');
  script.async = true;
  script.src = 'https://www.googletagmanager.com/gtag/js?id=' + measurementId;
  document.head.appendChild(script);

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
  window.gtag('js', new Date());
  window.gtag('config', measurementId);
})();
