// Ayudas pequeñas para construir elementos HTML sin repetir código.

// Crea un elemento HTML con clase y texto opcionales.
// El tipo de retorno cambia según la etiqueta: "a" devuelve un enlace,
// "button" un botón, etc.
export function crearElemento<K extends keyof HTMLElementTagNameMap>(
  etiqueta: K,
  clase = '',
  texto = '',
): HTMLElementTagNameMap[K] {
  // Crea el elemento vacío
  const elemento = document.createElement(etiqueta)
  // Si se indicó una clase CSS, la asigna
  if (clase !== '') {
    elemento.className = clase
  }
  // Si se indicó un texto, lo inserta como texto plano (nunca como HTML)
  if (texto !== '') {
    elemento.textContent = texto
  }
  // Devuelve el elemento listo
  return elemento
}
