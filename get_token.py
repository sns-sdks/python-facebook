"""
    Utility to get your access tokens.
    Refer: https://developers.facebook.com/docs/facebook-login/access-tokens/refreshing
"""

import click
import requests

DEFAULT_GRAPH_URL = 'https://graph.facebook.com/v4.0/'


@click.group()
def cli():
    pass


@cli.command()
def long_term_token():
    app_id = click.prompt('Please input your app id', type=str)
    app_secret = click.prompt('Please input your app secret', hide_input=True, type=str)
    short_token = click.prompt('Please input your short lived token', type=str)
    click.echo('Begin to exchange long term access token...')

    try:
        resp = requests.get(
            url=DEFAULT_GRAPH_URL + 'oauth/access_token',
            params={
                'grant_type': 'fb_exchange_token',
                'client_id': app_id,
                'client_secret': app_secret,
                'fb_exchange_token': short_token
            },
            timeout=5
        )
        if resp.status_code == 200:
            data = resp.json()
            if 'error' in data:
                click.echo('\nOps. May you input error.\n Info: {}'.format(data['error']))
            click.echo('\nYour long term token is: \n{}'.format(data.get('access_token', '')))
        else:
            click.echo('\nOps. Response error.\n Info: {}'.format(resp.text))
    except Exception as e:
        click.echo('\nOps. Error occurred.\n Info: {}'.format(e))


if __name__ == '__main__':
    cli()
