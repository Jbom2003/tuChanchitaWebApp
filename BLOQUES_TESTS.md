# Bloques de Pruebas Unitarias - Rangos de Líneas

## 1. Autenticación y Gestión de Usuarios

**Líneas: 22-55**

```python
class UserProfileTest(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(
            email='test@example.com',
            password=make_password('securepass123'),
            first_name='Gian',
            last_name='Franco',
            monthly_limit=1000.0,
            points=50,
            trivia_puntaje=200
        )

    def test_user_creation(self):
        """Test que el usuario se crea correctamente"""
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.monthly_limit, 1000.0)
        self.assertEqual(self.user.points, 50)
        self.assertEqual(self.user.trivia_puntaje, 200)
        self.assertEqual(str(self.user), "Gian Franco (test@example.com)")

    def test_user_unique_email(self):
        """Test que el email es único"""
        with self.assertRaises(Exception):
            UserProfile.objects.create(
                email='test@example.com',  # Email duplicado
                password='pass',
                first_name='Test',
                last_name='User'
            )

    def test_password_hashing(self):
        """Test que la contraseña se hashea correctamente"""
        self.assertTrue(check_password('securepass123', self.user.password))
```

---

## 2. Métodos de Pago

**Líneas: 57-90**

```python
class PaymentMethodTest(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(
            email='test2@example.com', 
            password=make_password('pass'),
            first_name='Test',
            last_name='User'
        )
        self.payment = PaymentMethod.objects.create(
            user=self.user,
            tipo=1,  # Crédito
            sistema_de_pago=2,  # Mastercard
            banco='BCP',
            ultimos_4_digitos='1234',
            mes_vencimiento=12,
            anio_vencimiento=2030
        )

    def test_payment_creation(self):
        """Test creación de método de pago"""
        self.assertEqual(self.payment.user, self.user)
        self.assertEqual(self.payment.banco, 'BCP')
        self.assertEqual(self.payment.ultimos_4_digitos, '1234')

    def test_payment_str(self):
        """Test representación string del método de pago"""
        self.assertIn('****1234', str(self.payment))
        self.assertIn('BCP', str(self.payment))

    def test_payment_choices(self):
        """Test que las opciones de tipo y sistema funcionan"""
        self.assertEqual(self.payment.get_tipo_display(), 'Crédito')
        self.assertEqual(self.payment.get_sistema_de_pago_display(), 'Mastercard')
```

---

## 3. Gestión de Gastos

**Líneas: 92-130**

```python
class ExpenseTest(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(
            email='test3@example.com', 
            password=make_password('pass'),
            first_name='Test',
            last_name='User'
        )
        self.payment = PaymentMethod.objects.create(
            user=self.user, tipo=1, sistema_de_pago=1,
            banco='Interbank', ultimos_4_digitos='5678',
            mes_vencimiento=1, anio_vencimiento=2030
        )
        self.expense = Expense.objects.create(
            user=self.user,
            amount=250.5,
            category='Comida',
            payment_method=self.payment,
            store_name='Norkys'
        )

    def test_expense_creation(self):
        """Test creación de gasto"""
        self.assertEqual(self.expense.amount, 250.5)
        self.assertEqual(self.expense.category, 'Comida')
        self.assertEqual(self.expense.user, self.user)

    def test_expense_str(self):
        """Test representación string del gasto"""
        expected = "Comida - S/.250.5 en Norkys"
        self.assertEqual(str(self.expense), expected)

    def test_expense_categories(self):
        """Test que las categorías están disponibles"""
        categories = [choice[0] for choice in Expense.CATEGORIAS]
        self.assertIn('Comida', categories)
        self.assertIn('Educación', categories)
        self.assertIn('Ahorro', categories)
```

---

## 4. Gestión de Inversiones

**Líneas: 132-187**

```python
class InvestmentTest(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(
            email='test4@example.com', 
            password=make_password('pass'),
            first_name='Test',
            last_name='User'
        )
        self.investment = Investment.objects.create(
            user=self.user,
            company='Apple Inc.',
            symbol='AAPL',
            shares=5.0,
            price_at_purchase=150.0
        )

    def test_investment_creation(self):
        """Test creación de inversión"""
        self.assertEqual(self.investment.company, 'Apple Inc.')
        self.assertEqual(self.investment.symbol, 'AAPL')
        self.assertEqual(self.investment.shares, 5.0)

    def test_total_invested(self):
        """Test cálculo del total invertido"""
        self.assertEqual(self.investment.total_invested(), 750.0)

    @patch('requests.get')
    def test_get_current_price(self, mock_get):
        """Test obtención del precio actual"""
        mock_response = MagicMock()
        mock_response.json.return_value = {'price': '175.50'}
        mock_get.return_value = mock_response
        
        price = self.investment.get_current_price()
        self.assertEqual(price, 175.50)

    @patch('requests.get')
    def test_current_value(self, mock_get):
        """Test cálculo del valor actual"""
        mock_response = MagicMock()
        mock_response.json.return_value = {'price': '175.50'}
        mock_get.return_value = mock_response
        
        current_value = self.investment.current_value()
        self.assertEqual(current_value, 877.5)  # 5 * 175.50

    @patch('requests.get')
    def test_profit_loss(self, mock_get):
        """Test cálculo de ganancia/pérdida"""
        mock_response = MagicMock()
        mock_response.json.return_value = {'price': '175.50'}
        mock_get.return_value = mock_response
        
        profit = self.investment.profit_loss()
        self.assertEqual(profit, 127.5)  # 877.5 - 750.0
```

---

## 5. Sistema de Retos (Gamificación)

**Líneas: 189-258**

```python
class ChallengeTest(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(
            email='test5@example.com',
            password=make_password('pass'),
            first_name='Test',
            last_name='User',
            points=100
        )
        self.challenge_ahorro = Challenge.objects.create(
            title='Reto de Ahorro',
            description='Ahorra S/.100 en 7 días',
            type='ahorro',
            goal_amount=100.0,
            points=50,
            duration_days=7,
            condition='Ahorra mínimo S/.100'
        )
        self.challenge_no_gastos = Challenge.objects.create(
            title='No Gastar',
            description='No gastes más de S/.50 en 3 días',
            type='no_gastos',
            goal_amount=50.0,
            points=30,
            duration_days=3,
            condition='No gastar más de S/.50'
        )

    def test_challenge_creation(self):
        """Test creación de reto"""
        self.assertEqual(str(self.challenge_ahorro), 'Reto de Ahorro')
        self.assertEqual(self.challenge_ahorro.type, 'ahorro')
        self.assertEqual(self.challenge_ahorro.goal_amount, 100.0)

    def test_user_challenge_creation(self):
        """Test creación de reto de usuario"""
        user_challenge = UserChallenge.objects.create(
            user=self.user,
            challenge=self.challenge_ahorro
        )
        self.assertEqual(user_challenge.user, self.user)
        self.assertEqual(user_challenge.challenge, self.challenge_ahorro)
        self.assertFalse(user_challenge.completed)
        self.assertFalse(user_challenge.failed)

    def test_challenge_completion_ahorro(self):
        """Test completar reto de ahorro"""
        user_challenge = UserChallenge.objects.create(
            user=self.user,
            challenge=self.challenge_ahorro,
            start_date=timezone.now() - timedelta(days=1)
        )
        
        # Crear gasto de ahorro
        Expense.objects.create(
            user=self.user,
            amount=150.0,
            category='Ahorro',
            store_name='Banco',
            date=timezone.now()
        )
        
        # Simular verificación del reto
        user_challenge.check_status()
        user_challenge.refresh_from_db()
        self.user.refresh_from_db()
        
        self.assertTrue(user_challenge.completed)
        self.assertEqual(user_challenge.earned_points, 50)
```

---

## 6. Sistema de Trivia (Gamificación)

**Líneas: 260-313**

```python
class TriviaTest(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(
            email='test6@example.com',
            password=make_password('pass'),
            first_name='Test',
            last_name='User'
        )
        self.question = TriviaQuestion.objects.create(
            pregunta="¿Cuánto es 2+2?",
            puntos=10
        )
        self.option_correct = TriviaOption.objects.create(
            pregunta=self.question,
            texto="4",
            es_correcta=True
        )
        self.option_wrong = TriviaOption.objects.create(
            pregunta=self.question,
            texto="5",
            es_correcta=False
        )
        self.pregunta_trivia = PreguntaTrivia.objects.create(
            pregunta="¿Qué es el interés compuesto?",
            opciones={"a": "Interés simple", "b": "Interés sobre interés", "c": "Sin interés"},
            respuesta_correcta="b"
        )

    def test_trivia_question_creation(self):
        """Test creación de pregunta de trivia"""
        self.assertEqual(str(self.question), "¿Cuánto es 2+2?")
        self.assertEqual(self.question.puntos, 10)

    def test_trivia_options(self):
        """Test opciones de trivia"""
        self.assertEqual(str(self.option_correct), "4")
        self.assertTrue(self.option_correct.es_correcta)
        self.assertFalse(self.option_wrong.es_correcta)

    def test_pregunta_trivia_model(self):
        """Test modelo PreguntaTrivia"""
        self.assertEqual(str(self.pregunta_trivia), "¿Qué es el interés compuesto?")
        self.assertEqual(self.pregunta_trivia.respuesta_correcta, "b")

    def test_puntaje_trivia_creation(self):
        """Test creación de puntaje de trivia"""
        puntaje = PuntajeTrivia.objects.create(
            user=self.user,
            puntaje_total=500,
            intentos=3
        )
        self.assertEqual(puntaje.puntaje_total, 500)
        self.assertEqual(puntaje.intentos, 3)
```

---

## 7. Validación de Formularios

**Líneas: 315-430**

```python
class FormsTest(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(
            email='test@example.com',
            password=make_password('pass'),
            first_name='Test',
            last_name='User'
        )

    def test_login_form_valid(self):
        """Test formulario de login válido"""
        form_data = {
            'email': 'test@example.com',
            'password': 'password123'
        }
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form_invalid(self):
        """Test formulario de login inválido"""
        form_data = {
            'email': 'invalid-email',
            'password': ''
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())

    @patch('requests.get')
    def test_register_form_valid(self, mock_get):
        """Test formulario de registro válido"""
        # Mock de la API de validación de email
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'is_valid_format': {'value': True},
            'is_disposable_email': {'value': False},
            'deliverability': 'DELIVERABLE'
        }
        mock_get.return_value = mock_response
        
        form_data = {
            'email': 'nuevo@example.com',
            'password': 'Password123!',
            'first_name': 'Nuevo',
            'last_name': 'Usuario'
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_expense_form_valid(self):
        """Test formulario de gastos válido"""
        payment_method = PaymentMethod.objects.create(
            user=self.user,
            tipo=1,
            sistema_de_pago=1,
            banco='BCP',
            ultimos_4_digitos='1234',
            mes_vencimiento=12,
            anio_vencimiento=2025
        )
        
        form_data = {
            'amount': 100.50,
            'category': 'Comida',
            'payment_method': payment_method.id,
            'date': date.today(),
            'store_name': 'Restaurant'
        }
        form = ExpenseForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())

    def test_payment_method_form_valid(self):
        """Test formulario de método de pago válido"""
        form_data = {
            'tipo': 1,
            'sistema_de_pago': 1,
            'banco': 'BCP',
            'ultimos_4_digitos': '5678',
            'mes_vencimiento': 12,
            'anio_vencimiento': 2025
        }
        form = PaymentMethodForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_investment_form_valid(self):
        """Test formulario de inversión válido"""
        form_data = {
            'company': 'AAPL',
            'shares': 5.5
        }
        form = InvestmentForm(data=form_data)
        self.assertTrue(form.is_valid())
```

---

## 8. Pruebas de Vistas (Views)

**Líneas: 432-581**

```python
class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserProfile.objects.create(
            email='test@example.com',
            password=make_password('testpass123'),
            first_name='Test',
            last_name='User',
            monthly_limit=1000.0
        )

    def test_register_view_get(self):
        """Test vista de registro GET"""
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')

    @patch('requests.get')
    @patch('django.core.mail.send_mail')
    def test_register_view_post_valid(self, mock_send_mail, mock_get):
        """Test vista de registro POST válido"""
        # Mock de la API de validación de email
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'is_valid_format': {'value': True},
            'is_disposable_email': {'value': False},
            'deliverability': 'DELIVERABLE'
        }
        mock_get.return_value = mock_response
        mock_send_mail.return_value = True
        
        response = self.client.post('/register/', {
            'email': 'nuevo@example.com',
            'password': 'Newpass123!',
            'first_name': 'Nuevo',
            'last_name': 'Usuario'
        })
        
        # Verificar redirección al dashboard
        self.assertEqual(response.status_code, 302)
        
        # Verificar que el usuario fue creado
        user_exists = UserProfile.objects.filter(email='nuevo@example.com').exists()
        self.assertTrue(user_exists)

    def test_login_view_post_valid(self):
        """Test vista de login POST válido"""
        response = self.client.post('/login/', {
            'email': 'test@example.com',
            'password': 'testpass123'
        })
        
        # Verificar redirección al dashboard
        self.assertEqual(response.status_code, 302)
        
        # Verificar que la sesión fue creada
        self.assertIn('user_id', self.client.session)

    def test_login_view_post_invalid(self):
        """Test vista de login POST inválido"""
        response = self.client.post('/login/', {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })
        
        # No debe redirigir
        self.assertEqual(response.status_code, 200)
        
        # No debe crear sesión
        self.assertNotIn('user_id', self.client.session)

    def test_dashboard_view_authenticated(self):
        """Test vista de dashboard con usuario autenticado"""
        # Simular sesión
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()
        
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.first_name)

    def test_dashboard_view_unauthenticated(self):
        """Test vista de dashboard sin autenticación"""
        response = self.client.get('/dashboard/')
        # Debe redirigir o dar error 500 (dependiendo de tu implementación)
        self.assertIn(response.status_code, [302, 500])

    def test_logout_view(self):
        """Test vista de logout"""
        # Crear sesión
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()
        
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)
        
        # Verificar que la sesión fue eliminada
        self.assertNotIn('user_id', self.client.session)

    def test_profile_view(self):
        """Test vista de perfil"""
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()
        
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)

    @patch('requests.get')
    def test_investment_view_with_api(self, mock_get):
        """Test vista de inversiones con API mock"""
        mock_response = MagicMock()
        mock_response.json.return_value = {'price': '150.00'}
        mock_get.return_value = mock_response
        
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()
        
        response = self.client.post('/inversiones/', {
            'company': 'AAPL',
            'shares': 2.5
        })
        
        # Verificar que la inversión fue creada
        investment_exists = Investment.objects.filter(user=self.user).exists()
        self.assertTrue(investment_exists)
```

---

## 9. Pruebas de Integración

**Líneas: 583-696**

```python
class IntegrationTest(TestCase):
    """Tests de integración que prueban flujos completos"""
    
    def setUp(self):
        self.client = Client()
        self.user = UserProfile.objects.create(
            email='integration@example.com',
            password=make_password('testpass123'),
            first_name='Integration',
            last_name='Test',
            monthly_limit=2000.0
        )

    @patch('requests.get')
    @patch('django.core.mail.send_mail')
    def test_complete_user_flow(self, mock_send_mail, mock_get):
        """Test flujo completo: registro, login, agregar tarjeta, registrar gasto"""
        # Mock de la API de validación de email
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'is_valid_format': {'value': True},
            'is_disposable_email': {'value': False},
            'deliverability': 'DELIVERABLE'
        }
        mock_get.return_value = mock_response
        mock_send_mail.return_value = True
        
        # 1. Registro de usuario
        response = self.client.post('/register/', {
            'email': 'newuser@example.com',
            'password': 'Newpass123!',
            'first_name': 'New',
            'last_name': 'User'
        })
        self.assertEqual(response.status_code, 302)

        # 2. Login
        response = self.client.post('/login/', {
            'email': 'newuser@example.com',
            'password': 'Newpass123!'
        })
        self.assertEqual(response.status_code, 302)
        
        # Verificar que la sesión fue creada
        self.assertIn('user_id', self.client.session)

        # 3. Agregar método de pago
        response = self.client.post('/add-card/', {
            'tipo': 1,
            'sistema_de_pago': 1,
            'banco': 'Test Bank',
            'ultimos_4_digitos': '9999',
            'mes_vencimiento': 12,
            'anio_vencimiento': 2025
        })
        self.assertEqual(response.status_code, 302)

        # 4. Verificar que la tarjeta fue creada
        user = UserProfile.objects.get(email='newuser@example.com')
        payment_methods = PaymentMethod.objects.filter(user=user)
        self.assertEqual(payment_methods.count(), 1)

        # 5. Registrar gasto
        payment_method = payment_methods.first()
        response = self.client.post('/register-expense/', {
            'amount': 50.0,
            'category': 'Comida',
            'payment_method': payment_method.id,
            'date': date.today(),
            'store_name': 'Test Store'
        })
        self.assertEqual(response.status_code, 302)

        # 6. Verificar que el gasto fue registrado
        expenses = Expense.objects.filter(user=user)
        self.assertEqual(expenses.count(), 1)
        self.assertEqual(expenses.first().amount, 50.0)

    def test_challenge_completion_flow(self):
        """Test flujo completo de reto"""
        
        # Crear reto de ahorro
        challenge = Challenge.objects.create(
            title='Test Saving Challenge',
            description='Save S/.200 in 7 days',
            type='ahorro',
            goal_amount=200.0,
            points=100,
            duration_days=7,
            condition='Save at least S/.200'
        )

        # Usuario se une al reto
        user_challenge = UserChallenge.objects.create(
            user=self.user,
            challenge=challenge,
            start_date=timezone.now() - timedelta(days=1)
        )

        # Usuario hace gastos de ahorro
        Expense.objects.create(
            user=self.user,
            amount=250.0,
            category='Ahorro',
            store_name='Bank',
            date=timezone.now()
        )

        # Verificar estado del reto
        user_challenge.check_status()
        user_challenge.refresh_from_db()
        self.user.refresh_from_db()

        # El reto debe estar completado
        self.assertTrue(user_challenge.completed)
        self.assertEqual(user_challenge.earned_points, 100)
```

---

## 10. Pruebas de Utilidad

**Líneas: 698-725**

```python
class UtilityTest(TestCase):
    """Tests para funciones de utilidad"""
    
    def test_password_hashing(self):
        """Test que las contraseñas se hashean correctamente"""
        password = 'testpass123'
        hashed = make_password(password)
        
        self.assertNotEqual(password, hashed)
        self.assertTrue(check_password(password, hashed))
        self.assertFalse(check_password('wrongpass', hashed))

    def test_date_calculations(self):
        """Test cálculos de fechas"""
        today = date.today()
        week_ago = today - timedelta(days=7)
        
        self.assertEqual((today - week_ago).days, 7)

    def test_money_calculations(self):
        """Test cálculos monetarios"""
        amount1 = 123.45
        amount2 = 67.89
        total = amount1 + amount2
        
        self.assertEqual(round(total, 2), 191.34)
```

---

## 11. Pruebas Adicionales de Vistas

**Líneas: 728-1110**

```python
class AdditionalViewsTest(TestCase):
    """Tests adicionales para vistas que no están cubiertas"""
    
    def setUp(self):
        self.client = Client()
        self.user = UserProfile.objects.create(
            email='test@example.com',
            password=make_password('Testpass123!'),
            first_name='Test',
            last_name='User',
            monthly_limit=1000.0
        )
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

    def test_upload_profile_photo_get(self):
        """Test GET de upload_profile_photo"""
        response = self.client.get('/upload-profile-photo/')
        self.assertEqual(response.status_code, 302)

    def test_upload_profile_photo_post(self):
        """Test POST de upload_profile_photo con archivo"""
        # ... código de prueba con imagen ...

    def test_update_limit_view_get(self):
        """Test GET de update_limit_view"""
        # ... código de prueba ...

    def test_update_limit_view_post(self):
        """Test POST de update_limit_view"""
        # ... código de prueba ...

    def test_add_card_view_get(self):
        """Test GET de add_card_view"""
        # ... código de prueba ...

    def test_add_card_view_post(self):
        """Test POST de add_card_view"""
        # ... código de prueba ...

    def test_register_expense_view_get(self):
        """Test GET de register_expense_view"""
        # ... código de prueba ...

    def test_register_expense_view_post(self):
        """Test POST de register_expense_view"""
        # ... código de prueba ...

    def test_reports_view(self):
        """Test reports_view"""
        # ... código de prueba ...

    @patch('xhtml2pdf.pisa.CreatePDF')
    def test_export_pdf_view(self, mock_pdf):
        """Test export_pdf_view"""
        # ... código de prueba ...

    def test_recommendations_view(self):
        """Test recommendations_view"""
        # ... código de prueba ...

    @patch('myapp.views.client')
    def test_chatbot_view_get(self, mock_client):
        """Test GET de chatbot_view"""
        # ... código de prueba ...

    @patch('myapp.views.client')
    def test_chatbot_view_post(self, mock_client):
        """Test POST de chatbot_view"""
        # ... código de prueba ...

    def test_retos_view_get(self):
        """Test GET de retos_view"""
        # ... código de prueba ...

    def test_retos_view_post(self):
        """Test POST de retos_view (unirse a reto)"""
        # ... código de prueba ...

    def test_historial_retos_view(self):
        """Test historial_retos_view"""
        # ... código de prueba ...

    def test_trivia_view_get(self):
        """Test GET de trivia_view"""
        # ... código de prueba ...

    def test_trivia_view_post_correct(self):
        """Test POST de trivia_view con respuesta correcta"""
        # ... código de prueba ...

    def test_trivia_view_post_incorrect(self):
        """Test POST de trivia_view con respuesta incorrecta"""
        # ... código de prueba ...

    def test_ranking_trivia_view(self):
        """Test ranking_trivia_view"""
        # ... código de prueba ...

    @patch('django.core.mail.send_mail')
    def test_solicitar_reset_contrasena_post(self, mock_send_mail):
        """Test POST de solicitar_reset_contrasena"""
        # ... código de prueba ...

    def test_solicitar_reset_contrasena_get(self):
        """Test GET de solicitar_reset_contrasena"""
        # ... código de prueba ...

    def test_resetear_contrasena_get_valid_token(self):
        """Test GET de resetear_contrasena con token válido"""
        # ... código de prueba ...

    def test_resetear_contrasena_post_valid(self):
        """Test POST de resetear_contrasena con datos válidos"""
        # ... código de prueba ...

    def test_delete_card(self):
        """Test delete_card"""
        # ... código de prueba ...

    @patch('requests.get')
    def test_delete_investment_view(self, mock_get):
        """Test delete_investment_view"""
        # ... código de prueba ...

    def test_delete_investment_view_not_owner(self):
        """Test delete_investment_view con inversión que no pertenece al usuario"""
        # ... código de prueba ...
```

---

## 12. Pruebas Adicionales de Modelos

**Líneas: 1111-1274**

```python
class AdditionalModelsTest(TestCase):
    """Tests adicionales para modelos"""
    
    def setUp(self):
        self.user = UserProfile.objects.create(
            email='test@example.com',
            password=make_password('Testpass123!'),
            first_name='Test',
            last_name='User'
        )

    def test_recommendation_video_creation(self):
        """Test creación de RecommendationVideo"""
        video = RecommendationVideo.objects.create(
            titulo='Test Video',
            descripcion='Test Description',
            url_video='https://youtube.com/test'
        )
        self.assertEqual(str(video), 'Test Video')

    def test_trivia_respuesta_usuario_creation(self):
        """Test creación de TriviaRespuestaUsuario"""
        # ... código de prueba ...

    def test_user_challenge_check_status_already_completed(self):
        """Test check_status cuando ya está completado"""
        # ... código de prueba ...

    def test_user_challenge_check_status_expired(self):
        """Test check_status cuando el reto expiró"""
        # ... código de prueba ...

    def test_user_challenge_check_status_ahorro(self):
        """Test check_status de UserChallenge para reto de ahorro"""
        # ... código de prueba ...

    def test_investment_str(self):
        """Test __str__ de Investment"""
        # ... código de prueba ...

    def test_investment_current_value_none(self):
        """Test current_value cuando la API no devuelve precio"""
        # ... código de prueba ...

    def test_investment_profit_loss_none(self):
        """Test profit_loss cuando current_value es None"""
        # ... código de prueba ...
```

---

## 13. Pruebas Adicionales de Formularios

**Líneas: 1275-1524**

```python
class AdditionalFormsTest(TestCase):
    """Tests adicionales para formularios"""
    
    def setUp(self):
        self.user = UserProfile.objects.create(
            email='test@example.com',
            password=make_password('Testpass123!'),
            first_name='Test',
            last_name='User',
            monthly_limit=1000.0
        )

    def test_update_limit_form_valid(self):
        """Test UpdateLimitForm válido"""
        # ... código de prueba ...

    def test_update_limit_form_invalid_negative(self):
        """Test UpdateLimitForm con valor negativo"""
        # ... código de prueba ...

    def test_monthly_limit_form_valid(self):
        """Test MonthlyLimitForm válido"""
        # ... código de prueba ...

    @patch('requests.get')
    def test_register_form_invalid_email_format(self, mock_get):
        """Test RegisterForm con email de formato inválido"""
        # ... código de prueba ...

    @patch('requests.get')
    def test_register_form_deliverability_not_deliverable(self, mock_get):
        """Test RegisterForm con deliverability != DELIVERABLE"""
        # ... código de prueba ...

    @patch('requests.get')
    def test_register_form_disposable_email(self, mock_get):
        """Test RegisterForm con email desechable"""
        # ... código de prueba ...

    def test_register_form_password_too_short(self):
        """Test RegisterForm con contraseña muy corta"""
        # ... código de prueba ...

    def test_register_form_password_no_uppercase(self):
        """Test RegisterForm sin mayúscula"""
        # ... código de prueba ...

    def test_register_form_password_no_number(self):
        """Test RegisterForm sin número"""
        # ... código de prueba ...

    def test_register_form_password_no_special(self):
        """Test RegisterForm sin carácter especial"""
        # ... código de prueba ...

    def test_register_form_invalid_first_name(self):
        """Test RegisterForm con nombre inválido"""
        # ... código de prueba ...

    def test_register_form_invalid_last_name(self):
        """Test RegisterForm con apellido inválido"""
        # ... código de prueba ...

    def test_payment_method_form_invalid_digits(self):
        """Test PaymentMethodForm con dígitos inválidos"""
        # ... código de prueba ...

    def test_payment_method_form_digits_wrong_length(self):
        """Test PaymentMethodForm con dígitos de longitud incorrecta"""
        # ... código de prueba ...

    def test_payment_method_form_mes_none(self):
        """Test PaymentMethodForm con mes None"""
        # ... código de prueba ...

    def test_payment_method_form_anio_none(self):
        """Test PaymentMethodForm con año None"""
        # ... código de prueba ...

    def test_payment_method_form_expired_card_clean(self):
        """Test PaymentMethodForm con tarjeta vencida en clean"""
        # ... código de prueba ...

    def test_payment_method_form_invalid_month(self):
        """Test PaymentMethodForm con mes inválido"""
        # ... código de prueba ...

    def test_payment_method_form_expired_card(self):
        """Test PaymentMethodForm con tarjeta vencida"""
        # ... código de prueba ...
```

---

## 14. Pruebas de Casos Edge

**Líneas: 1525-1716**

```python
class EdgeCasesTest(TestCase):
    """Tests para casos edge y errores"""
    
    def setUp(self):
        self.client = Client()
        self.user = UserProfile.objects.create(
            email='test@example.com',
            password=make_password('Testpass123!'),
            first_name='Test',
            last_name='User'
        )

    def test_login_blocked_user(self):
        """Test login con usuario bloqueado"""
        # ... código de prueba ...

    def test_login_multiple_attempts(self):
        """Test login con múltiples intentos fallidos"""
        # ... código de prueba ...

    def test_login_user_not_exists(self):
        """Test login con usuario que no existe"""
        # ... código de prueba ...

    def test_profile_view_no_session(self):
        """Test profile_view sin sesión"""
        # ... código de prueba ...

    def test_dashboard_view_no_expenses(self):
        """Test dashboard_view sin gastos"""
        # ... código de prueba ...

    def test_register_expense_no_payment_methods(self):
        """Test register_expense_view sin métodos de pago"""
        # ... código de prueba ...

    def test_resetear_contrasena_passwords_dont_match(self):
        """Test resetear_contrasena con contraseñas que no coinciden"""
        # ... código de prueba ...

    def test_resetear_contrasena_same_password(self):
        """Test resetear_contrasena con la misma contraseña"""
        # ... código de prueba ...

    def test_trivia_no_questions(self):
        """Test trivia_view sin preguntas disponibles"""
        # ... código de prueba ...

    def test_trivia_three_failures(self):
        """Test trivia_view con 3 fallos"""
        # ... código de prueba ...

    @patch('requests.get')
    def test_investment_view_api_error(self, mock_get):
        """Test investment_view con error de API"""
        # ... código de prueba ...

    def test_retos_view_challenge_already_joined(self):
        """Test retos_view uniéndose a reto ya unido"""
        # ... código de prueba ...
```

---

## 15. Pruebas de Decoradores

**Líneas: 1717-1743**

```python
class DecoratorTest(TestCase):
    """Tests para decoradores"""
    
    def setUp(self):
        self.client = Client()

    def test_session_login_required_with_session(self):
        """Test session_login_required con sesión válida"""
        user = UserProfile.objects.create(
            email='test@example.com',
            password=make_password('Testpass123!'),
            first_name='Test',
            last_name='User'
        )
        session = self.client.session
        session['user_id'] = user.id
        session.save()
        
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)

    def test_session_login_required_without_session(self):
        """Test session_login_required sin sesión"""
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 302)
```

---

## 16. Pruebas de Funciones Auxiliares

**Líneas: 1744-1833**

```python
class FunctionTest(TestCase):
    """Tests para funciones auxiliares"""
    
    def setUp(self):
        self.user = UserProfile.objects.create(
            email='test@example.com',
            password=make_password('Testpass123!'),
            first_name='Test',
            last_name='User'
        )

    def test_actualizar_retos_usuario_no_gastos(self):
        """Test actualizar_retos_usuario sin gastos"""
        # ... código de prueba ...

    def test_actualizar_retos_usuario_no_gastos_type(self):
        """Test actualizar_retos_usuario para reto no_gastos"""
        # ... código de prueba ...

    def test_actualizar_retos_usuario_expired(self):
        """Test actualizar_retos_usuario con reto expirado"""
        # ... código de prueba ...
```

---

## 17. Pruebas Adicionales de Cobertura

**Líneas: 1834-2766**

```python
class AdditionalCoverageTest(TestCase):
    """Tests adicionales para aumentar cobertura de views.py"""
    
    def setUp(self):
        self.client = Client()
        self.user = UserProfile.objects.create(
            email='test@example.com',
            password=make_password('Testpass123!'),
            first_name='Test',
            last_name='User',
            monthly_limit=1000.0
        )
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

    @patch('requests.get')
    def test_register_view_post_invalid(self, mock_get):
        """Test register_view POST con formulario inválido"""
        # ... código de prueba ...

    def test_login_view_get(self):
        """Test login_view GET"""
        # ... código de prueba ...

    def test_login_view_post_invalid_form(self):
        """Test login_view POST con formulario inválido"""
        # ... código de prueba ...

    def test_register_view_get(self):
        """Test register_view GET"""
        # ... código de prueba ...

    def test_investment_view_get(self):
        """Test investment_view GET"""
        # ... código de prueba ...

    @patch('requests.get')
    def test_investment_view_post_no_price(self, mock_get):
        """Test investment_view POST sin precio en respuesta"""
        # ... código de prueba ...

    @patch('requests.get')
    def test_investment_view_post_valid_with_price(self, mock_get):
        """Test investment_view POST válido con precio"""
        # ... código de prueba ...

    def test_chatbot_view_no_message(self):
        """Test chatbot_view POST sin mensaje"""
        # ... código de prueba ...

    @patch('myapp.views.client')
    def test_chatbot_view_exception(self, mock_client):
        """Test chatbot_view con excepción en OpenAI"""
        # ... código de prueba ...

    @patch('xhtml2pdf.pisa.CreatePDF')
    def test_export_pdf_view_error(self, mock_pdf):
        """Test export_pdf_view con error en generación PDF"""
        # ... código de prueba ...

    def test_resetear_contrasena_password_too_short(self):
        """Test resetear_contrasena con contraseña muy corta"""
        # ... código de prueba ...

    def test_upload_profile_photo_no_file(self):
        """Test upload_profile_photo POST sin archivo"""
        # ... código de prueba ...

    def test_upload_profile_photo_with_existing_photo(self):
        """Test upload_profile_photo cuando ya existe una foto"""
        # ... código de prueba ...

    def test_retos_view_challenge_completed_during_view(self):
        """Test retos_view cuando un reto se completa durante la vista"""
        # ... código de prueba ...

    def test_retos_view_challenge_failed_during_view(self):
        """Test retos_view cuando un reto falla durante la vista"""
        # ... código de prueba ...

    def test_trivia_view_all_questions_answered(self):
        """Test trivia_view cuando todas las preguntas fueron respondidas"""
        # ... código de prueba ...

    def test_actualizar_retos_usuario_no_retos(self):
        """Test actualizar_retos_usuario sin retos activos"""
        # ... código de prueba ...

    def test_actualizar_retos_usuario_reto_expired_ahorro(self):
        """Test actualizar_retos_usuario con reto de ahorro expirado"""
        # ... código de prueba ...

    def test_actualizar_retos_usuario_reto_expired_no_gastos(self):
        """Test actualizar_retos_usuario con reto no_gastos expirado"""
        # ... código de prueba ...

    def test_actualizar_retos_usuario_ahorro_insuficiente(self):
        """Test actualizar_retos_usuario con ahorro insuficiente pero no expirado"""
        # ... código de prueba ...

    def test_actualizar_retos_usuario_no_gastos_under_limit(self):
        """Test actualizar_retos_usuario con reto no_gastos bajo el límite"""
        # ... código de prueba ...

    def test_retos_view_exclude_completed_failed(self):
        """Test retos_view excluyendo retos completados y fallidos"""
        # ... código de prueba ...

    def test_historial_retos_view_empty(self):
        """Test historial_retos_view sin historial"""
        # ... código de prueba ...

    def test_ranking_trivia_view_empty(self):
        """Test ranking_trivia_view sin usuarios"""
        # ... código de prueba ...

    def test_register_expense_view_post_invalid(self):
        """Test register_expense_view POST con formulario inválido"""
        # ... código de prueba ...

    def test_add_card_view_post_invalid(self):
        """Test add_card_view POST con formulario inválido"""
        # ... código de prueba ...

    def test_update_limit_view_post_invalid(self):
        """Test update_limit_view POST con formulario inválido"""
        # ... código de prueba ...

    @patch('requests.get')
    @patch('django.core.mail.send_mail')
    def test_register_view_send_mail_exception(self, mock_send_mail, mock_get):
        """Test register_view cuando send_mail lanza excepción"""
        # ... código de prueba ...

    def test_trivia_view_pregunta_does_not_exist(self):
        """Test trivia_view cuando la pregunta no existe"""
        # ... código de prueba ...

    def test_trivia_view_pregunta_id_not_in_respondidas(self):
        """Test trivia_view cuando pregunta_id no está en preguntas_respondidas"""
        # ... código de prueba ...

    def test_retos_view_no_gastos_no_expenses(self):
        """Test retos_view con reto no_gastos sin gastos"""
        # ... código de prueba ...

    def test_retos_view_no_gastos_expired(self):
        """Test retos_view con reto no_gastos expirado"""
        # ... código de prueba ...

    # ... más métodos de prueba ...
```

---

## 18. Bloque Principal (Main)

**Líneas: 2767-2769**

```python
if __name__ == '__main__':
    import unittest
    unittest.main()
```

---

## Resumen de Rangos

| Bloque | Líneas | Descripción |
|--------|--------|-------------|
| 1. Autenticación y Gestión de Usuarios | 22-55 | UserProfileTest |
| 2. Métodos de Pago | 57-90 | PaymentMethodTest |
| 3. Gestión de Gastos | 92-130 | ExpenseTest |
| 4. Gestión de Inversiones | 132-187 | InvestmentTest |
| 5. Sistema de Retos | 189-258 | ChallengeTest |
| 6. Sistema de Trivia | 260-313 | TriviaTest |
| 7. Validación de Formularios | 315-430 | FormsTest |
| 8. Pruebas de Vistas | 432-581 | ViewsTest |
| 9. Pruebas de Integración | 583-696 | IntegrationTest |
| 10. Pruebas de Utilidad | 698-725 | UtilityTest |
| 11. Pruebas Adicionales de Vistas | 728-1110 | AdditionalViewsTest |
| 12. Pruebas Adicionales de Modelos | 1111-1274 | AdditionalModelsTest |
| 13. Pruebas Adicionales de Formularios | 1275-1524 | AdditionalFormsTest |
| 14. Pruebas de Casos Edge | 1525-1716 | EdgeCasesTest |
| 15. Pruebas de Decoradores | 1717-1743 | DecoratorTest |
| 16. Pruebas de Funciones Auxiliares | 1744-1833 | FunctionTest |
| 17. Pruebas Adicionales de Cobertura | 1834-2766 | AdditionalCoverageTest |
| 18. Bloque Principal | 2767-2769 | if __name__ == '__main__' |

**Total de líneas del archivo: 2769**
