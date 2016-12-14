# -*- coding: utf-8  -*-

import pywikibot
from pywikibot import pagegenerators
import discogs_client
from XmlArtistsParsing import read_xml_artists
from pywikibot import Claim

MEMBER_OF_PROP = "P463"
NATIONALITY_PROP = "P27"
OCCUPATION_PROP = "P106"
INSTRUMENT_PROP = "P1303"
HAS_PART_OF_PROP = "P527"
DATE_OF_BIRTH_PROP = "P569"
DISCOGS_ARTIST_ID_PROP = "P1953"

# cl = Claim()
# cl.


def create_item(wd_site, repo, artist):
    new_item = pywikibot.ItemPage(wd_site)
    new_item.editLabels(labels=artist.name, summary="Setting labels")
    new_item.editAliases(aliases=([artist.name_variations] + [artist.aliases]), summary="Setting Aliases")

    if len(artist.groups) > 0:
        for group in artist.groups:
            new_claim = pywikibot.Claim(repo, MEMBER_OF_PROP)

    # Add description here or in another function
    return new_item.getID()



def print_dict(dictionary, level=0):

    tabs = "\t" * level
    for key, value in dictionary.items():
        if isinstance(value, dict):
            print tabs + unicode(key)
            print_dict(value, (level + 1))
        else:
            print tabs + unicode(key) + ": " + unicode(value)


def check_artist(artist, wd_site, repo):

    print "\n----\n"
    print "New Artist: " + artist.name
    print "\n----\n"
    items = set()
    names = [artist.name] + artist.aliases + artist.name_variations
    for name in names:
        if name.strip().endswith(')'):
            name = name[:name.find('(')].strip()

        print 'Checking ' + name
        if isinstance(name, str):
            safe_name = name
        elif isinstance(name, unicode):
            safe_name = unicode.encode(name, 'utf-8')
        else:
            print "format not supported"
            continue
        sparql_query = 'SELECT ?item ' \
               'WHERE {' \
               ' ?item rdfs:label ' + '\'' + safe_name + '\'@en' + '. ' \
               ' {?item wdt:P106/wdt:P279* wd:Q639669 }' \
                  'UNION' \
               ' {?item wdt:P31:P279* wd:Q2088357} . ' \
               '}' \
               'LIMIT 1000'
        generator = pagegenerators.WikidataSPARQLPageGenerator(sparql_query, site=wd_site)
        for item in generator:
            print "Here!"
            item.get()
            items.add(item)

    print items

    if len(items) == 0:
        print "Page for " + artist.name + " does not exists"
        # create_item(artist, wd_site, repo)
    elif len(items) == 1:
        for item in items:
            # update item if needed
            item.get()

            new_aliases = []
            print "ALIASES"
            for alias in names:
                if alias not in item.labels and alias not in item.aliases:
                    new_aliases.append(alias)

            if len(new_aliases) > 0:
                new_alias_dict = {"en": new_aliases}
                print new_alias_dict
                # item.editAliases(new_alias_dict)
            print item.labels

            print "MEMBER_PROP START"
            if item.claims.has_key(MEMBER_OF_PROP):
                # check how to iterate through properties
                for claim in item.claims[MEMBER_OF_PROP]:
                    sub_item = claim.getTarget()
                    sub_item.get()
                    print sub_item.labels['en']

            print "MEMBER_PROP END"
            print "HAS_PART_OF_PROP START"
            if item.claims.has_key(HAS_PART_OF_PROP):
                for claim in item.claims[HAS_PART_OF_PROP]:
                    sub_item = claim.getTarget()
                    sub_item.get()
                    print sub_item.labels['en']

            print "HAS_PART_OF_PROP END"
            print "OCCUPATION START"
            if item.claims.has_key(OCCUPATION_PROP):
                for claim in item.claims[OCCUPATION_PROP]:
                    sub_item = claim.getTarget()
                    sub_item.get()
                    print sub_item.labels['en']
                    # sub_item = pywikibot.ItemPage(repo, claim.getTarget())
            print "OCCUPATION END"

            print "DISCOGS ARTIST ID PROP START"
            if item.claims.has_key(DISCOGS_ARTIST_ID_PROP):
                for claim in item.claims[DISCOGS_ARTIST_ID_PROP]:
                    sub_item = claim.getTarget()
                    sub_item.get()
                    print sub_item.labels["en"]
            print "DISCOGS ARTIST ID PROP END"

            print item.claims
            if item.claims.has_key(OCCUPATION_PROP):
                print item.claims[OCCUPATION_PROP][0].getTarget()
            else:
                print "No occupation found"
            print item.getID()
            print item.sitelinks
            print "\n----\n"

    elif len(items) > 1:
        #check homonymity
        print "check homonymity"
    else:
        print "error"



    # page = pywikibot.Page(wd_site, member.name.strip())
    # item = pywikibot.ItemPage(repo, "Q33011")
    # item = pywikibot.ItemPage.fromPage(page)
    # print item.get()

if __name__ == "__main__":

    xml_dump_file_name = 'partial_cc_artists_1.xml'

    artists = read_xml_artists(xml_dump_file_name)
    temp_artists = artists[45:50]


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
    repo = wd_site.data_repository()
    # item = pywikibot.ItemPage(repo, 'Q42')

    # item.get()
    #
    # print item.labels

    for artist in temp_artists:
        check_artist(artist, wd_site, repo)

    # clm = item.claims["P17"][0]
    #
    # clm.changeTarget(pywikibot.ItemPage(repo, "Q232"))





