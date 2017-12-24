from .coin_market import CoinMarket
import asyncio
import discord


class CmdHandler:
    """
    Processes commands sent from Discord
    """
    def __init__(self, config_data, coin_symbol):
        self.coin_market_prefix = '$'
        self.coin_market_cmd_handler = CoinMarketCommand(coin_symbol)
        self.config_data = config_data

    async def process_command(self, client, message):
        if message.content.startswith('$'):
            await self.coin_market_cmd_handler.process_command(self.config_data,
                                                               client,
                                                               message)


class CoinMarketCommand:
    """
    Handles all Coin Market Cap related commands
    """
    def __init__(self, coin_symbol):
        self.coin_market = CoinMarket()
        self.coin_symbol = coin_symbol
        self.live_on = False

    async def search(self, client, message):
        """
        Displays the data of the specified currency.

        @param client - bot client
        @param message - command received
        """
        param = message.content.split()
        # get currency name based on symbol
        if param[1] in self.coin_symbol:
            param[1] = self.coin_symbol[param[1]]
        if len(param) == 3:
            data, isPositivePercent = await self.coin_market.get_currency(param[1], param[2])
        elif len(param) == 2:
            data, isPositivePercent = await self.coin_market.get_currency(param[1])
        else:
            await client.send_message(message.channel,
                                      "```Please enter a currency to search. A "
                                      "particular fiat is optional.```")
        if isPositivePercent:
            em = discord.Embed(title="Search results",
                               description=data,
                               colour=0x008000)
        else:
            em = discord.Embed(title="Search results",
                               description=data,
                               colour=0xD14836)
        await client.send_message(message.channel, embed=em)

    async def stats(self, client, message):
        """
        Displays the market stats.

        @param client - bot client
        @param message - command received
        """
        data = await self.coin_market.get_stats()
        em = discord.Embed(title="Market Stats",
                           description=data,
                           colour=0x008000)
        await client.send_message(message.channel, embed=em)

    #async def live(self, currency_list, live_channel, timer, client, message):
        """
        Displays live updates of coin stats in n-second intervals

        @param currency_list - list of currencies
        @param live_channel - the channel to message in
        @param timer - time interval between live updates
        @param client - bot client
        @param message - command received
        """
        #if not self.live_on:
        #    self.live_on = True
        #    param = message.content.split()
        #    while True:
        #        try:
        #            await client.purge_from(message.channel, limit=100)
        #        except:
        #            pass
        #        if param == 2:
        #            data = await self.coin_market.get_live_data(currency_list,
        #                                                        param[1])
        #        else:
        #            data = await self.coin_market.get_live_data(currency_list)
        #        em = discord.Embed(title="Live Currency Update",
        #                           description=data,
        #                           colour=0xFFD700)
        #        await client.send_message(message.channel, embed=em)
        #        await asyncio.sleep(float(timer))

    async def get_help(self, client, message):
        """
        Displays helpful commands

        @param client - bot client
        @param message - command received
        """

        data = "```$search currency\n"
        #data += "$live\n"
        data += "$mcap\n"
        data += "$update symbol full-name\n"
        data += "$symbol btc ltc etc```"
        em = discord.Embed(title="Commands",
                           description=data,
                           colour=0xFFD700)
        await client.send_message(message.channel, embed=em)

    async def update_symbol(self, client, message):
        """
        Map a symbol to a full currency name

        @param client - bot client
        @param message - command received
        """
        import json
        param = message.content.split()
        if len(param) != 3:
            await client.send_message(message.channel,
                                     "```Please enter a symbol and a currency "
                                     "to map it to```")
        else:
            symbol = param[1]
            full_name = param[2]
            self.coin_symbol[symbol] = full_name
            data = "Updated {} -> {}".format(symbol, full_name)
            # update cryptocurrencies.json with new value
            with open("cryptocurrencies.json", "w") as f:
                json.dump(self.coin_symbol, f, indent=2, sort_keys=True)
            em = discord.Embed(title="Update",
                               description=data,
                               colour=0xFFD700)
            await client.send_message(message.channel, embed=em)

    async def check_symbol_value(self, client, message):
        """
        Check which name the symbol is mapped to

        @param client - bot client
        @param message - command received
        """
        param = message.content.split()
        symbols = param[1:]
        data = ""
        for symbol in symbols:
            if symbol in self.coin_symbol:
                data += "{} -> {}\n".format(symbol, self.coin_symbol[symbol])
            else:
                data += "{} -> symbol not defined\n".format(symbol)
        em = discord.Embed(title="Symbols and Values",
                           description=data,
                           colour=0xFFD700)
        await client.send_message(message.channel, embed=em)

    async def process_command(self, config_data, client, message):
        """
        Processes commands to use

        @param client - bot client
        @param message - command received
        """
        if message.content.startswith("$symbol"):
            await self.check_symbol_value(client, message)
        elif message.content.startswith("$s"):
            await self.search(client, message)
        elif message.content.startswith("$mcap"):
            await self.stats(client, message)
        elif message.content.startswith("$update"):
            await self.update_symbol(client, message)
        #elif message.content.startswith("$live"):
        #    await self.live(config_data['live_check_currency'],
        #                    config_data['live_channel'],
        #                    config_data['live_update_interval'],
        #                    client,
        #                    message)

        elif message.content.startswith("$help"):
            await self.get_help(client, message)
