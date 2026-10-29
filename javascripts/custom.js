document.addEventListener("DOMContentLoaded", function() {
  var headerTitle = document.querySelector('.md-header__title');
  var logo = document.querySelector('.md-header__button.md-logo');
  
  if (headerTitle && logo) {
    headerTitle.style.cursor = 'pointer';
    headerTitle.title = 'Gå til forsiden';
    headerTitle.addEventListener('click', function() {
      window.location.href = logo.href;
    });
  }
});
