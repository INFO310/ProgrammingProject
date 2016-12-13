# -*- coding: utf-8  -*-

import pywikibot
from pywikibot import pagegenerators
import discogs_client
from XmlArtist import XmlArtist
from XmlArtistsParsing import read_xml_artists
from discogs_client import Artist
from discogs_client import Master
from discogs_client import Release

def print_dict(dictionary, level=0):

    tabs = "\t" * level
    for key, value in dictionary.items():
        if isinstance(value, dict):
            print tabs + unicode(key)
            print_dict(value, (level + 1))
        else:
            print tabs + unicode(key) + ": " + unicode(value)


def check_artist(name):
    if name.strip().endswith(')'):
        name = name[:name.find('(')].strip()

        print 'Checking ' + member.name
        sparql_query = 'SELECT ?item ' \
               'WHERE {' \
               ' ?item rdfs:label ' + '\'' + name + '\'@en' + '. ' \
               ' {?item wdt:P106/wdt:P279* wd:Q639669 }' \
                  'UNION' \
               ' {?item wdt:P31:P279* wd:Q2088357} . ' \
               '}' \
               'LIMIT 1000'
        generator = pagegenerators.WikidataSPARQLPageGenerator(sparql_query,site=wd_site)

        count = 0
        for item in generator:
            count += 1
            item.get()

            print item.labels
            print item.claims
            if item.claims.has_key('P463'):
                print item.claims["P463"][0].getTarget()
            else:
                print "Not a member of anything"
            print item.getID()
            print item.sitelinks
            print "\n----\n"

        if count == 0:
            print "Page for " + member.name + " does not exists"
        # page = pywikibot.Page(wd_site, member.name.strip())
        # item = pywikibot.ItemPage(repo, "Q33011")
        # item = pywikibot.ItemPage.fromPage(page)
        # print item.get()

if __name__ == "__main__":

    MEMBER_OF_PROP = "P463"
    NATIONALITY_PROP = "P27"
    OCCUPATION_PROP = "P106"
    INSTRUMENT_PROP = "P1303"

    xml_dump_file_name = 'partial_cc_artists_1.xml'

    artists = read_xml_artists(xml_dump_file_name)

    # user_agent = 'INFO310Project/0.1'
    # user_token = 'JHLqrbdwbuolTUfCpmMuaiuZqLbDXBuJcdTBHNtG'
    #
    # # instantiate our discogs_client object.
    # client = discogs_client.Client(user_agent=user_agent, user_token=user_token)
    # results = client.search('Depeche Mode', type='artist')
    #
    # artist = results[0]
    # print 'artist.data'
    # print artist.data
    # print 'artist.urls'
    # print artist.urls
    # print 'artist.url'
    # print artist.url
    # members = artist.members
    # for member in artist.members:
    #
    #     print "name"
    #     print member.name
    #     print "variations"
    #     print member.name_variations
    #     print "aliases"
    #     for alias in member.aliases:
    #         print alias.name
    #     print "profile"
    #     print member.profile
    #     print 'member.data'
    #     print member.data
    #     art = client.artist(member.data['id'])
    #     print 'artist.data'
    #     print artist.data
    #     print 'artist.urls'
    #     print artist.urls
    #     print 'artist.url'
    #     print artist.url
    #     # print type(release)
    #     # print release.title
    #
    # print " \n\n"

    # art = Artist()
    # art.

    # mst = Master()
    # mst.
    #
    # rls = Release()
    # rls.

    # wiki_site = pywikibot.Site("en", "wikipedia")
    # page = pywikibot.Page(wiki_site, u'James Johnston')
    # item = pywikibot.ItemPage.fromPage(page)
    # #
    # print_dict(item.get())
    # print "\n\t" + str(item.claims["P31"][0].getTarget())
    # print "\n----\n"
    #
    # print "Gotcha!"
    # print item.claims['P106'][0]

    wd_site = pywikibot.Site('wikidata', 'wikidata')
    # repo = wd_site.data_repository()
    # item = pywikibot.ItemPage(repo, 'Q42')

    # item.get()
    #
    # print item.labels

    for artist in artists:

        if len(artist.members.keys()) > 0:

            for member in artist.members:

                name = member.name
                if name.strip().endswith(')'):
                    name = name[:name.find('(')].strip()

                print 'Checking ' + member.name
                sparql_query = 'SELECT ?item ' \
                       'WHERE {' \
                       ' ?item rdfs:label ' + '\'' + name + '\'@en' + '. ' \
                       ' {?item wdt:P106/wdt:P279* wd:Q639669 }' \
                          'UNION' \
                       ' {?item wdt:P31:P279* wd:Q2088357} . ' \
                       '}' \
                       'LIMIT 1000'
                generator = pagegenerators.WikidataSPARQLPageGenerator(sparql_query,site=wd_site)

                count = 0
                for item in generator:
                    count += 1
                    item.get()

                    print item.labels
                    print item.claims
                    if item.claims.has_key('P463'):
                        print item.claims["P463"][0].getTarget()
                    else:
                        print "Not a member of anything"
                    print item.getID()
                    print item.sitelinks
                    print "\n----\n"

                if count == 0:
                    print "Page for " + member.name + " does not exists"
                # page = pywikibot.Page(wd_site, member.name.strip())
                # item = pywikibot.ItemPage(repo, "Q33011")
                # item = pywikibot.ItemPage.fromPage(page)
                # print item.get()

    # clm = item.claims["P17"][0]
    #
    # clm.changeTarget(pywikibot.ItemPage(repo, "Q232"))





