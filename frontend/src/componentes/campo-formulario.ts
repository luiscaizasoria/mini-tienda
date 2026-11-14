// Componente: un campo de formulario con su etiqueta.

// Crea un campo con su etiqueta y devuelve ambos dentro de un <label>
export function crearCampo(
  texto: string,
  nombre: string,
  atributos: Record<string, string>,
): HTMLLabelElement {
  // La etiqueta envuelve al campo: al pulsar el texto se enfoca el campo
  const etiqueta = document.createElement('label')
  // Texto visible de la etiqueta
  etiqueta.textContent = texto

  // Crea el campo de entrada
  const campo = document.createElement('input')
  // "name" es la clave con la que se leerá el valor en FormData
  campo.name = nombre
  // Aplica atributos extra (type, min, step...)
  for (const [clave, valor] of Object.entries(atributos)) {
    campo.setAttribute(clave, valor)
  }

  // Mete el campo dentro de la etiqueta
  etiqueta.append(campo)
  // Devuelve la etiqueta terminada
  return etiqueta
}
