# Test for creation of new Item

import pywikibot
from pywikibot import WbQuantity

wd_site = pywikibot.Site("test", "wikidata")
repo = wd_site.data_repository()
item = pywikibot.ItemPage(repo, "Q33011")

item.get()
print item.labels

item = pywikibot.ItemPage(repo, "Q33011")

item.get()
print item.labels

new_item = pywikibot.ItemPage(wd_site)
new_item.editLabels(labels={"en": "Ciao"}, summary="Setting labels")
new_item.editAliases(aliases={"en": ["Salve", "Buongiorno"]}, summary="Setting Aliases")

new_item.get()

# Add description here or in another function
print new_item.getID()


new_claim = pywikibot.Claim(repo, "P63")
wb_quant = pywikibot.WbQuantity(u'1234')
new_claim.setTarget(wb_quant)

new_item.addClaim(new_claim, bot=True) 

new_claim2 = pywikibot.Claim(repo, "P7")
value_item = pywikibot.ItemPage(repo, "Q9")
new_claim2.setTarget(value_item)

new_item.addClaim(new_claim2, bot=True)



