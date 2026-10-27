# Sistema de Gestión de Estudiantes

## Descripción

Aplicación de consola desarrollada en Python para administrar asignaturas, grupos, estudiantes y calificaciones. El proyecto aplica principios de programación orientada a objetos (POO), incluyendo herencia, encapsulamiento, abstracción y polimorfismo.

## Funcionalidades

- Crear y administrar asignaturas.
- Organizar estudiantes en grupos.
- Registrar estudiantes presenciales y a distancia.
- Registrar calificaciones de exámenes y prácticas.
- Calcular notas finales según la modalidad de estudio.
- Consultar listados de calificaciones.
- Generar reportes por asignatura y grupo.
- Calcular el porcentaje de estudiantes aprobados.

## Conceptos técnicos

### Programación orientada a objetos

- **Abstracción:** clase base `Estudiante` con métodos abstractos.
- **Herencia:** clases `EstudiantePresencial` y `EstudianteDistancia`.
- **Encapsulamiento:** atributos y métodos para controlar el acceso a los datos.
- **Polimorfismo:** implementación del cálculo de notas según la modalidad.

### Manejo de resultados

El sistema utiliza `OperationResult` para representar el resultado de las operaciones, incluyendo un mensaje, un indicador de éxito y datos adicionales cuando corresponda.

## Cálculo de calificaciones

Las ponderaciones dependen de la modalidad:

| Modalidad | Examen | Prácticas |
|---|---:|---:|
| Presencial | 40 % | 60 % |
| A distancia | 30 % | 70 % |

El criterio de aprobación indicado por el sistema es una nota final igual o superior a 70.

## Requisitos

- Python 3.7 o la versión mínima compatible con el código.
- Windows, macOS o Linux.
- No requiere dependencias externas, siempre que el proyecto utilice únicamente la biblioteca estándar de Python.

## Instalación y ejecución

Clona el repositorio:

```bash
git clone https://github.com/Ale3241/Gestor-de-estudiantes.git
cd Gestor-de-estudiantes
```

Ejecuta el archivo principal utilizando el nombre real del archivo Python del proyecto:

```bash
python nombre_del_archivo.py
```

## Almacenamiento

Los datos se mantienen en memoria durante la ejecución. Al cerrar la aplicación, los datos se pierden.

Como posibles mejoras futuras, se puede incorporar persistencia mediante JSON o SQLite.

## Autor

Solin A. Mordan Acosta
