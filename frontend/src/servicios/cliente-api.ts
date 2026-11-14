// Cliente HTTP base: todas las llamadas a la API pasan por aquí.

// Configuración con la dirección de la API
import { entorno } from '../config/entorno.ts'

// Hace una petición a la API y devuelve la respuesta ya convertida desde JSON.
// <T> es el tipo de dato que quien llama espera recibir.
export async function pedirJson<T>(
  ruta: string,
  opciones?: RequestInit,
): Promise<T> {
  // Une la dirección base con la ruta (por ejemplo, /productos) y pide
  const respuesta = await fetch(`${entorno.apiUrl}${ruta}`, opciones)

  // fetch no falla con errores HTTP (404, 500...): hay que revisarlos
  if (!respuesta.ok) {
    // Lanza un error que quien llame a esta función podrá capturar
    throw new Error(`La API respondió con el código ${respuesta.status}`)
  }

  // Convierte el cuerpo JSON de la respuesta al tipo esperado
  return (await respuesta.json()) as T
}
