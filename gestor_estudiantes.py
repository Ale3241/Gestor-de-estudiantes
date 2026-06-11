"""Sistema de Gestión de Estudiantes - Aplicación de consola"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class OperationResult:
    """Encapsula el resultado de una operación (éxito, mensaje y datos)."""
    
    def __init__(self, message: str, success: bool, data: Any = None):
        self.message = message
        self.success = success
        self.data = data
    
    def __str__(self) -> str:
        status = "ÉXITO" if self.success else "ERROR"
        return f"[{status}] {self.message}"


class Estudiante(ABC):
    """Clase base para estudiantes con cálculo de nota final y datos."""
    
    _contador_id = 1000
    
    def __init__(self, nombre: str):
        self._id = Estudiante._contador_id
        Estudiante._contador_id += 1
        self._nombre = nombre
        self._calificaciones: List[Dict[str, Any]] = []
    
    def get_id(self) -> int:
        return self._id
    
    def get_nombre(self) -> str:
        return self._nombre
    
    def agregar_calificacion(self, tipo: str, valor: float) -> OperationResult:
        if not 0 <= valor <= 100:
            return OperationResult("Calificación fuera de rango (0-100)", False)
        
        self._calificaciones.append({'tipo': tipo, 'valor': valor})
        return OperationResult(f"Calificación de {tipo} registrada: {valor}", True)
    
    def get_calificaciones(self) -> List[Dict[str, Any]]:
        return self._calificaciones.copy()
    
    @abstractmethod
    def calcular_nota_final(self) -> float:
        pass
    
    @abstractmethod
    def mostrar_datos(self) -> str:
        pass


class EstudiantePresencial(Estudiante):
    """Estudiante presencial: 40% examen, 60% prácticas."""
    
    def calcular_nota_final(self) -> float:
        if not self._calificaciones:
            return 0.0
        
        examenes = [c['valor'] for c in self._calificaciones if c['tipo'] == 'examen']
        practicas = [c['valor'] for c in self._calificaciones if c['tipo'] == 'práctica']
        
        nota_final = 0.0
        if examenes:
            nota_final += (sum(examenes) / len(examenes)) * 0.4
        if practicas:
            nota_final += (sum(practicas) / len(practicas)) * 0.6
        
        return round(nota_final, 2)
    
    def mostrar_datos(self) -> str:
        nota_final = self.calcular_nota_final()
        estado = "APROBADO" if nota_final >= 70 else "REPROBADO"
        return (f"[PRESENCIAL] ID: {self._id} | Nombre: {self._nombre} | "
                f"Nota Final: {nota_final} | Estado: {estado}")


class EstudianteDistancia(Estudiante):
    """Estudiante a distancia: 30% examen, 70% prácticas."""
    
    def calcular_nota_final(self) -> float:
        if not self._calificaciones:
            return 0.0
        
        examenes = [c['valor'] for c in self._calificaciones if c['tipo'] == 'examen']
        practicas = [c['valor'] for c in self._calificaciones if c['tipo'] == 'práctica']
        
        nota_final = 0.0
        if examenes:
            nota_final += (sum(examenes) / len(examenes)) * 0.3
        if practicas:
            nota_final += (sum(practicas) / len(practicas)) * 0.7
        
        return round(nota_final, 2)
    
    def mostrar_datos(self) -> str:
        nota_final = self.calcular_nota_final()
        estado = "APROBADO" if nota_final >= 70 else "REPROBADO"
        return (f"[DISTANCIA] ID: {self._id} | Nombre: {self._nombre} | "
                f"Nota Final: {nota_final} | Estado: {estado}")


class Grupo:
    """Gestiona un grupo de estudiantes."""
    
    def __init__(self, nombre: str):
        self._nombre = nombre
        self._estudiantes: List[Estudiante] = []
    
    def get_nombre(self) -> str:
        return self._nombre
    
    def agregar_estudiante(self, estudiante: Estudiante) -> OperationResult:
        if any(e.get_id() == estudiante.get_id() for e in self._estudiantes):
            return OperationResult(
                f"El estudiante {estudiante.get_nombre()} ya existe en el grupo",
                False
            )
        self._estudiantes.append(estudiante)
        return OperationResult(
            f"Estudiante {estudiante.get_nombre()} agregado al grupo {self._nombre}",
            True
        )
    
    def obtener_estudiantes(self) -> List[Estudiante]:
        return self._estudiantes.copy()
    
    def registrar_calificacion(self, id_estudiante: int, tipo: str, valor: float) -> OperationResult:
        for estudiante in self._estudiantes:
            if estudiante.get_id() == id_estudiante:
                return estudiante.agregar_calificacion(tipo, valor)
        return OperationResult(
            f"Estudiante con ID {id_estudiante} no encontrado en el grupo",
            False
        )
    
    def calcular_porcentaje_aprobados(self) -> OperationResult:
        if not self._estudiantes:
            return OperationResult("No hay estudiantes en el grupo", False)
        
        aprobados = sum(1 for e in self._estudiantes if e.calcular_nota_final() >= 70)
        porcentaje = (aprobados / len(self._estudiantes)) * 100
        
        return OperationResult(
            f"Porcentaje de aprobados en {self._nombre}: {porcentaje:.2f}%",
            True,
            {'porcentaje': round(porcentaje, 2), 'aprobados': aprobados, 
             'total': len(self._estudiantes)}
        )
    
    def obtener_listado_calificaciones(self) -> str:
        if not self._estudiantes:
            return f"Grupo {self._nombre}: No hay estudiantes registrados"
        
        listado = f"\n{'='*80}\n"
        listado += f"LISTADO DE CALIFICACIONES - GRUPO: {self._nombre}\n"
        listado += f"{'='*80}\n"
        
        for estudiante in self._estudiantes:
            listado += f"\n{estudiante.mostrar_datos()}\n"
            calificaciones = estudiante.get_calificaciones()
            if calificaciones:
                listado += "  Calificaciones registradas:\n"
                for cal in calificaciones:
                    listado += f"    - {cal['tipo'].capitalize()}: {cal['valor']}\n"
            else:
                listado += "  Sin calificaciones registradas\n"
        
        listado += f"\n{'='*80}\n"
        return listado


class Asignatura:
    """Gestiona múltiples grupos dentro de una asignatura."""
    
    def __init__(self, nombre: str, codigo: str):
        self._nombre = nombre
        self._codigo = codigo
        self._grupos: Dict[str, Grupo] = {}
    
    def get_nombre(self) -> str:
        return self._nombre
    
    def get_codigo(self) -> str:
        return self._codigo
    
    def crear_grupo(self, nombre_grupo: str) -> OperationResult:
        if nombre_grupo in self._grupos:
            return OperationResult(
                f"El grupo {nombre_grupo} ya existe en {self._nombre}",
                False
            )
        self._grupos[nombre_grupo] = Grupo(nombre_grupo)
        return OperationResult(
            f"Grupo {nombre_grupo} creado en {self._nombre}",
            True
        )
    
    def obtener_grupo(self, nombre_grupo: str) -> Optional[Grupo]:
        return self._grupos.get(nombre_grupo)
    
    def listar_grupos(self) -> List[str]:
        return list(self._grupos.keys())
    
    def obtener_reporte_asignatura(self) -> str:
        reporte = f"\n{'='*80}\n"
        reporte += f"REPORTE DE ASIGNATURA: {self._nombre} ({self._codigo})\n"
        reporte += f"{'='*80}\n"
        
        if not self._grupos:
            reporte += "No hay grupos creados en esta asignatura\n"
        else:
            for nombre_grupo, grupo in self._grupos.items():
                reporte += grupo.obtener_listado_calificaciones()
                resultado_aprobados = grupo.calcular_porcentaje_aprobados()
                if resultado_aprobados.success:
                    datos = resultado_aprobados.data
                    reporte += (f"Resumen {nombre_grupo}: "
                               f"{datos['aprobados']}/{datos['total']} aprobados "
                               f"({datos['porcentaje']:.2f}%)\n\n")
        
        reporte += f"{'='*80}\n"
        return reporte


class SistemaGestion:
    """Coordina todas las asignaturas del sistema."""
    
    def __init__(self):
        self._asignaturas: Dict[str, Asignatura] = {}
    
    def crear_asignatura(self, nombre: str, codigo: str) -> OperationResult:
        if codigo in self._asignaturas:
            return OperationResult(
                f"La asignatura con código {codigo} ya existe",
                False
            )
        self._asignaturas[codigo] = Asignatura(nombre, codigo)
        return OperationResult(
            f"Asignatura '{nombre}' ({codigo}) creada exitosamente",
            True
        )
    
    def obtener_asignatura(self, codigo: str) -> Optional[Asignatura]:
        return self._asignaturas.get(codigo)
    
    def listar_asignaturas(self) -> List[str]:
        return list(self._asignaturas.keys())
    
    def listar_asignaturas_detallado(self) -> str:
        if not self._asignaturas:
            return "No hay asignaturas creadas en el sistema"
        
        listado = "\nASIGNATURAS DISPONIBLES:\n"
        listado += "-" * 40 + "\n"
        for codigo, asignatura in self._asignaturas.items():
            num_grupos = len(asignatura.listar_grupos())
            listado += f"  {codigo}: {asignatura.get_nombre()} ({num_grupos} grupo(s))\n"
        listado += "-" * 40 + "\n"
        return listado


# INTERFAZ DE USUARIO

class MenuConsola:
    """Interfaz interactiva en consola."""
    
    def __init__(self):
        self.sistema = SistemaGestion()
        self.asignatura_actual: Optional[Asignatura] = None
        self.grupo_actual: Optional[Grupo] = None
    
    def limpiar_pantalla(self):
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def mostrar_titulo(self, titulo: str):
        print(f"\n{'='*60}")
        print(f"  {titulo}")
        print(f"{'='*60}\n")
    
    def mostrar_menu_principal(self):
        self.limpiar_pantalla()
        self.mostrar_titulo("SISTEMA DE GESTIÓN DE ESTUDIANTES")
        print("1. Crear asignatura")
        print("2. Seleccionar asignatura")
        print("3. Listar asignaturas")
        print("4. Ver reporte de asignatura")
        print("5. Salir")
        print()
    
    def mostrar_menu_asignatura(self):
        self.mostrar_titulo(f"ASIGNATURA: {self.asignatura_actual.get_nombre()}")
        print("1. Crear grupo")
        print("2. Seleccionar grupo")
        print("3. Listar grupos")
        print("4. Volver al menú principal")
        print()
    
    def mostrar_menu_grupo(self):
        self.mostrar_titulo(
            f"GRUPO: {self.grupo_actual.get_nombre()} - "
            f"{self.asignatura_actual.get_nombre()}"
        )
        print("1. Agregar estudiante presencial")
        print("2. Agregar estudiante a distancia")
        print("3. Registrar calificación")
        print("4. Ver listado de calificaciones")
        print("5. Ver porcentaje de aprobados")
        print("6. Volver a asignatura")
        print()
    
    def crear_asignatura(self):
        self.mostrar_titulo("CREAR ASIGNATURA")
        nombre = input("Nombre de la asignatura: ").strip()
        if not nombre:
            print("Error: El nombre no puede estar vacío")
            input("Presione Enter para continuar...")
            return
        
        codigo = input("Código de la asignatura: ").strip().upper()
        if not codigo:
            print("Error: El código no puede estar vacío")
            input("Presione Enter para continuar...")
            return
        
        resultado = self.sistema.crear_asignatura(nombre, codigo)
        print(f"\n{resultado}")
        input("Presione Enter para continuar...")
    
    def seleccionar_asignatura(self):
        if not self.sistema.listar_asignaturas():
            print("No hay asignaturas disponibles")
            input("Presione Enter para continuar...")
            return
        
        self.mostrar_titulo("SELECCIONAR ASIGNATURA")
        print(self.sistema.listar_asignaturas_detallado())
        
        codigo = input("Ingrese el código de la asignatura: ").strip().upper()
        asignatura = self.sistema.obtener_asignatura(codigo)
        
        if asignatura:
            self.asignatura_actual = asignatura
            self.grupo_actual = None
            self.menu_asignatura()
        else:
            print(f"Error: Asignatura con código '{codigo}' no encontrada")
            input("Presione Enter para continuar...")
    
    def listar_asignaturas(self):
        self.mostrar_titulo("LISTADO DE ASIGNATURAS")
        print(self.sistema.listar_asignaturas_detallado())
        input("Presione Enter para continuar...")
    
    def ver_reporte_asignatura(self):
        if not self.sistema.listar_asignaturas():
            print("No hay asignaturas disponibles")
            input("Presione Enter para continuar...")
            return
        
        self.mostrar_titulo("SELECCIONAR ASIGNATURA PARA REPORTE")
        print(self.sistema.listar_asignaturas_detallado())
        
        codigo = input("Ingrese el código de la asignatura: ").strip().upper()
        asignatura = self.sistema.obtener_asignatura(codigo)
        
        if asignatura:
            print(asignatura.obtener_reporte_asignatura())
            input("Presione Enter para continuar...")
        else:
            print(f"Error: Asignatura con código '{codigo}' no encontrada")
            input("Presione Enter para continuar...")
    
    def crear_grupo(self):
        self.mostrar_titulo("CREAR GRUPO")
        nombre = input("Nombre del grupo: ").strip()
        if not nombre:
            print("Error: El nombre del grupo no puede estar vacío")
            input("Presione Enter para continuar...")
            return
        
        resultado = self.asignatura_actual.crear_grupo(nombre)
        print(f"\n{resultado}")
        input("Presione Enter para continuar...")
    
    def seleccionar_grupo(self):
        grupos = self.asignatura_actual.listar_grupos()
        if not grupos:
            print("No hay grupos disponibles en esta asignatura")
            input("Presione Enter para continuar...")
            return
        
        self.mostrar_titulo("SELECCIONAR GRUPO")
        for i, nombre_grupo in enumerate(grupos, 1):
            print(f"{i}. {nombre_grupo}")
        print()
        
        try:
            opcion = int(input("Seleccione el número del grupo: "))
            if 1 <= opcion <= len(grupos):
                grupo = self.asignatura_actual.obtener_grupo(grupos[opcion - 1])
                self.grupo_actual = grupo
                self.menu_grupo()
            else:
                print("Opción inválida")
                input("Presione Enter para continuar...")
        except ValueError:
            print("Error: Ingrese un número válido")
            input("Presione Enter para continuar...")
    
    def listar_grupos(self):
        self.mostrar_titulo("GRUPOS DE LA ASIGNATURA")
        grupos = self.asignatura_actual.listar_grupos()
        
        if not grupos:
            print("No hay grupos disponibles")
        else:
            for i, nombre_grupo in enumerate(grupos, 1):
                grupo = self.asignatura_actual.obtener_grupo(nombre_grupo)
                num_estudiantes = len(grupo.obtener_estudiantes())
                print(f"{i}. {nombre_grupo} ({num_estudiantes} estudiante(s))")
        
        print()
        input("Presione Enter para continuar...")
    
    def agregar_estudiante(self, tipo_modalidad: str):
        self.mostrar_titulo(f"AGREGAR ESTUDIANTE {tipo_modalidad.upper()}")
        nombre = input("Nombre del estudiante: ").strip()
        if not nombre:
            print("Error: El nombre no puede estar vacío")
            input("Presione Enter para continuar...")
            return
        
        if tipo_modalidad.lower() == "presencial":
            estudiante = EstudiantePresencial(nombre)
        else:
            estudiante = EstudianteDistancia(nombre)
        
        resultado = self.grupo_actual.agregar_estudiante(estudiante)
        print(f"\n{resultado}")
        print(f"ID del estudiante: {estudiante.get_id()}")
        input("Presione Enter para continuar...")
    
    def registrar_calificacion(self):
        estudiantes = self.grupo_actual.obtener_estudiantes()
        if not estudiantes:
            print("No hay estudiantes en este grupo")
            input("Presione Enter para continuar...")
            return
        
        self.mostrar_titulo("REGISTRAR CALIFICACIÓN")
        print("Estudiantes disponibles:")
        for i, est in enumerate(estudiantes, 1):
            print(f"{i}. {est.get_nombre()} (ID: {est.get_id()})")
        print()
        
        try:
            opcion = int(input("Seleccione el número del estudiante: "))
            if 1 <= opcion <= len(estudiantes):
                estudiante = estudiantes[opcion - 1]
            else:
                print("Opción inválida")
                input("Presione Enter para continuar...")
                return
        except ValueError:
            print("Error: Ingrese un número válido")
            input("Presione Enter para continuar...")
            return
        
        print()
        print("Tipos de calificación disponibles:")
        print("1. Examen")
        print("2. Práctica")
        print()
        
        try:
            opcion_tipo = int(input("Seleccione el tipo de calificación: "))
            tipo = "examen" if opcion_tipo == 1 else "práctica" if opcion_tipo == 2 else None
            if not tipo:
                print("Opción inválida")
                input("Presione Enter para continuar...")
                return
        except ValueError:
            print("Error: Ingrese un número válido")
            input("Presione Enter para continuar...")
            return
        
        try:
            valor = float(input("Valor de la calificación (0-100): "))
            resultado = self.grupo_actual.registrar_calificacion(
                estudiante.get_id(),
                tipo,
                valor
            )
            print(f"\n{resultado}")
        except ValueError:
            print("Error: Ingrese un valor numérico válido")
        
        input("Presione Enter para continuar...")
    
    def ver_listado_calificaciones(self):
        self.mostrar_titulo("LISTADO DE CALIFICACIONES")
        print(self.grupo_actual.obtener_listado_calificaciones())
        input("Presione Enter para continuar...")
    
    def ver_porcentaje_aprobados(self):
        self.mostrar_titulo("PORCENTAJE DE APROBADOS")
        resultado = self.grupo_actual.calcular_porcentaje_aprobados()
        print(f"{resultado}")
        
        if resultado.success:
            datos = resultado.data
            print(f"\nDetalles:")
            print(f"  - Estudiantes aprobados: {datos['aprobados']}")
            print(f"  - Total de estudiantes: {datos['total']}")
            print(f"  - Porcentaje: {datos['porcentaje']}%")
        
        print()
        input("Presione Enter para continuar...")
    
    def menu_grupo(self):
        while True:
            self.mostrar_menu_grupo()
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == "1":
                self.agregar_estudiante("presencial")
            elif opcion == "2":
                self.agregar_estudiante("distancia")
            elif opcion == "3":
                self.registrar_calificacion()
            elif opcion == "4":
                self.ver_listado_calificaciones()
            elif opcion == "5":
                self.ver_porcentaje_aprobados()
            elif opcion == "6":
                break
            else:
                print("Opción no válida. Intente nuevamente.")
                input("Presione Enter para continuar...")
    
    def menu_asignatura(self):
        while True:
            self.mostrar_menu_asignatura()
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == "1":
                self.crear_grupo()
            elif opcion == "2":
                self.seleccionar_grupo()
            elif opcion == "3":
                self.listar_grupos()
            elif opcion == "4":
                self.asignatura_actual = None
                self.grupo_actual = None
                break
            else:
                print("Opción no válida. Intente nuevamente.")
                input("Presione Enter para continuar...")
    
    def menu_principal(self):
        while True:
            self.mostrar_menu_principal()
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == "1":
                self.crear_asignatura()
            elif opcion == "2":
                self.seleccionar_asignatura()
            elif opcion == "3":
                self.listar_asignaturas()
            elif opcion == "4":
                self.ver_reporte_asignatura()
            elif opcion == "5":
                self.mostrar_titulo("SALIENDO DEL SISTEMA")
                print("Gracias por usar el Sistema de Gestión de Estudiantes")
                print("Adiós!")
                break
            else:
                print("Opción no válida. Intente nuevamente.")
                input("Presione Enter para continuar...")
    
    def iniciar(self):
        self.menu_principal()


if __name__ == "__main__":
    aplicacion = MenuConsola()
    aplicacion.iniciar()
