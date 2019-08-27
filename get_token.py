"""
    Utility to get your access tokens.
    Refer: https://developers.facebook.com/docs/facebook-login/access-tokens/refreshing
"""
import webbrowser

import click
import requests
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix

DEFAULT_GRAPH_URL = 'https://graph.facebook.com/v4.0/'
DEFAULT_OAUTH_URL = 'https://www.facebook.com/v4.0/dialog/oauth'
DEFAULT_TOKEN_URL = 'https://graph.facebook.com/v4.0/oauth/access_token'
DEFAULT_REDIRECT_URL = 'https://localhost:5000/'


@click.group()
def cli():
    pass


@cli.command(short_help='get long term access token by short token.')
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


@cli.command(short_help='get app access token by app info.')
def app_token():
    app_id = click.prompt('Please input your app id', type=str)
    app_secret = click.prompt('Please input your app secret', hide_input=True, type=str)
    click.echo('Begin to retrieve app access token...')
    try:
        resp = requests.get(
            url=DEFAULT_GRAPH_URL + 'oauth/access_token',
            params={
                'grant_type': 'client_credentials',
                'client_id': app_id,
                'client_secret': app_secret,
            },
            timeout=5
        )
        if resp.status_code == 200:
            data = resp.json()
            if 'error' in data:
                click.echo('\nOps. May you input error.\n Info: {}'.format(data['error']))
            click.echo('\nYour app access token is: \n{}'.format(data.get('access_token', '')))
        else:
            click.echo('\nOps. Response error.\n Info: {}'.format(resp.text))

    except Exception as e:
        click.echo('\nOps. Error occurred.\n Info: {}'.format(e))


@cli.command(short_help='get user access token by login.')
def user_access_token():
    app_id = click.prompt('Please input your app id', type=str)
    app_secret = click.prompt('Please input your app secret', hide_input=True, type=str)

    facebook = OAuth2Session(client_id=app_id, redirect_uri=DEFAULT_REDIRECT_URL)
    facebook = facebook_compliance_fix(facebook)

    authorization_url, state = facebook.authorization_url(DEFAULT_OAUTH_URL)

    webbrowser.open(authorization_url)

    response = click.prompt('Please input full callback url', type=str)
    facebook.fetch_token(
        token_url=DEFAULT_TOKEN_URL, client_secret=app_secret,
        authorization_response=response
    )
    click.echo("Your access token is: \n{}".format(facebook.access_token))


if __name__ == '__main__':
    cli()
