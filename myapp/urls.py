from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/', views.profile_view, name='profile'),
    path('add-card/', views.add_card_view, name='add_card'),
    path('update-limit/', views.update_limit_view, name='update_limit'),
    path('register-expense/', views.register_expense_view, name='register_expense'),
    path('reports/', views.reports_view, name='reports'),
    path('reports/export/', views.export_pdf_view, name='export_pdf'),
    path('recomendaciones/', views.recommendations_view, name='recommendations'),
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path('inversiones/', views.investment_view, name='investments'),
    path('retos/', views.retos_view, name='retos'),
    path('logout/', views.logout_view, name='logout'),
    path('eliminar-inversion/<int:id>/', views.delete_investment_view, name='delete_investment'),
    path('historial-retos/', views.historial_retos_view, name='historial_retos'),
    path('juegos/', views.juegos_seleccion_view, name='juegos'),
    path('trivia/', views.trivia_view, name='trivia'),
    path('trivia-ranking/', views.ranking_trivia_view, name='trivia_ranking'),
    path('completar-frases/', views.completar_frases_view, name='completar_frases'),
    path('completar-frases-ranking/', views.ranking_completar_frases_view, name='completar_frases_ranking'),
    path('upload-profile-photo/', views.upload_profile_photo, name='upload_profile_photo'),
    path("olvide-contrasena/", views.solicitar_reset_contrasena, name="olvide_contrasena"),
    path("resetear/<uidb64>/<token>/", views.resetear_contrasena, name="resetear_contrasena"),
    path('delete_card/<int:card_id>/', views.delete_card, name='delete_card'),
    
    # ============================================
    # URLs PARA INVESTIGACION
    # ============================================
    
    # FASE 1: Evaluacion y Metricas
    path('evaluacion/', views.evaluacion_view, name='evaluacion_view'),
    path('evaluacion-inicial/', views.evaluacion_inicial_view, name='evaluacion_inicial'),
    path('evaluacion-periodica/', views.evaluacion_periodica_view, name='evaluacion_periodica'),
    path('progreso-individual/', views.progreso_individual_view, name='progreso_individual'),
    path('recomendaciones-personalizadas/', views.recomendaciones_personalizadas_view, name='recomendaciones_personalizadas'),
    path('recomendacion/<int:recomendacion_id>/vista/', views.marcar_recomendacion_vista, name='marcar_recomendacion_vista'),
    
    # FASE 2: Alertas
    path('alertas-riesgo/', views.alertas_riesgo_view, name='alertas_riesgo'),
    
    # FASE 3: Gamificacion y Educacion
    path('biblioteca-educativa/', views.biblioteca_educativa_view, name='biblioteca_educativa'),
    path('contenido/<int:contenido_id>/', views.ver_contenido_view, name='ver_contenido'),
    path('logros/', views.logros_view, name='logros'),
    path('narrativa/', views.narrativa_view, name='narrativa'),
    path('narrativa/capitulo/<int:capitulo_id>/', views.ver_capitulo_view, name='ver_capitulo'),
    path('narrativa/completar/<int:capitulo_id>/', views.completar_capitulo_view, name='completar_capitulo'),
    
    # FASE 4: Prevencion de Fraudes y Admin
    path('prevencion-fraudes/', views.prevencion_fraudes_view, name='prevencion_fraudes'),
    path('fraude/<int:fraude_id>/', views.ver_fraude_view, name='ver_fraude'),
    path('reporte-impacto/', views.reporte_impacto_admin_view, name='reporte_impacto_admin'),
    
    # Admin personalizado
    path('admin-panel/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin-panel/usuario/<int:usuario_id>/', views.admin_editar_usuario_view, name='admin_editar_usuario'),
]
