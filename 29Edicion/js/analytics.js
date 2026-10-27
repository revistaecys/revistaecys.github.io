// Sustituir el ID únicamente después de crear el flujo GA4 de la Edición XXIX.
const ECYS_GA4_ID = 'G-XXXXXXXXXX';
if (/^G-[A-Z0-9]{6,}$/.test(ECYS_GA4_ID) && !ECYS_GA4_ID.includes('XXXX')) {
  const script=document.createElement('script'); script.async=true;
  script.src='https://www.googletagmanager.com/gtag/js?id='+encodeURIComponent(ECYS_GA4_ID);
  document.head.appendChild(script);
  window.dataLayer=window.dataLayer||[];
  window.gtag=function(){dataLayer.push(arguments)};
  gtag('js', new Date());
  gtag('config', ECYS_GA4_ID);
}
