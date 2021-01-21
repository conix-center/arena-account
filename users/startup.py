import datetime
import json
import logging
import os
import ssl
from urllib import parse, request
from urllib.error import HTTPError, URLError

import jwt
from allauth.socialaccount.models import SocialApp
from django.conf import settings
from django.contrib.sites.models import Site

from .models import Scene

SAPP_PROV = 'google'
SAPP_NAME = 'Google ARENA OAuth Web'

logger = logging.getLogger(__name__)


def setup_socialapps():
    # add host to Sites if not there already
    host = os.getenv('HOSTNAME')
    hc = Site.objects.filter(domain=host).count()
    logger.info(f"Site table found expected '{host}': {hc}")
    if hc == 0:
        logger.info(f"Adding '{host}' to Site table...")
        site = Site(name=host, domain=host)
        site.save()
        # TODO: potentially should confirm id == settings.SITE_ID

    # add google to SocialApps if not there already
    ac = SocialApp.objects.filter(provider=SAPP_PROV).count()
    logger.info(f"SocialApp table found expected '{SAPP_PROV}': {ac}")
    if ac == 0:
        logger.info(f"Adding '{SAPP_PROV}' to SocialApp table...")
        gclientid = os.getenv('GAUTH_CLIENTID')
        gsecret = os.getenv('GAUTH_CLIENTSECRET')
        sapp = SocialApp(provider=SAPP_PROV, name=SAPP_NAME,
                         client_id=gclientid, secret=gsecret)
        sapp.save()
        sapp.sites.add(settings.SITE_ID)


def get_persist_scenes():
    p_scenes = []
    config = settings.PUBSUB
    privkeyfile = settings.MQTT_TOKEN_PRIVKEY

    # get key for persist
    if not os.path.exists(privkeyfile):
        privkeyfile = '../data/keys/pubsubkey.pem'
    logger.info('Using keyfile at: ' + privkeyfile)
    with open(privkeyfile) as privatefile:
        private_key = privatefile.read()

    payload = {
        'sub': config['mqtt_username'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'subs': [f"{config['mqtt_realm']}/s/#"],
    }
    token = jwt.encode(payload, private_key, algorithm='RS256')

    # request all _scenes from persist
    host = config['mqtt_server']['host']
    # in docker on localhost this url will fail
    url = f'https://{host}/persist/!allscenes'
    try:
        req = request.Request(url)
        req.add_header("Cookie", f"mqtt_token={token.decode('utf-8')}")
        if settings.DEBUG:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            res = request.urlopen(req, context=context)
        else:
            res = request.urlopen(req)
        result = res.read().decode('utf-8')
        p_scenes = json.loads(result)
    except (URLError, HTTPError) as err:
        logger.info("{0}: ".format(err)+url)
    except ValueError as err:
        logger.info(f"{result} {0}: ".format(err)+url)
    return p_scenes


def migrate_persist():
    logger.info('starting persist name migrate')
    p_scenes = get_persist_scenes()

    # add only-missing scenes to scene database
    logger.info(f'persist scenes: {p_scenes}')
    a_scenes = Scene.objects.values_list('name', flat=True)
    logger.info(f'account scenes: {a_scenes}')
    for p_scene in p_scenes:
        logger.info(f'persist scene test: {p_scene}')
        if p_scene not in a_scenes:
            s = Scene(
                name=p_scene,
                summary='Existing scene name migrated from persistence database.',
            )
            logger.info(f'Adding scene to account database: {p_scene}')
            s.save()

    logger.info('ending persist name migrate')
