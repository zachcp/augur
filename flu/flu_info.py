"""
all of this information can one day make it to the DB I would think
It lives in a seperate file simply to make flu.prepare.py less cluttered
"""

segments = ["pb2", "pb1", "pa", "ha", "np", "na", "mp", "ns"]

# regions is list of tuples (region, acronym)
# acronym = "" means ignore for frequency calcs
regions = [
    ('africa',            ""),
    ('europe',            "EU"),
    ('north_america',     "NA"),
    ('china',             "AS"),
    ('south_asia',        "AS"),
    ('japan_korea',       "AS"),
    ('south_pacific',     "OC"),
    ('oceania',           "OC"),
    ('south_america',     ""),
    ('southeast_asia',    "AS"),
    ('west_asia',         "AS")
]

outliers = {
    'h3n2':[
        "A/Chile/8266/2003", "A/Louisiana/4/2003", "A/Lousiana/4/2003", "A/Chile/8266/2003",
        "A/OSAKA/31/2005", "A/Ontario/RV1273/2005", "A/OSAKA/31/2005", "A/Kunming/1-Va10/2005",
        "A/India/D0512577/2005", "A/Sari/388/2006", "A/Ontario/1252/2007", "A/HongKong/HK1/2008",
        "A/HongKong/HK1MA21-1/2008", "A/HongKong/HK1MA21-2/2008", "A/HongKong/HK1MA21-3/2008",
        "A/HongKong/HK1MA21-4/2008", "A/HongKong/HK2/2008", "A/HongKong/HK2MA21-1/2008",
        "A/HongKong/HK2MA21-2/2008", "A/HongKong/HK2MA21-3/2008", "A/HongKong/HK4/2008",
        "A/HongKong/HK5/2008", "A/HongKong/HK5MA21-1/2008", "A/HongKong/HK5MA21-3/2008",
        "A/HongKong/HK6/2008", "A/HongKong/HK6MA21-2/2008", "A/HongKong/HK6MA21-3/2008",
        "A/HongKong/HK7/2008", "A/HongKong/HK8/2008", "A/HongKong/HK8MA21-1/2008",
        "A/HongKong/HK8MA21-2/2008", "A/HongKong/HK8MA21-3/2008", "A/HongKong/HK8MA21-4/2008",
        "A/HongKong/HK9/2008", "A/HongKong/HK9MA21-1/2008", "A/HongKong/HK9MA21-2/2008",
        "A/HongKong/HK9MA21-3/2008", "A/HongKong/HK10/2008", "A/HongKong/HK10MA21-1/2008",
        "A/HongKong/HK10MA21-2/2008", "A/HongKong/HK10MA21-3/2008", "A/HongKong/HK10MA21-4/2008",
        "A/HongKong/HK11/2008", "A/HongKong/HK11MA21-1/2008", "A/HongKong/HK11MA21-3/2008",
        "A/HongKong/HK11MA21-4/2008", "A/HongKong/HK12/2008", "A/HongKong/HK12MA21-2/2008",
        "A/HongKong/HKMA12/2008", "A/HongKong/HKMA12A/2008", "A/HongKong/HKMA12B/2008",
        "A/HongKong/HKMA12C/2008", "A/HongKong/HKMA12D/2008", "A/HongKong/HKMA12E/2008",
        "A/HongKong/HKMA20A/2008", "A/HongKong/HKMA20B/2008", "A/HongKong/HKMA20E/2008",
        "A/HongKong/HK6MA21-1/2008", "A/HongKong/HK1MA21-1/2008","A/HongKong/HK1MA21-4/2008",
        "A/HongKong/HK1MA21-2/2008", "A/HongKong/HK2MA21-1/2008", "A/HongKong/HK2MA21-2/2008",
        "A/HongKong/HK4/2008", "A/HongKong/HK5/2008", "A/HongKong/HK5MA21-3/2008", "A/HongKong/HK6/2008",
        "A/HongKong/HK6MA21-3/2008", "A/HongKong/HK7/2008", "A/HongKong/HK8MA21-1/2008",
        "A/HongKong/HK8MA21-2/2008", "A/HongKong/HK8MA21-4/2008", "A/HongKong/HK9/2008",
        "A/HongKong/HK9MA21-2/2008", "A/HongKong/HK9MA21-3/2008", "A/HongKong/HK10MA21-1/2008",
        "A/HongKong/HK10MA21-2/2008", "A/HongKong/HK10MA21-4/2008", "A/HongKong/HKMA12D/2008",
        "A/Kansas/13/2009", "A/Busan/15453/2009", "A/Busan/15453/2009", "A/Kansas/13/2009",
        "A/StPetersburg/5/2009", "A/Cambodia/NHRCC00001/2009","A/Cambodia/NHRCC00002/2009",
        "A/Cambodia/NHRCC00003/2009", "A/Cambodia/NHRCC00006/2009", "A/Cambodia/NHRCC00007/2009",
        "A/Cambodia/NHRCC00008/2009", "A/Cambodia/NHRCC00010/2009", "A/Cambodia/NHRCC00011/2009",
        "A/Pennsylvania/14/2010", "A/Pennsylvania/40/2010", "A/Pennsylvania/14/2010", "A/Nanjing/1/2010",
        "A/Guam/AF2771/2011", "A/Indiana/8/2011", "A/Kenya/155/2011", "A/Kenya/168/2011",
        "A/Kenya/170/2011", "A/Nepal/142/2011", "A/Pennsylvania/09/2011", "A/Pennsylvania/9/2011",
        "A/Quebec/167936/2011", "A/Quebec/170658/2011", "A/Kenya/168/2011", "A/Nepal/142/2011",
        "A/Guam/AF2771/2011", "A/Indiana/8/2011", "A/India/6352/2012", "A/Indiana/8/2012",
        "A/Indiana/13/2012", "A/Ohio/34/2012", "A/Ohio/34/2012", "A/Helsinki/942/2013", "A/Indiana/11/2013",
        "A/Indiana/21/2013", "A/Jiangsu-Tianning/1707/2013", "A/Indiana/21/2013", "A/Indiana/5/2013",
        "A/Indiana/6/2013", "A/Indiana/17/2013", "A/Indiana/06/2013", "A/Jiangsu-Tianning/1707/2013",
        "A/HuNan/01/2014", "A/Jiangsu-Chongchuan/1830/2014", "A/Jiangsu-Chongchuan/12179/2014",
        "A/Ohio/2/2014", "A/Ohio/4319/2014", "A/SaoPaulo/3-34891/2014", "A/Wisconsin/24/2014",
        "A/HuNan/1/2014", "A/Iran/227/2014", "A/Iran/234/2014", "A/Iran/140/2014", "A/Iran/407/2014",
        "A/NewJersey/53/2015", "A/SaoPaulo/36178/2015", "A/SaoPaulo/61282/2015", "A/SaoPaulo/65194/2015",
        "A/Michigan/39/2015", "A/Sydney/53/2015", "A/Michigan/82/2016", "A/Michigan/83/2016",
        "A/Michigan/84/2016", "A/Michigan/87/2016", "A/Michigan/89/2016", "A/Michigan/90/2016",
        "A/Michigan/91/2016", "A/Michigan/93/2016", "A/Michigan/94/2016", "A/Michigan/95/2016",
        "A/Michigan/96/2016", "A/Ohio/27/2016", "A/Ohio/28/2016", "A/Ohio/32/2016", "A/Ohio/33/2016",
        "A/Ohio/35/2016", "A/Zhejiang-Wuxin/1300/2016", "A/Catalonia/NSVH100560486/2017",
        "A/Catalonia/NSVH100533399/2017"
    ],
    'h1n1pdm': ["A/Kenya/264/2012", "A/Iowa/39/2015", "A/Asturias/RR6898/2010", "A/Wisconsin/28/2011",
                "A/Brest/1161/2014", "A/Tomsk/273-MA1/2010", "A/Minnesota/46/2015", "A/Poland/16/2013",
                "A/Hungary/02/2013", "A/Hungary/16/2013", "A/California/07/2009NYMC-X18113/198",
                "A/Christchurch/16/2010NIB-74xp13/202", "A/Bari/166/2016", "A/Bari/167/2016", "A/Dakar/3/2014",
                "A/Arkansas/15/2013", "A/Wisconsin/87/2005", 'A/Norway/1929/2014', 'A/Ohio/9/2015',
                "A/Belgium/G0027/2016", "A/Shandong/1/2009"],
    'vic':["B/Bangkok/SI17/2012", "B/Bangkok/SI58/2012", "B/Kol/2024/2008", "B/Kolkata/2024/2008"],
    "yam":[]
}

reference_maps = {
    "h3n2": {
        "ha": {
            "path": "metadata/h3n2_ha_outgroup.gb",
            "metadata": {
                'strain': "A/Beijing/32/1992",
                'isolate_id': "CY113677",
                'date': "1992-XX-XX",
                'region': "china",
                'country': "China",
                "city": "Beijing",
                "passage": "unknown",
                'lab': "unknown",
                'age': "unknown",
                'gender': "unknown"
            },
            "include": 0,
            "genes": ["HA1", "HA2"]
        }
    },
    "yam": {
        "ha": {
            "path": "metadata/yam_ha_outgroup.gb",
            "metadata": {
                'strain': "B/Singapore/11/1994",
                'isolate_id': "CY019707",
                'date': "1994-05-10",
                'region': "southeast_asia",
                'country': "Singapore",
                "city": "Singapore",
                "passage": "unknown",
                'lab': "unknown",
                'age': "unknown",
                'gender': "M"
            },
            "include": 0,
            "genes": ["HA"]
        },
        "na": {
            "path": "metadata/yam_na_outgroup.gb",
            "include": 0,
            "genes": ["NA", "NB"]
        }
    },
    "vic": {
        "ha": {
            "path": "metadata/vic_ha_outgroup.gb",
            "metadata": {
                'strain': "B/Hong Kong/02/1993",
                'isolate_id': "CY018813",
                'date': "1993-02-15",
                'region': "china",
                'country': "Hong Kong",
                "city": "Hong Kong",
                "passage": "4",
                'lab': "unknown",
                'age': "unknown",
                'gender': "unknown"
            },
            "include": 0,
            "genes": ["HA"]
        }
    },
    "h1n1pdm": {
        "ha": {
            "path": "metadata/h1n1pdm_ha_outgroup.gb",
            "metadata": {
                'strain': "A/Swine/Indiana/P12439/00",
                'isolate_id': "AF455680",
                'date': "unknown",
                'region': "north america",
                'country': "USA",
                "city": "unknown",
                "passage": "unknown",
                'lab': "unknown",
                'age': "unknown",
                'gender': "unknown"
            },
            "include": 0,
            "genes": ["HA"]
        }
    }
}

## lots of the references share data
reference_maps["yam"]["na"]["metadata"] = reference_maps["yam"]["ha"]["metadata"]

reference_viruses = {
    'h3n2': ['A/Wisconsin/67/2005', 'A/Brisbane/10/2007',  'A/Perth/16/2009', 'A/Victoria/361/2011','A/Texas/50/2012', 'A/Switzerland/9715293/2013', 'A/HongKong/4801/2014', 'A/Alaska/232/2015'],
    'h1n1pdm':[],
    'vic':[],
    'yam':[]
}

clade_designations = {
    "h3n2":{
        "3c3.a":[('HA1',128,'A'), ('HA1',142,'G'), ('HA1',159,'S')],
        "3c3":   [('HA1',128,'A'), ('HA1',142,'G'), ('HA1',159,'F')],
        "3c2.a": [('HA1',144,'S'), ('HA1',159,'Y'), ('HA1',225,'D'), ('HA1',311,'H'), ('HA1',160,'T')],
        "171K": [('HA1',144,'S'), ('HA1',159,'Y'), ('HA1',171,'K'), ('HA1',225,'D'), ('HA1',311,'H'), ('HA2',77,'V'), ('HA2',155,'E'), ('HA2',160,'N')],
        "3c2":   [('HA1',144,'N'), ('HA1',159,'F'), ('HA1',225,'N'), ('HA1',160,'T'), ('HA1',142,'R')],
        "3c3.b": [('HA1',83,'R'), ('HA1',261,'Q'), ('HA1',62,'K'),  ('HA1',122,'D')]
    },
    "h1n1pdm":{
        '2': [('HA1', 125, 'N'), ('HA1', 134 ,'A'), ('HA1', 183, 'S'), ('HA1', 31,'D'), ('HA1', 172,'N'), ('HA1', 186,'T')],
        '3': [('HA1', 134 ,'T'), ('HA1', 183, 'P')],
        '4': [('HA1', 125, 'D'), ('HA1', 134 ,'A'), ('HA1', 183, 'S')],
        '5': [('HA1', 87, 'N'), ('HA1', 205, 'K'), ('HA1', 216, 'V'), ('HA1', 149, 'L')],
        '6': [('HA1', 185,'T'),  ('HA1', 97, 'N'), ('HA1', 197, 'A')],
        '6c':[('HA1', 234,'I'),  ('HA1', 97, 'N'), ('HA1', 197, 'A'), ('HA1', 283,'E')],
        '6b':[('HA1', 163,'Q'),  ('HA1', 256, 'T'), ('HA1', 197, 'A'), ('HA1', 283,'E')],
        '7': [('HA1', 143,'G'),  ('HA1', 97, 'D'), ('HA1', 197, 'T')],
        '8': [('HA1', 186,'T'),  ('HA1', 272,'A')],
        '6b.1':[('HA1', 163,'Q'),  ('HA1', 256, 'T'), ('HA1', 197, 'A'), ('HA1', 283, 'E'), ('SigPep', 13, 'T'), ('HA1', 84, 'N'), ('HA1', 162, 'N')],
        '6b.2':[('HA1', 163,'Q'),  ('HA1', 256, 'T'), ('HA1', 197, 'A'), ('HA1', 283, 'E'), ('HA2', 164, 'G'), ('HA1', 152, 'T'), ('HA2', 174, 'E')]
    },
    "yam":{
        '2':  [('HA1', 48,'K'), ('HA1', 108, 'A'), ('HA1', 150, 'S')],
        '3':  [('HA1', 48,'R'), ('HA1', 108, 'P'), ('HA1', 150, 'I')],
        '3a': [('HA1', 37,'A'), ('HA1', 298, 'E'), ('HA1', 48,'R'), ('HA1', 105, 'P'), ('HA1', 150, 'I')],
        '172Q': [('HA1', 48,'R'), ('HA1', 108, 'P'), ('HA1', 150, 'I'), ('HA1', 116, 'K'), ('HA1', 172, 'Q')]
    },
    "vic":{
        '1A': [('HA1', 75,'K'), ('HA1', 58, 'L'), ('HA1', 165, 'K')],
        '1B': [('HA1', 75,'K'), ('HA1', 58, 'P'), ('HA1', 165, 'K')],
        '117V': [('HA1', 75,'K'), ('HA1', 58, 'L'), ('HA1', 165, 'K'), ('HA1', 129, 'D'), ('HA1', 117, 'V')]
    }
}
