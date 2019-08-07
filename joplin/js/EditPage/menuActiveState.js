export default function() {
  // If we're on a snippet edit page don't turn on the pencil
  if (window.location.href.includes('snippet')) return;

  // Make the content index icon active in Edit Mode
  // This decision came from Tori as she considers the edit pages as a sub-nav
  // This would've required updates to the MenuItem class and its HTML template in Wagtail so I decided to write JS noodles.
  $('.icon-home')
    .closest('.menu-item')
    .addClass('menu-active');
}
