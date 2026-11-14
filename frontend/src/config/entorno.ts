// Única puerta de entrada a la configuración: el resto del código importa
// desde aquí y nunca lee import.meta.env directamente.

// Lee una variable obligatoria; si falta, falla al arrancar con un mensaje claro
function leerVariable(nombre: keyof ImportMetaEnv): string {
  // Busca la variable en el archivo .env del modo actual
  const valor = import.meta.env[nombre]

  // Si no existe o está vacía, detiene la aplicación
  if (!valor) {
    throw new Error(
      `Falta la variable ${nombre}. Revisa los archivos .env (ver .env.example).`,
    )
  }

  // Devuelve el valor encontrado
  return valor
}

// Configuración de la aplicación, ya validada
export const entorno = {
  // Dirección de la API, sin "/" al final para poder unirla con rutas
  apiUrl: leerVariable('VITE_API_URL').replace(/\/$/, ''),
} as const
