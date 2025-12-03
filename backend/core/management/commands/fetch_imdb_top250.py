# backend/core/management/commands/fetch_imdb_top250.py
import requests
import time
import re
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from backend.core.models.filme import Filme

def get_high_res_poster_url(image_url: str) -> str:
    if not image_url:
        return ""
    return re.sub(r'\._V1_.*\.jpg', '._V1_.jpg', image_url)

class Command(BaseCommand):
    help = 'Procura os 250 filmes melhores classificados do IMDb, incluindo sinopse e poster de alta qualidade.'

    IMDB_URL = 'https://www.imdb.com'
    TOP_250_URL = f'{IMDB_URL}/chart/top/'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando o scraper para o Top 250 do IMDb...'))
        
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        })

        try:
            response = session.get(self.TOP_250_URL)
            response.raise_for_status()
        except requests.RequestException as e:
            self.stderr.write(self.style.ERROR(f'Erro ao aceder à lista do IMDb: {e}'))
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        movie_items = soup.select('li.ipc-metadata-list-summary-item')

        if not movie_items:
            self.stderr.write(self.style.ERROR('Não foi possível encontrar a lista de filmes. O layout do IMDb pode ter mudado.'))
            return

        created_count = 0
        updated_count = 0

        for movie_item in movie_items:
            try:
                title_link_elem = movie_item.select_one('a.ipc-title-link-wrapper')
                title_h3 = title_link_elem.select_one('h3.ipc-title__text')
                title = title_h3.text.strip()
                
                href = title_link_elem['href']
                imdb_id = href.split('/')[2]
                detail_url = f"{self.IMDB_URL}{href}"

                year_elem = movie_item.select_one('div.cli-title-metadata span.cli-title-metadata-item')
                year = int(year_elem.text.strip())

                rating_elem = movie_item.select_one('span.ipc-rating-star--imdb span.ipc-rating-star--rating')
                rating = float(rating_elem.text.strip().replace(',', '.'))

                description, poster_url, backdrop_url = "", "", ""
                try:
                    self.stdout.write(f'  - Visitando página de detalhes para "{title}"...')
                    time.sleep(0.2)
                    detail_response = session.get(detail_url)
                    if detail_response.status_code == 200:
                        detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
                        
                        description_elem = detail_soup.select_one('span[data-testid="plot-xl"]')
                        if description_elem: description = description_elem.text.strip()
                        
                        # NOVO SELETOR: Procura pela imagem principal na secção "hero"
                        poster_elem = detail_soup.select_one('div[data-testid="hero-media__poster"] img')
                        if poster_elem:
                            poster_url = get_high_res_poster_url(poster_elem['src'])

                        backdrop_elem = detail_soup.select_one('div[data-testid="hero-media__backdrop"] img')
                        if backdrop_elem:
                            backdrop_url = get_high_res_poster_url(backdrop_elem['src'])

                except requests.RequestException as e:
                    self.stderr.write(self.style.WARNING(f'    [!] Falha ao buscar detalhes para "{title}": {e}'))

                filme, created = Filme.objects.get_or_create(
                    imdb_id=imdb_id,
                    defaults={'titulo': title, 'ano_lancamento': year, 'slug': slugify(f"{title}-{year}-{imdb_id}")}
                )
                
                filme.media_rating = rating
                filme.poster = poster_url
                filme.backdrop = backdrop_url
                filme.descricao = description
                filme.save()

                if created: created_count += 1
                else: updated_count += 1
                
                self.stdout.write(self.style.SUCCESS(f'  {"[+]" if created else "[~]"} Processado: {filme.titulo} ({filme.ano_lancamento})'))

            except Exception as e:
                self.stderr.write(self.style.ERROR(f'  [!] Erro fatal ao processar um item: {e}'))
                continue

        self.stdout.write(self.style.SUCCESS(f'\nScraping concluído! {created_count} novos filmes adicionados, {updated_count} filmes atualizados.'))