import discord
from discord.ext import commands
import random
import stock_data

class Replies(commands.Cog):
    """
    Cog Class encompassing basic replies to commands
    I.e: Greetings commands, weather commands, etc

    ===== Public Attributes =====
    bot: commands.Bot
        The bot object

    ==== Representation Invariants ====
    bot is a valid commands.Bot object

    """
    bot: commands.Bot

    def __init__(self, bot):
        self.bot = bot

    @commands.command() 
    async def ticker(self, ctx, company: str):
        """
        ticker(self, ctx, company) produces the ticker value of comapny given

        Requires:
        ctx is a valid commands.Context object
        self.bot is ready and connected to discord
        company is valid
        
        """
        ticker = stock_data.get_ticker_symbol(company)
        company_name = stock_data.get_company_name(ticker)
        embed=discord.Embed(title= f"The ticker symbol for {company_name} is: {ticker}", url=None, 
                            description= None , 
                            color=discord.Color.yellow())
        await ctx.send(embed=embed) 
    
    @commands.command() 
    async def company(self, ctx, ticker: str):
        """
        company(self, ctx, ticker) produces the company name of ticker given

        Requires:
        ctx is a valid commands.Context object
        self.bot is ready and connected to discord
        ticker is valid
        
        """
        corrected_ticker = stock_data.get_ticker_symbol(ticker)
        company_name = stock_data.get_company_name(corrected_ticker)
        embed=discord.Embed(title= f"The company with the ticker symbol {corrected_ticker} is {company_name}", url=None, 
                            description= None , 
                            color=discord.Color.yellow())
        await ctx.send(embed=embed) 

    @commands.command()
    async def price(self, ctx, company:str):
        """
        price (self, ctx, company) produces current stock price and daily increase of stock price in $ and %

        Requires:
        ctx is a valid commands.Context object
        self.bot is ready and connected to discord
        company is valid

        """
        sign = ""
        ticker = stock_data.get_ticker_symbol(company)
        company_name = stock_data.get_company_name(ticker)
        price_data = stock_data.get_current_price(ticker)
        if price_data[1] >= 0: 
            embed=discord.Embed(title= company_name + "'s current stock price:", url=None, 
                            description= f"${price_data[0]}    +{price_data[1]}    +{price_data[2]}%" , 
                            color=discord.Color.green())
        elif price_data[1] < 0: 
            embed=discord.Embed(title= company_name + "'s current stock price:", url=None, 
                            description= f"${price_data[0]}    {price_data[1]}    {price_data[2]}%" , 
                            color=discord.Color.red())
        await ctx.send(embed=embed)  

    @commands.command()
    async def graph(self, ctx, company: str, time_period: str = None): 
        """
        graph(self, ctx, company, time_period) produces graph of company's stock performance in given time period
        if time period is not given, it time_period will be 1 year by default

        Valid intervals are: 2d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max

        Requires:
        ctx is a valid commands.Context object
        self.bot is ready and connected to discord
        company is valid
        time_period is a valid interval

        """
        ticker = stock_data.get_ticker_symbol(company)
        stock_data.stock_graph(ticker, time_period)
        await ctx.send(file=discord.File('graph.png'))
    
    @commands.command()
    async def news(self, ctx, company): 
        """
        news(self, ctx, company) randomly generates a recent financial news article relevant to the company name given

        Requires:
        ctx is a valid commands.Context object
        self.bot is ready and connected to discord
        company is valid
        
        """
        ticker = stock_data.get_ticker_symbol(company)
        news = stock_data.get_headlines(ticker)
        num_of_headlines = len(news)
        headline_num = random.randint(0,num_of_headlines-1)
        news_title = news[headline_num]['title']
        publisher = news[headline_num]['publisher']
        link = news[headline_num]['link']
        if 'thumbnail' in news[headline_num]: 
            thumbnail = news[headline_num]['thumbnail']['resolutions'][0]['url']
        else: 
            thumbnail = "https://corp.smartbrief.com/wp-content/uploads/2020/07/AdobeStock_331489342-scaled.jpeg"
        
        embed=discord.Embed(title= news_title, url=link, 
                            description= f"The following article is published by: {publisher}. Feel free to click on the title to view the full article!", 
                            color=discord.Color.blue())
        embed.set_thumbnail(url=f"{thumbnail}")
        await ctx.send(embed=embed)
    
    @commands.command()
    async def info(self, ctx): 
        """
        info(self, ctx) produces a message to guide user on how to use various commands

        Requires:
        ctx is a valid commands.Context object
        self.bot is ready and connected to discord
        
        """
        help_message = "!ticker (company name) -> returns (company name)'s ticker value\n\n" \
                   "!company (ticker) -> returns (ticker)'s company name\n\n" \
                   "!price (company name or ticker) -> returns (company name or ticker)'s most recent stock price and performance\n\n" \
                   "!graph (company name or ticker) (*optional* time period) -> returns graph of (company name or ticker)'s stock performance in given time period\n" \
                   " - if time period is not given, it defaults to 1 year\n" \
                   " - valid intervals are: 2d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max\n\n" \
                   "!news (company name or ticker) -> randomly generates a recent financial news article relevant to (company name or ticker)"
        embed=discord.Embed(title= f"Hello! Here are a few commands and there functionality to get you started!", url=None, 
                            description= help_message, 
                            color=discord.Color.yellow())
        await ctx.send(embed=embed) 
    

    


        
