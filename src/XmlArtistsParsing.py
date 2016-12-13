# -*- coding: utf-8 -*-

import xml.etree.ElementTree as eTree
from XmlArtist import XmlArtist


def write_xml_on_file(artists, n=0):
    output_file_name = '/home/piuma/Scrivania/INFO310/partial_cc_artists_' + str(n) + '.xml'

    root_elem = eTree.Element('artists')

    for artist in artists:
        artist_elem = eTree.SubElement(root_elem, "artist")
        if artist.id is not None:
            sub_elem = eTree.SubElement(artist_elem, 'id')
            sub_elem.text = artist.id

        if artist.name is not None:
            sub_elem = eTree.SubElement(artist_elem, 'name')
            sub_elem.text = artist.name

        if artist.profile is not None:
            sub_elem = eTree.SubElement(artist_elem, 'profile')
            sub_elem.text = artist.profile

        if artist.real_name is not None:
            sub_elem = eTree.SubElement(artist_elem, 'realname')
            sub_elem.text = artist.real_name

        if artist.data_quality is not None:
            sub_elem = eTree.SubElement(artist_elem, 'data_quality')
            sub_elem.text = artist.data_quality

        if len(artist.urls) > 0:
            sub_elem_1 = eTree.SubElement(artist_elem, 'urls')
            for url in artist.urls:
                if url is not None:
                    sub_elem_2 = eTree.SubElement(sub_elem_1, 'url')
                    sub_elem_2.text = url

        if len(artist.name_variations) > 0:
            sub_elem_1 = eTree.SubElement(artist_elem, 'namevariations')
            for variation in artist.name_variations:
                if variation is not None:
                    sub_elem_2 = eTree.SubElement(sub_elem_1, 'name')
                    sub_elem_2.text = variation

        if len(artist.groups) > 0:
            sub_elem_1 = eTree.SubElement(artist_elem, 'groups')
            for group in artist.groups:
                if group is not None:
                    sub_elem_2 = eTree.SubElement(sub_elem_1, 'name')
                    sub_elem_2.text = group

        if len(artist.aliases) > 0:
            sub_elem_1 = eTree.SubElement(artist_elem, 'aliases')
            for alias in artist.aliases:
                if alias is not None:
                    sub_elem_2 = eTree.SubElement(sub_elem_1, 'name')
                    sub_elem_2.text = alias

        if len(artist.members.keys()) > 0:
            sub_elem_1 = eTree.SubElement(artist_elem, 'members')
            for member_id, name in artist.members:
                if name is not None:
                    sub_elem_2 = eTree.SubElement(sub_elem_1, 'id')
                    sub_elem_2.text = member_id
                    sub_elem_2 = eTree.SubElement(sub_elem_1, 'name')
                    sub_elem_2.text = name

    tree = eTree.ElementTree(root_elem)
    tree.write(output_file_name)


def read_xml_artists(filename):

    artists = []
    new_artist = None

    is_alias = False
    is_member = False
    is_in_group = False
    have_variations = False

    last_member_id = -1
    n = 1
    count = 0
    for event, elem in eTree.iterparse(filename, events=('start', 'end')):
        # print elem.tag, elem.text, event

        if event == 'start':
            if elem.tag == 'artist':
                count += 1
                print len(artists)
                new_artist = XmlArtist()

            elif new_artist is not None and elem.tag == 'profile':
                new_artist.profile = elem.text

            elif new_artist is not None and elem.tag == 'id':
                if is_member:
                    new_artist.members[elem.text] = None
                    last_member_id = elem.text
                else:
                    new_artist.id = elem.text

            elif new_artist is not None and elem.tag == 'aliases':
                is_alias = True

            elif new_artist is not None and elem.tag == 'groups':
                is_in_group = True

            elif new_artist is not None and elem.tag == 'name':
                if is_alias:
                    new_artist.aliases.append(elem.text)
                elif is_in_group:
                    new_artist.groups.append(elem.text)
                elif is_member and last_member_id >= 0:
                    new_artist.members[last_member_id] = elem.text
                elif have_variations:
                    new_artist.name_variations.append(elem.text)
                else:
                    new_artist.name = elem.text

            elif new_artist is not None and elem.tag == 'data_quality':
                new_artist.data_quality = elem.text

            elif new_artist is not None and elem.tag == 'realname':
                new_artist.real_name = elem.text

            elif new_artist is not None and elem.tag == 'namevariations':
                have_variations = True

            elif new_artist is not None and elem.tag == 'url':
                new_artist.urls.append(elem.text)

        elif event == 'end':

            if new_artist is not None and elem.tag == 'artist':

                if new_artist.data_quality is not None and "Complete and Correct" in new_artist.data_quality:
                    artists.append(new_artist)
                new_artist = None
            elif new_artist is not None and elem.tag == 'aliases':
                is_alias = False
            elif new_artist is not None and elem.tag == 'namevariations':
                have_variations = False
            elif new_artist is not None and elem.tag == 'groups':
                is_in_group = False
            elif new_artist is not None and elem.tag == 'members':
                is_member = False
            elif new_artist is not None and elem.tag == 'name' and is_member:
                last_member_id = -1

        elem.clear()

    return artists

# if __name__ == "__main__":
#     filename = "/home/piuma/Scrivania/INFO310/artists0.xml"
#
#     # root = eTree.Element("artists")
#
#     artists = []
#     new_artist = None
#
#     is_alias = False
#     is_member = False
#     is_in_group = False
#     have_variations = False
#
#     last_member_id = -1
#     n = 1
#     count = 0
#     for event, elem in eTree.iterparse(filename, events=('start', 'end')):
#         # print elem.tag, elem.text, event
#
#         if event == 'start':
#             if elem.tag == 'artist':
#                 count += 1
#                 print count, "len artists:", len(artists)
#                 new_artist = XMLArtist()
#
#             elif new_artist is not None and elem.tag == 'profile':
#                 new_artist.profile = elem.text
#
#             elif new_artist is not None and elem.tag == 'id':
#                 if is_member:
#                     new_artist.members[elem.text] = None
#                     last_member_id = elem.text
#                 else:
#                     new_artist.id = elem.text
#
#             elif new_artist is not None and elem.tag == 'aliases':
#                 is_alias = True
#
#             elif new_artist is not None and elem.tag == 'groups':
#                 is_in_group = True
#
#             elif new_artist is not None and elem.tag == 'name':
#                 if is_alias:
#                     new_artist.aliases.append(elem.text)
#                 elif is_in_group:
#                     new_artist.groups.append(elem.text)
#                 elif is_member and last_member_id >= 0:
#                     new_artist.members[last_member_id] = elem.text
#                 elif have_variations:
#                     new_artist.name_variations.append(elem.text)
#                 else:
#                     new_artist.name = elem.text
#
#             elif new_artist is not None and elem.tag == 'data_quality':
#                 new_artist.data_quality = elem.text
#
#             elif new_artist is not None and elem.tag == 'realname':
#                 new_artist.real_name = elem.text
#
#             elif new_artist is not None and elem.tag == 'namevariations':
#                 have_variations = True
#
#             elif new_artist is not None and elem.tag == 'url':
#                 new_artist.urls.append(elem.text)
#
#         elif event == 'end':
#
#             if new_artist is not None and elem.tag == 'artist':
#                 # try:
#                 #     print new_artist
#                 # except UnicodeEncodeError:
#                 #     print "Ascii error!"
#                 #     print new_artist.id
#                 #     print new_artist.name
#                 #     print new_artist.name_variations
#                 #     print new_artist.real_name
#                 #     print new_artist.aliases
#                 #     print ""
#
#                 if new_artist.data_quality is not None and "Complete and Correct" in new_artist.data_quality:
#                     artists.append(new_artist)
#                 new_artist = None
#             elif new_artist is not None and elem.tag == 'aliases':
#                 is_alias = False
#             elif new_artist is not None and elem.tag == 'namevariations':
#                 have_variations = False
#             elif new_artist is not None and elem.tag == 'groups':
#                 is_in_group = False
#             elif new_artist is not None and elem.tag == 'members':
#                 is_member = False
#             elif new_artist is not None and elem.tag == 'name' and is_member:
#                 last_member_id = -1
#
#         elem.clear()
#
#         if len(artists) >= 10000:
#
#             write_XML_on_file(artists, n)
#             n += 1
#             artists = []
#
#     write_xml_on_file(artists, n)
#
#     print len(artists)


    # '''
    # artists_file = open(filename, "r")
    #
    # lines = []
    # line = artists_file.readline()
    # count = 0
    # while line:
    #     if "<data_quality>Needs Vote</data_quality>" not in line:
    #         lines.append(line)
    #     line = artists_file.readline()
    #
    # artists_file.close()
    # print len(lines)
    #
    # fileout = open("artists2.xml", "w+")
    # for line in lines:
    #     fileout.write(line)
    #
    # fileout.close()
    # '''
