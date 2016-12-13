# -*- coding: utf-8 -*-

class XmlArtist:

    def __init__(self, is_member=False, member_of=None):
        self.id = None
        self.name = None
        self.profile = None
        self.data_quality = None
        self.urls = []
        self.real_name = None
        self.name_variations = []
        self.aliases = []
        self.groups = []
        self.members = {}
        self.is_member = is_member
        if self.is_member:
            self.member_of = member_of
        else:
            self.member_of = member_of

    def __str__(self):

        if self.id is not None:
            result = "id: \t" + self.id + "\n"
        else:
            result = "id: \tNone\n"
        if self.name is not None:
            result += "name:\t" + self.name + "\n"
        if self.data_quality is not None:
            result += "data_quality:\t" + self.data_quality + "\n"
        if self.profile is not None:
            result += "profile: \t: " + self.profile + "\n"
        if self.real_name is not None:
            result += "real_name\t: " + self.real_name + "\n"
        for url in self.urls:
            if url is not None:
                result += "url:\t" + url + "\n"
        for group in self.groups:
            if group is not None:
                result += "group:\t" + group + "\n"
        for alias in self.aliases:
            if alias is not None:
                result += "alias:\t" + alias + "\n"
        for variation in self.name_variations:
            if variation is not None:
                result += "variation:\t" + variation + "\n"
        for member_id, name in self.members:
            if name is not None:
                result += "member id:\t" + member_id + "\tmember name:\t " + name + "\n"

        return result
