(function () {
  var index = [];
  var searchBox = document.getElementById('search-box');
  if (!searchBox) return;

  fetch('../search_index.json')
    .then(function (r) { return r.json(); })
    .then(function (data) { index = data; })
    .catch(function () {});

  searchBox.addEventListener('input', function () {
    var q = this.value.trim().toLowerCase();
    var cards = document.querySelectorAll('[data-searchable]');
    cards.forEach(function (card) {
      var text = card.getAttribute('data-searchable').toLowerCase();
      card.style.display = (!q || text.includes(q)) ? '' : 'none';
    });
  });
})();
