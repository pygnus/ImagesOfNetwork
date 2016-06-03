import feedparser
from images_of import command, settings, Reddit
from images_of.logging import getLogger
from praw.errors import AlreadySubmitted, APIException, HTTPException

LOG = getLogger(__name__)

@command
def main():
    r = Reddit('posts relevant feeds to the {} - /u/{}'.format(settings.NETWORK_NAME, settings.USERNAME))
    r.oauth()
    children = settings.CHILD_SUBS
    for child in children:
        checkforfeeds = child.get('feeds', None)
        if checkforfeeds: 
            for feed in child['feeds']:
                thisfeed = feedparser.parse(feed)
                for i in range(len(thisfeed.entries)):
                    LOG.info('Posting OC into /r/{}: {}', child['name'], thisfeed.entries[i].title)
                    try:
                        r.submit(child['name'], title=thisfeed.entries[i].title, url=thisfeed.entries[i].link, captcha=None, send_replies=True, resubmit=False)
                    except AlreadySubmitted:
                        LOG.info('Already submitted. Skipping.')
                    except APIException as e:
                        LOG.warning(e)

if __name__ == '__main__':
    main()
