
const api = "/productos";
let todosLosProductos = [];

async function obtenerProductos() {
  const res = await fetch(api);
  return await res.json();
}

function renderizarProductos(productos) {
  const contenedor = document.getElementById("listaProductos");
  contenedor.innerHTML = "";
  if (productos.length === 0) {
    contenedor.innerHTML = '<div class="alert alert-warning">No se encontraron productos con los filtros seleccionados.</div>';
    return;
  }
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

function llenarSelectUnicos(productos, campo, selectId) {
  const valores = [...new Set(productos.map(p => (p[campo] || '').trim()).filter(v => v))];
  const select = document.getElementById(selectId);
  select.innerHTML = '<option value="">Todas</option>';
  valores.forEach(valor => {
    const option = document.createElement('option');
    option.value = valor;
    option.textContent = valor;
    select.appendChild(option);
  });
}

function aplicarFiltros() {
  const categoria = document.getElementById('filtroCategoria').value;
  const marca = document.getElementById('filtroMarca').value;
  let filtrados = todosLosProductos;
  if (categoria) {
    filtrados = filtrados.filter(p => (p.categoria || '').trim() === categoria);
  }
  if (marca) {
    filtrados = filtrados.filter(p => (p.marca || '').trim() === marca);
  }
  renderizarProductos(filtrados);
}

async function inicializarCatalogo() {
  todosLosProductos = await obtenerProductos();
  llenarSelectUnicos(todosLosProductos, 'categoria', 'filtroCategoria');
  llenarSelectUnicos(todosLosProductos, 'marca', 'filtroMarca');
  renderizarProductos(todosLosProductos);

  document.getElementById('filtroCategoria').addEventListener('change', aplicarFiltros);
  document.getElementById('filtroMarca').addEventListener('change', aplicarFiltros);
  document.getElementById('btnLimpiarFiltros').addEventListener('click', function(e) {
    e.preventDefault();
    document.getElementById('filtroCategoria').value = '';
    document.getElementById('filtroMarca').value = '';
    renderizarProductos(todosLosProductos);
  });
}

inicializarCatalogo();
