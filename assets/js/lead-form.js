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

  document.querySelectorAll('form[data-lead]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      // Temporary UX until dedicated Worker/bot is wired:
      // open Telegram with prefilled brief, then continue to thanks page.
      try {
        var text = encodeURIComponent(toTelegramText(form));
        window.open('https://t.me/Cenzyk?text=' + text, '_blank', 'noopener');
      } catch (err) {}
      // allow native navigation to thanks/
    });
  });
})();
