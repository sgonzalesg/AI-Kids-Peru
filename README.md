# AI Kids Perú 

> **ONG desentralizada que usa la Inteligencia Artificial Multimodal para la Auditoría y Validación de Evidencias de Ciencia Ciudadana Escolar en la Web3.**

---

## El Problema: Fraude de Datos en Ciencia Ciudadana
Los proyectos de monitoreo ambiental escolar y ciencia ciudadana suelen enfrentarse a un gran desafío al intentar escalar: **la integridad de los datos**. Los estudiantes, intencionalmente o por error, pueden subir imágenes de internet (fotos de stock, paisajes falsos) o reportar ubicaciones incorrectas. Validar manualmente miles de muestras de agua o biodiversidad es logísticamente imposible, lo que contamina las bases de datos científicas y rompe la confianza en los sistemas de incentivos Web3.

## La Solución: La implementación de un "Agente Maestro"
**AI Kids Perú** resuelve esto implementando un pipeline automatizado de auditoría científica:
1. **Interfaz Accesible (Discord Proxy Bot):** Los escolares envían sus muestras en el campo usando un comando nativo `/subir_dato` de forma lúdica y directa.
2. **Capa Cognitiva de Auditoría:** Un agente inteligente, basado en modelo **Gemini 3.1 Flash Lite**, procesa la imagen y la descripción del alumno en paralelo usando ejecución multi-hilo.
3. **Filtros Estrictos de Veracidad:** El modelo no evalúa si la foto es "bonita", sino que aplica un análisis de **Morfología Fluvial** e identidad geográfica local, además de un filtro **Anti-Stock** (detección de imágenes profesionales o de internet).
4. **Payload Web3 Ready:** Si la IA da luz verde, empaqueta un JSON limpio optimizado para habilitar la acuñación de un **Pasaporte STEM (Soulbound Token - SBT)** en redes como *zkSyscoin*.


## Estructura del Repositorio
- src/proxy_bot.py: Manejador de la interfaz de Discord, interacción de comandos de barra, control de timeouts (defer) y concurrencia.
- src/agent.py: Conector nativo con Google AI Studio, carga de prompts y parseo estructurado de JSON.
- config/SOUL.md: Define el rol institucional, tono y límites éticos del agente auditor.
- config/INSTINCT.md: Define las heurísticas científicas e instrucciones de morfología local para el filtrado de imágenes.

---

##  Arquitectura del Sistema Bot de Discord

```text
  [ Alumno en Discord ] 
          │
          ▼ Comando: /subir_dato (Descripción + Foto + Wallet)
  ┌─────────────────────────────────────────────────────────────┐
  │                   DISCORD PROXY BOT (src/)                  │
  │  - Valida formatos de imagen (PNG/JPG)                      │
  │  - Ejecución Asíncrona Multi-Hilo (Evita timeouts de red)   │
  │  - Empaqueta Estructura de Datos (Payload)                  │
  └──────────────────────────────┬──────────────────────────────┘
                                 │
                                 ▼ Inyección de Contexto Estricto
  ┌─────────────────────────────────────────────────────────────┐
  │                    AGENTE MAESTRO ORÁCULO                   │
  │  - SOUL.md: Identidad académica y rol institucional         │
  │  - INSTINCT.md: Reglas de validación y contexto peruano     │
  └──────────────────────────────┬──────────────────────────────┘
                                 │
                                 ▼ Google GenAI SDK (API Directa)
  ┌─────────────────────────────────────────────────────────────┐
  │                 GEMINI 3.1 FLASH LITE ENGINE                │
  │  - Detección de anomalías (Efecto seda, iluminación stock)  │
  │  - Análisis geográfico real (Ej: Cuenca del Río Rímac)      │
  │  - Restricción Estricta de Salida (Formato JSON Nativo)     │
  └──────────────────────────────┬──────────────────────────────┘
                                 │
                                 ▼ 
  [ Veredicto Embed Estético ] ──┴──► [ Payload Listo para Contrato Web3 ]
```
