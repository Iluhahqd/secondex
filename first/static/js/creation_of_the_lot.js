document.getElementById('AddProductForm').addEventListener('submit', function(e) {
  alert('Товар добавлен!');
});

document.getElementById('productType').addEventListener('change', function() {
  var skisOptions = document.getElementById('skisOptions');
  var snowboardOptions = document.getElementById('snowboardOptions');
  if (this.value === 'skis') {
    skisOptions.style.display = 'block';
    snowboardOptions.style.display = 'none';
    // Populate skisOptions with necessary fields if not already done
  } else if (this.value === 'snowboard') {
    skisOptions.style.display = 'none';
    snowboardOptions.style.display = 'block';
    // Populate snowboardOptions with necessary fields if not already done
  } else {
    skisOptions.style.display = 'none';
    snowboardOptions.style.display = 'none';
  }
});