import requests
from discord.ext import commands
from fuzzywuzzy import process

class Soccer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.team_ids = self.fetch_team_data()

    def fetch_team_data(self):
        # Fetch all teams from the API and create a dictionary of team names to their IDs
        endpoint = 'teams'
        data = self.get_api_data(endpoint)
        team_dict = {}
        if 'teams' in data:
            for team in data['teams']:
                team_dict[team['name'].lower()] = team['id']
                # Add alternative names
                if 'shortName' in team:
                    team_dict[team['shortName'].lower()] = team['id']
                if 'tla' in team:
                    team_dict[team['tla'].lower()] = team['id']
        return team_dict

    def get_api_data(self, endpoint):
        url = f'https://api.football-data.org/v2/{endpoint}'
        headers = {'X-Auth-Token': 'YOUR_API_KEY'}
        response = requests.get(url, headers=headers)
        return response.json()

    def get_team_id(self, team_name):
        # Use fuzzy matching to find the closest team name
        team_name = team_name.lower()
        closest_match = process.extractOne(team_name, self.team_ids.keys())
        if closest_match:
            return self.team_ids[closest_match[0]]
        return None

    @commands.command()
    async def scores(self, ctx, league: str):
        data = self.get_api_data(f'competitions/{league}/matches')
        if 'matches' in data:
            matches = data['matches']
            for match in matches:
                await ctx.send(f"{match['homeTeam']['name']} vs {match['awayTeam']['name']} - {match['score']['fullTime']['homeTeam']}:{match['score']['fullTime']['awayTeam']}")
        else:
            await ctx.send('No data available.')

    @commands.command()
    async def events(self, ctx):
        data = self.get_api_data('competitions')
        events = [comp['name'] for comp in data['competitions']]
        await ctx.send('\n'.join(events))

    @commands.command()
    async def upcoming(self, ctx, *, team_name: str):
        team_id = self.get_team_id(team_name)
        if not team_id:
            await ctx.send(f"Team '{team_name}' not found. Please use a valid team name.")
            return

        data = self.get_api_data(f'teams/{team_id}/matches?status=SCHEDULED')
        if 'matches' in data:
            matches = data['matches']
            for match in matches:
                await ctx.send(f"Upcoming: {match['homeTeam']['name']} vs {match['awayTeam']['name']} on {match['utcDate']}")
        else:
            await ctx.send('No upcoming matches found.')

    @commands.command()
    async def standings(self, ctx, league_id: int):
        data = self.get_api_data(f'competitions/{league_id}/standings')
        if 'standings' in data:
            for table in data['standings']:
                for team in table['table']:
                    await ctx.send(f"{team['position']}. {team['team']['name']} - {team['points']} points")
        else:
            await ctx.send('No standings data available.')

    @commands.command()
    async def event_info(self, ctx, competition_id: int):
        data = self.get_api_data(f'competitions/{competition_id}')
        if 'name' in data:
            await ctx.send(f"Competition: {data['name']}")
            await ctx.send(f"Area: {data['area']['name']}")
            await ctx.send(f"Season Start Date: {data['currentSeason']['startDate']}")
            await ctx.send(f"Season End Date: {data['currentSeason']['endDate']}")
        else:
            await ctx.send('No event information available.')

def setup(bot):
    bot.add_cog(Soccer(bot))