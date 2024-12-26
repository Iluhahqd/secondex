document.addEventListener('DOMContentLoaded', function() {
    var table = document.getElementById('ratingTable');
    var rows = Array.from(table.getElementsByTagName('tbody')[0].getElementsByTagName('tr'));

    // Сортируем строки по убыванию рейтинга
    rows.sort(function(rowA, rowB) {
        var ratingA = parseFloat(rowA.getElementsByTagName('td')[2].textContent);
        var ratingB = parseFloat(rowB.getElementsByTagName('td')[2].textContent);
        return ratingB - ratingA;
    });

    // Устанавливаем номера мест и переупорядочиваем строки
    for (var i = 0; i < rows.length; i++) {
        var cell = rows[i].getElementsByTagName('td')[0];
        cell.textContent = i + 1;
        table.getElementsByTagName('tbody')[0].appendChild(rows[i]);
    }
});