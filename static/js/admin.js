// JavaScript para el panel de administración - Extraído del index.html funcionando

const api = "/productos";

// Función para cargar productos existentes
async function cargarProductos() {
  try {
    const res = await fetch(api);
    const productos = await res.json();
    const contenedor = document.getElementById("listaProductos");
    contenedor.innerHTML = "";

    productos.forEach(prod => {
      const urlImagen = prod.imagen_url && prod.imagen_url.trim() !== "" 
        ? prod.imagen_url 
        : "https://via.placeholder.com/100";

      const card = document.createElement("div");
      card.className = "card producto-card";
      card.innerHTML = `
        <div class="card-body d-flex">
          <img src="${urlImagen}" onerror="this.onerror=null; this.src='https://via.placeholder.com/100'" class="producto-imagen me-3">
          <div class="flex-grow-1">
            <h5>${prod.nombre}</h5>
            <p><strong>Marca:</strong> ${prod.marca} | <strong>Categoría:</strong> ${prod.categoria}</p>
            <p><strong>Cantidad:</strong> ${prod.cantidad}</p>
            <p><small>${prod.descripcion}</small></p>
            <button class="btn btn-warning btn-sm me-2" onclick='editar(${JSON.stringify(prod)})'>Editar</button>
            <button class="btn btn-danger btn-sm" onclick="eliminar(${prod.id})">Eliminar</button>
          </div>
        </div>
      `;
      contenedor.appendChild(card);
    });
  } catch (error) {
    console.error('Error al cargar productos:', error);
  }
}

// Función para eliminar producto
async function eliminar(id) {
  if (confirm('¿Estás seguro de que quieres eliminar este producto?')) {
    try {
      await fetch(`${api}/${id}`, { method: "DELETE" });
      cargarProductos();
    } catch (error) {
      console.error('Error al eliminar producto:', error);
      alert('Error al eliminar el producto');
    }
  }
}

// Función para llenar formulario para edición
function editar(prod) {
  document.getElementById("productoId").value = prod.id;
  document.getElementById("nombre").value = prod.nombre;
  document.getElementById("cantidad").value = prod.cantidad;
  document.getElementById("descripcion").value = prod.descripcion;
  document.getElementById("marca").value = prod.marca;
  document.getElementById("categoria").value = prod.categoria;
  document.getElementById("imagenActual").value = prod.imagen_url || "";
}

// Configurar el formulario cuando se carga la página
document.addEventListener("DOMContentLoaded", function() {
  // Manejar envío del formulario
  document.getElementById("formProducto").addEventListener("submit", async e => {
    e.preventDefault();
    
    try {
      const id = document.getElementById("productoId").value;
      const imagen = document.getElementById("imagen");
      let imagen_url = document.getElementById("imagenActual").value;

      // Subir imagen si hay una nueva
      if (imagen.files.length > 0) {
        const formData = new FormData();
        formData.append("file", imagen.files[0]);
        const resImg = await fetch("/upload-imagen/", { 
          method: "POST", 
          body: formData 
        });
        const dataImg = await resImg.json();
        imagen_url = dataImg.url;
      }

      // Crear objeto producto
      const producto = {
        nombre: document.getElementById("nombre").value,
        cantidad: parseInt(document.getElementById("cantidad").value),
        descripcion: document.getElementById("descripcion").value,
        marca: document.getElementById("marca").value,
        categoria: document.getElementById("categoria").value,
        imagen_url
      };

      // Determinar método y URL
      const method = id ? "PUT" : "POST";
      const url = id ? `${api}/${id}` : `${api}/`;

      // Enviar datos
      await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(producto)
      });

      // Limpiar formulario y recargar productos
      e.target.reset();
      document.getElementById("productoId").value = "";
      document.getElementById("imagenActual").value = "";
      cargarProductos();
      
      // Mostrar mensaje de éxito
      alert(id ? 'Producto actualizado exitosamente' : 'Producto creado exitosamente');
      
    } catch (error) {
      console.error('Error al guardar producto:', error);
      alert('Error al guardar el producto');
    }
  });

  // Cargar productos al iniciar
  cargarProductos();
});
