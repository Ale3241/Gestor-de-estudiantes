# Sistema de Gestión de Estudiantes

## Descripción General

Sistema de consola desarrollado en Python que implementa un gestor completo de estudiantes, asignaturas y calificaciones. Aplica principios de Programación Orientada a Objetos (POO) como herencia, encapsulamiento, polimorfismo y abstracción.

## Características Principales

- **Gestión de Asignaturas**: Crear y administrar múltiples asignaturas
- **Gestión de Grupos**: Organizar estudiantes en grupos dentro de cada asignatura
- **Modalidades de Estudio**: Soporte para estudiantes presenciales y a distancia con diferentes ponderaciones de calificaciones
- **Registro de Calificaciones**: Registrar calificaciones de exámenes y prácticas
- **Reportes**: Generar reportes de calificaciones y porcentaje de aprobados
- **Interfaz Interactiva**: Menú de consola intuitivo para todas las operaciones

## Conceptos OOP Implementados

### Herencia
- Clase base abstracta `Estudiante` 
- Clases derivadas: `EstudiantePresencial` y `EstudianteDistancia`

### Encapsulamiento
- Atributos privados (prefijo `_`) en todas las clases
- Métodos getter para acceso controlado a datos
- Métodos de negocio encapsulados en las clases correspondientes

### Polimorfismo
- Método abstracto `calcular_nota_final()` implementado diferentemente en cada clase derivada
- Método `mostrar_datos()` con comportamiento específico según modalidad
- Ponderaciones diferentes:
  - **Presencial**: 40% examen, 60% prácticas
  - **Distancia**: 30% examen, 70% prácticas

### Abstracción
- Clase abstracta `Estudiante` define la interfaz
- Métodos abstractos que deben ser implementados en subclases
- Patrón OperationResult para encapsular resultados de operaciones

### Patrón OperationResult
Cada operación retorna un objeto `OperationResult` con:
- `message`: Descripción del resultado
- `success`: Booleano indicando éxito o fallo
- `data`: Datos adicionales (opcional)

## Estructura de Clases

### Clase `OperationResult`
Encapsula el resultado de cualquier operación del sistema:
```python
result = OperationResult(message="Éxito", success=True, data={"valor": 100})
```

### Clase Base `Estudiante` (Abstracta)
Define la estructura base para todos los estudiantes:
- Atributos: `_id`, `_nombre`, `_calificaciones`
- Métodos abstractos: `calcular_nota_final()`, `mostrar_datos()`
- Métodos concretos: `agregar_calificacion()`, `get_id()`, `get_nombre()`, `get_calificaciones()`

### Clases Derivadas: `EstudiantePresencial` y `EstudianteDistancia`
Implementan comportamiento específico según modalidad de estudio.

### Clase `Grupo`
Gestiona un conjunto de estudiantes:
- Métodos: `agregar_estudiante()`, `registrar_calificacion()`, `calcular_porcentaje_aprobados()`, `obtener_listado_calificaciones()`

### Clase `Asignatura`
Gestiona múltiples grupos dentro de una asignatura:
- Métodos: `crear_grupo()`, `obtener_grupo()`, `listar_grupos()`, `obtener_reporte_asignatura()`

### Clase `SistemaGestion`
Coordina todas las asignaturas del sistema:
- Métodos: `crear_asignatura()`, `obtener_asignatura()`, `listar_asignaturas()`, `listar_asignaturas_detallado()`

### Clase `MenuConsola`
Interfaz de usuario basada en menú:
- Menú principal para crear asignaturas y ver reportes
- Menú de asignatura para gestionar grupos
- Menú de grupo para administrar estudiantes y calificaciones

## Requisitos

- Python 3.7 o superior
- Sistema operativo: Windows, macOS o Linux

## Instalación

1. Descargar o clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/gestor-estudiantes.git
cd gestor-estudiantes
```

2. No requiere instalación de dependencias externas (utiliza solo librerías estándar de Python)

## Uso

### Ejecutar la aplicación:
```bash
python gestor_estudiantes.py
```

### Flujo de uso típico:

1. **Crear una asignatura**: Opción 1 del menú principal
   - Ingresar nombre (ej: "Estructura de Datos")
   - Ingresar código único (ej: "ED101")

2. **Seleccionar la asignatura**: Opción 2 del menú principal
   - Elegir código de la asignatura

3. **Crear un grupo**: Opción 1 del menú de asignatura
   - Ingresar nombre del grupo (ej: "Grupo A", "101", etc.)

4. **Agregar estudiantes**: Opción 1 o 2 del menú de grupo
   - Seleccionar modalidad (presencial o distancia)
   - Ingresar nombre del estudiante
   - Se genera automáticamente un ID

5. **Registrar calificaciones**: Opción 3 del menú de grupo
   - Seleccionar estudiante
   - Seleccionar tipo (Examen o Práctica)
   - Ingresar calificación (0-100)

6. **Ver listado de calificaciones**: Opción 4 del menú de grupo
   - Muestra todas las calificaciones registradas
   - Incluye nota final calculada de cada estudiante

7. **Ver porcentaje de aprobados**: Opción 5 del menú de grupo
   - Calcula el porcentaje de estudiantes con nota >= 70
   - Muestra cantidad de aprobados y total

8. **Ver reporte completo**: Opción 4 del menú principal
   - Muestra toda la información de una asignatura en formato reporteable

## Ejemplo de Operación

```
===========================================
  REGISTRAR CALIFICACIÓN
===========================================

Estudiantes disponibles:
1. Juan Pérez (ID: 1000)
2. María García (ID: 1001)

Seleccione el número del estudiante: 1

Tipos de calificación disponibles:
1. Examen
2. Práctica

Seleccione el tipo de calificación: 1
Valor de la calificación (0-100): 85

[ÉXITO] Calificación de examen registrada: 85

Presione Enter para continuar...
```

## Almacenamiento de Datos

El sistema mantiene todos los datos en memoria utilizando:
- **Diccionarios** para acceso rápido a asignaturas y grupos
- **Listas** para almacenar estudiantes y calificaciones

Los datos se pierden al cerrar la aplicación. Para persistencia, se puede extender fácilmente agregando:
- Serialización a JSON
- Base de datos SQLite
- Archivo CSV

## Estructura de Archivos

```
gestor-estudiantes/
├── gestor_estudiantes.py    # Archivo principal con todas las clases
├── README.md                # Este archivo
└── .gitignore              # Configuración git (recomendado)
```

## Ejemplo de .gitignore recomendado

```
# Caché de Python
__pycache__/
*.py[cod]
*$py.class
*.so

# Entornos virtuales
venv/
ENV/
env/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# Sistema operativo
.DS_Store
Thumbs.db
```

## Cálculo de Notas

### Estudiante Presencial
- **Examen**: 40% del promedio de calificaciones de tipo "examen"
- **Prácticas**: 60% del promedio de calificaciones de tipo "práctica"
- **Nota Final** = (Examen × 0.4) + (Prácticas × 0.6)

### Estudiante a Distancia
- **Examen**: 30% del promedio de calificaciones de tipo "examen"
- **Prácticas**: 70% del promedio de calificaciones de tipo "práctica"
- **Nota Final** = (Examen × 0.3) + (Prácticas × 0.7)

### Criterio de Aprobado
- **Nota Final >= 70**: APROBADO
- **Nota Final < 70**: REPROBADO

## Extensiones Posibles

El código está diseñado para ser extensible:

1. **Persistencia de datos**:
   - Guardar y cargar desde archivos JSON
   - Integración con base de datos

2. **Más modalidades de estudio**:
   - Híbrido
   - Sincrónico/Asincrónico

3. **Evaluaciones adicionales**:
   - Proyectos
   - Participación
   - Asistencia

4. **Reportes avanzados**:
   - Exportar a PDF
   - Gráficos de rendimiento
   - Análisis estadístico

5. **Autenticación**:
   - Login para docentes
   - Portal para estudiantes

## Autor

Solin A. Mordan Acosta

## Contacto

Para preguntas o sugerencias sobre el código, por favor contacta al desarrollador.
alexacosta3241@gmail.com
---

**Notas para el uso académico**:
- El código está comentado para facilitar el aprendizaje
- Cada clase tiene docstrings explicativos
- El menú interactivo proporciona retroalimentación clara mediante `OperationResult`
- Los patrones OOP están claramente demarcados en el código
