# -*- coding: utf-8  -*-

import pywikibot
from pywikibot import pagegenerators
from pywikibot.data.api import APIError
import discogs_client
from XmlArtistsParsing import read_xml_artists

MEMBER_OF_PROP = "P120" # The correct property for wikidata is "P463"
NATIONALITY_PROP = "P27"
OCCUPATION_PROP = "P204" # The correct property for wikidata is "P106"
INSTRUMENT_PROP = "P1303"
HAS_PART_OF_PROP = "P17429" # The correct property for wikidata is"P527"
DATE_OF_BIRTH_PROP = "P569"
DISCOGS_ARTIST_ID_PROP = "P17427" # The correct property for wikidata is "P1953"

#listOccupations = {"writer":"Q36180", "singer":"Q177220", "composer":"Q36834", "guitarist":"Q855091", "musician":"Q639669", "bassist":"Q584301", "drummer":"Q386854", "songwriter":"Q753110", "pianist":"Q486748"}
listOccupations = {"writer":"Q36737", "singer":"Q36738", "composer":"Q36739", "guitarist":"Q36740", "musician":"Q36741", "bassist":"Q36742", "drummer":"Q36743", "songwriter":"Q36744", "pianist":"Q36745"}

user_agent = 'INFO310Project/0.1'
user_token = 'JHLqrbdwbuolTUfCpmMuaiuZqLbDXBuJcdTBHNtG'


def get_group_sparql(group):
    items = set()

    # Check for music ensambles
    sparql_query = 'SELECT ?item ' \
               'WHERE {' \
               ' ?item rdfs:label ' + '\'' + group + '\'@en' + '. ' \
               ' ?item wdt:P31:P279* wd:Q2088357 . ' \
               '}' \
               'LIMIT 1000'
    generator = pagegenerators.WikidataSPARQLPageGenerator(sparql_query, site=wd_site)
    for item in generator:
        item.get()
        items.add(item)

    return items


def get_member_sparql(member):
    items = set()

    # Check for musicians
    sparql_query = 'SELECT ?item ' \
               'WHERE {' \
               ' ?item rdfs:label ' + '\'' + member + '\'@en' + '. ' \
               ' ?item wdt:P106/wdt:P279* wd:Q639669 . ' \
               '}' \
               'LIMIT 1000'
    generator = pagegenerators.WikidataSPARQLPageGenerator(sparql_query, site=wd_site)
    for item in generator:
        item.get()
        items.add(item)

    return items


def get_occupation(artist):

    profile = artist.profile
    artistOccupations = []

    for occupation in listOccupations.keys():
        if (profile.find(occupation) != -1):
            artistOccupations.append(occupation)
            print "Occupation added "+occupation
        else:
            print "Occupation not added"

    if len(artistOccupations) > 0:
        return artistOccupations
    else:
        return None


def update_item(item, artist, wd_site, repo):
    item.get()
    print "Updating item: " + str(item.getID())
    names = [artist.name] + artist.aliases + artist.name_variations
    aliases = item.aliases["en"] + [item.labels["en"]]
    new_aliases = []

    for alias in names:
        if alias not in item.labels and alias not in item.aliases:
            new_aliases.append(alias)

    if new_aliases:
        new_alias_dict = {"en": new_aliases}
        print "Adding aliases to item"
        print new_alias_dict
        item.editAliases({"en": new_alias_dict})

    # (Eventually) Adding who are the members of the group
    if artist.members:
        member_names = []
        if item.claims.has_key(HAS_PART_OF_PROP):

            # I get all the names and aliases of the partecipants of the group
            for claim in item.claims[HAS_PART_OF_PROP]:
                    member_item = claim.getTarget()
                    member_item.get()
                    member_names += [member_item.labels['en']] + member_item.aliases['en']

        # If the member retrieved from discogs are not among the ones in wikidata, I add
        # the member as a statement to the 'member of' property
        for artist_member in artists.members:
            if artist_member not in member_names:
                new_member = get_member_sparql(artist_member)
                if len(new_member) == 0:
                    # create new member
                    print "Member not existing, creating Member"
                if len(new_member) == 1:
                    member_entity = new_member.pop()
                    new_member_claim = pywikibot.Claim(repo, HAS_PART_OF_PROP)
                    new_member_claim.setTarget(member_entity)
                    item.addClaim(new_member_claim)

    # (Eventually) Adding to which group the artist belongs
    if artist.groups:
        group_names = []
        if item.claims.has_key(MEMBER_OF_PROP):

            # I get all the names and aliases of the partecipants of the group
            for claim in item.claims[MEMBER_OF_PROP]:
                    group_item = claim.getTarget()
                    group_item.get()
                    group_names += [group_item.labels['en']] + group_item.aliases['en']

        # If the member retrieved from discogs are not among the ones in wikidata, I add
        # the member as a statement to the 'member of' property
        for artist_group in artists.groups:
            if artist_group not in group_names:
                new_group = get_group_sparql(artist_group)
                if len(new_group) == 0:
                    # create new group
                    print "Group not existing, creating Group"
                if len(new_group) == 1:
                    group_entity = new_group.pop()
                    new_group_claim = pywikibot.Claim(repo, MEMBER_OF_PROP)
                    new_group_claim.setTarget(group_entity)
                    item.addClaim(new_group_claim)

    # Adding occupation of the artist
    if not item.claims.has_key(OCCUPATION_PROP):
        # This return the item associated with the new occupation of the artist
        occupations = get_occupation(artist)
        if occupations is not None:

            for occupation in occupations:
                new_occupation_claim = pywikibot.Claim(repo, OCCUPATION_PROP)
                new_occupation_claim.setTarget(pywikibot.ItemPage(repo, listOccupations[occupation]))
                item.addClaim(new_occupation_claim)

    # Adding discogs id of the artist
    if artist.id and not item.claims.has_key(DISCOGS_ARTIST_ID_PROP):

        new_discogs_id_claim = pywikibot.Claim(repo, DISCOGS_ARTIST_ID_PROP)
        new_discogs_id_claim.setTarget(artist.id)
        item.addClaim(new_discogs_id_claim)

    print "\n----\n"


def check_artist_discogs(group):

    # instantiate our discogs_client object.
    client = discogs_client.Client(user_agent=user_agent, user_token=user_token)
    results = client.search(group, type='artist')

    if len(results) > 0:
        artist = results[0]
        if "Correct" in artist.data_quality:
            return artist
        else:
            return None


def create_item(wd_site, repo, artist):

    new_aliases = artist.name_variations + artist.aliases

    new_item = pywikibot.ItemPage(wd_site)
    if artist.name:
        new_item.editLabels(labels={"en": artist.name}, summary="Setting labels")
    if new_aliases:
        new_item.editAliases(aliases={"en": new_aliases}, summary="Setting Aliases")
    new_item.get()

    if len(artist.groups) > 0:
        for group in artist.groups:
            new_group_claim = pywikibot.Claim(repo, MEMBER_OF_PROP)

            group_list = get_group_sparql(group)

            # This is the case in which the group does not exists
            if len(group_list) == 0:
                new_group_item = pywikibot.ItemPage(wd_site)
                new_group_item.editLabels(labels={"en": group}, summary="Setting labels")
                new_group_item.get()
                new_group_claim.setTarget(new_group_item)
                new_item.addClaim(new_group_claim,
                                  summary="CLAIM [{}:{}]".format(HAS_PART_OF_PROP, new_group_item.getID()))

                new_member_claim = pywikibot.Claim(repo, HAS_PART_OF_PROP)
                new_member_claim.setTarget(new_item)
                new_group_item.addClaim(new_member_claim)

                # get_artist = check_artist_discogs(group)
                # if get_artist is not None
                # update_item(new_group_item, get_artist, wd_site, repo)

            # This is for the case in which the group already exists
            if len(group_list) == 1:
                group_item = group_list.pop()
                new_group_claim.setTarget(group_item)
                group_item.get()
                new_item.addClaim(new_group_claim, summary="CLAIM [{}:{}]".format(MEMBER_OF_PROP, group_item.getID()))

                # ALSO TO THE GROUP IS UPDATED WITH THE MEMBER WHO PARTECIPATE TO IT
                new_member_claim = pywikibot.Claim(repo, HAS_PART_OF_PROP)
                new_member_claim.setTarget(new_item)
                group_item.addClaim(new_member_claim)

    if len(artist.members) > 0:
        for member in artist.members:
            new_member_claim = pywikibot.Claim(repo, HAS_PART_OF_PROP)

            member_list = get_member_sparql(member)

            # This is the case in which the group does not exists
            if len(member_list) == 0:
                new_member_item = pywikibot.ItemPage(wd_site)
                new_member_item.get()
                new_member_item.editLabels(labels={"en": member}, summary="Setting labels")
                new_member_claim.setTarget(new_member_item)
                new_item.addClaim(new_member_claim,
                                  summary="CLAIM [{}:{}]".format(HAS_PART_OF_PROP, new_member_item.getID()))

                new_group_claim = pywikibot.Claim(repo, MEMBER_OF_PROP)
                new_group_claim.setTarget(new_item)
                new_member_item.addClaim(new_group_claim)

                # get_artist = check_artist_discogs(member)
                # if get_artist is not None
                #   update_item(new_member_item, get_artist, wd_site, repo)

            # This is for the case in which the group already exists
            if len(member_list) == 1:
                member_item = pywikibot.ItemPage(member_list.pop())
                member_item.get()
                new_member_claim.setTarget(member_item)
                new_item.addClaim(new_member_claim,
                                  summary="CLAIM [{}:{}]".format(HAS_PART_OF_PROP, member_item.getID()))

                # ALSO TO THE MEMBER IS UPDATED WITH THE GROUP TO WHICH THEY BELONG
                new_group_claim = pywikibot.Claim(repo, MEMBER_OF_PROP)
                new_group_claim.setTarget(new_item)
                member_item.addClaim(new_group_claim)

    # This return the item associated with the new occupation of the artist
    occupations = get_occupation(artist)
    if occupations is not None:

        for occupation in occupations:
            new_occupation_claim = pywikibot.Claim(repo, OCCUPATION_PROP)
            new_occupation_claim.setTarget(pywikibot.ItemPage(repo, listOccupations[occupation]))
            new_item.addClaim(new_occupation_claim)


    if artist.profile:
        try:
            new_item.editDescriptions({"en": artist.profile})
        except APIError:
            print "An item with this description already exists"

    if artist.id:
        discogs_id_claim = pywikibot.Claim(repo, DISCOGS_ARTIST_ID_PROP)
        discogs_id_claim.setTarget(artist.id)
        new_item.addClaim(discogs_id_claim, summary="CLAIM [{}:{}]".format(DISCOGS_ARTIST_ID_PROP, artist.id))

    print new_item.getID(), (": " + artist.name + " created")
    return new_item.getID()


def print_dict(dictionary, level=0):

    tabs = "\t" * level
    for key, value in dictionary.items():
        if isinstance(value, dict):
            print tabs + unicode(key)
            print_dict(value, (level + 1))
        else:
            print tabs + unicode(key) + ": " + unicode(value)


def check_homonymity(artist, items):

    for item in items:
        #print item.get()
        description = item.descriptions["en"]
        #print description
        artistOccupations = []

        #check for occupations in description of wikidata result
        for occupation in listOccupations:
            if (description.find(occupation) != -1):
                artistOccupations.append(occupation)
            else:
                print "Occupation not inserted"

        checkDiscogs = 0
        #print artistOccupations
        #print artist.profile
        for artistOcc in artistOccupations:
            if (artist.profile.find(artistOcc) != -1):
                print artistOcc
                checkDiscogs += 1

        if checkDiscogs > 0:
            #print description
            return item

    #no items compatible with occupations scearched
    return None



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
            try:
                item.get()
                items.add(item)
            except pywikibot.NoPage:
                print "Item not existing on test.wikidata"

    print items

    if len(items) == 0:
        print "Page for " + artist.name + " does not exists"
        create_item(wd_site, repo, artist)
    elif len(items) == 1:
        for item in items:
            # update item if needed
            print "Page found for "+artist.name
            update_item(item, artist, wd_site, repo)

    elif len(items) > 1:
        #check homonymity
        print "check homonymity"
        selected_item = check_homonymity(artist, items)
        if selected_item is not None:
            update_item(selected_item, artist, wd_site, repo)

    else:
        print "error"


if __name__ == "__main__":

    xml_dump_file_name = 'partial_cc_artists_1.xml'

    artists = read_xml_artists(xml_dump_file_name)
    temp_artists = artists[0:1]

    wd_site = pywikibot.Site('test', 'wikidata')
    repo = wd_site.data_repository()

    for artist in temp_artists:
        check_artist(artist, wd_site, repo)






