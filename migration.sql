
-- ============================================================
-- Surf Dash — Supabase Migration
-- Run this in Supabase SQL Editor
-- ============================================================

CREATE TABLE IF NOT EXISTS athletes (
    id SERIAL PRIMARY KEY,
    sheet_key TEXT UNIQUE,
    name TEXT,
    country TEXT,
    discipline TEXT,
    tour TEXT,
    ranking_season TEXT,
    current_ranking TEXT,
    stance TEXT,
    home_break TEXT,
    known_for TEXT,
    notes TEXT,
    photo_url TEXT DEFAULT '',
    gender TEXT DEFAULT 'Men'
);

CREATE TABLE IF NOT EXISTS sponsors (
    id SERIAL PRIMARY KEY,
    athlete_id INTEGER REFERENCES athletes(id),
    name TEXT,
    type TEXT,
    since TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS injuries (
    id SERIAL PRIMARY KEY,
    athlete_id INTEGER REFERENCES athletes(id),
    inj_date TEXT,
    type TEXT,
    body_part TEXT,
    severity TEXT,
    return_date TEXT,
    notes TEXT,
    active INTEGER DEFAULT 1,
    logged_by TEXT DEFAULT '',
    logged_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS comp_results (
    id SERIAL PRIMARY KEY,
    athlete_id INTEGER REFERENCES athletes(id),
    season TEXT,
    event TEXT,
    tour TEXT,
    event_date TEXT,
    location TEXT,
    round TEXT,
    place INTEGER,
    points REAL,
    heat_score TEXT,
    notes TEXT,
    source_url TEXT
);

CREATE TABLE IF NOT EXISTS ranking_history (
    id SERIAL PRIMARY KEY,
    athlete_id INTEGER REFERENCES athletes(id),
    season TEXT,
    tour TEXT,
    as_of TEXT,
    ranking INTEGER,
    points REAL,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS physical_testing (
    id SERIAL PRIMARY KEY,
    athlete_id INTEGER REFERENCES athletes(id),
    test_date TEXT,
    test_type TEXT,
    metric TEXT,
    value TEXT,
    unit TEXT,
    notes TEXT,
    logged_by TEXT DEFAULT '',
    logged_at TIMESTAMP DEFAULT NOW()
);


-- Athletes
INSERT INTO athletes VALUES ('1','Annette_Gonzalez_Etxabarri','Annette Gonzalez Etxabarri','Spain','Challenger','WSL Challenger','2026','CS Competitor','Regular','Getxo, Basque Country, Spain','European Junior Champion; rising CS competitor with powerful backhand and strong rail surfing.','Promising Spanish prospect. Strong Basque surf culture background.','','Men');
INSERT INTO athletes VALUES ('2','Arthur_Vilar','Arthur Vilar','Brazil','Challenger','WSL Challenger','2026','CS/Junior','Regular','Baía Formosa, Rio Grande do Norte, Brazil','Young Brazilian prodigy; Italo Ferreira protégé. Multi-time Brazilian national youth champion.','From same hometown as Italo Ferreira. Multiple national youth titles. One to watch.','','Men');
INSERT INTO athletes VALUES ('3','Ben_Larg','Ben Larg','UK','Big Wave','Big Wave','2026','Big Wave','Regular','Tiree, Scotland, UK','Youngest surfer to charge Mullaghmore Head; Scotland''s top big wave name charging 50ft+ Atlantic slabs.','Cold-water big wave charger. Represents UK in XXL-level surf.','','Men');
INSERT INTO athletes VALUES ('4','Caity_Simmers','Caity Simmers','USA','CT','WSL CT','2026','#5 WSL CT (2026)','Goofy','Oceanside, California, USA','2024 World Champion at 18 — youngest ever. Punk-rock freesurfing approach with explosive aerials, alley-oops, and creative improvisation.','Youngest women''s world champ. Took break post-2024. Wildcard for 2026.','','Women');
INSERT INTO athletes VALUES ('5','Carissa_Moore','Carissa Moore','USA','CT','WSL CT','2026','5x World Champion / Wildcard 2026','Regular','Waikiki, Oahu, Hawaii, USA','5x World Champion (2011/13/15/19/21) and 2021 Olympic Gold medalist. Power surfing with creative flair; dominant across all conditions.','GOAT of women''s surfing. Returned to tour post-motherhood 2026. Pioneered mental health advocacy.','','Women');
INSERT INTO athletes VALUES ('6','Caroline_Marks','Caroline Marks','USA','CT','WSL CT','2026','#2 WSL CT','Goofy','San Clemente, California, USA','2023 World Champion and 2024 Olympic Gold medalist. Outstanding barrel riding, heat strategy, and consistency.','Withdrew mid-2022 for health reasons; came back stronger. Grew up in Melbourne Beach, FL.','','Women');
INSERT INTO athletes VALUES ('7','Conor_Maguire','Conor Maguire','Ireland','Big Wave','Big Wave','2026','Big Wave','Regular','Bundoran, Ireland','Surfed 60ft wave at Mullaghmore in 2025; six-time Big Wave Awards nominee. Ireland''s premier big wave surfer.','WSL Big Wave Tour competitor. Fearless cold-water surfer. Six BWA nominations.','','Men');
INSERT INTO athletes VALUES ('8','Dominique_Charrier','Dominique Charrier','Chile','Big Wave','Big Wave','2026','Big Wave','Regular','Punta de Lobos, Chile','Top women''s big wave charger pursuing world records at Nazaré and beyond. Breaking into the world''s heaviest lineups.','Chilean big wave pioneer. Broke into the Nazaré lineup.','','Men');
INSERT INTO athletes VALUES ('9','Erin_Brooks','Erin Brooks','Canada','CT','WSL CT','2026','2025 Rookie of the Year','Regular','Kailua, Hawaii, USA','2025 CT Rookie of the Year. Landed a perfect 360 air at age 13. Canada''s fastest-rising competitive surfer.','Canadian-born, Hawaii-raised. Explosive progression through junior ranks.','','Women');
INSERT INTO athletes VALUES ('10','Griffin_Colapinto','Griffin Colapinto','USA','CT','WSL CT','2026','#4 WSL CT (2026 Preseason)','Regular','San Clemente, California, USA','One of the best backside surfers on tour. Powerful vertical approach. Came close to becoming California''s first male world champ since Tom Curren.','Switched to Quiksilver from Billabong. Works with shaper Matt Biolos. WSL Finals regular.','','Men');
INSERT INTO athletes VALUES ('11','Ian_Walsh','Ian Walsh','USA','Big Wave','Big Wave','2026','Big Wave','Regular','Maui, Hawaii, USA','Pioneer of paddle surfing at Pe''ahi (Jaws). One of the most respected big wave professionals; charges 60ft+ Maui swells.','Active in ocean safety and rescue. Multi-time Eddie Aikau competitor.','','Men');
INSERT INTO athletes VALUES ('12','Italo_Ferreira','Italo Ferreira','Brazil','CT','WSL CT','2026','2019 World Champion','Goofy','Baía Formosa, Rio Grande do Norte, Brazil','2019 World Champ and first Olympic gold medalist in surfing (Tokyo 2020). Impossibly high aerials, full-rotation moves, explosive power from a tiny fishing village.','Overcame poverty in NE Brazil. One of the most progressive surfers ever. Consistent top-5 threat.','','Men');
INSERT INTO athletes VALUES ('13','Izzi_Gomez','Izzi Gomez','USA','Free Surf','Other','2026','Free Surf / Big Wave','Regular','Jupiter, Florida, USA','Five-time SUP World Champion by age 21. Transitioned to big wave surfing and foiling. Multi-discipline water sports athlete.','Child prodigy in SUP; crossed over to big wave and foil events.','','Men');
INSERT INTO athletes VALUES ('14','Jack_Robinson','Jack Robinson','Australia','CT','WSL CT','2026','4th WSL CT 2024 / Olympic Silver','Regular','Margaret River, Western Australia, Australia','Elite barrel rider — the best tube rider of his generation. Master of Pipeline, Cloudbreak, and The Box. Patient, calculating, deadly in heavy surf.','Silver medalist Paris 2024. Meniscus repaired late 2025. Grew up at Margaret River.','','Men');
INSERT INTO athletes VALUES ('15','Jaime_Veselko','Jaime Veselko','Slovenia','Challenger','WSL Challenger','2026','CS Competitor','Regular','Carcavelos, Portugal (trains) / Slovenia','Slovenia''s first internationally competitive surfer. Competing in WSL Junior and Challenger Series events.','Rare European prospect from non-traditional surf nation. Based in Portugal for training.','','Men');
INSERT INTO athletes VALUES ('16','Jamie_OBrien','Jamie O’Brien','USA','Free Surf','Free Surf','2026','Free Surf','Regular','Pipeline, North Shore, Oahu, Hawaii, USA','2004 Pipeline Masters champion. One of the greatest tube riders at Pipe. Creator of hugely popular WHO IS JOB YouTube and social content.','Pipeline local legend. Charges Pipe on any craft — bodyboard, alaia, foil. Massive social following.','','Men');
INSERT INTO athletes VALUES ('17','Jarvis_Earle','Jarvis Earle','Australia','Challenger','WSL Challenger','2026','CS Competitor','Goofy','Cronulla, New South Wales, Australia','2022 WSL World Junior Champion. Dynamic, powerful surfing with strong CT aspirations.','Won World Juniors 2022. Working through Challenger Series to earn CT spot.','','Men');
INSERT INTO athletes VALUES ('18','Joao_Chianca','João Chianca','Brazil','CT','WSL CT','2026','Top 5 CT Threat','Regular','Saquarema, Rio de Janeiro, Brazil','Nicknamed Chumbinho. Unlimited speed and tenacity. Made WSL Finals 2023. Remarkable comeback from near-fatal skull fracture at Pipeline.','Fractured skull + brain bleeding at Pipeline Dec 2023. Returned to tour mid-2024 stronger.','','Men');
INSERT INTO athletes VALUES ('19','Jordy_Smith','Jordy Smith','South Africa','CT','WSL CT','2026','#1 WSL CT 2025','Regular','Durban, KwaZulu-Natal, South Africa','#1 ranked CT surfer (2025). Won first event in 8 years in 2025. Power surfing with enormous frame and explosive turns.','Veteran campaigner. Won Bells Beach 2025. South Africa''s greatest competitive surfer.','','Men');
INSERT INTO athletes VALUES ('20','Josh_Kerr','Josh Kerr','Australia','Free Surf','Free Surf','2026','Free Surf','Regular','Tweed Heads, New South Wales, Australia','Pioneer of progressive air surfing. Founder of Red Bull Airborne competition. Founder of Draft Surfboards. Retired CT competitor.','Retired from CT; pure freesurfer/entrepreneur. Influential in pushing aerial surfing mainstream.','','Men');
INSERT INTO athletes VALUES ('21','Justine_Dupont','Justine Dupont','France','Big Wave','Big Wave','2026','Big Wave','Regular','Bordeaux, France','12x XXL World Champion. Second-largest wave ever by a woman (70.5ft at Nazaré). Won 2025 Nazaré Big Wave event. Greatest female big wave surfer alive.','Partner of Lucas Chianca. Charges Nazaré, Jaws, Mullaghmore.','','Men');
INSERT INTO athletes VALUES ('22','Kai_Lenny','Kai Lenny','USA','Big Wave','Big Wave','2026','Big Wave / Foil','Regular','Maui, Hawaii, USA','First athlete with world titles in surfing, wind foiling, SUP, and kiteboarding. Pioneer of downwind foiling. Ultimate waterman.','Eddie Aikau invitee. Charges Jaws on foil. Game-changer across all ocean sports.','','Men');
INSERT INTO athletes VALUES ('23','Kamiel_Deraeve','Kamiel Deraeve','Belgium','Big Wave','Big Wave','2026','Big Wave (Young Gun)','Regular','Fuerteventura, Canary Islands','Belgium''s prodigy big wave charger. One of the youngest surfers to paddle Nazaré. Big Wave Awards contender at an exceptionally young age.','Born 2011. Belgian/Canary Islands-based. Youngest competitor at 2025 Big Wave Challenge Awards.','','Men');
INSERT INTO athletes VALUES ('24','Kanoa_Igarashi','Kanoa Igarashi','Japan','CT','WSL CT','2026','Top 10 CT','Regular','Huntington Beach, California, USA','Two-time US Open champion. First Japanese surfer to win a WSL CT event. Tokyo 2020 Olympic Silver medalist. Chose Japan over USA at 18.','Parents moved to Huntington Beach specifically for his surfing. Fashion-forward personality.','','Men');
INSERT INTO athletes VALUES ('25','Kauli_Vaast','Kauli Vaast','France','CT','WSL CT','2026','#22 WSL CT (2026 Rookie)','Goofy','Teahupo''o, Tahiti, French Polynesia','2024 Olympic Gold medalist at his home break Teahupo''o. Powerful rail surfer with elite barrel ability. First-year CT rookie in 2026.','Won Olympic gold at the most fearsome wave on earth. Signed Dior brand deal post-Olympics.','','Men');
INSERT INTO athletes VALUES ('26','Lachlan_Cullen','Lachlan Cullen','Australia','Challenger','WSL Challenger','2026','CS Competitor','Regular','Australia','Australian Challenger Series competitor and Red Bull athlete.','Limited public profile. Competes on WSL Challenger Series.','','Men');
INSERT INTO athletes VALUES ('27','Laura_Coviella','Laura Coviella','Spain','Big Wave','Big Wave','2026','Big Wave','Regular','Canary Islands, Spain','First Spanish woman to surf Nazaré. Pioneering women''s big wave surfing in Europe at just 24 years old.','Young Spanish big wave pioneer. Breaking barriers in European big wave surfing.','','Men');
INSERT INTO athletes VALUES ('28','Leon_Glatzer','Leon Glatzer','Germany','Free Surf','Free Surf','2026','Free Surf','Goofy','Ericeira, Portugal (trains) / Germany','Germany''s top professional surfer. Olympic representative (Tokyo 2020). Explosive aerial game and unpredictable freesurfing style.','Based in Portugal for training. Pioneered German surfing on world stage.','','Men');
INSERT INTO athletes VALUES ('29','Leonardo_Fioravanti','Leonardo Fioravanti','Italy','CT','WSL CT','2026','#8 WSL CT 2026','Regular','Rome, Italy','Italy''s first CT surfer. Powerful vertical forehand and impressive aerial game. Remarkable comeback from fractured L1 vertebra in 2015 with 2 surgical plates.','Won ISA World Title 8 months after back surgery. Twice Pipe Pro runner-up.','','Men');
INSERT INTO athletes VALUES ('30','Lucas_Chianca','Lucas Chianca','Brazil','Big Wave','Big Wave','2026','Top 5 Big Wave','Regular','Saquarema, Rio de Janeiro, Brazil','Brazil''s most dominant big wave charger. Record-holder for largest wave in Brazil. Consistently one of Nazaré''s best performers.','Partner of Justine Dupont. Brother of João Chianca. Elite surfing family from Saquarema.','','Men');
INSERT INTO athletes VALUES ('31','Lucas_Fink','Lucas Fink','Brazil','Free Surf','Other','2026','Free Surf / Skimboard','Regular','Rio de Janeiro, Brazil','Five-time Skimboard World Champion and first non-American to win the UST overall title. Multi-discipline ocean athlete.','Unique profile blending skimboarding and surfing. Pioneer for Brazilian skimboard/surf crossover.','','Men');
INSERT INTO athletes VALUES ('32','Lukas_Skinner','Lukas Skinner','UK','Challenger','WSL Challenger','2026','CS/Junior','Regular','Cornwall, England, UK','2023 WSL GromSearch World Champion — first British surfer to win the title. Historic 2nd at World Junior Championships.','UK''s brightest young competitive talent. Working through junior and CS pathway to CT.','','Men');
INSERT INTO athletes VALUES ('33','Nathan_Florence','Nathan Florence','USA','Big Wave','Big Wave','2026','Big Wave / Free Surf','Regular','North Shore, Oahu, Hawaii, USA','Pioneer of the ''Slab Tour'' — seeking the world''s heaviest technical waves. 2024 SURFER Big Wave Challenge winner. Brother of John John Florence.','Member of the Florence family. Prolific content creator documenting missions to obscure heavy waves.','','Men');
INSERT INTO athletes VALUES ('34','Natxo_Gonzalez','Natxo González','Spain','Big Wave','Big Wave','2026','Big Wave','Goofy','Basque Country, Spain','First surfer to receive a perfect 10-point score at Nazaré (2019). Paddled some of Nazaré''s biggest waves. Spain''s premier big wave surfer.','Suffered serious cerebral injury in 2024. Rehabilitation ongoing. Veteran Nazaré charger.','','Men');
INSERT INTO athletes VALUES ('35','Pedro_Scooby','Pedro Scooby','Brazil','Big Wave','Big Wave','2026','Big Wave','Regular','Rio de Janeiro, Brazil','Brazil''s most famous big wave surfer. Rode 80ft+ wave at Nazaré in 2018. Larger-than-life personality and celebrity in Brazil.','Massive social media following. TV personality and celebrity beyond surfing community.','','Men');
INSERT INTO athletes VALUES ('36','Rocco_Rinaldi','Rocco Rinaldi','Italy','Free Surf','Free Surf','2026','Free Surf','Regular','Italy','Italian Red Bull athlete and surfer.','Limited public profile available.','','Men');
INSERT INTO athletes VALUES ('37','Sanoa_Dempfle_Olin','Sanoa Dempfle-Olin','Canada','Challenger','Challenger Series','2026','CT Rookie','Goofy','Tofino, British Columbia, Canada','Canada''s first Olympic surfer (Paris 2024). Youngest female to win Tofino Rip Curl Pro at age 11. Pioneer for Canadian competitive surfing.','Cold-water upbringing in Tofino. Competed Paris 2024 Olympics.','','Women');
INSERT INTO athletes VALUES ('38','Sky_Brown','Sky Brown','UK','Free Surf','Free Surf','2026','Free Surf','Regular','Miyazaki, Japan / Huntington Beach, USA','Dual Olympic athlete — youngest British Olympic medalist ever (skateboarding bronze, Tokyo 2020). Also competes in surfing. Fearless and inspirational.','Born to Japanese mother and British father. Primarily known as skateboarder. Represents UK.','','Men');
INSERT INTO athletes VALUES ('39','Teresa_Bonvalot','Teresa Bonvalot','Portugal','CT','Challenger Series','2026','WSL CT','Goofy','Cascais, Portugal','First Portuguese woman to qualify for WSL Championship Tour (2019). Competed in 2020 and 2024 Olympics. Power surfing with heavy rail.','Pioneer for Portuguese women''s surfing. Trains at Supertubos, Peniche.','','Women');
INSERT INTO athletes VALUES ('40','Tya_Zebrowski','Tya Zebrowski','France','CT','WSL CT','2026','WSL CT 2026 Rookie','Goofy','Hossegor, France','Youngest surfer ever to qualify for WSL Championship Tour — qualified at age 14 for 2026. Generational French talent with Tahitian big wave experience.','Trained at Hossegor. Massive upside potential. Historic youngest CT qualifier.','','Women');

-- Sponsors
INSERT INTO sponsors VALUES ('1','1','Quiksilver','Apparel','','');
INSERT INTO sponsors VALUES ('2','1','Roxy','Apparel','','');
INSERT INTO sponsors VALUES ('3','1','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('4','2','Billabong','Apparel','','');
INSERT INTO sponsors VALUES ('5','2','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('6','3','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('7','3','Thirty Square','Apparel','','');
INSERT INTO sponsors VALUES ('8','4','O'Neill','Apparel','','');
INSERT INTO sponsors VALUES ('9','4','Oakley','Other','','');
INSERT INTO sponsors VALUES ('10','4','Yeti','Other','','');
INSERT INTO sponsors VALUES ('11','4','SkullCandy','Other','','');
INSERT INTO sponsors VALUES ('12','4','Nixon','Watch','','');
INSERT INTO sponsors VALUES ('13','4','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('14','5','Nike','Apparel','','');
INSERT INTO sponsors VALUES ('15','5','Target','Other','','');
INSERT INTO sponsors VALUES ('16','5','DaKine','Other','','');
INSERT INTO sponsors VALUES ('17','5','Hurley','Apparel','','');
INSERT INTO sponsors VALUES ('18','5','Lost Surfboards','Board','','');
INSERT INTO sponsors VALUES ('19','5','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('20','6','Roxy','Apparel','','');
INSERT INTO sponsors VALUES ('21','6','Chemistry Surfboards','Board','','');
INSERT INTO sponsors VALUES ('22','6','FCS','Other','','');
INSERT INTO sponsors VALUES ('23','6','Tonic','Other','','');
INSERT INTO sponsors VALUES ('24','6','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('25','7','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('26','7','Ethos','Apparel','','');
INSERT INTO sponsors VALUES ('27','8','Billabong','Apparel','','');
INSERT INTO sponsors VALUES ('28','8','SurfEars','Other','','');
INSERT INTO sponsors VALUES ('29','8','Cipres','Other','','');
INSERT INTO sponsors VALUES ('30','8','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('31','9','Nike','Apparel','','');
INSERT INTO sponsors VALUES ('32','9','Rip Curl','Apparel','','');
INSERT INTO sponsors VALUES ('33','9','Oakley','Other','','');
INSERT INTO sponsors VALUES ('34','9','FCS','Other','','');
INSERT INTO sponsors VALUES ('35','9','Mayhem','Board','','');
INSERT INTO sponsors VALUES ('36','9','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('37','10','Quiksilver','Apparel','','');
INSERT INTO sponsors VALUES ('38','10','Youtheory','Other','','');
INSERT INTO sponsors VALUES ('39','10','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('40','11','Patagonia','Apparel','','');
INSERT INTO sponsors VALUES ('41','11','Christenson','Board','','');
INSERT INTO sponsors VALUES ('42','11','KT Surfing','Other','','');
INSERT INTO sponsors VALUES ('43','11','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('44','12','Ford','Auto','','');
INSERT INTO sponsors VALUES ('45','12','Vivo','Other','','');
INSERT INTO sponsors VALUES ('46','12','Riachuelo','Apparel','','');
INSERT INTO sponsors VALUES ('47','12','Nike','Apparel','','');
INSERT INTO sponsors VALUES ('48','12','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('49','13','GoPro','Other','','');
INSERT INTO sponsors VALUES ('50','13','Infinity Surfboards','Board','','');
INSERT INTO sponsors VALUES ('51','13','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('52','14','Volcom','Apparel','','');
INSERT INTO sponsors VALUES ('53','14','SharpEye Surfboards','Board','','');
INSERT INTO sponsors VALUES ('54','14','Futures Fins','Other','','');
INSERT INTO sponsors VALUES ('55','14','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('56','15','Quiksilver','Apparel','','');
INSERT INTO sponsors VALUES ('57','15','Polen','Board','','');
INSERT INTO sponsors VALUES ('58','15','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('59','16','Volcom','Apparel','','');
INSERT INTO sponsors VALUES ('60','16','Hydro Flask','Other','','');
INSERT INTO sponsors VALUES ('61','16','Billabong','Apparel','','');
INSERT INTO sponsors VALUES ('62','16','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('63','17','Hurley','Apparel','','');
INSERT INTO sponsors VALUES ('64','17','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('65','18','Volcom','Apparel','','');
INSERT INTO sponsors VALUES ('66','18','Veia Supplies','Other','','');
INSERT INTO sponsors VALUES ('67','18','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('68','19','O'Neill','Apparel','','');
INSERT INTO sponsors VALUES ('69','19','Channel Islands','Board','','');
INSERT INTO sponsors VALUES ('70','19','Oakley','Other','','');
INSERT INTO sponsors VALUES ('71','19','Futures','Other','','');
INSERT INTO sponsors VALUES ('72','19','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('73','20','Draft Surf','Board','','');
INSERT INTO sponsors VALUES ('74','20','ACCIONA','Other','','');
INSERT INTO sponsors VALUES ('75','20','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('76','21','Adidas','Apparel','','');
INSERT INTO sponsors VALUES ('77','21','Breitling','Watch','','');
INSERT INTO sponsors VALUES ('78','21','Manera','Wetsuit','','');
INSERT INTO sponsors VALUES ('79','21','Roxy','Apparel','','');
INSERT INTO sponsors VALUES ('80','21','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('81','22','Nike','Apparel','','');
INSERT INTO sponsors VALUES ('82','22','Hurley','Apparel','','');
INSERT INTO sponsors VALUES ('83','22','Oakley','Other','','');
INSERT INTO sponsors VALUES ('84','22','GoPro','Other','','');
INSERT INTO sponsors VALUES ('85','22','TAG Heuer','Watch','','');
INSERT INTO sponsors VALUES ('86','22','Cariuma','Footwear','','');
INSERT INTO sponsors VALUES ('87','22','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('88','23','MATTA Surfboards','Board','','');
INSERT INTO sponsors VALUES ('89','23','O'Neill','Wetsuit','','');
INSERT INTO sponsors VALUES ('90','23','Vans','Footwear','','');
INSERT INTO sponsors VALUES ('91','23','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('92','24','Quiksilver','Apparel','','');
INSERT INTO sponsors VALUES ('93','24','Kinoshita Group','Other','','');
INSERT INTO sponsors VALUES ('94','24','Shiseido','Other','','');
INSERT INTO sponsors VALUES ('95','24','Oakley','Other','','');
INSERT INTO sponsors VALUES ('96','24','G-Shock','Watch','','');
INSERT INTO sponsors VALUES ('97','24','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('98','25','Quiksilver','Apparel','','');
INSERT INTO sponsors VALUES ('99','25','Dior','Other','','');
INSERT INTO sponsors VALUES ('100','25','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('101','26','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('102','27','Volcom','Apparel','','');
INSERT INTO sponsors VALUES ('103','27','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('104','28','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('105','29','Quiksilver','Apparel','','');
INSERT INTO sponsors VALUES ('106','29','Gucci','Other','','');
INSERT INTO sponsors VALUES ('107','29','K-Way','Apparel','','');
INSERT INTO sponsors VALUES ('108','29','Bell','Other','','');
INSERT INTO sponsors VALUES ('109','29','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('110','30','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('111','31','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('112','32','Rip Curl','Apparel','','');
INSERT INTO sponsors VALUES ('113','32','Skindog','Board','','');
INSERT INTO sponsors VALUES ('114','32','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('115','33','Florence Marine X','Apparel','','');
INSERT INTO sponsors VALUES ('116','33','FCS','Other','','');
INSERT INTO sponsors VALUES ('117','33','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('118','34','Oxbow','Apparel','','');
INSERT INTO sponsors VALUES ('119','34','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('120','35','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('121','36','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('122','37','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('123','38','Billabong','Apparel','','');
INSERT INTO sponsors VALUES ('124','38','Nike','Apparel','','');
INSERT INTO sponsors VALUES ('125','38','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('126','39','Rip Curl','Apparel','','');
INSERT INTO sponsors VALUES ('127','39','JS Industries','Board','','');
INSERT INTO sponsors VALUES ('128','39','Red Bull','Energy Drink','','');
INSERT INTO sponsors VALUES ('129','40','Red Bull','Energy Drink','','');

-- Injuries
INSERT INTO injuries VALUES ('1','6','Health/medical issues, withdrew mid-season','General','','','Recovered','','0','','2026-01-01');
INSERT INTO injuries VALUES ('2','10','Torn meniscus','Knee','','','Recovered','','0','','2026-01-01');
INSERT INTO injuries VALUES ('3','12','Torn ankle ligament','Ankle','','','Recovered','','0','','2026-01-01');
INSERT INTO injuries VALUES ('4','12','Bruised MCL','Knee','','','Recovered','','0','','2026-01-01');
INSERT INTO injuries VALUES ('5','14','Meniscus tear (right knee)','Knee','','','Recovered','','0','','2026-01-01');
INSERT INTO injuries VALUES ('6','18','Fractured skull + brain bleeding at Pipeline','Head','','','Recovered','','0','','2026-01-01');
INSERT INTO injuries VALUES ('7','22','Head injury at Pipeline','Head','','','Recovered','','0','','2026-01-01');
INSERT INTO injuries VALUES ('8','22','Ankle injury','Ankle','','','Recovered','','0','','2026-01-01');
INSERT INTO injuries VALUES ('9','25','Back/reef impact at Tahiti Pro','Back','','','Recovered','','0','','2026-01-01');
INSERT INTO injuries VALUES ('10','29','Fractured L1 vertebra, 2 surgical plates','Back','','','Recovered','','0','','2026-01-01');
INSERT INTO injuries VALUES ('11','32','Foot injury','Foot','','','Recovered','','0','','2026-01-01');
INSERT INTO injuries VALUES ('12','34','Cerebral injury','Head','','','Rehab','','0','','2026-01-01');
INSERT INTO injuries VALUES ('13','34','Shoulder injury','Shoulder','','','Recovered','','0','','2026-01-01');
INSERT INTO injuries VALUES ('14','38','Skateboard crash — skull fracture, wrist, heart bruise (2020)','Multiple','','','Recovered','','0','','2026-01-01');

-- Comp Results
INSERT INTO comp_results VALUES ('25','4','2026','Rip Curl Pro Bells Beach','WSL CT','2026-04-06','Bells Beach, Australia','Quarterfinal','5','4745.0',NULL,'QF exit',NULL);
INSERT INTO comp_results VALUES ('26','4','2026','Western Australia Pro Margaret River','WSL CT','2026-04-18','Margaret River, WA, Australia','Round 1 (in progress)','17','2000.0',NULL,'Event on standby — Round 1 Heat 8',NULL);
INSERT INTO comp_results VALUES ('28','10','2026','Rip Curl Pro Bells Beach','WSL CT','2026-04-06','Bells Beach, Australia','Semifinal','3','6085.0',NULL,'',NULL);
INSERT INTO comp_results VALUES ('29','10','2026','Western Australia Pro Margaret River','WSL CT','2026-04-17','Margaret River, WA, Australia','Round 3','9','3320.0',NULL,'',NULL);
INSERT INTO comp_results VALUES ('30','24','2026','Rip Curl Pro Bells Beach','WSL CT','2026-04-06','Bells Beach, Australia','Quarterfinal','5','4745.0',NULL,'',NULL);
INSERT INTO comp_results VALUES ('31','24','2026','Western Australia Pro Margaret River','WSL CT','2026-04-17','Margaret River, WA, Australia','Round 3','9','3320.0',NULL,'',NULL);
INSERT INTO comp_results VALUES ('32','29','2026','Rip Curl Pro Bells Beach','WSL CT','2026-04-06','Bells Beach, Australia','Quarterfinal','5','4745.0',NULL,'',NULL);
INSERT INTO comp_results VALUES ('33','29','2026','Western Australia Pro Margaret River','WSL CT','2026-04-17','Margaret River, WA, Australia','Round 3','9','3320.0',NULL,'',NULL);
INSERT INTO comp_results VALUES ('34','12','2026','Rip Curl Pro Bells Beach','WSL CT','2026-04-06','Bells Beach, Australia','Round 3','9','3320.0',NULL,'',NULL);
INSERT INTO comp_results VALUES ('35','12','2026','Western Australia Pro Margaret River','WSL CT','2026-04-17','Margaret River, WA, Australia','Round 3','9','3320.0',NULL,'',NULL);
INSERT INTO comp_results VALUES ('36','19','2026','Rip Curl Pro Bells Beach','WSL CT','2026-04-06','Bells Beach, Australia','Round 3','9','3320.0',NULL,'',NULL);
INSERT INTO comp_results VALUES ('37','19','2026','Western Australia Pro Margaret River','WSL CT','2026-04-17','Margaret River, WA, Australia','Round 2','17','1000.0',NULL,'',NULL);
INSERT INTO comp_results VALUES ('38','18','2026','Rip Curl Pro Bells Beach','WSL CT','2026-04-06','Bells Beach, Australia','Round 2','17','1000.0',NULL,'',NULL);
INSERT INTO comp_results VALUES ('39','18','2026','Western Australia Pro Margaret River','WSL CT','2026-04-17','Margaret River, WA, Australia','Round 3','9','3320.0',NULL,'',NULL);
INSERT INTO comp_results VALUES ('40','14','2026','Rip Curl Pro Bells Beach','WSL CT','2026-04-06','Bells Beach, Australia','Round 2','17','1000.0',NULL,'',NULL);
INSERT INTO comp_results VALUES ('41','14','2026','Western Australia Pro Margaret River','WSL CT','2026-04-17','Margaret River, WA, Australia','Round 3','9','3320.0',NULL,'',NULL);
INSERT INTO comp_results VALUES ('42','25','2026','Rip Curl Pro Bells Beach','WSL CT','2026-04-06','Bells Beach, Australia','Round 2','17','1000.0',NULL,'',NULL);
INSERT INTO comp_results VALUES ('43','25','2026','Western Australia Pro Margaret River','WSL CT','2026-04-17','Margaret River, WA, Australia','Round 2','17','1000.0',NULL,'',NULL);
INSERT INTO comp_results VALUES ('44','9','2026','Rip Curl Pro Bells Beach','WSL CT','2026-04-06','Bells Beach, Australia','Round 2','0','2000.0',NULL,NULL,NULL);
INSERT INTO comp_results VALUES ('45','9','2026','Western Australia Pro Margaret River','WSL CT','2026-04-17','Margaret River, WA, Australia','Round 2 (in progress)','0','2000.0',NULL,'In progress',NULL);
INSERT INTO comp_results VALUES ('46','5','2026','Rip Curl Pro Bells Beach','WSL CT','2026-04-06','Bells Beach, Australia','Round 2','0','2000.0',NULL,NULL,NULL);
INSERT INTO comp_results VALUES ('47','5','2026','Western Australia Pro Margaret River','WSL CT','2026-04-17','Margaret River, WA, Australia','Round 2 (in progress)','0','2000.0',NULL,'In progress',NULL);
INSERT INTO comp_results VALUES ('48','6','2026','Rip Curl Pro Bells Beach','WSL CT','2026-04-06','Bells Beach, Australia','Round 2','0','2000.0',NULL,NULL,NULL);
INSERT INTO comp_results VALUES ('49','6','2026','Western Australia Pro Margaret River','WSL CT','2026-04-17','Margaret River, WA, Australia','Round 2 (in progress)','0','2000.0',NULL,'In progress',NULL);
INSERT INTO comp_results VALUES ('50','40','2026','Rip Curl Pro Bells Beach','WSL CT','2026-04-06','Bells Beach, Australia','Round 1','0','1000.0',NULL,NULL,NULL);
INSERT INTO comp_results VALUES ('51','40','2026','Western Australia Pro Margaret River','WSL CT','2026-04-17','Margaret River, WA, Australia','Round 1 (in progress)','0','1000.0',NULL,'In progress',NULL);

-- Ranking History
INSERT INTO ranking_history VALUES ('9','10','2026','WSL CT','2026-04-17','4','9405.0','Live after CT Event 2 R2');
INSERT INTO ranking_history VALUES ('10','24','2026','WSL CT','2026-04-17','6','8065.0','Live after CT Event 2 R2');
INSERT INTO ranking_history VALUES ('11','29','2026','WSL CT','2026-04-17','7','8065.0','Live after CT Event 2 R2');
INSERT INTO ranking_history VALUES ('12','12','2026','WSL CT','2026-04-17','9','6640.0','Live after CT Event 2 R2');
INSERT INTO ranking_history VALUES ('13','19','2026','WSL CT','2026-04-17','16','4320.0','Live after CT Event 2 R2');
INSERT INTO ranking_history VALUES ('14','18','2026','WSL CT','2026-04-17','19','4320.0','Live after CT Event 2 R2');
INSERT INTO ranking_history VALUES ('15','14','2026','WSL CT','2026-04-17','21','4320.0','Live after CT Event 2 R2');
INSERT INTO ranking_history VALUES ('16','25','2026','WSL CT','2026-04-17','24','2000.0','Live after CT Event 2 R2');
INSERT INTO ranking_history VALUES ('17','4','2026','WSL CT','2026-04-17','5','6745.0','Live — after CT EVENT 02 R1 H8');
INSERT INTO ranking_history VALUES ('18','9','2026','WSL CT','2026-04-17','9','4000.0','Live after CT02 R1H8');
INSERT INTO ranking_history VALUES ('19','5','2026','WSL CT','2026-04-17','10','4000.0','Live after CT02 R1H8');
INSERT INTO ranking_history VALUES ('20','6','2026','WSL CT','2026-04-17','11','4000.0','Live after CT02 R1H8');
INSERT INTO ranking_history VALUES ('21','40','2026','WSL CT','2026-04-17','20','2000.0','Live after CT02 R1H8');

-- Reset sequences so new inserts don't conflict
SELECT setval('athletes_id_seq', (SELECT MAX(id) FROM athletes));
SELECT setval('sponsors_id_seq', (SELECT MAX(id) FROM sponsors));
SELECT setval('injuries_id_seq', (SELECT MAX(id) FROM injuries));
SELECT setval('comp_results_id_seq', (SELECT MAX(id) FROM comp_results));
SELECT setval('ranking_history_id_seq', (SELECT MAX(id) FROM ranking_history));
SELECT setval('physical_testing_id_seq', 1);
