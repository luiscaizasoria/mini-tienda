// Declara qué variables de entorno existen, para que TypeScript las conozca.

// Amplía los tipos que Vite ya trae (por eso va dentro de "declare global")
declare global {
  // Variables disponibles en import.meta.env
  interface ImportMetaEnv {
    // Dirección de la API de Python
    readonly VITE_API_URL: string
  }
}

// Convierte este archivo en módulo, requisito para usar "declare global"
export {}
