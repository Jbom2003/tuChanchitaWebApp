"""
Comando de management para poblar la base de datos con retos financieros
"""
from django.core.management.base import BaseCommand
from myapp.models import Challenge


class Command(BaseCommand):
    help = 'Pobla la base de datos con retos financieros'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando poblacion de retos...'))
        
        retos_data = [
            {
                'title': 'Ahorro Semanal: S/. 50',
                'description': 'Ahorra S/. 50 en una semana. Este reto te ayudará a desarrollar el hábito del ahorro constante.',
                'type': 'ahorro',
                'goal_amount': 50.0,
                'points': 30,
                'duration_days': 7,
                'condition': 'Registra gastos en la categoría "Ahorro" hasta alcanzar S/. 50',
                'is_active': True
            },
            {
                'title': 'Ahorro Mensual: S/. 200',
                'description': 'Ahorra S/. 200 en un mes. Un reto más ambicioso para quienes ya tienen el hábito del ahorro.',
                'type': 'ahorro',
                'goal_amount': 200.0,
                'points': 100,
                'duration_days': 30,
                'condition': 'Registra gastos en la categoría "Ahorro" hasta alcanzar S/. 200',
                'is_active': True
            },
            {
                'title': 'No Gastar en Comida Fuera: 3 Días',
                'description': 'No gastes en comida fuera de casa durante 3 días. Cocina en casa y ahorra dinero.',
                'type': 'no_gastos',
                'goal_amount': 0.0,
                'points': 25,
                'duration_days': 3,
                'condition': 'No registres gastos en la categoría "Comida" durante 3 días',
                'is_active': True
            },
            {
                'title': 'Ahorro Quincenal: S/. 100',
                'description': 'Ahorra S/. 100 en 15 días. Un reto intermedio perfecto para desarrollar disciplina financiera.',
                'type': 'ahorro',
                'goal_amount': 100.0,
                'points': 60,
                'duration_days': 15,
                'condition': 'Registra gastos en la categoría "Ahorro" hasta alcanzar S/. 100',
                'is_active': True
            },
            {
                'title': 'Semana Sin Gastos Innecesarios',
                'description': 'No gastes más de S/. 30 en gastos no esenciales durante 7 días. Enfócate solo en lo necesario.',
                'type': 'no_gastos',
                'goal_amount': 30.0,
                'points': 40,
                'duration_days': 7,
                'condition': 'No gastes más de S/. 30 en gastos no esenciales durante 7 días',
                'is_active': True
            },
        ]
        
        self.stdout.write(self.style.WARNING('Creando retos...'))
        for reto in retos_data:
            obj, created = Challenge.objects.get_or_create(
                title=reto['title'],
                defaults=reto
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  [OK] Creado: {obj.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'  [-] Ya existe: {obj.title}'))
        
        self.stdout.write(self.style.SUCCESS(f'\nTotal retos: {Challenge.objects.count()}'))
        self.stdout.write(self.style.SUCCESS('¡Poblacion de retos completada!'))

