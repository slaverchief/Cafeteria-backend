document.getElementById('search-button').addEventListener("click", function() {
    window.location.replace(`?tn=${document.getElementById("search-input").value}`);
  });

function delete_order(pk){
    url = `delete/${pk}`
    fetch(url)
    row = document.getElementById(pk)
    row.innerHTML = ""
}