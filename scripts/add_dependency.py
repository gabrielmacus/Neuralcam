#!/usr/bin/env python3
"""
Script para agregar dependencias automáticamente al pyproject.toml
Uso: python scripts/add_dependency.py nombre_paquete [--dev] [--version=">=1.0.0"]
"""

import argparse
import subprocess
import sys
from pathlib import Path

import toml


def load_pyproject():
    """Cargar el archivo pyproject.toml"""
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        print("❌ Error: No se encontró pyproject.toml en el directorio actual")
        sys.exit(1)

    with open(pyproject_path, "r", encoding="utf-8") as f:
        return toml.load(f)


def save_pyproject(data):
    """Guardar los datos al archivo pyproject.toml"""
    with open("pyproject.toml", "w", encoding="utf-8") as f:
        toml.dump(data, f)


def add_dependency(package_name, version="", is_dev=False):
    """Agregar una dependencia al pyproject.toml"""
    data = load_pyproject()

    # Formar el string de la dependencia
    if version:
        dep_string = f"{package_name}{version}"
    else:
        dep_string = package_name

    # Agregar a la sección correspondiente
    if is_dev:
        if "project" not in data:
            data["project"] = {}
        if "optional-dependencies" not in data["project"]:
            data["project"]["optional-dependencies"] = {}
        if "dev" not in data["project"]["optional-dependencies"]:
            data["project"]["optional-dependencies"]["dev"] = []

        dependencies = data["project"]["optional-dependencies"]["dev"]
        section_name = "dependencias de desarrollo"
    else:
        if "project" not in data:
            data["project"] = {}
        if "dependencies" not in data["project"]:
            data["project"]["dependencies"] = []

        dependencies = data["project"]["dependencies"]
        section_name = "dependencias principales"

    # Verificar si ya existe
    for dep in dependencies:
        if dep.startswith(package_name):
            print(f"⚠️  La dependencia '{package_name}' ya existe en {section_name}")
            return False

    # Agregar la nueva dependencia
    dependencies.append(dep_string)
    dependencies.sort()  # Mantener ordenado

    # Guardar cambios
    save_pyproject(data)
    print(f"✅ Agregada '{dep_string}' a {section_name}")
    return True


def install_dependencies(is_dev=False):
    """Instalar las dependencias actualizadas"""
    print("📦 Instalando dependencias...")

    if is_dev:
        cmd = ["pip", "install", "-e", ".[dev]"]
    else:
        cmd = ["pip", "install", "-e", "."]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False


def update_requirements():
    """Actualizar archivos de requirements usando pip-tools"""
    print("📋 Actualizando archivos de requirements...")

    try:
        # Requirements principales
        subprocess.run(
            ["pip-compile", "pyproject.toml"], check=True, capture_output=True, text=True
        )

        # Requirements de desarrollo
        subprocess.run(
            ["pip-compile", "--extra", "dev", "pyproject.toml", "-o", "requirements-dev.txt"],
            check=True,
            capture_output=True,
            text=True,
        )

        print("✅ Archivos de requirements actualizados")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️  pip-tools no disponible o error: {e}")
        return False
    except FileNotFoundError:
        print("⚠️  pip-tools no está instalado")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Agregar dependencias automáticamente al pyproject.toml"
    )
    parser.add_argument("package", help="Nombre del paquete a agregar")
    parser.add_argument("--dev", action="store_true", help="Agregar como dependencia de desarrollo")
    parser.add_argument("--version", default="", help="Especificador de versión (ej: >=1.0.0)")
    parser.add_argument(
        "--no-install", action="store_true", help="No instalar automáticamente las dependencias"
    )
    parser.add_argument(
        "--no-requirements", action="store_true", help="No actualizar archivos de requirements"
    )

    args = parser.parse_args()

    print(f"🔧 Agregando {args.package} al proyecto...")

    # Agregar dependencia
    if not add_dependency(args.package, args.version, args.dev):
        sys.exit(1)

    # Instalar dependencias
    if not args.no_install:
        if not install_dependencies(args.dev):
            sys.exit(1)

    # Actualizar requirements
    if not args.no_requirements:
        update_requirements()

    print("🎉 ¡Dependencia agregada exitosamente!")


if __name__ == "__main__":
    main()
