// Lee en qué pantalla está el usuario según la dirección de la página.

// Devuelve la ruta actual: "#/productos" -> "/productos"; sin "#" -> "/"
export function rutaActual(): string {
  // location.hash es la parte de la dirección que empieza con "#"
  return window.location.hash.replace(/^#/, '') || '/'
}
