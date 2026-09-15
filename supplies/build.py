# -*- coding: utf-8 -*-
"""Sortable/filterable supply price comparison for the 6 rentals.
Same pattern as build_truck_html.py: sortable headers, mobile cards, localStorage remove-pills."""
import html, datetime, os

OUT_LOCAL = r"C:\Users\wmmmo\OneDrive\Desktop\supply_prices.html"
OUT_WEB   = r"C:\temp\mvp-guest-guides\supplies\index.html"

# cat, product, retailer, pack, pack_price, unit_cost, unit, pick, take, url
D = [
# ---------- PAPER TOWELS  ($/100 sq ft) ----------
("Paper towels","Kirkland Signature Create-A-Size 2-ply","Costco warehouse","12 rolls / 1,027 sq ft",20.49,2.00,"/100 sq ft","PICK",
 "Biggest sheet in the study at 11x7, 4.8 stars on 40,704 reviews, cheapest verified price per square foot. Costco.com charges 17% more for the same box, so this one is a warehouse run.",
 "https://www.costco.com/kirkland-signature-paper-towels-2-ply-160-sheets-12-individually-wrapped-rolls.product.100234271.html"),
("Paper towels","Member's Mark Select & Tear 2-ply","Sam's Club","15 rolls / 1,031 sq ft",20.93,2.03,"/100 sq ft","",
 "Best quality signal anywhere in the study at 4.9 stars on 153,800 ratings, and the lowest cost per roll at $1.40. The smaller 11x6 sheet actually wastes less per guest grab. Sam's site was bot-blocked, so this price came off a search tile.",
 "https://www.samsclub.com/p/members-mark-super-premium-individually-wrapped-paper-towels/prod21231906"),
("Paper towels","Great Value Ultra Strong, 12 triple","Walmart","12 rolls / 892 sq ft",19.97,2.24,"/100 sq ft","",
 "Cheapest real 2-ply outside the clubs, 4.7 stars on 19,100 ratings. Currently on rollback from $22.56, so expect it to drift back toward $2.53.",
 "https://www.walmart.com/ip/Great-Value-Ultra-Strong-Paper-Towels-Triple-Rolls-12-Count/970754121"),
("Paper towels","Kirkland Create-A-Size, delivered","Costco.com","12 rolls / 1,027 sq ft",23.99,2.34,"/100 sq ft","",
 "The same box delivered instead of driving. You pay 34 cents per 100 sq ft for the convenience.",
 "https://www.costco.com/kirkland-signature-paper-towels-2-ply-160-sheets-12-individually-wrapped-rolls.product.100234271.html"),
("Paper towels","Lavex More Than Enough 2-ply, 2+ cases","WebstaurantStore","12 rolls / 1,027 sq ft",24.99,2.43,"/100 sq ft","",
 "Spec-for-spec a Kirkland clone: 2-ply, 12 rolls, 160 half sheets at 11x7. Same product, same price, and freight is on top. Buy it only if you want it delivered.",
 "https://www.webstaurantstore.com/lavex-more-than-enough-2ply-premium-half-sheet-paper-towel-roll-160-half-sheetsroll-case/5002HRMRENBOX12.html"),
("Paper towels","Presto! Ultra-Strong, 12 huge","Amazon","12 rolls / ~855 sq ft",24.00,2.81,"/100 sq ft","",
 "The delivered-to-the-door option with no membership and no freight surprise. Sold and shipped by Amazon, 4.6 stars on 115,000 ratings.",
 "https://www.amazon.com/s?k=presto+ultra-strong+paper+towels+huge+rolls"),
("Paper towels","Bounty Advanced, warehouse sale","Costco warehouse","12 rolls / 669 sq ft",22.39,3.35,"/100 sq ft","",
 "Genuinely the strongest sheet made, and it costs 68% more per square foot to get it. Both house brands are already 2-ply rated 4.8 or better, so the durability premium does not pay for itself.",
 "https://www.costco.com/p/-/bounty-advanced-paper-towels-2-ply-103-sheets-12-count/4000346087"),
("Paper towels","Lavex 8in hardwound roll, 1-ply","WebstaurantStore","6 rolls / 3,200 sq ft",29.49,0.92,"/100 sq ft","CLEANERS",
 "Cheapest paper on this page by a mile, but it needs a bolted wall dispenser and reads as gas-station restroom. Buy one case for the cleaners' supply closet, never for a guest kitchen.",
 "https://www.webstaurantstore.com/lavex-janitorial-800-white-hardwound-roll-paper-towel-case/5001RT800B.html"),
# ---------- TOILET PAPER  ($/100 sheets) ----------
("Toilet paper","Scott ComfortPlus 1-ply, 48 rolls","Amazon","48 rolls / 11,088 sheets",21.59,0.1947,"/100 sheets","PICK",
 "The one product that resolves the tension: 1-ply so it dissolves, but engineered 3x thicker than the leading value brand so guests read it as premium. It carries a dissolve claim with a named comparator, which almost nothing else does.",
 "https://www.amazon.com/dp/B0DX33Q9QH"),
("Toilet paper","Scott ComfortPlus, 36 rolls","Target","36 rolls / 8,316 sheets",16.99,0.2043,"/100 sheets","",
 "Identical product for a top-up run rather than a portfolio buy.",
 "https://www.target.com/p/scott-comfortplus-1-ply-toilet-paper-36-rolls/-/A-95195025"),
("Toilet paper","Scott 1000 1-ply, 45 rolls","Sam's Club","45 rolls / 45,000 sheets",30.48,0.0677,"/100 sheets","",
 "Cheapest septic-qualified paper found anywhere and the strongest dissolve claim on the market. It is also thin, and thin paper is a documented review complaint. Use it in utility and basement baths, not the primary guest bath.",
 "https://www.samsclub.com/ip/Scott-1000-1-Ply-Toilet-Paper-45-rolls-1-000-sheets-roll/5400048554"),
("Toilet paper","Great Value 1000 sheets, 12 rolls","Walmart","12 rolls / 12,000 sheets",9.48,0.0790,"/100 sheets","",
 "Same play as Scott 1000 with a weaker claim. The 1-ply construction is the real evidence, not the label.",
 "https://www.walmart.com/ip/Great-Value-1000-Sheets-per-Roll-Toilet-Paper-12-Rolls/15110314418"),
("Toilet paper","Kirkland Signature 2-ply, 30 rolls","Costco warehouse","30 rolls / 11,400 sheets",19.99,0.1754,"/100 sheets","",
 "Guest-presentable 2-ply at a good warehouse price. Its septic evidence is just the two words on the box, so it ranks below ComfortPlus on the thing you actually care about.",
 "https://www.costco.com/kirkland-signature-bath-tissue-2-ply-380-sheets-30-rolls.product.100645583.html"),
("Toilet paper","Scott Rapid-Dissolving, 48 rolls","Amazon","48 rolls / 11,088 sheets",31.99,0.2885,"/100 sheets","INSURANCE",
 "The only national brand with a genuine RV and marine dissolve rating. It costs 48% more per sheet, so it is not the everyday stock. Put it in whichever property has the weakest drain field.",
 "https://www.amazon.com/dp/B0FSP8HRLK"),
("Toilet paper","Amazon Basics RV/Marine 2-ply, 24 rolls","Amazon","24 rolls / 7,200 sheets",20.99,0.2915,"/100 sheets","",
 "The only 2-ply with a real waste-tank rating. This is the swap if a property gets a specific guest complaint about 1-ply.",
 "https://www.amazon.com/dp/B08XYQP5QM"),
("Toilet paper","Charmin Ultra Soft, 30 rolls","Costco","30 rolls / 5,910 sheets",34.99,0.5920,"/100 sheets","AVOID",
 "Most expensive per sheet in the study and the worst thing you can put in a drain field. Plush cushioned 2-ply built for wet strength, which is the opposite of dissolving.",
 "https://www.costco.com/CatalogSearch?keyword=charmin+ultra+soft"),
("Toilet paper","Quilted Northern Ultra Plush 3-ply, 36 rolls","Sam's Club","36 rolls / 9,180 sheets",27.98,0.3048,"/100 sheets","AVOID",
 "3-ply plush is the single worst construction for a septic system. Every septic source says the same thing: avoid 3-ply, quilted and lotion-infused.",
 "https://www.samsclub.com/ip/Quilted-Northern-Ultra-Plush-3-Ply-Toilet-Paper-36-rolls-255-sheets-roll/13611256081"),
# ---------- KITCHEN BAGS ($/bag) ----------
("Kitchen bags 13gal","Kirkland Flex-Tech drawstring, 200ct","Costco warehouse","200 bags",15.79,0.0790,"/bag","PICK",
 "The only bag in the field that publishes its thickness: a 1.8 mil reinforced top over a 0.9 mil body. The top is exactly where a drawstring bag tears on lift-out. 4.8 stars on 11,857 reviews.",
 "https://www.costco.com/p/-/kirkland-signature-flex-tech-13-gallon-kitchen-trash-bag-200-count/100342484"),
("Kitchen bags 13gal","Kirkland Flex-Tech, regular price","Costco","200 bags",22.49,0.1125,"/bag","",
 "The same bag off sale. Still second cheapest in the field, and a non-member pays only 5% over that online.",
 "https://www.costco.com/p/-/kirkland-signature-flex-tech-13-gallon-kitchen-trash-bag-200-count/100342484"),
("Kitchen bags 13gal","Member's Mark Power Flex, 200ct","Sam's Club","200 bags",17.68,0.0884,"/bag","",
 "Cheapest number found, but Sam's was bot-blocked so nothing on this row is page-verified, including the thickness.",
 "https://www.samsclub.com/p/members-mark-power-flex-tall-kitchen-drawstring-trash-bags-13-gal-200ct/P03020054"),
("Kitchen bags 13gal","Amazon Basics Flextra, 120ct","Amazon","120 bags",17.08,0.1420,"/bag","",
 "The substitute if Costco is out of stock. Flextra is the reinforced line, not the base Amazon Basics.",
 "https://www.amazon.com/Amazon-Basics-Flextra-Kitchen-Drawstring/dp/B092VPGJB9"),
("Kitchen bags 13gal","Lavex 501LD13WU drawstring, 2+ cases","WebstaurantStore","200 bags",19.49,0.1233,"/bag","",
 "Identical published construction to the Kirkland bag and 56% more expensive once measured freight is added. The commercial channel loses this one outright.",
 "https://www.webstaurantstore.com/lavex-13-gallon-0-9-mil-24-x-27-unscented-low-density-medium-duty-white-tall-kitchen-drawstring-can-liner-trash-bag-case/501LD13WU.html"),
("Kitchen bags 13gal","Lavex 15gal 8-micron flat liner, 2+ cases","WebstaurantStore","1,000 bags",34.99,0.0350,"/bag","CLEANERS",
 "Half the price of Kirkland on sale, but there is no drawstring, it is clear rather than white, and it will tear on bottle caps. Fine where the cleaner ties the knot, wrong where a guest changes the bag.",
 "https://www.webstaurantstore.com/15-gallon-8-micron-24-x-33-olympian-high-density-can-liner-trash-bag-case/50224338CL.html"),
("Kitchen bags 13gal","Hefty Ultra Strong, 150ct","Walmart","150 bags",25.89,0.1730,"/bag","",
 "The same 0.9 mil body as Kirkland at 119% more per bag.",
 "https://www.walmart.com/ip/Hefty-Ultra-Strong-13-gallon-Trash-Bags-Tall-Kitchen-Trash-Bags-White-Unscented-150-Bags/386903095"),
# ---------- SMALL BAGS ($/bag) ----------
("Small bags 4gal","Lavex 4gal 6-micron liner, 2+ cases","WebstaurantStore","2,000 bags",17.49,0.0087,"/bag","PICK",
 "The biggest single win in the whole study: a factor of nine to fourteen cheaper than retail, and freight is zero when you bundle it onto any other Webstaurant order. One case is over a year of supply across all six houses. Bathroom liners hold tissue and packaging, so a thin flat liner does that job perfectly.",
 "https://www.webstaurantstore.com/4-gallon-6-micron-17-x-18-olympian-high-density-can-liner-trash-bag-case/50217186CL.html"),
("Small bags 4gal","Plasticplace 4gal liner, 2,000ct","Amazon","2,000 bags",32.59,0.0163,"/bag","",
 "The same flat liner delivered free with no freight math and no order structuring. Twice the Lavex price and still a fraction of retail.",
 "https://www.amazon.com/s?k=plasticplace+4+gallon+high+density+liner+2000"),
("Small bags 4gal","Great Value 4gal small drawstring, 40ct","Walmart","40 bags",5.22,0.1310,"/bag","",
 "Cheapest unscented drawstring small bag at retail, 4.7 stars on 3,393 reviews. Drawstring is only worth paying for where guests handle the bag.",
 "https://www.walmart.com/ip/Great-Value-4-Gallon-Small-Drawstring-Trash-Bags-40-Bags/5343498243"),
("Small bags 4gal","Kirkland 10gal wastebasket liner, 500ct","Costco","500 bags",14.99,0.0300,"/bag","",
 "Costco does not sell a 4-gallon bag at all. This is the closest thing, and at 0.34 mil it is genuinely flimsy, clear, and has no drawstring.",
 "https://www.costco.com/kirkland-signature-10-gallon-wastebasket-liner-clear-500-count.product.100224137.html"),
("Small bags 4gal","Amazon Basics small 4gal, 80ct","Amazon","80 bags",12.01,0.1500,"/bag","AVOID",
 "Scented. Fresh Scent is the only version Amazon makes in this size, so there is no unscented fallback.",
 "https://www.amazon.com/Amazon-Basics-Gallon-Trash-Bags/dp/B09NQGR39K"),
# ---------- DISH TABS ($/tab) ----------
("Dish tabs","Great Value Original Dishwasher Pacs, 115ct","Walmart","115 tabs",13.94,0.1212,"/tab","PICK",
 "Lowest verified cost per tab, and the only product here whose retail page actually prints 'Safe for septic systems'. No membership fee, same-day pickup, 4.6 stars on 1,030 ratings.",
 "https://www.walmart.com/ip/Great-Value-Automatic-Dishwasher-Pacs-Fresh-Scent-115-Count/16759055075"),
("Dish tabs","Kirkland Platinum UltraShine, 115ct","Costco","115 tabs",13.99,0.1216,"/tab","",
 "Ties on price with more reviews, and its published ingredient list independently confirms no phosphates. Currently out of stock for delivery to 18704 and not sold at the Allentown warehouse, which is why it is not the pick.",
 "https://www.costco.com/p/-/kirkland-signature-platinum-performance-ultrashine-dishwasher-detergent-pacs-115-count/100737171"),
("Dish tabs","Finish Quantum, 100ct","Amazon","100 tabs",21.67,0.2167,"/tab","",
 "The one product with a first-party septic sentence on the manufacturer's own site. You pay 79% more per tab for that wording. 4.8 stars on 45,248 ratings.",
 "https://www.amazon.com/Finish-Dishwasher-Pre-Rinse-Detergent-Virtually/dp/B0GR6M1Q5C"),
("Dish tabs","Cascade Platinum Plus ActionPacs, 82ct","Costco","82 tabs",23.99,0.2926,"/tab","AVOID",
 "Two and a half times the Great Value pac for no septic advantage. Every tab on this page is already phosphate-free by Pennsylvania law and the 2010 industry ban, so 'septic safe' on a dish tab is a legal baseline, not a feature.",
 "https://www.costco.com/cascade-platinum-plus-dishwasher-detergent-actionpacs-fresh-82-count.product.4000350951.html"),
# ---------- LAUNDRY ($/load) ----------
("Laundry detergent","Arm & Hammer Sensitive Skin Free & Clear, 170oz","Walmart","170 loads",12.48,0.0734,"/load","PICK",
 "Cheapest verified load in the study and the right chemistry for bleached white towels: no oxygen bleach to double the septic load, no enzymes for your chlorine to destroy, plus an optical brightener and a chelating agent for hard well water. Arm & Hammer's own FAQ states its liquids are safe for septic systems.",
 "https://www.walmart.com/ip/ARM-HAMMER-Sensitive-Skin-Free-Clear-Liquid-Laundry-Detergent-Soap-170-fl-oz-170-Loads/5144605535"),
("Laundry detergent","Arm & Hammer Sensitive Skin Free & Clear, 170oz","Target","170 loads",12.49,0.0735,"/load","",
 "The same jug a penny apart, confirmed in stock at Wilkes-Barre. Two chains pricing it identically is what cross-checks the figure.",
 "https://www.target.com/p/arm-38-hammer-sensitive-skin-free-clear-liquid-laundry-detergent-170-loads-170oz/-/A-94877093"),
("Laundry detergent","Purex Unscented Free & Clear, 150oz","Target","115 loads",9.99,0.0869,"/load","",
 "The sensible backup, and it drops to about $0.074 with the $1.50 Target coupon.",
 "https://www.target.com/p/purex-unscented-free-clear-liquid-laundry-detergents-115-loads-150oz/-/A-94874782"),
("Laundry detergent","Arm & Hammer Free & Clear 2X HE, 5 gallon","WebstaurantStore","640 loads",72.49,0.1133,"/load","AVOID",
 "The counterintuitive result: the commercial pail costs 54% MORE per load than the retail jug of the same brand, needs a dispensing valve, and is awkward to move between six houses. Buy jugs, not pails.",
 "https://www.webstaurantstore.com/arm-hammer-free-clear-5-gallon-2x-he-liquid-laundry-detergent/22597550.html"),
("Laundry detergent","Kirkland Ultra Clean Free & Clear HE, 194oz","Costco","146 loads",21.49,0.1472,"/load","",
 "Twice the Arm & Hammer cost plus a membership fee.",
 "https://www.costco.com/kirkland-signature-ultra-clean-free--clear-he-liquid-laundry-detergent-146-loads-194-fl-oz.product.100525739.html"),
("Laundry detergent","Tide Pods Free & Gentle, 152ct","Costco","152 loads",34.99,0.2302,"/load","AVOID",
 "Pods cost about 3.1x the cheapest fragrance-free liquid. They only earn that premium when an untrained guest is dosing the machine, and your cleaners are dosing it.",
 "https://www.costco.com/CatalogSearch?keyword=tide+pods+free+and+gentle"),
("Laundry detergent","Noble 50 lb low-suds powder","WebstaurantStore","~150 loads",55.49,0.3700,"/load","AVOID",
 "Powder is out on principle, not price. University of Minnesota septic guidance warns that powder adds fine particles to tank sludge. On six systems that is a maintenance bill, not a saving.",
 "https://www.webstaurantstore.com/noble-chemical-50lb-low-suds-concentrated-laundry-detergent-powder/147LOWSUDS50.html"),
# ---------- K-CUPS ($/pod) ----------
("Coffee - K-Cups","Kirkland Summit Roast Organic, 120ct","Costco","120 pods",39.99,0.3330,"/pod","PICK",
 "Medium roast, organic, Fair Trade, in stock at 627 of 641 warehouses, and less than half the per-pod cost of every foodservice case. It has hit $31.99 in the last 60 days, so it is worth timing.",
 "https://app.warehouserunner.com/costco/4054210-kirkland-signature-summit-roast-120-ct-organic-k-cups-pods"),
("Coffee - K-Cups","Kirkland Summit Roast, 60-day low","Costco","120 pods",31.99,0.2670,"/pod","",
 "What the same box costs when the instant savings run. Buy deep when it does.",
 "https://app.warehouserunner.com/costco/4054210-kirkland-signature-summit-roast-120-ct-organic-k-cups-pods"),
("Coffee - K-Cups","Caffe de Aroma Colombian Supreme, 24ct","WebstaurantStore","24 pods",15.49,0.6450,"/pod","",
 "The cheapest foodservice case found, and still nearly double Costco. Every commercial K-Cup channel lands between $0.65 and $0.88.",
 "https://www.webstaurantstore.com/caffe-de-aroma-colombian-supreme-coffee-single-serve-cups-24-case/876CDACOLOM.html"),
("Coffee - K-Cups","Green Mountain Breakfast Blend, 96ct","WebstaurantStore","96 pods",72.99,0.7600,"/pod","AVOID",
 "A name brand through the restaurant channel at 2.3x the Costco pod.",
 "https://www.webstaurantstore.com/green-mountain-breakfast-blend-coffee-single-serve-cups-96-case/876GMT6520.html"),
# ---------- DRIP COFFEE ($/oz ground) ----------
("Coffee - drip","Kirkland Medium Roast ground, 40oz","Costco","40 oz",18.49,0.4620,"/oz ground","",
 "Cheapest verified medium roast, about $0.173 a cup. Buy this if you would rather the cleaners pre-load the machines. Kirkland Colombian is a hair cheaper but it is a dark roast, which is the wrong call for a rental.",
 "https://app.warehouserunner.com/costco/756053-kirkland-signature-medium-roast-coffee-40-oz-2-5-lbs"),
("Coffee - drip","Folgers Classic Roast 1.5oz frac packs, 42/case","WebstaurantStore","42 packets",40.49,0.6430,"/oz ground","PICK",
 "About 39% more per ounce than loose ground, which lands near thirty cents a pot. That buys you out of the guest-dosing problem entirely, and one review complaining the coffee was undrinkable costs far more than that.",
 "https://www.webstaurantstore.com/folgers-classic-roast-coffee-packet-1-5-oz-case/110FGPK6430.html"),
("Coffee - drip","Folgers Classic Roast, 25.9oz can","Target","25.9 oz",14.29,0.5520,"/oz ground","",
 "Sale price on the retail can, for when a Costco run is not happening.",
 "https://www.target.com/s?searchTerm=folgers+classic+roast+ground+coffee"),
("Coffee - drip","Folgers Classic, single can","WebstaurantStore","25.9 oz",23.49,0.9070,"/oz ground","AVOID",
 "Roughly double the warehouse-club rate for the identical can. Never buy loose ground coffee through the restaurant channel.",
 "https://www.webstaurantstore.com/search/folgers-classic-roast-coffee.html"),
# ---------- TEA ($/bag) ----------
("Tea","Lipton Classic Black, 1,000/case","WebstaurantStore","1,000 bags",50.99,0.0510,"/bag","PICK",
 "Individually wrapped envelopes at a nickel a bag, verified on the listing. This is the everyday black tea.",
 "https://www.webstaurantstore.com/lipton-classic-black-tea-bags-case/110LIP2912CS.html"),
("Tea","Bigelow Herbal Assortment, 168ct","Costco","168 bags",20.99,0.1250,"/bag","PICK",
 "Six flavors, foil-sealed, covering the caffeine-free and flavored side. Running these two together costs about a third of putting Bigelow everywhere.",
 "https://app.warehouserunner.com/costco/291446-bigelow-herbal-tea-assortment-6-28-ct-168-ct"),
("Tea","Bromley Estate Regular, 1,000/case","WebstaurantStore","1,000 bags",30.99,0.0310,"/bag","",
 "Cheapest tea found, but the listing says nothing about individual wrapping and I would not assume it.",
 "https://www.webstaurantstore.com/search/bromley-estate-tea.html"),
("Tea","Bigelow Variety Tray, 384ct","WebstaurantStore","384 bags",82.99,0.2160,"/bag","AVOID",
 "Four times the Lipton cost for the same job. The tray is built for a hotel lobby, not six kitchens.",
 "https://www.webstaurantstore.com/bigelow-assorted-green-and-black-teas-case/11015577.html"),
# ---------- SPONGES ($/sponge) ----------
("Sponges","DZee Individually Wrapped Sponge Combo, 2 cases","DZee","600 sponges",158.90,0.2650,"/sponge","PICK",
 "Real scouring pad, individually wrapped, landed price including the flat $39 delivery. Roughly 40% under the best Costco price. Six hundred sponges is close to a year of turnovers across six properties.",
 "https://dzeeusa.com/individually-wrapped-sponge-combo-300-case.html"),
("Sponges","DZee sponge combo, one case landed","DZee","300 sponges",98.95,0.3300,"/sponge","",
 "The same product, one case. The flat $39 freight under $999 is why buying two at a time matters.",
 "https://dzeeusa.com/individually-wrapped-sponge-combo-300-case.html"),
("Sponges","Scotch-Brite Zero Scratch, 24ct","Costco","24 sponges",10.79,0.4500,"/sponge","",
 "The practical Costco fallback with no freight and no minimum. It has no aggressive abrasive side, which matters on baked-on pans.",
 "https://app.warehouserunner.com/costco/1717856-scotch-brite-zero-scratch-sponge-24-count"),
("Sponges","Scotch-Brite Heavy Duty, 24ct","Costco","24 sponges",13.01,0.5420,"/sponge","",
 "Genuinely individually wrapped with a true abrasive side, and out of stock at 87% of warehouses right now.",
 "https://app.warehouserunner.com/costco/1717853-scotch-brite-heavy-duty-sponge-24-ct"),
("Sponges","Boardwalk BWK174, 20ct","Home Depot","20 sponges",27.05,1.3530,"/sponge","AVOID",
 "Five times the DZee price for the same wrapped-sponge job.",
 "https://www.homedepot.com/s/boardwalk%2520BWK174%2520sponge"),
# ---------- HAND SOAP ($/fl oz) ----------
("Hand soap","Ginger Lily Farms Club & Fitness, fragrance free, 1 gal","Amazon","128 fl oz",19.99,0.1562,"/fl oz","PICK",
 "Unscented so it offends nobody, gentle on sensitive skin, not antibacterial, 4.6 stars on 1,305 reviews, and free delivery over $35 with no membership and no freight surprise.",
 "https://www.amazon.com/dp/B0BYKQW3DN"),
("Hand soap","Softsoap Advanced Clean, 80oz x 2","Costco","160 fl oz",12.99,0.0812,"/fl oz","",
 "Half the price of the true gallons, 4.8 stars on 8,146 ratings. Two 80oz jugs pour into a dispenser exactly like a gallon does. Limit five per membership.",
 "https://www.costco.com/softsoap-advanced-clean-liquid-hand-soap-refill-80-oz-2-pack.product.100385266.html"),
("Hand soap","Noble Free & Clear, 4-gallon case","WebstaurantStore","512 fl oz",38.49,0.0752,"/fl oz","",
 "Less than half the Amazon gallon per ounce, dye and fragrance free. Budget for unverified freight on a 36 lb case before committing.",
 "https://www.webstaurantstore.com/noble-chemical-1-gallon-128-oz-free-clear-liquid-hand-soap/999FREECLR.html"),
("Hand soap","Advantage Chemicals, 4-gallon case","WebstaurantStore","512 fl oz",30.99,0.0605,"/fl oz","",
 "Absolute floor price per ounce in the study. The page does not specify scent, and freight is unquoted.",
 "https://www.webstaurantstore.com/advantage-chemicals-1-gallon-hand-soap-case/146HANDSOAP.html"),
("Hand soap","Dial Antibacterial & Sensitive, 1 gal","WebstaurantStore","128 fl oz",27.49,0.2148,"/fl oz","AVOID",
 "Antibacterial. The biocide kills the working bacteria in the septic tank along with everything else. Same reason to skip Dial Gold, Member's Mark Commercial Antibacterial and any Softsoap Antibacterial variant.",
 "https://www.webstaurantstore.com/search/dial-antibacterial-hand-soap-gallon.html"),
# ---------- DISH SOAP ($/fl oz) ----------
("Dish soap","Dawn Professional Original, 1 gal, item 169750","Costco","128 fl oz",15.79,0.1234,"/fl oz","PICK",
 "Cheapest verified gallon in the study and it ships with a locking pump included, which is a $7.89 part you do not have to buy six of. The page states no phosphate and biodegradable surfactants. The $3.20 instant saving runs 8/24 through 9/20, limit 5 per member.",
 "https://www.costco.com/dawn-professional-dish-detergent-original-1-gal.product.100768392.html"),
("Dish soap","Kirkland Signature Ultra Shine, 90oz","Costco","90 fl oz",9.99,0.1110,"/fl oz","",
 "Cheapest per ounce, but it is not a gallon and not a concentrate, so it does not fit the pump-and-refill setup as cleanly.",
 "https://www.costco.com/CatalogSearch?keyword=dish+soap"),
("Dish soap","Ginger Lily Farms Plant-Based, fragrance free, 1 gal","Amazon","128 fl oz",19.99,0.1562,"/fl oz","",
 "The only product in the entire report that states 'is septic tank safe' in writing and names the compounds it leaves out. Buy this one if you want the explicit wording rather than the lowest price.",
 "https://www.amazon.com/Ginger-Lily-Farms-Fragrance-Free-802309/dp/B08QL53RFN"),
("Dish soap","Palmolive Ultra Professional, 4-pack case","WebstaurantStore","580 fl oz",74.99,0.1293,"/fl oz","",
 "Ready-to-use rather than concentrated, and freight is on top.",
 "https://www.webstaurantstore.com/palmolive-ultra-professional-cpc61034142ea-145-oz-original-scent-dishwashing-liquid/999CPCP6134142.html"),
# ---------- BODY WASH ($/fl oz) ----------
("Body wash","Ginger Lily Farms Island Tranquility, 1 gal","Amazon","128 fl oz",21.99,0.1718,"/fl oz","PICK",
 "Green tea, lemongrass and ginger. It smells like a spa, which is exactly the failure mode of the institutional hair-and-body gallons. 4.5 stars on 8,076 reviews is the deepest review base in the category.",
 "https://www.amazon.com/Ginger-Lily-Farms-Botanicals-Cruelty-Free/dp/B00DQSKVIO"),
("Body wash","Ginger Lily Farms Club & Fitness, fragrance free, 1 gal","Walmart","128 fl oz",19.99,0.1562,"/fl oz","",
 "The unscented option, and the cheapest gallon body wash found.",
 "https://www.walmart.com/ip/Ginger-Lily-Farms-Club-Fitness-Conditioning-Liquid-Hand-Soap-Refill-100-Vegan-Cruelty-Free-Fragrance-Free-1-Gallon-128-fl-oz/3289431897"),
("Body wash","Zogics Organics Fresh Air, 1 gal","Zogics","128 fl oz",19.95,0.1559,"/fl oz","",
 "Citrus scent, free of parabens and phthalates. Only two reviews, so there is no real quality signal behind it.",
 "https://zogics.com/bath-body/zogics-organics-fresh-air-body-wash-1-gallon"),
("Body wash","Dial Professional Hair + Body, 4-gallon case","WebstaurantStore","512 fl oz",76.49,0.1494,"/fl oz","",
 "Cheaper per ounce in a case, but the fragrance is unnamed institutional and it reads as gym locker room in a guest shower.",
 "https://www.webstaurantstore.com/dial-dia03986-1-gallon-hair-and-body-wash-refill/999DIA03986.html"),
("Body wash","Pharmacopia Verbena Hotel Collection, 1 gal","Pharmacopia","128 fl oz",125.00,0.9766,"/fl oz","AVOID",
 "Nearly six times the pick for a scent nobody will name in a review.",
 "https://store.pharmacopia.net/products/verbena-hotel-collection-body-wash-1-gallon-refill"),
# ---------- HARDWARE ($ each) ----------
("Dispensers & pumps","Dispenser Amenities Aviva 2-chamber shower unit","WebstaurantStore","20 oz, 2 chambers",34.49,34.49,"each","PICK",
 "Body wash and shampoo in one shower unit, tamper-proof locking lid, adhesive mount so you are not drilling tile. Six of these is $206.94.",
 "https://www.webstaurantstore.com/dispenser-amenities-37250-aviva-20-oz-solid-white-2-chamber-wall-mounted-locking-shower-dispenser-with-bottles/52637250.html"),
("Dispensers & pumps","Dispenser Amenities Aviva 1-chamber, satin silver","WebstaurantStore","10 oz",25.49,25.49,"each","",
 "The vanity version. Translucent bottle so cleaners can see the level without opening it. Twelve of these is $305.88.",
 "https://www.webstaurantstore.com/dispenser-amenities-36134-aviva-10-oz-satin-silver-wall-mounted-locking-soap-dispenser-with-translucent-bottle/52636134.html"),
("Dispensers & pumps","Lavex 11in gallon pump, lot of 10","WebstaurantStore","1 oz per stroke",5.99,5.99,"each","PICK",
 "Back-of-house only. Screws onto the gallon jugs in the utility closet so cleaners pump into a carry bottle and top off the wall units on turnover. Fits a 38mm cap, trimmable dip tube.",
 "https://www.webstaurantstore.com/lavex-11-1-oz-plastic-pump-dispenser-for-1-gallon-plastic-bottles/000DP30CC.html"),
("Dispensers & pumps","38/400 white gallon jug pump","Wholesale Supplies Plus","1 oz per stroke",3.86,3.86,"each","",
 "Cheapest verified US pump, 4.88 stars on 103 reviews, Ohio seller. Forty-six dollars for twelve.",
 "https://www.wholesalesuppliesplus.com/products/38-400-gallon-jug-pump.aspx"),
("Dispensers & pumps","Lavex 40oz manual soap dispenser","WebstaurantStore","40 oz",14.49,14.49,"each","AVOID",
 "2.3 stars on 6 reviews with repeated leak complaints. Cheap for a reason.",
 "https://www.webstaurantstore.com/search/lavex-manual-soap-dispenser.html"),
]

CATS = []
for r in D:
    if r[0] not in CATS:
        CATS.append(r[0])

BADGE = {"PICK": ("#1b7f4b", "#e6f4ec"), "AVOID": ("#a33", "#f6d0d0"),
         "CLEANERS": ("#7a5b12", "#fdf3c9"), "INSURANCE": ("#7a5b12", "#fdf3c9")}

rows = []
for cat, prod, ret, pack, pp, uc, unit, pick, take, url in D:
    fg, bg = BADGE.get(pick, ("", "#ffffff"))
    badge = '<span class="badge" style="color:%s">%s</span>' % (fg, pick) if pick else ""
    ucs = ("$%.4f" % uc).rstrip("0").rstrip(".") if uc < 1 else "$%,.2f".replace("%,", "%") % uc
    rows.append("""<tr style="background:{bg}" data-key="{k}" data-cat="{cat}">
      <td data-label="" class="rmcell"><span class="rm" onclick="rm(this)" title="Remove from list">&#10005; remove</span></td>
      <td data-label="Category">{cat}</td>
      <td data-label="Product"><a href="{k}" target="_blank">{prod}</a> {badge}</td>
      <td data-label="Where">{ret}</td>
      <td data-label="Unit cost" data-v="{uc}" class="num"><b>{ucs}</b> <span class="u">{unit}</span></td>
      <td data-label="Pack price" data-v="{pp}" class="num">${ppf}</td>
      <td data-label="Pack">{pack}</td>
      <td data-label="My take" class="take">{take}</td></tr>""".format(
        bg=bg, k=html.escape(url), cat=html.escape(cat), prod=html.escape(prod), badge=badge,
        ret=html.escape(ret), uc=uc, ucs=ucs, unit=html.escape(unit), pp=pp, ppf="{:,.2f}".format(pp),
        pack=html.escape(pack), take=html.escape(take)))
body = "\n".join(rows)
opts = "\n".join('<option value="%s">%s</option>' % (html.escape(c), html.escape(c)) for c in CATS)
# Date these prices were actually gathered. Update ONLY when you re-price.
# Never use datetime.now() here - a plain rebuild would falsely claim fresh prices.
ts = "Sep 10, 2026 04:20 PM"

CSS = """
body{font-family:-apple-system,Segoe UI,Arial,sans-serif;margin:24px;background:#fafafa;color:#1a1a1a}
h1{margin:0 0 2px} .sub{color:#666;margin:0 0 14px;font-size:14px}
table{border-collapse:collapse;width:100%;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.12);font-size:14px}
th,td{padding:8px 10px;border-bottom:1px solid #eee;text-align:left;vertical-align:top}
th{background:#1f4e5f;color:#fff;cursor:pointer;position:sticky;top:0;white-space:nowrap}
th:hover{background:#2e7d8a} .num{text-align:right;white-space:nowrap}
td a{color:#1155cc;text-decoration:none;font-weight:600} td a:hover{text-decoration:underline}
.take{color:#333;max-width:560px} .u{color:#777;font-size:11px}
.badge{font-size:10px;font-weight:800;letter-spacing:.4px;margin-left:6px;white-space:nowrap}
.rm{display:inline-block;border:1px solid #c66;color:#c33;border-radius:12px;padding:1px 8px;font-size:12px;font-weight:700;cursor:pointer;user-select:none}
.rm:hover{background:#c33;color:#fff}
.hint{color:#888;font-size:12px;margin:6px 0 10px}
.ctrl{margin:10px 0;font-size:15px;font-weight:600}
.ctrl select{font-size:16px;padding:6px 8px;border-radius:6px;border:1px solid #bbb;margin:0 14px 0 6px}
.msort{display:none}
@media (max-width:760px){
  .msort{display:inline}
  body{margin:10px;font-size:15px} h1{font-size:20px}
  .ctrl select{display:block;margin:6px 0 12px;width:100%}
  table{box-shadow:none;background:transparent;font-size:15px}
  thead{display:none}
  tbody tr{display:block;border:1px solid #ddd;border-radius:10px;margin:0 0 12px;padding:10px 12px;
           box-shadow:0 1px 3px rgba(0,0,0,.12)}
  tbody td{display:flex;justify-content:space-between;gap:14px;border:0;padding:4px 0;text-align:left}
  tbody td:before{content:attr(data-label);font-weight:700;color:#5a5a5a;font-size:12px;
                  text-transform:uppercase;letter-spacing:.3px;flex:0 0 auto}
  tbody td.take{display:block} tbody td.take:before{display:block;margin-bottom:3px}
  tbody td.rmcell{justify-content:flex-end;padding-top:6px} tbody td.rmcell:before{display:none}
  .rm{padding:6px 14px;font-size:14px}
  td a{font-size:16px} .take{max-width:none}
}
"""

JS = """
var RK='supply_prices_removed';
function getRm(){try{return JSON.parse(localStorage.getItem(RK)||'[]')}catch(e){return []}}
function rm(el){var tr=el.closest('tr');var k=tr.dataset.key;var l=getRm();if(l.indexOf(k)<0)l.push(k);
try{localStorage.setItem(RK,JSON.stringify(l))}catch(e){}tr.dataset.rm='1';show(tr);}
function show(tr){var f=document.getElementById('f').value;
tr.style.display=(tr.dataset.rm=='1'||(f&&tr.dataset.cat!=f))?'none':'';}
function applyRm(){var l=getRm();document.querySelectorAll('#t tbody tr').forEach(function(tr){
if(l.indexOf(tr.dataset.key)>=0)tr.dataset.rm='1';show(tr);});}
function resetRm(){try{localStorage.removeItem(RK)}catch(e){}
document.querySelectorAll('#t tbody tr').forEach(function(tr){tr.dataset.rm='';show(tr);});}
function filt(){document.querySelectorAll('#t tbody tr').forEach(show);}
document.addEventListener('DOMContentLoaded',applyRm);
function s(c){var tb=document.querySelector('#t tbody');var rs=[].slice.call(tb.rows);
var asc=tb.getAttribute('sc')!=c+'a';rs.sort(function(a,b){
var x=a.cells[c].dataset.v!==undefined?a.cells[c].dataset.v:a.cells[c].innerText;
var y=b.cells[c].dataset.v!==undefined?b.cells[c].dataset.v:b.cells[c].innerText;
var nx=parseFloat(x),ny=parseFloat(y);if(!isNaN(nx)&&!isNaN(ny)){x=nx;y=ny}
return (x>y?1:x<y?-1:0)*(asc?1:-1);});
tb.setAttribute('sc',c+(asc?'a':'d'));rs.forEach(function(r){tb.appendChild(r)});}
"""

doc = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Rental Supply Prices</title>
<meta property="og:title" content="MVP Rentals - Supply Price Comparison">
<meta property="og:description" content="Unit-cost comparison across Costco, Sam's Club, Walmart, Target, Amazon and the commercial channel.">
<meta property="og:image" content="https://a799608.github.io/mvp-guest-guides/og-cover.jpg">
<meta property="og:url" content="https://a799608.github.io/mvp-guest-guides/supplies/">
<style>%CSS%</style></head><body>
<h1>Rental supplies &mdash; unit cost comparison</h1>
<p class="sub">Priced %TS% &middot; Costco, Sam's Club, Walmart, Target, Amazon, WebstaurantStore and hotel supply &middot; every row ranked on unit cost, not pack price</p>
<div class="ctrl">Category: <select id="f" onchange="filt()"><option value="">All</option>
%OPTS%
</select><span class="msort">Sort: <select onchange="s(+this.value)"><option value="4">Unit cost</option><option value="5">Pack price</option><option value="1">Category</option><option value="2">Product</option></select></span></div>
<p class="hint">Green = my pick &middot; red = do not buy &middot; yellow = back-of-house or insurance only &middot; &#10005; drops a row for good on this browser &middot; <a href="#" onclick="resetRm();return false">show removed / reset</a></p>
<table id="t"><thead><tr>
<th></th><th onclick="s(1)">Category</th><th onclick="s(2)">Product (opens the listing)</th><th onclick="s(3)">Where</th>
<th onclick="s(4)">Unit cost</th><th onclick="s(5)">Pack price</th><th onclick="s(6)">Pack</th><th onclick="s(7)">My take</th>
</tr></thead><tbody>
%BODY%
</tbody></table>
<p class="hint">Sam's Club blocked every automated read with a bot wall, so its rows came off search tiles and are not page-verified. Costco warehouse prices differ from Costco.com. Costco membership is $65 a year or a 5% online surcharge; Sam's is $60 a year or a 10% guest surcharge. WebstaurantStore freight is real money on paper goods and zero on small liners bundled onto a bigger order.</p>
<script>%JS%</script></body></html>"""

doc = doc.replace("%CSS%", CSS).replace("%JS%", JS).replace("%TS%", ts).replace("%OPTS%", opts).replace("%BODY%", body)

os.makedirs(os.path.dirname(OUT_WEB), exist_ok=True)
for p in (OUT_LOCAL, OUT_WEB):
    open(p, "w", encoding="utf-8").write(doc)
    print("SAVED:", p)
print("rows:", len(D), "cats:", len(CATS))
