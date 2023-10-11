import requests

# An API key is emailed to you when you sign up for a plan.
# Get a free API key at https://api.the-odds-api.com/
API_KEY = "bce8c3b7b013150ddece1f6444b326b6"

SPORT = 'soccer_epl'
REGIONS = 'uk'
MARKETS = 'h2h'
ODDS_FORMAT = 'decimal'
DATE_FORMAT = 'iso'

# Fetch odds data
odds_response = requests.get(
    f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds',
    params={
        'api_key': API_KEY,
        'regions': REGIONS,
        'markets': MARKETS,
        'oddsFormat': ODDS_FORMAT,
        'dateFormat': DATE_FORMAT,
    }
)

if odds_response.status_code != 200:
    print(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')
else:
    odds_json = odds_response.json()

    for event in odds_json:
        print(f"Event: {event['home_team']} vs. {event['away_team']}")
        for bookmaker in event['bookmakers']:
            print(f"Bookmaker: {bookmaker['title']}")
            for outcome in bookmaker['markets'][0]['outcomes']:
                print(f"{outcome['name']}: {outcome['price']}")
            print()
