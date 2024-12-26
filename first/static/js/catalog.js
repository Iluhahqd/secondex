document.getElementById('productTypeFilter').addEventListener('change', function() {
    var skisOptions = document.getElementById('skisFilterOptions');
    var snowboardOptions = document.getElementById('snowboardFilterOptions');
    if (this.value === 'skis') {
        skisOptions.style.display = 'block';
        snowboardOptions.style.display = 'none';
        // Снимаем обязательность с полей сноуборда
        document.querySelectorAll('#snowboardFilterOptions select').forEach(function(select) {
            select.removeAttribute('');
        });
        // Добавляем обязательность полям лыж
        document.querySelectorAll('#skisFilterOptions select').forEach(function(select) {
            select.setAttribute('', '');
        });
    } else if (this.value === 'snowboard') {
        skisOptions.style.display = 'none';
        snowboardOptions.style.display = 'block';
        // Снимаем обязательность с полей лыж
        document.querySelectorAll('#skisFilterOptions select').forEach(function(select) {
            select.removeAttribute('');
        });
        // Добавляем обязательность полям сноуборда
        document.querySelectorAll('#snowboardFilterOptions select').forEach(function(select) {
            select.setAttribute('', '');
        });
    } else {
        skisOptions.style.display = 'none';
        snowboardOptions.style.display = 'none';
        // Снимаем обязательность со всех дополнительных полей
        document.querySelectorAll('#skisFilterOptions select, #snowboardFilterOptions select').forEach(function(select) {
            select.removeAttribute('');
        });
    }
});

document.getElementById('add_product').onclick = function() {
    window.location.href = '/product/add';
}

function initFavs()
  {
    // Handle Favorites
    console.log(3);
    var items = document.getElementsByClassName('favorite-btn');
    for(var x = 0; x < items.length; x++)
    {
      var item = items[x];
      item.addEventListener('click', function(fn)
      {
        console.log(fn.target.classList);
        fn.target.classList.toggle('favorite-btn-fav');
      });
    }
  }

function add_to_fav(n, user) {
    $.ajax({
        url: 'add_to_fav_ajax/',
        data: {'id': n, 'user_id': user},
        success : function(json) {
            $("#request-access").hide();
            console.log("requested access complete");
        }
    });
};

function add_to_cart(n, user) {
    $.ajax({
        url: 'add_to_cart_ajax/',
        data: {'id': n, 'user_id': user},
        success : function(json) {
            $("#request-access").hide();
            console.log("requested access complete");
        }
    });
};

initFavs()
console.log(13)