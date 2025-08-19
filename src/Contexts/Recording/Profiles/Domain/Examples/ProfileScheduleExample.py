"""
Ejemplo de uso de las configuraciones de tiempo periódicas para perfiles.
Muestra cómo crear y usar perfiles con configuraciones de horario.
"""

from datetime import datetime, date, time
from src.Contexts.Recording.Profiles.Domain.Entities.Profile import Profile
from src.Contexts.Recording.Profiles.Domain.ValueObjects.DateRangeValueObject import DateRangeValueObject
from src.Contexts.Recording.Profiles.Domain.ValueObjects.WeekDaysValueObject import WeekDaysValueObject
from src.Contexts.Recording.Profiles.Domain.ValueObjects.ScheduleConfigurationValueObject import ScheduleConfigurationValueObject
from src.Contexts.SharedKernel.Domain.ValueObjects.TimeRangeValueObject import TimeRangeValueObject


def create_example_profile():
    """
    Crea un perfil de ejemplo con configuración de horario completa:
    - Del 19 de agosto al 20 de diciembre
    - De 22:00 a 06:00 hs
    - Los lunes, miércoles y jueves
    """
    
    # 1. Crear rango de fechas (del 19 de agosto al 20 de diciembre)
    date_range = DateRangeValueObject(
        start_date=date(2024, 8, 19),
        end_date=date(2024, 12, 20)
    )
    
    # 2. Crear rango de horas (de 22:00 a 06:00)
    time_range = TimeRangeValueObject(
        start_time=(22, 0),  # 22:00
        end_time=(6, 0)      # 06:00
    )
    
    # 3. Crear días de la semana (lunes, miércoles y jueves)
    week_days = WeekDaysValueObject.from_strings(["lunes", "miércoles", "jueves"])
    
    # 4. Crear configuración completa
    schedule_config = ScheduleConfigurationValueObject.create_full_schedule(
        date_range=date_range,
        time_range=time_range,
        week_days=week_days
    )
    
    # 5. Crear el perfil
    profile = Profile(
        id="profile-001",
        name="Perfil de Grabación Nocturno",
        schedule_configuration=schedule_config
    )
    
    return profile


def test_profile_schedule():
    """Prueba las funciones de validación de horario del perfil"""
    profile = create_example_profile()
    
    print(f"Perfil: {profile.name}")
    print(f"Configuración: {profile.schedule_configuration}")
    print("-" * 50)
    
    # Casos de prueba
    test_cases = [
        # Caso 1: Lunes 19 de agosto de 2024 a las 23:00 - DEBERÍA SER ACTIVO
        datetime(2024, 8, 19, 23, 0),
        
        # Caso 2: Martes 20 de agosto de 2024 a las 23:00 - NO ACTIVO (martes)
        datetime(2024, 8, 20, 23, 0),
        
        # Caso 3: Miércoles 21 de agosto de 2024 a las 05:00 - ACTIVO
        datetime(2024, 8, 21, 5, 0),
        
        # Caso 4: Miércoles 21 de agosto de 2024 a las 15:00 - NO ACTIVO (hora)
        datetime(2024, 8, 21, 15, 0),
        
        # Caso 5: Lunes 23 de diciembre de 2024 a las 01:00 - NO ACTIVO (fuera de rango de fecha)
        datetime(2024, 12, 23, 1, 0),
        
        # Caso 6: Jueves 21 de noviembre de 2024 a las 02:00 - ACTIVO
        datetime(2024, 11, 21, 2, 0),
    ]
    
    for i, test_datetime in enumerate(test_cases, 1):
        is_active = profile.is_active_at(test_datetime)
        day_name = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"][test_datetime.weekday()]
        
        print(f"Caso {i}: {day_name} {test_datetime.strftime('%d/%m/%Y %H:%M')}")
        print(f"  ¿Activo?: {'✅ SÍ' if is_active else '❌ NO'}")
        print()


def create_profile_from_microservice_data():
    """
    Ejemplo de cómo crear un perfil desde datos que vienen de otro microservicio
    """
    
    # Simular datos que vienen de otro microservicio
    microservice_data = {
        "id": "profile-002",
        "name": "Perfil de Fin de Semana",
        "schedule_configuration": {
            "date_range": {
                "start_date": "2024-01-01",
                "end_date": "2024-12-31"
            },
            "time_range": [
                [8, 0],   # 08:00
                [20, 0]   # 20:00
            ],
            "week_days": [5, 6]  # Sábado y Domingo
        }
    }
    
    # Crear perfil desde los datos del microservicio
    profile = Profile.from_dict(microservice_data)
    
    print(f"Perfil creado desde microservicio: {profile.name}")
    print(f"Configuración: {profile.schedule_configuration}")
    
    # Probar si está activo un sábado a las 14:00
    test_datetime = datetime(2024, 11, 23, 14, 0)  # Sábado
    is_active = profile.is_active_at(test_datetime)
    print(f"¿Activo el sábado 23/11/2024 a las 14:00?: {'✅ SÍ' if is_active else '❌ NO'}")
    
    return profile


if __name__ == "__main__":
    print("=== EJEMPLO DE CONFIGURACIÓN DE HORARIOS EN PERFILES ===\n")
    
    print("1. Perfil con configuración completa:")
    test_profile_schedule()
    
    print("\n" + "=" * 60 + "\n")
    
    print("2. Perfil desde datos de microservicio:")
    create_profile_from_microservice_data()