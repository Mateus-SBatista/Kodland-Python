import discord
from discord.ext import commands
from bot_logic import gen_pass
import os, random, requests

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'Estamos logados como {bot.user}')

@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Olá eu sou um bot {bot.user}!')

@bot.command()
async def pasw(ctx):
    await ctx.send(gen_pass(10))


@bot.command()
async def meme(ctx):
    with open('bot Discord\images\meme1.png', 'rb') as f:
        #Vamos armazenar o arquivo convertido da biblioteca do Discord nesta variável!
        picture = discord.File(f)
    # Podemos então enviar esse arquivo como um parâmetro
    await ctx.send(file=picture)

@bot.command()
async def memes(ctx):
    img_name = random.choice(os.listdir('bot Discord\images'))
    with open(f'bot Discord\images/{img_name}', 'rb') as f:
        picture = discord.File(f)

    await ctx.send(file=picture)

def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']


@bot.command('duck')
async def duck(ctx):
    '''Uma vez que chamamos o comando duck, o programa chama a função get_duck_image_url '''
    image_url = get_duck_image_url()
    await ctx.send(image_url)

#API DE CACHORRO
def get_dog_image_url():
    url = 'https://random.dog/woof.json'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.command('dog')
async def duck(ctx):
    '''Sempre que a requisição de cachorro é chamada, o programa chama a função **get_dog_image_url**.'''
    image_url = get_dog_image_url()
    await ctx.send(image_url)

#API DE RAPOSA
def get_fox_image_url():
    url = 'https://randomfox.ca/floof/'
    res = requests.get(url)
    data = res.json()
    return data['link']

@bot.command('fox')
async def duck(ctx):
    '''Sempre que a requisição de raposa é chamada, o programa chama a função **get_fox_image_url**.'''
    image_url = get_fox_image_url()
    await ctx.send(image_url)

#API DE POKEMON
@bot.command(name='pokemon')
async def get_pokemon_info(ctx, nome_pokemon: str):

    nome_pokemon = nome_pokemon.lower()
    url = f"https://pokeapi.co/api/v2/pokemon/{nome_pokemon}"

    resposta = requests.get(url)

    if resposta.status_code == 200:
        pokemon = resposta.json()

        # Extrai os dados
        nome = pokemon['name'].capitalize()
        altura = pokemon['height'] / 10 # Altura em metros

        # Mapeia as estatísticas
        stats = {}
        for stat_info in pokemon['stats']:
            stat_name = stat_info['stat']['name'].replace('-', ' ').upper()
            stats[stat_name] = stat_info['base_stat']

        hp = stats.get('HP', 'N/A')
        ataque = stats.get('ATTACK', 'N/A')

        mensagem = (
            f"**Informações do Pokémon: {nome}**\n"
            f"* Altura: **{altura:.1f} m**\n"
            f"* HP Base: **{hp}**\n"
            f"* Ataque Base: **{ataque}**"
        )

        await ctx.send(mensagem)

    # Informa se o Pokémon não for encontrado
    elif resposta.status_code == 404:
        await ctx.send(f"❌ Pokémon **{nome_pokemon.capitalize()}** não encontrado. Verifique a grafia!")

    # Trata outros erros de resposta do servidor (500, 503, etc.)
    else:
        await ctx.send(f"⚠️ Ocorreu um erro ao buscar informações (Status Code: {resposta.status_code}).")

#API DE ANIME
@bot.command(name='anime', help='Busca informações de um anime na Kitsu API. Uso: $anime [título do anime]')
async def get_anime_info_sem_erros(ctx, *, search_query: str):
    """
    Comando que busca informações de um anime na Kitsu API.
    ATENÇÃO: Este código não trata erros de CONEXÃO de rede, apenas Status HTTP.
    """
    await ctx.send(f"🔍 Buscando informações de: **{search_query}**...")

    nome_anime = search_query.strip()
    url = f"https://kitsu.io/api/edge/anime?filter[text]={nome_anime}"

    # Faz a requisição
    resposta = requests.get(url)

    # Verifica o status HTTP
    if resposta.status_code == 200:
        # Sucesso
        data = resposta.json()

        if not data['data']:
            await ctx.send(f"❌ Não foi encontrado nenhum anime com o título **{nome_anime}**.")
            return

        primeiro_resultado = data['data'][0]
        attr = primeiro_resultado['attributes']

        # Extração de Dados
        titulo_principal = attr.get('canonicalTitle', 'N/A')
        episodios = attr.get('episodeCount', 'N/A')
        status = attr.get('status', 'N/A').capitalize()
        sinopse = attr.get('synopsis', 'N/A')
        if len(sinopse) > 500:
            sinopse = sinopse[:500] + "..."

        imagem_url = attr.get('posterImage', {}).get('original')

        # Criando o Embed
        embed = discord.Embed(
            title=titulo_principal,
            description=sinopse,
            color=0xDC143C
        )
        if imagem_url:
            embed.set_thumbnail(url=imagem_url)

        embed.add_field(name="Total de Episódios", value=str(episodios), inline=True)
        embed.add_field(name="Status", value=status, inline=True)
        embed.set_footer(text=f"Pesquisa da Kitsu API para: {nome_anime}")

        await ctx.send(embed=embed)

    # Trata Erros HTTP Conhecidos
    elif resposta.status_code in [400, 401, 403, 404]:
        # Erros comuns de cliente/recurso (embora 404 seja raro na Kitsu API para esta URL)
        await ctx.send(f"❌ Erro {resposta.status_code} ao buscar anime. Verifique a URL ou permissões.")

    # Trata Erros de Servidor
    else:
        # Erros como 500 (Erro Interno do Servidor) ou 503 (Serviço Indisponível)
        await ctx.send(f"⚠️ Ocorreu um erro interno no servidor da Kitsu. Status: {resposta.status_code}")

bot.run("TOKEN") #<-INSIRA O SEU TOKEN
