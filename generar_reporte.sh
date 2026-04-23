#!/bin/bash

# Colores para la terminal
VERDE='\033[0;32m'
AZUL='\033[0;34m'
ROJO='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${AZUL}--- Iniciando Pipeline de Simulación Aeroespacial Unificado ---${NC}"

# 1. Ejecutar simulaciones usando el simulador dinámico
echo -e "${VERDE}[1/3] Generando datos sintéticos con simulador.py...${NC}"

# Simulación 1: Ideal
python3 simulador.py --salida datos_lanzamiento.csv

# Simulación 2: Con Drag
python3 simulador.py --drag --salida datos_lanzamiento_drag.csv

# Simulación 3: Gravity Turn (Orbital)
python3 simulador.py --drag --gravity_turn --salida datos_orbitales.csv

# 2. Verificar integridad
echo -e "${VERDE}[2/3] Validando ficheros CSV...${NC}"
for file in datos_lanzamiento.csv datos_lanzamiento_drag.csv datos_orbitales.csv; do
    if [[ -f "$file" ]]; then
        echo -e "  [OK] $file"
    else
        echo -e "${ROJO}  [ERROR] Faltan datos: $file${NC}"
        exit 1
    fi
done

# 3. Análisis con Gemini CLI
echo -e "${VERDE}[3/3] Ejecutando analista de IA (Gemini CLI)...${NC}"

PROMPT="@datos_lanzamiento_drag.csv @datos_orbitales.csv Actúa como ingeniero jefe de misión. 
1) Compara la pérdida de energía entre el ascenso vertical y el Gravity Turn. 
2) Basado en los datos, ¿cuánto Delta-v horizontal ganamos gracias a la maniobra de cabeceo? 
3) Concluye si el diseño actual es apto para misiones suborbitales o si requiere una segunda etapa para órbita estable."

# Generar reporte final
gemini -p "$PROMPT" > reporte_vuelo.md

echo -e "${VERDE}--- Pipeline Finalizado ---${NC}"
echo -e "Reporte técnico guardado en: ${AZUL}reporte_vuelo.md${NC}"