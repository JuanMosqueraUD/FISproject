const api = "/productos";

async function cargarProductos() {
  const res = await fetch(api);
  const productos = await res.json();
  const contenedor = document.getElementById("listaProductos");
  contenedor.innerHTML = "";

  productos.forEach(prod => {
    const urlImagen = prod.imagen_url && prod.imagen_url.trim() !== ""
      ? prod.imagen_url
      : "https://via.placeholder.com/250";

    const card = document.createElement("div");
    card.className = "producto-card";
    card.innerHTML = `
      <img src="${urlImagen}" onerror="this.onerror=null; this.src='https://via.placeholder.com/250'" class="producto-imagen">
      <div class="producto-nombre">${prod.nombre}</div>
      <div class="producto-info"><strong>Marca:</strong> ${prod.marca}</div>
      <div class="producto-info"><strong>Categoría:</strong> ${prod.categoria}</div>
      <div class="producto-info"><strong>Cantidad:</strong> ${prod.cantidad}</div>
      <div class="producto-info"><em>${prod.descripcion}</em></div>
    `;
    contenedor.appendChild(card);
  });
}

cargarProductos();
