# Test for creation of new Item

import pywikibot

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
# new_item.editDescriptions({"en": "Italian Greeting"})

new_item.get()

# Add description here or in another function
print new_item.getID()


new_claim = pywikibot.Claim(repo, "P63")
wb_quant = pywikibot.WbQuantity(u'1234')
new_claim.setTarget(wb_quant)
new_claim5 = pywikibot.Claim(repo, "P63")
wb_quant2 = pywikibot.WbQuantity(u'5678')
new_claim5.setTarget(wb_quant2)

new_item.addClaim(new_claim, bot=True)
new_item.addClaim(new_claim5, bot=True)

new_claim2 = pywikibot.Claim(repo, "P7")
value_item = pywikibot.ItemPage(repo, "Q9")
new_claim2.setTarget(value_item)

new_item.addClaim(new_claim2, bot=True)

new_claim3 = pywikibot.Claim(repo, "P759")
link_item = u'https://www.google.com'
new_claim3.setTarget(link_item)

new_item.addClaim(new_claim3, bot=True)

new_claim4 = pywikibot.Claim(repo, "P17322")
ext_id_item = u'1234'
new_claim4.setTarget(ext_id_item)

new_item.addClaim(new_claim4, bot=True)









