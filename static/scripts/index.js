document.getElementById('sidebar_switch'); // para abrir el sidebar

  document.getElementById("sidebar_switch").addEventListener("click", function(event) {
    var nav = document.getElementById("nav-bar");
    var bottom = document.getElementById("sidebar_switch");
    nav.classList.toggle("hidden");
    bottom.classList.toggle("hidden");
    event.stopPropagation(); // Evita que el clic en el botón propague al div
  });
  
  // Event listener para cerrar el div cuando se haga clic en otra parte de la pantalla
  document.addEventListener("click", function(event) {
    let nav = document.getElementById("nav-bar");
    var bottom = document.getElementById("sidebar_switch");
     
    if (!nav.contains(event.target)) {
      nav.classList.add("hidden");
      bottom.classList.remove("hidden");

    }
  });