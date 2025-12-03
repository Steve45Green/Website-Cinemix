# -*- coding: utf-8 -*-
"""
Testes para a aplicação 'core'.

Este ficheiro contém testes unitários para verificar a lógica de negócio da aplicação,
como os sinais (signals) que atualizam automaticamente os dados agregados.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

# --- Importação direta dos modelos ---
# Importar diretamente dos ficheiros .py dos modelos é uma prática robusta
# que evita problemas de importação circular.
from .models.filme import Filme
from .models.review import Review

# Obtém o modelo de utilizador ativo no projeto.
# Esta é a forma recomendada pelo Django para referenciar o modelo de utilizador.
User = get_user_model()

class SignalTests(TestCase):
    """
    Conjunto de testes para os sinais (signals) relacionados com o modelo Review.

    Estes testes garantem que a criação, atualização e remoção de uma `Review`
    acionam corretamente a atualização dos campos `media_rating` e `reviews_count`
    no modelo `Filme` associado.
    """

    def setUp(self):
        """
        Método de configuração executado antes de cada teste.

        Cria os objetos necessários (utilizadores e um filme) para serem
        utilizados nos testes, garantindo um ambiente limpo e consistente.
        """
        # Cria dois utilizadores de teste.
        self.user_a = User.objects.create_user(username="user_a", password="123")
        self.user_b = User.objects.create_user(username="user_b", password="123")

        # Cria um filme de teste com valores iniciais para as métricas.
        self.filme = Filme.objects.create(
            titulo="Filme de Teste",
            slug="filme-de-teste",
            ano_lancamento=2025,
            media_rating=0.0,
            reviews_count=0
        )

    def test_review_signal_updates_rating(self):
        """
        Testa se o sinal post_save e post_delete de Review atualiza
        corretamente os campos `media_rating` e `reviews_count` em Filme.
        """

        # 1. VERIFICAÇÃO DO ESTADO INICIAL
        # Garante que o filme começa com os valores esperados.
        self.filme.refresh_from_db()  # Recarrega o objeto da base de dados.
        self.assertEqual(self.filme.media_rating, 0.0)
        self.assertEqual(self.filme.reviews_count, 0)

        # 2. CRIAÇÃO DA PRIMEIRA REVIEW (Rating 10)
        Review.objects.create(
            filme=self.filme,
            autor=self.user_a,
            rating=10,
        )
        self.filme.refresh_from_db()

        # VERIFICAÇÃO: A média deve ser 10.0 e a contagem 1.
        self.assertEqual(self.filme.media_rating, 10.0)
        self.assertEqual(self.filme.reviews_count, 1)

        # 3. CRIAÇÃO DA SEGUNDA REVIEW (Rating 5)
        review_b = Review.objects.create(
            filme=self.filme,
            autor=self.user_b,
            rating=5,
        )
        self.filme.refresh_from_db()

        # VERIFICAÇÃO: A média deve ser (10 + 5) / 2 = 7.5 e a contagem 2.
        self.assertEqual(self.filme.media_rating, 7.5)
        self.assertEqual(self.filme.reviews_count, 2)

        # 4. ATUALIZAÇÃO DE UMA REVIEW EXISTENTE (Rating 8)
        review_b.rating = 8
        review_b.save()  # O sinal `post_save` deve ser acionado novamente.
        self.filme.refresh_from_db()

        # VERIFICAÇÃO: A média deve ser (10 + 8) / 2 = 9.0 e a contagem permanece 2.
        self.assertEqual(self.filme.media_rating, 9.0)
        self.assertEqual(self.filme.reviews_count, 2)

        # 5. REMOÇÃO DE UMA REVIEW
        review_b.delete()  # O sinal `post_delete` deve ser acionado.
        self.filme.refresh_from_db()

        # VERIFICAÇÃO: A média deve voltar a ser 10.0 e a contagem 1.
        self.assertEqual(self.filme.media_rating, 10.0)
        self.assertEqual(self.filme.reviews_count, 1)
