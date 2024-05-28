document.getElementById('switch');

  
  document.getElementById("switch").addEventListener("click", function(event) {
    var nav = document.getElementById("side-bar");
    var bottom = document.getElementById("switch");
    nav.classList.toggle("hidden");
    bottom.classList.toggle("hidden");
    event.stopPropagation(); // Evita que el clic en el botón propague al div
  });
  
  // Event listener para cerrar el div cuando se haga clic en otra parte de la pantalla
  document.addEventListener("click", function(event) {
    let nav = document.getElementById("side-bar");
    var bottom = document.getElementById("switch");
     
    if (!nav.contains(event.target)) {
      nav.classList.add("hidden");
      bottom.classList.remove("hidden");

    }
  });