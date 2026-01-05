import nextcord
import nextcord.ui
import random
import peewee
import json
import urllib.request
from nextcord.ext import commands
from datetime import datetime, timedelta
from config import settings

intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix=settings['prefix'], intents=intents)


@bot.event
async def on_ready():
    print(f'Im ready')


@bot.event
async def on_message_delete(message):
    guild = bot.get_guild(1218450138788528148)
    ch = guild.get_channel(1457737827860218038)

    author = message.author
    if author.bot:
        return
    delta = timedelta(hours=3, minutes=0)
    message_time = message.created_at + delta
    date_time = datetime.now()

    emb = nextcord.Embed(title='Сообщение удалено', color=0xFF2400)
    emb.description = f'Чат: <#{message.channel.id}>\nАвтор: {author.mention}\nСообщение: `{message.content}`\nСообщение было отправлено в: `{message_time.strftime("%Y.%m.%d %H:%M:%S")}`\nВремя удаления: `{date_time.strftime("%Y.%m.%d %H:%M:%S")}`'
    await ch.send(embed=emb)


@bot.event
async def on_message_edit(before, after):
    ch = before.guild.get_channel(1457737827860218038)

    author = before.author
    if author.bot:
        return
    delta = timedelta(hours=3, minutes=0)
    message_time = before.created_at + delta
    date_time = datetime.now()

    emb = nextcord.Embed(title='Сообщение изменено', color=0xFFA500)
    emb.description = f'Чат: <#{before.channel.id}>\nАвтор: {author.mention}\nСообщение до: `{before.content}`\nСообщение после: `{after.content}`\nСообщение было отправлено в: `{message_time.strftime("%Y.%m.%d %H:%M:%S")}`\nВремя изменения: `{date_time.strftime("%Y.%m.%d %H:%M:%S")}`'
    await ch.send(embed=emb)


@bot.slash_command(description='Приветствие с ботом или с кем-то.')
async def hello(interaction: nextcord.Interaction, member: nextcord.Member = None):
    if member is None:
        await interaction.send(f'И тебе приветик, {interaction.user.mention}.')
    else:
        await interaction.send(
            f'{member.mention}, слушай, тебе тут {interaction.user.mention} привет передает.')


@bot.slash_command(description='мут человека')
async def mut(interaction: nextcord.Interaction, *, member: nextcord.Member, _time: int = None, _reason: str = None):
    root1 = interaction.guild.get_role(1445014144893059072)
    root2 = interaction.guild.get_role(1393655962463895613)
    root3 = interaction.guild.get_role(1393655962463895613)
    root4 = interaction.guild.get_role(1218451718497632276)
    root5 = interaction.guild.get_role(1218503473985753180)
    root6 = interaction.guild.get_role(1416511333192568902)

    if (root1 or root2 or root3 or root4 or root5 or root6) in interaction.user.roles:
        await member.timeout(timeout=timedelta(seconds=_time), reason=_reason)
        await interaction.send(f'{interaction.user.mention}, хозяин, ну все, чел в муте ахаха')
    else:
        await interaction.send(f'{interaction.user.mention}, ты как феменистка, у тебя нет прав', ephemeral=True)


@bot.slash_command(description='картиночкиии')
async def pic(interaction: nextcord.Interaction, text: str):
    _api_k = settings['api_key']

    if text.lower() == 'кот':
        with urllib.request.urlopen("https://api.thecatapi.com/v1/images/search") as data:
            url = json.load(data)  # получение json-ответа на http-запрос
            pict = url[0]['url']
            print('кот - ', url)
            emb = nextcord.Embed(title=text)
            emb.set_image(pict)
            await interaction.send(embed=emb)
    elif text.lower() == 'собака':
        with urllib.request.urlopen("https://api.thedogapi.com/v1/images/search") as data:
            url = json.load(data)
            pict = url[0]['url']
            print('собака - ', url)
            emb = nextcord.Embed(title=text)
            emb.set_image(pict)
            await interaction.send(embed=emb)
    else:
        await interaction.send(f'{interaction.user.mention}, ты тупой? напиши кот или собака', ephemeral=True)


@bot.slash_command(description='кто??')
async def who(interaction: nextcord.Interaction, *, text: str):
    members = interaction.guild.members
    mem: nextcord.Member = random.choice(members)
    if mem.bot:
        while mem.bot:
            mem: nextcord.Member = random.choice(members)
    await interaction.send(f'Хммм.. Я считаю, что {mem.mention} {text}')


@bot.slash_command(description='на сколько процентов')
async def percent(interaction: nextcord.Interaction, *, text: str):
    proc = random.randint(0, 100)
    await interaction.send(f'{text}\n'+
                           f'Нууу.... скорее всего на {proc}%')




@bot.command(description='синхронизация команд')
async def sync(ctx):
    await bot.sync_all_application_commands()
    print(f'готово')





bot.run(settings['token'])
