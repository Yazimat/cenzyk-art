(function () {
  function toTelegramText(form) {
    var data = new FormData(form);
    var lines = [
      'Заявка с cenzyk.art',
      'Тип: ' + (form.getAttribute('data-lead') || 'site'),
      'Имя: ' + (data.get('name') || ''),
      'Телефон: ' + (data.get('phone') || ''),
      'Связь: ' + (data.get('contact') || ''),
      'Адрес: ' + (data.get('address') || ''),
      'Бюджет: ' + (data.get('budget') || ''),
      'Комментарий: ' + (data.get('comment') || ''),
    ];
    return lines.join('\n');
  }

  document.addEventListener('submit', function (e) {
    var form = e.target;
    if (!form.matches || !form.matches('form[data-lead]')) return;
    try {
      var text = encodeURIComponent(toTelegramText(form));
      window.open('https://t.me/Cenzyk?text=' + text, '_blank', 'noopener');
    } catch (err) {}
  });
})();
