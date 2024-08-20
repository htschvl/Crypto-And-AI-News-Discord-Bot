import discord
import feedparser
import asyncio

# Configurações
TOKEN = ''

# Configurações de canais e feeds
FEEDS_CONFIG = {
    1275274798955626566: [  # AI feeds
        'https://rss.app/feeds/gkS98dS5aYElxHCJ.xml',
        'https://rss.app/feeds/yJNxIvQE4cSoS9ci.xml',
        'https://www.artificialintelligence-news.com/feed/',
        'https://aibusiness.com/rss.xml',
        'https://feeds.feedburner.com/venturebeat/SZYF',
        'https://aibrews.substack.com/feed',
        'https://aijourn.com/feed/',
        'https://syncedreview.com/feed/',
        'https://aitrendz.xyz/feed/',
    ],
    1275265550091685928: [  # Crypto feeds
        'https://rss.app/feeds/hvWo4PXRRGTl29Vp.xml',
        'https://cointelegraph.com/rss',
        'https://decrypt.co/feed',
        'https://thedefiant.io/api/feed',
        'https://blockworks.co/feed',
        'https://www.coindesk.com/arc/outboundfeeds/rss/',
        'https://beincrypto.com/feed/',
        'https://www.bankless.com/rss/feed',
        'https://cryptoslate.com/feed/',
    ]
}

CHECK_INTERVAL = 3600  # Intervalo de verificação em segundos (1 hora)

# Configurar o cliente do bot
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Evento on_ready
@client.event
async def on_ready():
    print(f'Bot conectado como {client.user}')
    for channel_id in FEEDS_CONFIG.keys():
        channel = client.get_channel(channel_id)
        if channel:
            await channel.send("Olá, mundo")
    
    # Iniciar o loop de verificação
    client.loop.create_task(check_feeds())

# Função para verificar os feeds RSS periodicamente
async def check_feeds():
    last_entries = {channel_id: {url: None for url in urls} for channel_id, urls in FEEDS_CONFIG.items()}

    while not client.is_closed():
        for channel_id, urls in FEEDS_CONFIG.items():
            channel = client.get_channel(channel_id)
            compiled_message = ""
            for url in urls:
                feed = feedparser.parse(url)
                if feed.entries:
                    entry = feed.entries[0]
                    if last_entries[channel_id][url] is None or entry.link != last_entries[channel_id][url]:
                        last_entries[channel_id][url] = entry.link
                        compiled_message += f"- [{entry.title}]({entry.link})\n"
            
            if compiled_message:
                await channel.send(compiled_message)
        
        await asyncio.sleep(CHECK_INTERVAL)

# Iniciar o bot
client.run(TOKEN)
