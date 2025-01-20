from = document.getElementById("from")
to = document.getElementById("to")
sum_block = document.getElementById("sum")
from.valueAsDate = new Date();
to.valueAsDate = new Date();
to.setAttribute('max', to.value)

function update_sum(){
    from.setAttribute('max', to.value)
    to.setAttribute('min', from.value)
    fetch('/orders/api/cash', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          from: from.value,
          to: to.value
        })
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Плохой ответ');
        }
        return response.json();
      })
      .then(data => {
        sum_block.innerHTML = `${data}₽`
      })
      .catch(error => console.error('Непредвиденная ошибка:', error));
}

update_sum()

to.addEventListener("change", function() {
    update_sum()
  });

from.addEventListener("change", function() {
    update_sum()
  });
