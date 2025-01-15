document.getElementById('search-button').addEventListener("click", function() {
    window.location.replace(`?tn=${document.getElementById("search-input").value}`);
  });