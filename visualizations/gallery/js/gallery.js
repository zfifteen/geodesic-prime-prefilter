
(function () {
  const cards = Array.from(document.querySelectorAll('[data-entry]'));
  const chips = Array.from(document.querySelectorAll('[data-filter]'));
  const empty = document.getElementById('filter-empty');
  let status = 'all';
  let tier = 'all';
  function apply() {
    let visible = 0;
    cards.forEach(card => {
      const okStatus = status === 'all' || card.dataset.status === status;
      const okTier = tier === 'all' || card.dataset.tier === tier;
      const show = okStatus && okTier;
      card.classList.toggle('hidden', !show);
      if (show) visible += 1;
    });
    if (empty) {
      empty.classList.toggle('hidden', visible > 0);
      empty.textContent = visible > 0
        ? ''
        : 'No entries match these filters (try status: all and tier: all).';
    }
    chips.forEach(chip => {
      const kind = chip.dataset.filter;
      const val = chip.dataset.value;
      let active = false;
      if (kind === 'status') active = status === val;
      if (kind === 'tier') active = tier === val;
      chip.classList.toggle('active', active);
      chip.setAttribute('aria-pressed', active ? 'true' : 'false');
    });
  }
  chips.forEach(chip => {
    chip.addEventListener('click', () => {
      const kind = chip.dataset.filter;
      const val = chip.dataset.value;
      if (kind === 'status') status = val;
      if (kind === 'tier') tier = val;
      apply();
    });
  });
  apply();
})();
