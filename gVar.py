import wx, datetime, time



lastPanel     = wx.Panel
previousPanel = wx.Panel
panelHistory =[]

darkGrey    = wx.Colour(50, 50, 50)
darkerGrey = wx.Colour(0,0,0)
mediumGrey  = wx.Colour(128, 128, 128)
barkleys    = wx.Colour(55, 200, 157)
white       = wx.Colour(255, 255, 255)

veto   = False
Online = False
editedFlag  = False
userIsAdmin = False

CKID = 0

vListCurrentID = 0
KKelas = 0
table= ''
column = ''
NoInduk   = ''
msg       = ''
groupList = ''
groupName = ''
lvID      = ''
lvName    = ''
guid      = ''
school    = '' 
current_view = ''
address = ''

gDate     = '17-10-2012'
schYr     = 0
regYr     = schYr + 1

monthNo   = 1
dayNo     = 1
semester  = 1
widget_id = 0
addr_id    = 0
user_id    = 0
student_id = 0

guardian_type = ''
school_id     = 0
form_id       = 0
level         = 0
course_id     = 0
studygroup_id = 0

parent_id   = 0
father_id   = 0
mother_id   = 0
guardian_id = 0

sash_pos    = 0
inserted_id = 0
 
dayNames   ={1:'Monday',
             2:'Tuesday',
             3:'Wednesday',
             4:'Thursday',
             5:'Friday'}

monthNames ={1:'July',     2:'August',   3:'September', 4:'October',
             5:'November', 6:'December', 7:'January',   8:'February',
             9:'March',   10:'April',   11:'May',      12:'June'}

namaBulan ={1:'Januari',     2:'Feburary',   3:'Maret', 4:'April',
             5:'Mai', 6:'Juni', 7:'Juli',   8:'Agustus',
             9:'September',   10:'Okctober',   11:'Nopember',      12:'Desember'}

numborBulan ={1:'Januari',     2:'Februari',   3:'Maret', 4:'April',
             5:'Mei', 6:'Juni', 7:'Juli',   8:'Agustus',
             9:'September',   10:'Oktober',   11:'Nopember',      12:'Desember'}

listCtrl = None

batchDivisionsList = teacherIDs         = []

privilageData      = {
    1: ('Admin', 'Can add/del/edit users & privilages', '1'),
    13: ("Sinead O'Connor", 'Nothing Compares 2 U', 'Rock')}

panelSize     = (900, 560)
current_panel = ''
branch = ''


font_family = {"FONTFAMILY_DECORATIVE":wx.FONTFAMILY_DECORATIVE, # A decorative font
                    "FONTFAMILY_DEFAULT":wx.FONTFAMILY_DEFAULT,
                    "FONTFAMILY_MODERN":wx.FONTFAMILY_MODERN,     # Usually a fixed pitch font
                    "FONTFAMILY_ROMAN":wx.FONTFAMILY_ROMAN,      # A formal, serif font
                    "FONTFAMILY_SCRIPT":wx.FONTFAMILY_SCRIPT,     # A handwriting font
                    "FONTFAMILY_SWISS":wx.FONTFAMILY_SWISS,      # A sans-serif font
                    "FONTFAMILY_TELETYPE":wx.FONTFAMILY_TELETYPE    # A teletype font
                    }
font_weight = {"FONTWEIGHT_BOLD":wx.FONTWEIGHT_BOLD,
                   "FONTWEIGHT_LIGHT":wx.FONTWEIGHT_LIGHT,
                   "FONTWEIGHT_NORMAL":wx.FONTWEIGHT_NORMAL
                   }
 
font_style = {"FONTSTYLE_ITALIC":wx.FONTSTYLE_ITALIC,
                  "FONTSTYLE_NORMAL":wx.FONTSTYLE_NORMAL,
                  "FONTSTYLE_SLANT":wx.FONTSTYLE_SLANT
                  }
font_size = [8, 10, 12, 14]

postcodeData = "\
    1	:	20851	Besilam Bukit Lembasa	Wampu	Kab.	Langkat	Sumatera Utara	,\
    2	:	20851	Bingai	Wampu	Kab.	Langkat	Sumatera Utara	,\
    3	:	20851	Bukit Melintang	Wampu	Kab.	Langkat	Sumatera Utara	,\
    4	:	20851	Gergas	Wampu	Kab.	Langkat	Sumatera Utara	,\
    5	:	20851	Gohor Lama	Wampu	Kab.	Langkat	Sumatera Utara	,\
    6	:	20851	Jentera Stabat	Wampu	Kab.	Langkat	Sumatera Utara	,\
    7	:	20851	Kebun Balok	Wampu	Kab.	Langkat	Sumatera Utara	,\
    8	:	20851	Mekar Jaya	Wampu	Kab.	Langkat	Sumatera Utara	,\
    9	:	20851	Paya Tusam	Wampu	Kab.	Langkat	Sumatera Utara	,\
    10	:	20851	Pertumbukan	Wampu	Kab.	Langkat	Sumatera Utara	,\
    11	:	20851	Stabat Lama	Wampu	Kab.	Langkat	Sumatera Utara	,\
    12	:	20851	Stabat Lama Barat	Wampu	Kab.	Langkat	Sumatera Utara	,\
    13	:	20851	Stungkit	Wampu	Kab.	Langkat	Sumatera Utara	,\
    14	:	20851	Sumber Mulyo	Wampu	Kab.	Langkat	Sumatera Utara	, \
    15	:	22873	Ambukha	Umbunasi	Kab.	Nias Selatan	Sumatera Utara	,\
    16	:	22873	Balohili Mola	Umbunasi	Kab.	Nias Selatan	Sumatera Utara	,\
    17	:	22873	Foikhugaga	Umbunasi	Kab.	Nias Selatan	Sumatera Utara	,\
    18	:	22873	Hilibadalu	Umbunasi	Kab.	Nias Selatan	Sumatera Utara	,\
    19	:	22873	Hiliuso	Umbunasi	Kab.	Nias Selatan	Sumatera Utara	,\
    20	:	22873	Lawindra	Umbunasi	Kab.	Nias Selatan	Sumatera Utara	,\
    21	:	22873	Lolozukhu	Umbunasi	Kab.	Nias Selatan	Sumatera Utara	,\
    22	:	22873	Orahili Mola	Umbunasi	Kab.	Nias Selatan	Sumatera Utara	,\
    23	:	22873	Orlin	Umbunasi	Kab.	Nias Selatan	Sumatera Utara	,\
    24	:	22873	Sifaoroasi Mola	Umbunasi	Kab.	Nias Selatan	Sumatera Utara	,\
    25	:	22873	Silima Banua Umbunasi	Umbunasi	Kab.	Nias Selatan	Sumatera Utara	,\
    26	:	22873	Sindrolo	Umbunasi	Kab.	Nias Selatan	Sumatera Utara	,\
    27	:	22873	Tobualo	Umbunasi	Kab.	Nias Selatan	Sumatera Utara	,\
    28	:	22873	Umbunasi	Umbunasi	Kab.	Nias Selatan	Sumatera Utara	,\
    29	:	22866	Amandraya Ulususua	Ulususua	Kab.	Nias Selatan	Sumatera Utara	,\
    30	:	22866	Foikhu Fondrako	Ulususua	Kab.	Nias Selatan	Sumatera Utara	,\
    31	:	22866	Fondrakoraya	Ulususua	Kab.	Nias Selatan	Sumatera Utara	,\
    32	:	22866	Hilinifaoso	Ulususua	Kab.	Nias Selatan	Sumatera Utara	,\
    33	:	22866	Hiliwosi	Ulususua	Kab.	Nias Selatan	Sumatera Utara	,\
    34	:	22866	Lahusa Susua	Ulususua	Kab.	Nias Selatan	Sumatera Utara	,\
    35	:	22866	Orahili Fondrako	Ulususua	Kab.	Nias Selatan	Sumatera Utara	,\
    36	:	22866	Orudu Sibohou	Ulususua	Kab.	Nias Selatan	Sumatera Utara	,\
    37	:	22866	Ramba-Ramba	Ulususua	Kab.	Nias Selatan	Sumatera Utara	,\
    38	:	22866	Sifaoroasi	Ulususua	Kab.	Nias Selatan	Sumatera Utara	,\
    39	:	22866	Sisarahili Susua	Ulususua	Kab.	Nias Selatan	Sumatera Utara	,\
    40	:	22866	Susua	Ulususua	Kab.	Nias Selatan	Sumatera Utara	,\
    41	:	22867	Ambukha Satu	Ulunoyo	Kab.	Nias Selatan	Sumatera Utara	,\
    42	:	22867	Amorosa	Ulunoyo	Kab.	Nias Selatan	Sumatera Utara	,\
    43	:	22867	Bawo Lolomatua	Ulunoyo	Kab.	Nias Selatan	Sumatera Utara	,\
    44	:	22867	Borowosi	Ulunoyo	Kab.	Nias Selatan	Sumatera Utara	,\
    45	:	22867	Hilifakhe	Ulunoyo	Kab.	Nias Selatan	Sumatera Utara	,\
    46	:	22867	Hilimaera	Ulunoyo	Kab.	Nias Selatan	Sumatera Utara	,\
    47	:	22867	Hiliwaebu	Ulunoyo	Kab.	Nias Selatan	Sumatera Utara	,\
    48	:	22867	Loloana`a	Ulunoyo	Kab.	Nias Selatan	Sumatera Utara	,\
    49	:	22867	Marao	Ulunoyo	Kab.	Nias Selatan	Sumatera Utara	,\
    50	:	22867	Orahili Ulunoyo	Ulunoyo	Kab.	Nias Selatan	Sumatera Utara	,\
    51	:	22867	Puncak Lolomatua	Ulunoyo	Kab.	Nias Selatan	Sumatera Utara	,\
    52	:	22867	Sambulu	Ulunoyo	Kab.	Nias Selatan	Sumatera Utara	,\
    53	:	22867	Suka Maju	Ulunoyo	Kab.	Nias Selatan	Sumatera Utara	,\
    54	:	22861	Fahandrona	Ulugawo	Kab.	Nias	Sumatera Utara	,\
    55	:	22861	Fatodano	Ulugawo	Kab.	Nias	Sumatera Utara	,\
    56	:	22861	Hilibadalu	Ulugawo	Kab.	Nias	Sumatera Utara	,\
    57	:	22861	Hiligafoa	Ulugawo	Kab.	Nias	Sumatera Utara	,\
    58	:	22861	Hilimbowo	Ulugawo	Kab.	Nias	Sumatera Utara	,\
    59	:	22861	Hiliweto Gela (Somolomolo)	Ulugawo	Kab.	Nias	Sumatera Utara	,\
    60	:	22861	Holi	Ulugawo	Kab.	Nias	Sumatera Utara	,\
    61	:	22861	Lawa-Lawaluo	Ulugawo	Kab.	Nias	Sumatera Utara	,\
    62	:	22861	Mohili	Ulugawo	Kab.	Nias	Sumatera Utara	,\
    63	:	22861	Onodalinga	Ulugawo	Kab.	Nias	Sumatera Utara	,\
    64	:	22861	Orahili Somolomolo	Ulugawo	Kab.	Nias	Sumatera Utara	,\
    65	:	22861	Sifaoroasi Ulugawo	Ulugawo	Kab.	Nias	Sumatera Utara	,\
    66	:	22861	Sisarahili Soroma`asi	Ulugawo	Kab.	Nias	Sumatera Utara	,\
    67	:	22861	Sisobahili Ulugawo	Ulugawo	Kab.	Nias	Sumatera Utara	,\
    68	:	22385	Dolok Nagodang	Uluan	Kab.	Toba Samosir	Sumatera Utara	,\
    69	:	22385	Dolok Saribu Janji Matogu	Uluan	Kab.	Toba Samosir	Sumatera Utara	,\
    70	:	22385	Dolok Saribu Lumban Nabolon	Uluan	Kab.	Toba Samosir	Sumatera Utara	,\
    71	:	22385	Lumban Binanga	Uluan	Kab.	Toba Samosir	Sumatera Utara	,\
    72	:	22385	Lumban Holbung	Uluan	Kab.	Toba Samosir	Sumatera Utara	,\
    73	:	22385	Lumban Nabolon	Uluan	Kab.	Toba Samosir	Sumatera Utara	,\
    74	:	22385	Marom	Uluan	Kab.	Toba Samosir	Sumatera Utara	,\
    75	:	22385	Parbagasan Janji Matogu	Uluan	Kab.	Toba Samosir	Sumatera Utara	,\
    76	:	22385	Parhabinsaran Janji Matogu	Uluan	Kab.	Toba Samosir	Sumatera Utara	,\
    77	:	22385	Parik	Uluan	Kab.	Toba Samosir	Sumatera Utara	,\
    78	:	22385	Partor Janji Matogu	Uluan	Kab.	Toba Samosir	Sumatera Utara	,\
    79	:	22385	Partoruan Janji Matogu	Uluan	Kab.	Toba Samosir	Sumatera Utara	,\
    80	:	22385	Sampuara	Uluan	Kab.	Toba Samosir	Sumatera Utara	,\
    81	:	22385	Sibuntuon	Uluan	Kab.	Toba Samosir	Sumatera Utara	,\
    82	:	22385	Sigaol Barat	Uluan	Kab.	Toba Samosir	Sumatera Utara	,\
    83	:	22385	Sigaol Timur	Uluan	Kab.	Toba Samosir	Sumatera Utara	,\
    84	:	22385	Siregar Aek Nalas	Uluan	Kab.	Toba Samosir	Sumatera Utara	,\
    85	:	22998	Alahan Kae	Ulu Pungkut	Kab.	Mandailing Natal	Sumatera Utara	,\
    86	:	22998	Habincaran	Ulu Pungkut	Kab.	Mandailing Natal	Sumatera Utara	,\
    87	:	22998	Huta Godang	Ulu Pungkut	Kab.	Mandailing Natal	Sumatera Utara	,\
    88	:	22998	Huta Padang Up	Ulu Pungkut	Kab.	Mandailing Natal	Sumatera Utara	,\
    89	:	22998	Huta Rimbaru Up (Hutaimbaru)	Ulu Pungkut	Kab.	Mandailing Natal	Sumatera Utara	,\
    90	:	22998	Muara Saladi	Ulu Pungkut	Kab.	Mandailing Natal	Sumatera Utara	,\
    91	:	22998	Patahajang	Ulu Pungkut	Kab.	Mandailing Natal	Sumatera Utara	,\
    92	:	22998	Simpang Banyak Jae	Ulu Pungkut	Kab.	Mandailing Natal	Sumatera Utara	,\
    93	:	22998	Simpang Banyak Julu	Ulu Pungkut	Kab.	Mandailing Natal	Sumatera Utara	,\
    94	:	22998	Simpang Duhu Lombang	Ulu Pungkut	Kab.	Mandailing Natal	Sumatera Utara	,\
    95	:	22998	Simpang Duku Dolok	Ulu Pungkut	Kab.	Mandailing Natal	Sumatera Utara	,\
    96	:	22998	Simpang Pining	Ulu Pungkut	Kab.	Mandailing Natal	Sumatera Utara	,\
    97	:	22998	Tolang	Ulu Pungkut	Kab.	Mandailing Natal	Sumatera Utara	,\
    98	:	22862	Bukit Tinggi	Ulu Moro`o (Ulu Narwo)	Kab.	Nias Barat	Sumatera Utara	,\
    99	:	22862	Hilibadalu	Ulu Moro`o (Ulu Narwo)	Kab.	Nias Barat	Sumatera Utara	,\
    100	:	22862	Hilisangawola	Ulu Moro`o (Ulu Narwo)	Kab.	Nias Barat	Sumatera Utara	,\
    101	:	22862	Lawelu	Ulu Moro`o (Ulu Narwo)	Kab.	Nias Barat	Sumatera Utara	,\
    102	:	22862	Saloo	Ulu Moro`o (Ulu Narwo)	Kab.	Nias Barat	Sumatera Utara	,\
    103	:	22763	Aekharuaya	Ulu Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    104	:	22763	Handang Kopo	Ulu Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    105	:	22763	Matondang	Ulu Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    106	:	22763	Paran Batu (Pagaran)	Ulu Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    107	:	22763	Paringgonan	Ulu Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    108	:	22763	Paringgonan Julu	Ulu Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    109	:	22763	Pasar Ipuh	Ulu Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    110	:	22763	Pintu Padang	Ulu Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    111	:	22763	Sibual Buali	Ulu Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    112	:	22763	Sibulus Salam	Ulu Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    113	:	22763	Simanuldang Jae	Ulu Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    114	:	22763	Simanuldang Julu	Ulu Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    115	:	22763	Siraisan	Ulu Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    116	:	22763	Tanjung	Ulu Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    117	:	22763	Tapian Nauli	Ulu Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    118	:	21187	Aek Ger Ger Sidodadi	Ujung Padang	Kab.	Simalungun	Sumatera Utara	,\
    119	:	21187	Bangun Sordang	Ujung Padang	Kab.	Simalungun	Sumatera Utara	,\
    120	:	21187	Dusun Ulu	Ujung Padang	Kab.	Simalungun	Sumatera Utara	,\
    121	:	21187	Huta Parik	Ujung Padang	Kab.	Simalungun	Sumatera Utara	,\
    122	:	21187	Kampung Lalang	Ujung Padang	Kab.	Simalungun	Sumatera Utara	,\
    123	:	21187	Pagar Bosi	Ujung Padang	Kab.	Simalungun	Sumatera Utara	,\
    124	:	21187	Pulo Pitu Marihat	Ujung Padang	Kab.	Simalungun	Sumatera Utara	,\
    125	:	21187	Riah Poso	Ujung Padang	Kab.	Simalungun	Sumatera Utara	,\
    126	:	21187	Sayur Matinggi	Ujung Padang	Kab.	Simalungun	Sumatera Utara	,\
    127	:	21187	Sei Merbou	Ujung Padang	Kab.	Simalungun	Sumatera Utara	,\
    128	:	21187	Siringan Ringan	Ujung Padang	Kab.	Simalungun	Sumatera Utara	,\
    129	:	21187	Sordang Bolon	Ujung Padang	Kab.	Simalungun	Sumatera Utara	,\
    130	:	21187	Tanjung Rapuan	Ujung Padang	Kab.	Simalungun	Sumatera Utara	,\
    131	:	21187	Taratak Nagodang	Ujung Padang	Kab.	Simalungun	Sumatera Utara	,\
    132	:	21187	Teluk Tapian	Ujung Padang	Kab.	Simalungun	Sumatera Utara	,\
    133	:	21187	Tinjoan (Tinjowan)	Ujung Padang	Kab.	Simalungun	Sumatera Utara	,\
    134	:	21187	Ujung Padang	Ujung Padang	Kab.	Simalungun	Sumatera Utara	,\
    135	:	22617	Aek Bontar	Tukka	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    136	:	22617	Bona Lumban	Tukka	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    137	:	22617	Huta Nabolon	Tukka	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    138	:	22618	Sait Nihuta Kalangan II	Tukka	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    139	:	22617	Sigiring Giring	Tukka	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    140	:	22617	Sipange	Tukka	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    141	:	22617	Tapian Nauli Saur Manggita	Tukka	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    142	:	22617	Tukka	Tukka	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    143	:	22852	Alooa	Tuhemberua	Kab.	Nias Utara	Sumatera Utara	,\
    144	:	22852	Banuagea	Tuhemberua	Kab.	Nias Utara	Sumatera Utara	,\
    145	:	22852	Botolakha	Tuhemberua	Kab.	Nias Utara	Sumatera Utara	,\
    146	:	22852	Fino	Tuhemberua	Kab.	Nias Utara	Sumatera Utara	,\
    147	:	22852	Laaya	Tuhemberua	Kab.	Nias Utara	Sumatera Utara	,\
    148	:	22852	Ladara	Tuhemberua	Kab.	Nias Utara	Sumatera Utara	,\
    149	:	22852	Silima Banua	Tuhemberua	Kab.	Nias Utara	Sumatera Utara	,\
    150	:	22852	Siofa Banua	Tuhemberua	Kab.	Nias Utara	Sumatera Utara	,\
    151	:	22861	Botona`ai	Tugala Oyo	Kab.	Nias Utara	Sumatera Utara	,\
    152	:	22861	Fabaliwa Oyo	Tugala Oyo	Kab.	Nias Utara	Sumatera Utara	,\
    153	:	22861	Gunung Tua	Tugala Oyo	Kab.	Nias Utara	Sumatera Utara	,\
    154	:	22861	Harefa	Tugala Oyo	Kab.	Nias Utara	Sumatera Utara	,\
    155	:	22861	Humene Siheneasi	Tugala Oyo	Kab.	Nias Utara	Sumatera Utara	,\
    156	:	22861	Ononazara	Tugala Oyo	Kab.	Nias Utara	Sumatera Utara	,\
    157	:	22861	Siwawo	Tugala Oyo	Kab.	Nias Utara	Sumatera Utara	,\
    158	:	22861	Te`olo	Tugala Oyo	Kab.	Nias Utara	Sumatera Utara	,\
    159	:	21464	Aek Batu	Torgamba	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    160	:	21464	Aek Raso	Torgamba	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    161	:	21464	Asam Jawa	Torgamba	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    162	:	21464	Bangai	Torgamba	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    163	:	21464	Beringin Jaya	Torgamba	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    164	:	21464	Bukit Tujuh	Torgamba	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    165	:	21464	Bunut	Torgamba	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    166	:	21464	Pangarungan	Torgamba	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    167	:	21464	Pinang Dame	Torgamba	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    168	:	21464	Rasau	Torgamba	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    169	:	21464	Sungai Meranti	Torgamba	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    170	:	21464	Teluk Rampah	Torgamba	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    171	:	21464	Torgamba	Torgamba	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    172	:	21464	Torganda	Torgamba	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    173	:	22865	Bawoganowo	Toma	Kab.	Nias Selatan	Sumatera Utara	,\
    174	:	22865	Hilialawa	Toma	Kab.	Nias Selatan	Sumatera Utara	,\
    175	:	22865	Hiliamaetaluo	Toma	Kab.	Nias Selatan	Sumatera Utara	,\
    176	:	22865	Hiliasi	Toma	Kab.	Nias Selatan	Sumatera Utara	,\
    177	:	22865	Hilimagari	Toma	Kab.	Nias Selatan	Sumatera Utara	,\
    178	:	22865	Hilinamoniha	Toma	Kab.	Nias Selatan	Sumatera Utara	,\
    179	:	22865	Hilindraso Raya	Toma	Kab.	Nias Selatan	Sumatera Utara	,\
    180	:	22865	Hilindrasoniha	Toma	Kab.	Nias Selatan	Sumatera Utara	,\
    181	:	22865	Hilisataro	Toma	Kab.	Nias Selatan	Sumatera Utara	,\
    182	:	22865	Hilisataro Eho Sofayo	Toma	Kab.	Nias Selatan	Sumatera Utara	,\
    183	:	22865	Hilisataro Gewa	Toma	Kab.	Nias Selatan	Sumatera Utara	,\
    184	:	22865	Hilisataro Nandisa	Toma	Kab.	Nias Selatan	Sumatera Utara	,\
    185	:	22865	Hilisataro Raya	Toma	Kab.	Nias Selatan	Sumatera Utara	,\
    186	:	22865	Hilisoromi	Toma	Kab.	Nias Selatan	Sumatera Utara	,\
    187	:	21261	Padang Sari	Tinggi Raja	Kab.	Asahan	Sumatera Utara	,\
    188	:	21261	Piasa Ulu	Tinggi Raja	Kab.	Asahan	Sumatera Utara	,\
    189	:	21261	Sidomulyo	Tinggi Raja	Kab.	Asahan	Sumatera Utara	,\
    190	:	21261	Sumber Harapan	Tinggi Raja	Kab.	Asahan	Sumatera Utara	,\
    191	:	21261	Teladan	Tinggi Raja	Kab.	Asahan	Sumatera Utara	,\
    192	:	21261	Terusan Tengah	Tinggi Raja	Kab.	Asahan	Sumatera Utara	,\
    193	:	21261	Tinggi Raja	Tinggi Raja	Kab.	Asahan	Sumatera Utara	,\
    194	:	22272	Buluh Tellang	Tinada	Kab.	Pakpak Bharat	Sumatera Utara	,\
    195	:	22272	Kuta Babo	Tinada	Kab.	Pakpak Bharat	Sumatera Utara	,\
    196	:	22272	Mahala	Tinada	Kab.	Pakpak Bharat	Sumatera Utara	,\
    197	:	22272	Prongil	Tinada	Kab.	Pakpak Bharat	Sumatera Utara	,\
    198	:	22272	Silima Kuta	Tinada	Kab.	Pakpak Bharat	Sumatera Utara	,\
    199	:	22272	Tinada	Tinada	Kab.	Pakpak Bharat	Sumatera Utara	,\
    200	:	22154	Gunung Merlawan	Tiganderket	Kab.	Karo	Sumatera Utara	,\
    201	:	22154	Jandi Meriah	Tiganderket	Kab.	Karo	Sumatera Utara	,\
    202	:	22154	Kuta Kepar	Tiganderket	Kab.	Karo	Sumatera Utara	,\
    203	:	22154	Kutagaluh	Tiganderket	Kab.	Karo	Sumatera Utara	,\
    204	:	22154	Kutambaru	Tiganderket	Kab.	Karo	Sumatera Utara	,\
    205	:	22154	Mardingding	Tiganderket	Kab.	Karo	Sumatera Utara	,\
    206	:	22154	Nari Gunung Dua	Tiganderket	Kab.	Karo	Sumatera Utara	,\
    207	:	22154	Nari Gunung Satu	Tiganderket	Kab.	Karo	Sumatera Utara	,\
    208	:	22154	Penampen	Tiganderket	Kab.	Karo	Sumatera Utara	,\
    209	:	22154	Perbaji	Tiganderket	Kab.	Karo	Sumatera Utara	,\
    210	:	22154	Suka Tendel	Tiganderket	Kab.	Karo	Sumatera Utara	,\
    211	:	22154	Susuk	Tiganderket	Kab.	Karo	Sumatera Utara	,\
    212	:	22154	Tanjung Mbelang	Tiganderket	Kab.	Karo	Sumatera Utara	,\
    213	:	22154	Tanjung Merawa	Tiganderket	Kab.	Karo	Sumatera Utara	,\
    214	:	22154	Tanjung Pulo	Tiganderket	Kab.	Karo	Sumatera Utara	,\
    215	:	22154	Temburun	Tiganderket	Kab.	Karo	Sumatera Utara	,\
    216	:	22154	Tiga Nderket (Tiganderket)	Tiganderket	Kab.	Karo	Sumatera Utara	,\
    217	:	22171	Ajibuhara	Tiga Panah	Kab.	Karo	Sumatera Utara	,\
    218	:	22171	Ajijahe	Tiga Panah	Kab.	Karo	Sumatera Utara	,\
    219	:	22171	Ajijulu	Tiga Panah	Kab.	Karo	Sumatera Utara	,\
    220	:	22171	Ajimbelang	Tiga Panah	Kab.	Karo	Sumatera Utara	,\
    221	:	22171	Bertah	Tiga Panah	Kab.	Karo	Sumatera Utara	,\
    222	:	22171	Bunuraya	Tiga Panah	Kab.	Karo	Sumatera Utara	,\
    223	:	22171	Kacinambun	Tiga Panah	Kab.	Karo	Sumatera Utara	,\
    224	:	22171	Kubu Simbelang	Tiga Panah	Kab.	Karo	Sumatera Utara	,\
    225	:	22171	Kuta Bale	Tiga Panah	Kab.	Karo	Sumatera Utara	,\
    226	:	22171	Kuta Kepar	Tiga Panah	Kab.	Karo	Sumatera Utara	,\
    227	:	22171	Kuta Mbelin	Tiga Panah	Kab.	Karo	Sumatera Utara	,\
    228	:	22171	Kutajulu	Tiga Panah	Kab.	Karo	Sumatera Utara	,\
    229	:	22171	Lambar	Tiga Panah	Kab.	Karo	Sumatera Utara	,\
    230	:	22171	Lau Riman	Tiga Panah	Kab.	Karo	Sumatera Utara	,\
    231	:	22171	Lepar Samura	Tiga Panah	Kab.	Karo	Sumatera Utara	,\
    232	:	22171	Manuk Mulia	Tiga Panah	Kab.	Karo	Sumatera Utara	,\
    233	:	22171	Mulawari	Tiga Panah	Kab.	Karo	Sumatera Utara	,\
    234	:	22171	Salit	Tiga Panah	Kab.	Karo	Sumatera Utara	,\
    235	:	22171	Seberaya	Tiga Panah	Kab.	Karo	Sumatera Utara	,\
    236	:	22171	Singa	Tiga Panah	Kab.	Karo	Sumatera Utara	,\
    237	:	22171	Suka	Tiga Panah	Kab.	Karo	Sumatera Utara	,\
    238	:	22171	Suka Mbayak	Tiga Panah	Kab.	Karo	Sumatera Utara	,\
    239	:	22171	Sukadame	Tiga Panah	Kab.	Karo	Sumatera Utara	,\
    240	:	22171	Sukamaju	Tiga Panah	Kab.	Karo	Sumatera Utara	,\
    241	:	22171	Sukapilihen	Tiga Panah	Kab.	Karo	Sumatera Utara	,\
    242	:	22171	Tigapanah	Tiga Panah	Kab.	Karo	Sumatera Utara	,\
    243	:	22252	Bertungen Julu	Tiga Lingga	Kab.	Dairi	Sumatera Utara	,\
    244	:	22252	Juma Gerat	Tiga Lingga	Kab.	Dairi	Sumatera Utara	,\
    245	:	22252	Lau Bagot	Tiga Lingga	Kab.	Dairi	Sumatera Utara	,\
    246	:	22252	Lau Mil	Tiga Lingga	Kab.	Dairi	Sumatera Utara	,\
    247	:	22252	Lau Molgap	Tiga Lingga	Kab.	Dairi	Sumatera Utara	,\
    248	:	22252	Lau Pakpak	Tiga Lingga	Kab.	Dairi	Sumatera Utara	,\
    249	:	22252	Lau Sireme	Tiga Lingga	Kab.	Dairi	Sumatera Utara	,\
    250	:	22252	Palding/Polding	Tiga Lingga	Kab.	Dairi	Sumatera Utara	,\
    251	:	22252	Palding/Polding Jaya Sumbul	Tiga Lingga	Kab.	Dairi	Sumatera Utara	,\
    252	:	22252	Sarintonu	Tiga Lingga	Kab.	Dairi	Sumatera Utara	,\
    253	:	22252	Sukandebi	Tiga Lingga	Kab.	Dairi	Sumatera Utara	,\
    254	:	22252	Sumbul Tengah	Tiga Lingga	Kab.	Dairi	Sumatera Utara	,\
    255	:	22252	Tiga Lingga	Tiga Lingga	Kab.	Dairi	Sumatera Utara	,\
    256	:	22252	Ujung Teran	Tiga Lingga	Kab.	Dairi	Sumatera Utara	,\
    257	:	22162	Batumanak	Tiga Binanga	Kab.	Karo	Sumatera Utara	,\
    258	:	22162	Bunga Baru	Tiga Binanga	Kab.	Karo	Sumatera Utara	,\
    259	:	22162	Gunung	Tiga Binanga	Kab.	Karo	Sumatera Utara	,\
    260	:	22162	Kem Kem	Tiga Binanga	Kab.	Karo	Sumatera Utara	,\
    261	:	22162	Kuala	Tiga Binanga	Kab.	Karo	Sumatera Utara	,\
    262	:	22162	Kuta Bangun	Tiga Binanga	Kab.	Karo	Sumatera Utara	,\
    263	:	22162	Kuta Buara	Tiga Binanga	Kab.	Karo	Sumatera Utara	,\
    264	:	22162	Kuta Galoh/Galuh	Tiga Binanga	Kab.	Karo	Sumatera Utara	,\
    265	:	22162	Kuta Gerat	Tiga Binanga	Kab.	Karo	Sumatera Utara	,\
    266	:	22162	Kuta Julu	Tiga Binanga	Kab.	Karo	Sumatera Utara	,\
    267	:	22162	Kuta Raya	Tiga Binanga	Kab.	Karo	Sumatera Utara	,\
    268	:	22162	Kutambaru Punti Batu Mama	Tiga Binanga	Kab.	Karo	Sumatera Utara	,\
    269	:	22162	Lau Kapur	Tiga Binanga	Kab.	Karo	Sumatera Utara	,\
    270	:	22162	Limang	Tiga Binanga	Kab.	Karo	Sumatera Utara	,\
    271	:	22162	Perbesi	Tiga Binanga	Kab.	Karo	Sumatera Utara	,\
    272	:	22162	Pergendangen	Tiga Binanga	Kab.	Karo	Sumatera Utara	,\
    273	:	22162	Pertumbuken	Tiga Binanga	Kab.	Karo	Sumatera Utara	,\
    274	:	22162	Simolap	Tiga Binanga	Kab.	Karo	Sumatera Utara	,\
    275	:	22162	Simpang Pergendangen Perlambe	Tiga Binanga	Kab.	Karo	Sumatera Utara	,\
    276	:	22162	Tiga Binanga	Tiga Binanga	Kab.	Karo	Sumatera Utara	,\
    277	:	21335	Beting Kwala/Kuala Kapias	Teluk Nibung	Kota	Tanjung Balai	Sumatera Utara	,\
    278	:	21331	Kapias Pulau Buaya	Teluk Nibung	Kota	Tanjung Balai	Sumatera Utara	,\
    279	:	21333	Pematang Pasir	Teluk Nibung	Kota	Tanjung Balai	Sumatera Utara	,\
    280	:	21332	Perjuangan	Teluk Nibung	Kota	Tanjung Balai	Sumatera Utara	,\
    281	:	21334	Sei Merbau	Teluk Nibung	Kota	Tanjung Balai	Sumatera Utara	,\
    282	:	20997	Bogak Besar	Teluk Mengkudu	Kab.	Serdang Bedagai	Sumatera Utara	,\
    283	:	20997	Liberia	Teluk Mengkudu	Kab.	Serdang Bedagai	Sumatera Utara	,\
    284	:	20997	Makmur	Teluk Mengkudu	Kab.	Serdang Bedagai	Sumatera Utara	,\
    285	:	20997	Matapao	Teluk Mengkudu	Kab.	Serdang Bedagai	Sumatera Utara	,\
    286	:	20997	Pasar Baru	Teluk Mengkudu	Kab.	Serdang Bedagai	Sumatera Utara	,\
    287	:	20997	Pekan Sialang Buah	Teluk Mengkudu	Kab.	Serdang Bedagai	Sumatera Utara	,\
    288	:	20997	Pematang Guntung	Teluk Mengkudu	Kab.	Serdang Bedagai	Sumatera Utara	,\
    289	:	20997	Pematang Kuala	Teluk Mengkudu	Kab.	Serdang Bedagai	Sumatera Utara	,\
    290	:	20997	Pematang Seterak (Strak)	Teluk Mengkudu	Kab.	Serdang Bedagai	Sumatera Utara	,\
    291	:	20997	Sei/Sungai Buluh	Teluk Mengkudu	Kab.	Serdang Bedagai	Sumatera Utara	,\
    292	:	20997	Sentang	Teluk Mengkudu	Kab.	Serdang Bedagai	Sumatera Utara	,\
    293	:	20997	Sialang Buah	Teluk Mengkudu	Kab.	Serdang Bedagai	Sumatera Utara	,\
    294	:	21271	Air Teluk Kiri	Teluk Dalam	Kab.	Asahan	Sumatera Utara	,\
    295	:	22865	Bawo Dobara	Teluk Dalam	Kab.	Nias Selatan	Sumatera Utara	,\
    296	:	22865	Bawo Lowalani	Teluk Dalam	Kab.	Nias Selatan	Sumatera Utara	,\
    297	:	22865	Bawo Nifaoso	Teluk Dalam	Kab.	Nias Selatan	Sumatera Utara	,\
    298	:	22865	Bawo Zaua	Teluk Dalam	Kab.	Nias Selatan	Sumatera Utara	,\
    299	:	22865	Ganowo Saua	Teluk Dalam	Kab.	Nias Selatan	Sumatera Utara	,\
    300	:	22865	Hilialito Saua	Teluk Dalam	Kab.	Nias Selatan	Sumatera Utara	,\
    301	:	22865	Hiliamuri	Teluk Dalam	Kab.	Nias Selatan	Sumatera Utara	,\
    302	:	22865	Hiliana`a	Teluk Dalam	Kab.	Nias Selatan	Sumatera Utara	,\
    303	:	22865	Hilifalago	Teluk Dalam	Kab.	Nias Selatan	Sumatera Utara	,\
    304	:	22865	Hilifalago Raya	Teluk Dalam	Kab.	Nias Selatan	Sumatera Utara	,\
    305	:	22865	Hilifarono	Teluk Dalam	Kab.	Nias Selatan	Sumatera Utara	,\
    306	:	22865	Hiliganowo	Teluk Dalam	Kab.	Nias Selatan	Sumatera Utara	,\
    307	:	22865	Hiliganowo Salo`o	Teluk Dalam	Kab.	Nias Selatan	Sumatera Utara	,\
    308	:	22865	Hiligeho	Teluk Dalam	Kab.	Nias Selatan	Sumatera Utara	,\
    309	:	22865	Hilikara	Teluk Dalam	Kab.	Nias Selatan	Sumatera Utara	,\
    310	:	22865	Hililaza	Teluk Dalam	Kab.	Nias Selatan	Sumatera Utara	,\
    311	:	22865	Hilimondregeraya	Teluk Dalam	Kab.	Nias Selatan	Sumatera Utara	,\
    312	:	22865	Hilinamozaua	Teluk Dalam	Kab.	Nias Selatan	Sumatera Utara	,\
    313	:	22865	Hilinamozaua Raya	Teluk Dalam	Kab.	Nias Selatan	Sumatera Utara	,\
    314	:	22865	Hilionaha	Teluk Dalam	Kab.	Nias Selatan	Sumatera Utara	,\
    315	:	22865	Hilisanekhehosi	Teluk Dalam	Kab.	Nias Selatan	Sumatera Utara	,\
    316	:	22865	Hilisaootoniha	Teluk Dalam	Kab.	Nias Selatan	Sumatera Utara	,\
    317	:	22865	Hilisondrekha	Teluk Dalam	Kab.	Nias Selatan	Sumatera Utara	,\
    318	:	22865	Hilitobara	Teluk Dalam	Kab.	Nias Selatan	Sumatera Utara	,\
    319	:	21271	Mekar Tanjung	Teluk Dalam	Kab.	Asahan	Sumatera Utara	,\
    320	:	22865	Nanowa	Teluk Dalam	Kab.	Nias Selatan	Sumatera Utara	,\
    321	:	22865	Pasar Teluk Dalam	Teluk Dalam	Kab.	Nias Selatan	Sumatera Utara	,\
    322	:	21271	Perkebunan Teluk Dalam	Teluk Dalam	Kab.	Asahan	Sumatera Utara	,\
    323	:	21271	Pulau Maria	Teluk Dalam	Kab.	Asahan	Sumatera Utara	,\
    324	:	21271	Pulau Tanjung	Teluk Dalam	Kab.	Asahan	Sumatera Utara	,\
    325	:	21271	Teluk Dalam	Teluk Dalam	Kab.	Asahan	Sumatera Utara	,\
    326	:	20615	Badak Bejuang	Tebing Tinggi Kota	Kota	Tebing Tinggi	Sumatera Utara	,\
    327	:	20613	Bandar Utama	Tebing Tinggi Kota	Kota	Tebing Tinggi	Sumatera Utara	,\
    328	:	20626	Mandailing	Tebing Tinggi Kota	Kota	Tebing Tinggi	Sumatera Utara	,\
    329	:	20627	Pasar Baru	Tebing Tinggi Kota	Kota	Tebing Tinggi	Sumatera Utara	,\
    330	:	20628	Pasar Gambir	Tebing Tinggi Kota	Kota	Tebing Tinggi	Sumatera Utara	,\
    331	:	20633	Rambung	Tebing Tinggi Kota	Kota	Tebing Tinggi	Sumatera Utara	,\
    332	:	20632	Tebing Tinggi Lama	Tebing Tinggi Kota	Kota	Tebing Tinggi	Sumatera Utara	,\
    333	:	20998	Bah Sumbu	Tebing Tinggi	Kab.	Serdang Bedagai	Sumatera Utara	,\
    334	:	20998	Gunung Kataran	Tebing Tinggi	Kab.	Serdang Bedagai	Sumatera Utara	,\
    335	:	20998	Jambu	Tebing Tinggi	Kab.	Serdang Bedagai	Sumatera Utara	,\
    336	:	20998	Kedai Damar	Tebing Tinggi	Kab.	Serdang Bedagai	Sumatera Utara	,\
    337	:	20998	Kuta Baru	Tebing Tinggi	Kab.	Serdang Bedagai	Sumatera Utara	,\
    338	:	20998	Mariah Padang	Tebing Tinggi	Kab.	Serdang Bedagai	Sumatera Utara	,\
    339	:	20998	Naga Kesiangan	Tebing Tinggi	Kab.	Serdang Bedagai	Sumatera Utara	,\
    340	:	20998	Paya Bagas	Tebing Tinggi	Kab.	Serdang Bedagai	Sumatera Utara	,\
    341	:	20998	Paya Lombang	Tebing Tinggi	Kab.	Serdang Bedagai	Sumatera Utara	,\
    342	:	20998	Paya Mabar	Tebing Tinggi	Kab.	Serdang Bedagai	Sumatera Utara	,\
    343	:	20998	Penonggol	Tebing Tinggi	Kab.	Serdang Bedagai	Sumatera Utara	,\
    344	:	20998	Pertapaan	Tebing Tinggi	Kab.	Serdang Bedagai	Sumatera Utara	,\
    345	:	20998	Sei Priok (Sungai Periok)	Tebing Tinggi	Kab.	Serdang Bedagai	Sumatera Utara	,\
    346	:	20998	Sei Serimah	Tebing Tinggi	Kab.	Serdang Bedagai	Sumatera Utara	,\
    347	:	20998	Bahilang	Tebing Syahbandar	Kab.	Serdang Bedagai	Sumatera Utara	,\
    348	:	20998	Binjai	Tebing Syahbandar	Kab.	Serdang Bedagai	Sumatera Utara	,\
    349	:	20998	Kuta Pinang	Tebing Syahbandar	Kab.	Serdang Bedagai	Sumatera Utara	,\
    350	:	20998	Laut Tador	Tebing Syahbandar	Kab.	Serdang Bedagai	Sumatera Utara	,\
    351	:	20998	Paya Pasir	Tebing Syahbandar	Kab.	Serdang Bedagai	Sumatera Utara	,\
    352	:	20998	Paya Pinang	Tebing Syahbandar	Kab.	Serdang Bedagai	Sumatera Utara	,\
    353	:	20998	Penggalangan	Tebing Syahbandar	Kab.	Serdang Bedagai	Sumatera Utara	,\
    354	:	20998	Penggalian	Tebing Syahbandar	Kab.	Serdang Bedagai	Sumatera Utara	,\
    355	:	20998	Sibulan	Tebing Syahbandar	Kab.	Serdang Bedagai	Sumatera Utara	,\
    356	:	20998	Tanah Besih	Tebing Syahbandar	Kab.	Serdang Bedagai	Sumatera Utara	,\
    357	:	22413	Aek Siansimun / Siamsimun	Tarutung	Kab.	Tapanuli Utara	Sumatera Utara	,\
    358	:	22416	Hapoltahan	Tarutung	Kab.	Tapanuli Utara	Sumatera Utara	,\
    359	:	22411	Hutagalung Siwaluompu	Tarutung	Kab.	Tapanuli Utara	Sumatera Utara	,\
    360	:	22411	Hutapea Banuarea	Tarutung	Kab.	Tapanuli Utara	Sumatera Utara	,\
    361	:	22414	Hutatoruan I	Tarutung	Kab.	Tapanuli Utara	Sumatera Utara	,\
    362	:	22414	Hutatoruan III	Tarutung	Kab.	Tapanuli Utara	Sumatera Utara	,\
    363	:	22415	Hutatoruan IV	Tarutung	Kab.	Tapanuli Utara	Sumatera Utara	,\
    364	:	22412	Hutatoruan IX	Tarutung	Kab.	Tapanuli Utara	Sumatera Utara	,\
    365	:	22413	Hutatoruan V	Tarutung	Kab.	Tapanuli Utara	Sumatera Utara	,\
    366	:	22413	Hutatoruan VI	Tarutung	Kab.	Tapanuli Utara	Sumatera Utara	,\
    367	:	22413	Hutatoruan VII	Tarutung	Kab.	Tapanuli Utara	Sumatera Utara	,\
    368	:	22413	Hutatoruan VIII	Tarutung	Kab.	Tapanuli Utara	Sumatera Utara	,\
    369	:	22411	Hutatoruan X	Tarutung	Kab.	Tapanuli Utara	Sumatera Utara	,\
    370	:	22411	Hutatoruan XI	Tarutung	Kab.	Tapanuli Utara	Sumatera Utara	,\
    371	:	22411	Hutauruk	Tarutung	Kab.	Tapanuli Utara	Sumatera Utara	,\
    372	:	22452	Jambur Nauli	Tarutung	Kab.	Tapanuli Utara	Sumatera Utara	,\
    373	:	22411	Parbaju Julu	Tarutung	Kab.	Tapanuli Utara	Sumatera Utara	,\
    374	:	22416	Parbajutonga	Tarutung	Kab.	Tapanuli Utara	Sumatera Utara	,\
    375	:	22416	Parbajutoruan	Tarutung	Kab.	Tapanuli Utara	Sumatera Utara	,\
    376	:	22414	Parbubu Dolok	Tarutung	Kab.	Tapanuli Utara	Sumatera Utara	,\
    377	:	22414	Parbubu I	Tarutung	Kab.	Tapanuli Utara	Sumatera Utara	,\
    378	:	22414	Parbubu II	Tarutung	Kab.	Tapanuli Utara	Sumatera Utara	,\
    379	:	22414	Parbubu Pea	Tarutung	Kab.	Tapanuli Utara	Sumatera Utara	,\
    380	:	22416	Partali Julu	Tarutung	Kab.	Tapanuli Utara	Sumatera Utara	,\
    381	:	22416	Partali Toruan	Tarutung	Kab.	Tapanuli Utara	Sumatera Utara	,\
    382	:	22417	Siandor Andor	Tarutung	Kab.	Tapanuli Utara	Sumatera Utara	,\
    383	:	22452	Sihujur	Tarutung	Kab.	Tapanuli Utara	Sumatera Utara	,\
    384	:	22411	Simamora	Tarutung	Kab.	Tapanuli Utara	Sumatera Utara	,\
    385	:	22415	Siraja Oloan	Tarutung	Kab.	Tapanuli Utara	Sumatera Utara	,\
    386	:	22415	Sitampurung	Tarutung	Kab.	Tapanuli Utara	Sumatera Utara	,\
    387	:	22411	Sosunggulon	Tarutung	Kab.	Tapanuli Utara	Sumatera Utara	,\
    388	:	22456	Marpadan	Tara Bintang	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    389	:	22456	Mungkur	Tara Bintang	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    390	:	22456	Sibongkare	Tara Bintang	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    391	:	22456	Sibongkare Sianju	Tara Bintang	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    392	:	22456	Sihombu	Tara Bintang	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    393	:	22456	Sihotang Hasugian Toruan	Tara Bintang	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    394	:	22456	Simbara	Tara Bintang	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    395	:	22456	Sitanduk	Tara Bintang	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    396	:	22456	Tara Bintang	Tara Bintang	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    397	:	22618	Aloban	Tapian Nauli	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    398	:	22618	Bair	Tapian Nauli	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    399	:	22618	Mela Dolok	Tapian Nauli	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    400	:	22618	Mela I	Tapian Nauli	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    401	:	22618	Mela II	Tapian Nauli	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    402	:	22618	Tapian Nauli I	Tapian Nauli	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    403	:	22618	Tapian Nauli II	Tapian Nauli	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    404	:	22618	Tapian Nauli III	Tapian Nauli	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    405	:	22618	Tapian Nauli IV	Tapian Nauli	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    406	:	21154	Batu Silangit	Tapian Dolok	Kab.	Simalungun	Sumatera Utara	,\
    407	:	21154	Dolok Kahean	Tapian Dolok	Kab.	Simalungun	Sumatera Utara	,\
    408	:	21154	Dolok Maraja	Tapian Dolok	Kab.	Simalungun	Sumatera Utara	,\
    409	:	21154	Dolok Ulu	Tapian Dolok	Kab.	Simalungun	Sumatera Utara	,\
    410	:	21154	Naga Dolok	Tapian Dolok	Kab.	Simalungun	Sumatera Utara	,\
    411	:	21154	Nagur Usang	Tapian Dolok	Kab.	Simalungun	Sumatera Utara	,\
    412	:	21154	Negeri Bayu Muslimin	Tapian Dolok	Kab.	Simalungun	Sumatera Utara	,\
    413	:	21154	Pematang Dolok Kahean	Tapian Dolok	Kab.	Simalungun	Sumatera Utara	,\
    414	:	21154	Purba Sari	Tapian Dolok	Kab.	Simalungun	Sumatera Utara	,\
    415	:	21154	Sinaksak	Tapian Dolok	Kab.	Simalungun	Sumatera Utara	,\
    416	:	22774	Aek Kahombu	Tano Tombangan Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    417	:	22774	Aek Parupuk	Tano Tombangan Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    418	:	22774	Aek Uncim	Tano Tombangan Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    419	:	22774	Batu Horpak	Tano Tombangan Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    420	:	22774	Harean	Tano Tombangan Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    421	:	22774	Hutaraja	Tano Tombangan Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    422	:	22774	Ingul Jae	Tano Tombangan Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    423	:	22774	Kota Tua	Tano Tombangan Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    424	:	22774	Lumban Jabi-Jabi	Tano Tombangan Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    425	:	22774	Lumban Ratus	Tano Tombangan Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    426	:	22774	Panabari Hutatonga	Tano Tombangan Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    427	:	22774	Panindoan	Tano Tombangan Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    428	:	22774	Purba Tua	Tano Tombangan Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    429	:	22774	Simaninggir TT	Tano Tombangan Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    430	:	22774	Sisoma	Tano Tombangan Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    431	:	22774	Situmba	Tano Tombangan Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    432	:	22774	Tanjung Medan	Tano Tombangan Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    433	:	20853	Baja Kuning	Tanjungpura	Kab.	Langkat	Sumatera Utara	,\
    434	:	20853	Bubun	Tanjungpura	Kab.	Langkat	Sumatera Utara	,\
    435	:	20853	Karya Maju	Tanjungpura	Kab.	Langkat	Sumatera Utara	,\
    436	:	20853	Kwala Langkat	Tanjungpura	Kab.	Langkat	Sumatera Utara	,\
    437	:	20853	Kwala Serapuh	Tanjungpura	Kab.	Langkat	Sumatera Utara	,\
    438	:	20853	Lalang	Tanjungpura	Kab.	Langkat	Sumatera Utara	,\
    439	:	20853	Pantai Cermin	Tanjungpura	Kab.	Langkat	Sumatera Utara	,\
    440	:	20853	Paya Perupuk	Tanjungpura	Kab.	Langkat	Sumatera Utara	,\
    441	:	20853	Pekan Tanjung Pura	Tanjungpura	Kab.	Langkat	Sumatera Utara	,\
    442	:	20853	Pekubuan	Tanjungpura	Kab.	Langkat	Sumatera Utara	,\
    443	:	20853	Pematang Cengal	Tanjungpura	Kab.	Langkat	Sumatera Utara	,\
    444	:	20853	Pematang Cengal Barat	Tanjungpura	Kab.	Langkat	Sumatera Utara	,\
    445	:	20853	Pematang Serai	Tanjungpura	Kab.	Langkat	Sumatera Utara	,\
    446	:	20853	Pematang Tengah	Tanjungpura	Kab.	Langkat	Sumatera Utara	,\
    447	:	20853	Pulau Banyak	Tanjungpura	Kab.	Langkat	Sumatera Utara	,\
    448	:	20853	Serapuh Asli	Tanjungpura	Kab.	Langkat	Sumatera Utara	,\
    449	:	20853	Suka Maju	Tanjungpura	Kab.	Langkat	Sumatera Utara	,\
    450	:	20853	Tapak Kuda	Tanjungpura	Kab.	Langkat	Sumatera Utara	,\
    451	:	20853	Teluk Bakung	Tanjungpura	Kab.	Langkat	Sumatera Utara	,\
    452	:	21253	Bagan Arya	Tanjung Tiram	Kab.	Batu Bara	Sumatera Utara	,\
    453	:	21253	Bagan Baru	Tanjung Tiram	Kab.	Batu Bara	Sumatera Utara	,\
    454	:	21253	Bagan Dalam	Tanjung Tiram	Kab.	Batu Bara	Sumatera Utara	,\
    455	:	21253	Bandar Rahmat	Tanjung Tiram	Kab.	Batu Bara	Sumatera Utara	,\
    456	:	21253	Bandar Sono	Tanjung Tiram	Kab.	Batu Bara	Sumatera Utara	,\
    457	:	21253	Bogak	Tanjung Tiram	Kab.	Batu Bara	Sumatera Utara	,\
    458	:	21253	Guntung	Tanjung Tiram	Kab.	Batu Bara	Sumatera Utara	,\
    459	:	21253	Jati Mulia	Tanjung Tiram	Kab.	Batu Bara	Sumatera Utara	,\
    460	:	21253	Kampung Lalang	Tanjung Tiram	Kab.	Batu Bara	Sumatera Utara	,\
    461	:	21253	Kapal Merah	Tanjung Tiram	Kab.	Batu Bara	Sumatera Utara	,\
    462	:	21253	Lima Laras	Tanjung Tiram	Kab.	Batu Bara	Sumatera Utara	,\
    463	:	21253	Mekar Laras	Tanjung Tiram	Kab.	Batu Bara	Sumatera Utara	,\
    464	:	21253	Pahlawan	Tanjung Tiram	Kab.	Batu Bara	Sumatera Utara	,\
    465	:	21253	Pematang Rambe	Tanjung Tiram	Kab.	Batu Bara	Sumatera Utara	,\
    466	:	21253	Sei Mentaram	Tanjung Tiram	Kab.	Batu Bara	Sumatera Utara	,\
    467	:	21253	Suka Jaya	Tanjung Tiram	Kab.	Batu Bara	Sumatera Utara	,\
    468	:	21253	Suka Maju	Tanjung Tiram	Kab.	Batu Bara	Sumatera Utara	,\
    469	:	21253	Tali Air Permai	Tanjung Tiram	Kab.	Batu Bara	Sumatera Utara	,\
    470	:	21253	Tanjungmulia	Tanjung Tiram	Kab.	Batu Bara	Sumatera Utara	,\
    471	:	21253	Tanjungtiram	Tanjung Tiram	Kab.	Batu Bara	Sumatera Utara	,\
    472	:	21253	Ujung Kubu	Tanjung Tiram	Kab.	Batu Bara	Sumatera Utara	,\
    473	:	20362	Aek Pancur	Tanjung Morawa	Kab.	Deli Serdang	Sumatera Utara	,\
    474	:	20362	Bandar Labuhan	Tanjung Morawa	Kab.	Deli Serdang	Sumatera Utara	,\
    475	:	20362	Bangun Rejo	Tanjung Morawa	Kab.	Deli Serdang	Sumatera Utara	,\
    476	:	20362	Bangun Sari	Tanjung Morawa	Kab.	Deli Serdang	Sumatera Utara	,\
    477	:	20362	Bangun Sari Baru	Tanjung Morawa	Kab.	Deli Serdang	Sumatera Utara	,\
    478	:	20362	Buntu Badimbar (Bedimbar)	Tanjung Morawa	Kab.	Deli Serdang	Sumatera Utara	,\
    479	:	20362	Dagang Kelambir	Tanjung Morawa	Kab.	Deli Serdang	Sumatera Utara	,\
    480	:	20362	Dagang Krawan (Kerawan)	Tanjung Morawa	Kab.	Deli Serdang	Sumatera Utara	,\
    481	:	20362	Dalu X A (Dalu Sepuluh A)	Tanjung Morawa	Kab.	Deli Serdang	Sumatera Utara	,\
    482	:	20362	Dalu X B (Dalu Sepuluh B)	Tanjung Morawa	Kab.	Deli Serdang	Sumatera Utara	,\
    483	:	20362	Lengau Serpang	Tanjung Morawa	Kab.	Deli Serdang	Sumatera Utara	,\
    484	:	20362	Limau Manis	Tanjung Morawa	Kab.	Deli Serdang	Sumatera Utara	,\
    485	:	20362	Medan Sinembah	Tanjung Morawa	Kab.	Deli Serdang	Sumatera Utara	,\
    486	:	20362	Naga Timbul	Tanjung Morawa	Kab.	Deli Serdang	Sumatera Utara	,\
    487	:	20362	Pekan Tanjung Morawa	Tanjung Morawa	Kab.	Deli Serdang	Sumatera Utara	,\
    488	:	20362	Penara Kebon/Kebun	Tanjung Morawa	Kab.	Deli Serdang	Sumatera Utara	,\
    489	:	20362	Perdamean (Perdamaian)	Tanjung Morawa	Kab.	Deli Serdang	Sumatera Utara	,\
    490	:	20362	Punden Rejo	Tanjung Morawa	Kab.	Deli Serdang	Sumatera Utara	,\
    491	:	20362	Sei/Sungai Merah	Tanjung Morawa	Kab.	Deli Serdang	Sumatera Utara	,\
    492	:	20362	Tanjung Baru	Tanjung Morawa	Kab.	Deli Serdang	Sumatera Utara	,\
    493	:	20362	Tanjung Morawa A	Tanjung Morawa	Kab.	Deli Serdang	Sumatera Utara	,\
    494	:	20362	Tanjung Morawa B	Tanjung Morawa	Kab.	Deli Serdang	Sumatera Utara	,\
    495	:	20362	Tanjung Mulia	Tanjung Morawa	Kab.	Deli Serdang	Sumatera Utara	,\
    496	:	20362	Telaga Sari	Tanjung Morawa	Kab.	Deli Serdang	Sumatera Utara	,\
    497	:	20362	Ujung Serdang	Tanjung Morawa	Kab.	Deli Serdang	Sumatera Utara	,\
    498	:	20362	Wono Sari	Tanjung Morawa	Kab.	Deli Serdang	Sumatera Utara	,\
    499	:	20996	Bagan Kuala	Tanjung Beringin	Kab.	Serdang Bedagai	Sumatera Utara	,\
    500	:	20996	Mangga Dua	Tanjung Beringin	Kab.	Serdang Bedagai	Sumatera Utara	,\
    501	:	20996	Nagur	Tanjung Beringin	Kab.	Serdang Bedagai	Sumatera Utara	,\
    502	:	20996	Pekan Tanjung Beringin	Tanjung Beringin	Kab.	Serdang Bedagai	Sumatera Utara	,\
    503	:	20996	Pematang Cermai	Tanjung Beringin	Kab.	Serdang Bedagai	Sumatera Utara	,\
    504	:	20996	Pematang Terang	Tanjung Beringin	Kab.	Serdang Bedagai	Sumatera Utara	,\
    505	:	20996	Sukajadi	Tanjung Beringin	Kab.	Serdang Bedagai	Sumatera Utara	,\
    506	:	20996	Tebing Tinggi	Tanjung Beringin	Kab.	Serdang Bedagai	Sumatera Utara	,\
    507	:	21324	Kuala Silau Bestari	Tanjung Balai Utara	Kota	Tanjung Balai	Sumatera Utara	,\
    508	:	21325	Matahalasan	Tanjung Balai Utara	Kota	Tanjung Balai	Sumatera Utara	,\
    509	:	21323	Sejahtera	Tanjung Balai Utara	Kota	Tanjung Balai	Sumatera Utara	,\
    510	:	21321	Tanjungbalai Kota III	Tanjung Balai Utara	Kota	Tanjung Balai	Sumatera Utara	,\
    511	:	21322	Tanjungbalai Kota IV	Tanjung Balai Utara	Kota	Tanjung Balai	Sumatera Utara	,\
    512	:	21315	Indra Sakti	Tanjung Balai Selatan	Kota	Tanjung Balai	Sumatera Utara	,\
    513	:	21314	Karya	Tanjung Balai Selatan	Kota	Tanjung Balai	Sumatera Utara	,\
    514	:	21316	Pantai Burung	Tanjung Balai Selatan	Kota	Tanjung Balai	Sumatera Utara	,\
    515	:	21313	Perwira	Tanjung Balai Selatan	Kota	Tanjung Balai	Sumatera Utara	,\
    516	:	21311	Tanjungbalai Kota I	Tanjung Balai Selatan	Kota	Tanjung Balai	Sumatera Utara	,\
    517	:	21312	Tanjungbalai Kota II	Tanjung Balai Selatan	Kota	Tanjung Balai	Sumatera Utara	,\
    518	:	21352	Asahan Mati	Tanjung Balai	Kab.	Asahan	Sumatera Utara	,\
    519	:	21352	Bagan Asahan	Tanjung Balai	Kab.	Asahan	Sumatera Utara	,\
    520	:	21352	Bagan Asahan Baru	Tanjung Balai	Kab.	Asahan	Sumatera Utara	,\
    521	:	21352	Bagan Asahan Pekan	Tanjung Balai	Kab.	Asahan	Sumatera Utara	,\
    522	:	21352	Kapias Batu VIII	Tanjung Balai	Kab.	Asahan	Sumatera Utara	,\
    523	:	21352	Pematang Sungai/Sei Baru	Tanjung Balai	Kab.	Asahan	Sumatera Utara	,\
    524	:	21352	Sei/Sungai Apung	Tanjung Balai	Kab.	Asahan	Sumatera Utara	,\
    525	:	21352	Sei/Sungai Apung Jaya	Tanjung Balai	Kab.	Asahan	Sumatera Utara	,\
    526	:	22253	Gunung Tua	Tanah Pinem	Kab.	Dairi	Sumatera Utara	,\
    527	:	22253	Harapan	Tanah Pinem	Kab.	Dairi	Sumatera Utara	,\
    528	:	22253	Kempawa	Tanah Pinem	Kab.	Dairi	Sumatera Utara	,\
    529	:	22253	Kuta Gambir	Tanah Pinem	Kab.	Dairi	Sumatera Utara	,\
    530	:	22253	Kutabuluh	Tanah Pinem	Kab.	Dairi	Sumatera Utara	,\
    531	:	22253	Lau Primbon	Tanah Pinem	Kab.	Dairi	Sumatera Utara	,\
    532	:	22253	Lau Tawar	Tanah Pinem	Kab.	Dairi	Sumatera Utara	,\
    533	:	22253	Pamah	Tanah Pinem	Kab.	Dairi	Sumatera Utara	,\
    534	:	22253	Pasir Tengah	Tanah Pinem	Kab.	Dairi	Sumatera Utara	,\
    535	:	22253	Renun	Tanah Pinem	Kab.	Dairi	Sumatera Utara	,\
    536	:	22253	Suka Dame	Tanah Pinem	Kab.	Dairi	Sumatera Utara	,\
    537	:	22253	Tanah Pinem	Tanah Pinem	Kab.	Dairi	Sumatera Utara	,\
    538	:	22881	Baluta	Tanah Masa	Kab.	Nias Selatan	Sumatera Utara	,\
    539	:	22881	Bawo Analita Saeru	Tanah Masa	Kab.	Nias Selatan	Sumatera Utara	,\
    540	:	22881	Bawo Ofuloa	Tanah Masa	Kab.	Nias Selatan	Sumatera Utara	,\
    541	:	22881	Bawo Orudua	Tanah Masa	Kab.	Nias Selatan	Sumatera Utara	,\
    542	:	22881	Eho Baluta	Tanah Masa	Kab.	Nias Selatan	Sumatera Utara	,\
    543	:	22881	Hale Baluta	Tanah Masa	Kab.	Nias Selatan	Sumatera Utara	,\
    544	:	22881	Hiligeho Sogawu	Tanah Masa	Kab.	Nias Selatan	Sumatera Utara	,\
    545	:	22881	Hilimasio	Tanah Masa	Kab.	Nias Selatan	Sumatera Utara	,\
    546	:	22881	Jeke	Tanah Masa	Kab.	Nias Selatan	Sumatera Utara	,\
    547	:	22881	Makole	Tanah Masa	Kab.	Nias Selatan	Sumatera Utara	,\
    548	:	22881	Saeru Melayu	Tanah Masa	Kab.	Nias Selatan	Sumatera Utara	,\
    549	:	22881	Sifauruasi	Tanah Masa	Kab.	Nias Selatan	Sumatera Utara	,\
    550	:	21181	Bah Jambi II	Tanah Jawa	Kab.	Simalungun	Sumatera Utara	,\
    551	:	21181	Bah Jambi III	Tanah Jawa	Kab.	Simalungun	Sumatera Utara	,\
    552	:	21181	Bah Kisat	Tanah Jawa	Kab.	Simalungun	Sumatera Utara	,\
    553	:	21181	Baja Dolok	Tanah Jawa	Kab.	Simalungun	Sumatera Utara	,\
    554	:	21181	Baliju	Tanah Jawa	Kab.	Simalungun	Sumatera Utara	,\
    555	:	21181	Balimbingan	Tanah Jawa	Kab.	Simalungun	Sumatera Utara	,\
    556	:	21181	Bayu Bagasan	Tanah Jawa	Kab.	Simalungun	Sumatera Utara	,\
    557	:	21181	Bosar Galugur	Tanah Jawa	Kab.	Simalungun	Sumatera Utara	,\
    558	:	21181	Maligas Tongah	Tanah Jawa	Kab.	Simalungun	Sumatera Utara	,\
    559	:	21181	Marubun Bayu	Tanah Jawa	Kab.	Simalungun	Sumatera Utara	,\
    560	:	21181	Marubun Jaya	Tanah Jawa	Kab.	Simalungun	Sumatera Utara	,\
    561	:	21181	Mekar Mulia	Tanah Jawa	Kab.	Simalungun	Sumatera Utara	,\
    562	:	21181	Muara Mulia	Tanah Jawa	Kab.	Simalungun	Sumatera Utara	,\
    563	:	21181	Pagar Jambi	Tanah Jawa	Kab.	Simalungun	Sumatera Utara	,\
    564	:	21181	Panembean Marjanji (Panambean Marjandi)	Tanah Jawa	Kab.	Simalungun	Sumatera Utara	,\
    565	:	21181	Parbalogan	Tanah Jawa	Kab.	Simalungun	Sumatera Utara	,\
    566	:	21181	Pardamean Asih	Tanah Jawa	Kab.	Simalungun	Sumatera Utara	,\
    567	:	21181	Pematang Tanah Jawa	Tanah Jawa	Kab.	Simalungun	Sumatera Utara	,\
    568	:	21181	Tanjung Pasir	Tanah Jawa	Kab.	Simalungun	Sumatera Utara	,\
    569	:	21181	Totap Majawa	Tanah Jawa	Kab.	Simalungun	Sumatera Utara	,\
    570	:	22312	Gukguk/Gurgur Aek Raja	Tampahan	Kab.	Toba Samosir	Sumatera Utara	,\
    571	:	22312	Lintong Nihuta	Tampahan	Kab.	Toba Samosir	Sumatera Utara	,\
    572	:	22312	Meat	Tampahan	Kab.	Toba Samosir	Sumatera Utara	,\
    573	:	22312	Tangga Batu Barat	Tampahan	Kab.	Toba Samosir	Sumatera Utara	,\
    574	:	22312	Tangga Batu Timur	Tampahan	Kab.	Toba Samosir	Sumatera Utara	,\
    575	:	22312	Tara Bunga	Tampahan	Kab.	Toba Samosir	Sumatera Utara	,\
    576	:	22994	Angin Barat	Tambangan	Kab.	Mandailing Natal	Sumatera Utara	,\
    577	:	22994	Huta Tonga AB	Tambangan	Kab.	Mandailing Natal	Sumatera Utara	,\
    578	:	22994	Laru Baringin	Tambangan	Kab.	Mandailing Natal	Sumatera Utara	,\
    579	:	22994	Laru Bolak	Tambangan	Kab.	Mandailing Natal	Sumatera Utara	,\
    580	:	22994	Laru Dolok	Tambangan	Kab.	Mandailing Natal	Sumatera Utara	,\
    581	:	22994	Laru Lombang	Tambangan	Kab.	Mandailing Natal	Sumatera Utara	,\
    582	:	22994	Lumban Pasir	Tambangan	Kab.	Mandailing Natal	Sumatera Utara	,\
    583	:	22994	Muara Mais	Tambangan	Kab.	Mandailing Natal	Sumatera Utara	,\
    584	:	22994	Muara Mais Jambur	Tambangan	Kab.	Mandailing Natal	Sumatera Utara	,\
    585	:	22994	Padang Sanggar	Tambangan	Kab.	Mandailing Natal	Sumatera Utara	,\
    586	:	22994	Panjaringan	Tambangan	Kab.	Mandailing Natal	Sumatera Utara	,\
    587	:	22994	Pasar Laru	Tambangan	Kab.	Mandailing Natal	Sumatera Utara	,\
    588	:	22994	Pastap	Tambangan	Kab.	Mandailing Natal	Sumatera Utara	,\
    589	:	22994	Pastap Julu	Tambangan	Kab.	Mandailing Natal	Sumatera Utara	,\
    590	:	22994	Rao Rao Dolok	Tambangan	Kab.	Mandailing Natal	Sumatera Utara	,\
    591	:	22994	Rao Rao Lombang	Tambangan	Kab.	Mandailing Natal	Sumatera Utara	,\
    592	:	22994	Simangambat TB	Tambangan	Kab.	Mandailing Natal	Sumatera Utara	,\
    593	:	22994	Tambangan Jae	Tambangan	Kab.	Mandailing Natal	Sumatera Utara	,\
    594	:	22994	Tambangan Pasoman	Tambangan	Kab.	Mandailing Natal	Sumatera Utara	,\
    595	:	22994	Tambangan Tonga	Tambangan	Kab.	Mandailing Natal	Sumatera Utara	,\
    596	:	21254	Bangun Sari	Talawi	Kab.	Batu Bara	Sumatera Utara	,\
    597	:	21254	Benteng	Talawi	Kab.	Batu Bara	Sumatera Utara	,\
    598	:	21254	Binjai Baru	Talawi	Kab.	Batu Bara	Sumatera Utara	,\
    599	:	21254	Dahari Indah	Talawi	Kab.	Batu Bara	Sumatera Utara	,\
    600	:	21254	Dahari Selebar	Talawi	Kab.	Batu Bara	Sumatera Utara	,\
    601	:	21254	Glugur Makmur	Talawi	Kab.	Batu Bara	Sumatera Utara	,\
    602	:	21254	Gunung Rante	Talawi	Kab.	Batu Bara	Sumatera Utara	,\
    603	:	21254	Indra Yaman	Talawi	Kab.	Batu Bara	Sumatera Utara	,\
    604	:	21254	Karang Baru	Talawi	Kab.	Batu Bara	Sumatera Utara	,\
    605	:	21254	Labuhan Ruku	Talawi	Kab.	Batu Bara	Sumatera Utara	,\
    606	:	21254	Mekar Baru	Talawi	Kab.	Batu Bara	Sumatera Utara	,\
    607	:	21254	Mesjid Lama	Talawi	Kab.	Batu Bara	Sumatera Utara	,\
    608	:	21254	Padang Genting	Talawi	Kab.	Batu Bara	Sumatera Utara	,\
    609	:	21254	Pahang	Talawi	Kab.	Batu Bara	Sumatera Utara	,\
    610	:	21254	Panjang	Talawi	Kab.	Batu Bara	Sumatera Utara	,\
    611	:	21254	Perkebunan Petatal	Talawi	Kab.	Batu Bara	Sumatera Utara	,\
    612	:	21254	Perkebunan Tanah Datar	Talawi	Kab.	Batu Bara	Sumatera Utara	,\
    613	:	21254	Petatal	Talawi	Kab.	Batu Bara	Sumatera Utara	,\
    614	:	21254	Sei Muka	Talawi	Kab.	Batu Bara	Sumatera Utara	,\
    615	:	21254	Sumber Tani	Talawi	Kab.	Batu Bara	Sumatera Utara	,\
    616	:	22873	Bintang Baru	Susua	Kab.	Nias Selatan	Sumatera Utara	,\
    617	:	22873	Dao-dao Zanuwo	Susua	Kab.	Nias Selatan	Sumatera Utara	,\
    618	:	22873	Hiliadulosoi	Susua	Kab.	Nias Selatan	Sumatera Utara	,\
    619	:	22873	Hilianaa Susua	Susua	Kab.	Nias Selatan	Sumatera Utara	,\
    620	:	22873	Hilidanayao	Susua	Kab.	Nias Selatan	Sumatera Utara	,\
    621	:	22873	Hilimboe	Susua	Kab.	Nias Selatan	Sumatera Utara	,\
    622	:	22873	Hilimboho	Susua	Kab.	Nias Selatan	Sumatera Utara	,\
    623	:	22873	Hiliorahua	Susua	Kab.	Nias Selatan	Sumatera Utara	,\
    624	:	22873	Hilioru dua	Susua	Kab.	Nias Selatan	Sumatera Utara	,\
    625	:	22873	Hilisibohou	Susua	Kab.	Nias Selatan	Sumatera Utara	,\
    626	:	22873	Hilitobara Susua	Susua	Kab.	Nias Selatan	Sumatera Utara	,\
    627	:	22873	Hiliwaebu	Susua	Kab.	Nias Selatan	Sumatera Utara	,\
    628	:	22873	Hilizamurugo	Susua	Kab.	Nias Selatan	Sumatera Utara	,\
    629	:	22873	Orahili Boe	Susua	Kab.	Nias Selatan	Sumatera Utara	,\
    630	:	22873	Orahili Susua	Susua	Kab.	Nias Selatan	Sumatera Utara	,\
    631	:	22873	Orahua Uluzoi	Susua	Kab.	Nias Selatan	Sumatera Utara	,\
    632	:	22873	Sifalago Susua	Susua	Kab.	Nias Selatan	Sumatera Utara	,\
    633	:	22873	Sisobahili	Susua	Kab.	Nias Selatan	Sumatera Utara	,\
    634	:	20351	Helvetia	Sunggal	Kab.	Deli Serdang	Sumatera Utara	,\
    635	:	20351	Kampung Lalang	Sunggal	Kab.	Deli Serdang	Sumatera Utara	,\
    636	:	20351	Medan Krio	Sunggal	Kab.	Deli Serdang	Sumatera Utara	,\
    637	:	20351	Mulyo Rejo	Sunggal	Kab.	Deli Serdang	Sumatera Utara	,\
    638	:	20351	Paya Geli	Sunggal	Kab.	Deli Serdang	Sumatera Utara	,\
    639	:	20351	Puji Mulyo	Sunggal	Kab.	Deli Serdang	Sumatera Utara	,\
    640	:	20351	Purwodadi	Sunggal	Kab.	Deli Serdang	Sumatera Utara	,\
    641	:	20351	Sei Beras Sekata	Sunggal	Kab.	Deli Serdang	Sumatera Utara	,\
    642	:	20351	Sei Mencirim	Sunggal	Kab.	Deli Serdang	Sumatera Utara	,\
    643	:	20351	Sei Semayang	Sunggal	Kab.	Deli Serdang	Sumatera Utara	,\
    644	:	20351	Sm Diski	Sunggal	Kab.	Deli Serdang	Sumatera Utara	,\
    645	:	20351	Suka Maju	Sunggal	Kab.	Deli Serdang	Sumatera Utara	,\
    646	:	20351	Sukajadi (Serba Jadi)	Sunggal	Kab.	Deli Serdang	Sumatera Utara	,\
    647	:	20351	Tanjung Gusta	Sunggal	Kab.	Deli Serdang	Sumatera Utara	,\
    648	:	20351	Tanjung Selamat	Sunggal	Kab.	Deli Serdang	Sumatera Utara	,\
    649	:	20351	Telaga Sari	Sunggal	Kab.	Deli Serdang	Sumatera Utara	,\
    650	:	20351	Tunggal Kanan (Sungal Kanan)	Sunggal	Kab.	Deli Serdang	Sumatera Utara	,\
    651	:	22281	Dolok Tolong	Sumbul	Kab.	Dairi	Sumatera Utara	,\
    652	:	22281	Kuta Gugung	Sumbul	Kab.	Dairi	Sumatera Utara	,\
    653	:	22281	Pargambiran	Sumbul	Kab.	Dairi	Sumatera Utara	,\
    654	:	22281	Pegagan Julu I	Sumbul	Kab.	Dairi	Sumatera Utara	,\
    655	:	22281	Pegagan Julu II	Sumbul	Kab.	Dairi	Sumatera Utara	,\
    656	:	22281	Pegagan Julu III	Sumbul	Kab.	Dairi	Sumatera Utara	,\
    657	:	22281	Pegagan Julu IV	Sumbul	Kab.	Dairi	Sumatera Utara	,\
    658	:	22281	Pegagan Julu IX	Sumbul	Kab.	Dairi	Sumatera Utara	,\
    659	:	22281	Pegagan Julu V	Sumbul	Kab.	Dairi	Sumatera Utara	,\
    660	:	22281	Pegagan Julu VI	Sumbul	Kab.	Dairi	Sumatera Utara	,\
    661	:	22281	Pegagan Julu VII	Sumbul	Kab.	Dairi	Sumatera Utara	,\
    662	:	22281	Pegagan Julu VIII	Sumbul	Kab.	Dairi	Sumatera Utara	,\
    663	:	22281	Pegagan Julu X	Sumbul	Kab.	Dairi	Sumatera Utara	,\
    664	:	22281	Perjuangan	Sumbul	Kab.	Dairi	Sumatera Utara	,\
    665	:	22281	Tanjung Beringin	Sumbul	Kab.	Dairi	Sumatera Utara	,\
    666	:	22654	Janji Maria	Suka Bangun	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    667	:	22654	Pulo Pakkat I	Suka Bangun	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    668	:	22654	Pulo Pakkat II	Suka Bangun	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    669	:	22654	Sihadatuon	Suka Bangun	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    670	:	22654	Sihapas	Suka Bangun	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    671	:	22654	Tebing Tinggi	Suka Bangun	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    672	:	20811	Ara Condong	Stabat	Kab.	Langkat	Sumatera Utara	,\
    673	:	20811	Banyumas	Stabat	Kab.	Langkat	Sumatera Utara	,\
    674	:	20811	Dendang	Stabat	Kab.	Langkat	Sumatera Utara	,\
    675	:	20811	Karang Rejo	Stabat	Kab.	Langkat	Sumatera Utara	,\
    676	:	20811	Kwala Begumit	Stabat	Kab.	Langkat	Sumatera Utara	,\
    677	:	20811	Kwala Bingai	Stabat	Kab.	Langkat	Sumatera Utara	,\
    678	:	20811	Mangga	Stabat	Kab.	Langkat	Sumatera Utara	,\
    679	:	20812	Pantai Gemi	Stabat	Kab.	Langkat	Sumatera Utara	,\
    680	:	20816	Paya Mabar	Stabat	Kab.	Langkat	Sumatera Utara	,\
    681	:	20815	Perdamaian	Stabat	Kab.	Langkat	Sumatera Utara	,\
    682	:	20813	Sido Mulyo	Stabat	Kab.	Langkat	Sumatera Utara	,\
    683	:	20811	Stabat Baru	Stabat	Kab.	Langkat	Sumatera Utara	,\
    684	:	22564	Barambang	Sosor Gadong	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    685	:	22564	Baringin	Sosor Gadong	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    686	:	22564	Huta Tombak	Sosor Gadong	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    687	:	22564	Muara Bolak	Sosor Gadong	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    688	:	22564	Siantar Ca	Sosor Gadong	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    689	:	22564	Siantar Dolok	Sosor Gadong	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    690	:	22564	Sibintang	Sosor Gadong	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    691	:	22564	Sosor Gadong	Sosor Gadong	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    692	:	22564	Unte Boang	Sosor Gadong	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    693	:	22762	Aek Bargot	Sosopan	Kab.	Padang Lawas	Sumatera Utara	,\
    694	:	22762	Banua Tonga	Sosopan	Kab.	Padang Lawas	Sumatera Utara	,\
    695	:	22762	Binanga Tolu	Sosopan	Kab.	Padang Lawas	Sumatera Utara	,\
    696	:	22762	Hulim	Sosopan	Kab.	Padang Lawas	Sumatera Utara	,\
    697	:	22762	Huta Bara	Sosopan	Kab.	Padang Lawas	Sumatera Utara	,\
    698	:	22762	Huta Bargot	Sosopan	Kab.	Padang Lawas	Sumatera Utara	,\
    699	:	22762	Huta Baru Siundol	Sosopan	Kab.	Padang Lawas	Sumatera Utara	,\
    700	:	22762	Huta Baru Sosopan	Sosopan	Kab.	Padang Lawas	Sumatera Utara	,\
    701	:	22762	Pagaran Bira Jae	Sosopan	Kab.	Padang Lawas	Sumatera Utara	,\
    702	:	22762	Pagaran Bira Julu	Sosopan	Kab.	Padang Lawas	Sumatera Utara	,\
    703	:	22762	Sianggunan	Sosopan	Kab.	Padang Lawas	Sumatera Utara	,\
    704	:	22762	Sibual-Buali	Sosopan	Kab.	Padang Lawas	Sumatera Utara	,\
    705	:	22762	Sigala Gala	Sosopan	Kab.	Padang Lawas	Sumatera Utara	,\
    706	:	22762	Sihaporas	Sosopan	Kab.	Padang Lawas	Sumatera Utara	,\
    707	:	22762	Simaninggir Sosopan	Sosopan	Kab.	Padang Lawas	Sumatera Utara	,\
    708	:	22762	Simartolu	Sosopan	Kab.	Padang Lawas	Sumatera Utara	,\
    709	:	22762	Siundol Dolok	Sosopan	Kab.	Padang Lawas	Sumatera Utara	,\
    710	:	22762	Siundol Jae	Sosopan	Kab.	Padang Lawas	Sumatera Utara	,\
    711	:	22762	Siundol Julu	Sosopan	Kab.	Padang Lawas	Sumatera Utara	,\
    712	:	22762	Sosopan	Sosopan	Kab.	Padang Lawas	Sumatera Utara	,\
    713	:	22762	Sosopan Julu	Sosopan	Kab.	Padang Lawas	Sumatera Utara	,\
    714	:	22762	Ulu Aer	Sosopan	Kab.	Padang Lawas	Sumatera Utara	,\
    715	:	22765	Aek Tinga	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    716	:	22765	Aer Bale	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    717	:	22765	Ampolu	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    718	:	22765	Batu Gajah	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    719	:	22765	Bonan Dolok	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    720	:	22765	Gunung Baringin	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    721	:	22765	Gunung Tua	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    722	:	22765	Handio	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    723	:	22765	Hapung	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    724	:	22765	Hapung Torop	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    725	:	22765	Harang Jae	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    726	:	22765	Harang Julu	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    727	:	22765	Horuan	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    728	:	22765	Hurung Jilok	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    729	:	22765	Huta Imbaru	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    730	:	22765	Huta Raja Lama	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    731	:	22765	Janji Raja	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    732	:	22765	Lumban Huayan	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    733	:	22765	Mananti Sosa Julu	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    734	:	22765	Mandian	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    735	:	22765	Mondang	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    736	:	22765	Parapat	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    737	:	22765	Parau Sorat	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    738	:	22765	Pasar Ujung Batu	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    739	:	22765	Pasir Jae	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    740	:	22765	Pasir Julu	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    741	:	22765	Plasma Mondang (Trans Sosa IV)	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    742	:	22765	Ramba	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    743	:	22765	Rao Rao Dolok	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    744	:	22765	Roburan	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    745	:	22765	Siborna Bunut	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    746	:	22765	Siginduang	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    747	:	22765	Simarancar	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    748	:	22765	Sisoma	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    749	:	22765	Sungai Jior	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    750	:	22765	Tanjung	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    751	:	22765	Tanjung Bale	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    752	:	22765	Tanjung Botung Sosa Jae	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    753	:	22765	Ujung Batu	Sosa	Kab.	Padang Lawas	Sumatera Utara	,\
    754	:	22563	Aek Raso	Sorkam Barat	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    755	:	22563	Binasi	Sorkam Barat	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    756	:	22563	Maduma	Sorkam Barat	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    757	:	22563	Pahieme	Sorkam Barat	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    758	:	22563	Pahieme II	Sorkam Barat	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    759	:	22563	Pasar Sorkam	Sorkam Barat	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    760	:	22563	Pasaribu Tobing Jae	Sorkam Barat	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    761	:	22563	Sidikalang	Sorkam Barat	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    762	:	22563	Sipea Pea	Sorkam Barat	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    763	:	22563	Sorkam Kanan	Sorkam Barat	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    764	:	22563	Sorkam Kanan 2	Sorkam Barat	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    765	:	22563	Botot	Sorkam	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    766	:	22563	Dolok Pantis	Sorkam	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    767	:	22563	Fajar	Sorkam	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    768	:	22563	Gonting Mahe	Sorkam	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    769	:	22563	Nai Pos Pos Barat	Sorkam	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    770	:	22563	Pardamean	Sorkam	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    771	:	22563	Pargaringan	Sorkam	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    772	:	22563	Pargarutan	Sorkam	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    773	:	22563	Pearaja	Sorkam	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    774	:	22563	Pelita	Sorkam	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    775	:	22563	Rianiate	Sorkam	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    776	:	22563	Simarpinggan	Sorkam	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    777	:	22563	Sorkam	Sorkam	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    778	:	22563	Tarutung Bolak	Sorkam	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    779	:	22563	Teluk Roban	Sorkam	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    780	:	22871	Hiliborodano	Somolo-Molo (Samolo)	Kab.	Nias	Sumatera Utara	,\
    781	:	22871	Hiligodu Somolo-Molo	Somolo-Molo (Samolo)	Kab.	Nias	Sumatera Utara	,\
    782	:	22871	Huno (Hino)	Somolo-Molo (Samolo)	Kab.	Nias	Sumatera Utara	,\
    783	:	22871	Iodano	Somolo-Molo (Samolo)	Kab.	Nias	Sumatera Utara	,\
    784	:	22871	Lewuoguru I	Somolo-Molo (Samolo)	Kab.	Nias	Sumatera Utara	,\
    785	:	22871	Lewuombanua	Somolo-Molo (Samolo)	Kab.	Nias	Sumatera Utara	,\
    786	:	22871	Sifaoroasi	Somolo-Molo (Samolo)	Kab.	Nias	Sumatera Utara	,\
    787	:	22871	Sisaratandrawa	Somolo-Molo (Samolo)	Kab.	Nias	Sumatera Utara	,\
    788	:	22871	Sisobawino I	Somolo-Molo (Samolo)	Kab.	Nias	Sumatera Utara	,\
    789	:	22871	So`ewali	Somolo-Molo (Samolo)	Kab.	Nias	Sumatera Utara	,\
    790	:	22871	Somolo-Molo	Somolo-Molo (Samolo)	Kab.	Nias	Sumatera Utara	,\
    791	:	22874	Fanedanu	Somambawa	Kab.	Nias Selatan	Sumatera Utara	,\
    792	:	22874	Gabungan Tasua	Somambawa	Kab.	Nias Selatan	Sumatera Utara	,\
    793	:	22874	Golambanua II	Somambawa	Kab.	Nias Selatan	Sumatera Utara	,\
    794	:	22874	Hilialawa	Somambawa	Kab.	Nias Selatan	Sumatera Utara	,\
    795	:	22874	Hiliorahua Tasua	Somambawa	Kab.	Nias Selatan	Sumatera Utara	,\
    796	:	22874	Mehaga	Somambawa	Kab.	Nias Selatan	Sumatera Utara	,\
    797	:	22874	Oladano	Somambawa	Kab.	Nias Selatan	Sumatera Utara	,\
    798	:	22874	Sifitubanua	Somambawa	Kab.	Nias Selatan	Sumatera Utara	,\
    799	:	22874	Sihareo	Somambawa	Kab.	Nias Selatan	Sumatera Utara	,\
    800	:	22874	Silimabanua Somambawa	Somambawa	Kab.	Nias Selatan	Sumatera Utara	,\
    801	:	22874	Sinar Susua	Somambawa	Kab.	Nias Selatan	Sumatera Utara	,\
    802	:	22874	Sitolu Banua	Somambawa	Kab.	Nias Selatan	Sumatera Utara	,\
    803	:	22874	Siwalubanua	Somambawa	Kab.	Nias Selatan	Sumatera Utara	,\
    804	:	22874	Somambawa	Somambawa	Kab.	Nias Selatan	Sumatera Utara	,\
    805	:	22871	Baruzo	Sogae Adu (Sogaeadu)	Kab.	Nias	Sumatera Utara	,\
    806	:	22871	Hilibadalu	Sogae Adu (Sogaeadu)	Kab.	Nias	Sumatera Utara	,\
    807	:	22871	Hilimbana	Sogae Adu (Sogaeadu)	Kab.	Nias	Sumatera Utara	,\
    808	:	22871	Lauri	Sogae Adu (Sogaeadu)	Kab.	Nias	Sumatera Utara	,\
    809	:	22871	Saitagaramba (Saetagaramba)	Sogae Adu (Sogaeadu)	Kab.	Nias	Sumatera Utara	,\
    810	:	22871	Sihareo Sogaeadu	Sogae Adu (Sogaeadu)	Kab.	Nias	Sumatera Utara	,\
    811	:	22871	Sisarahili Sogeadu	Sogae Adu (Sogaeadu)	Kab.	Nias	Sumatera Utara	,\
    812	:	22871	Sogaeadu	Sogae Adu (Sogaeadu)	Kab.	Nias	Sumatera Utara	,\
    813	:	22871	Tuhembuasi	Sogae Adu (Sogaeadu)	Kab.	Nias	Sumatera Utara	,\
    814	:	22871	Tulumbaho	Sogae Adu (Sogaeadu)	Kab.	Nias	Sumatera Utara	,\
    815	:	22871	Wea-Wea	Sogae Adu (Sogaeadu)	Kab.	Nias	Sumatera Utara	,\
    816	:	22852	Batom Bawo	Sitolu Ori	Kab.	Nias Utara	Sumatera Utara	,\
    817	:	22852	Fulolo Saloo	Sitolu Ori	Kab.	Nias Utara	Sumatera Utara	,\
    818	:	22852	Hilimbosi	Sitolu Ori	Kab.	Nias Utara	Sumatera Utara	,\
    819	:	22852	Hilisaloo	Sitolu Ori	Kab.	Nias Utara	Sumatera Utara	,\
    820	:	22852	Tetehosi Maziaya	Sitolu Ori	Kab.	Nias Utara	Sumatera Utara	,\
    821	:	22852	Umbubalodano	Sitolu Ori	Kab.	Nias Utara	Sumatera Utara	,\
    822	:	22395	Buntu Mauli	Sitio-Tio	Kab.	Samosir	Sumatera Utara	,\
    823	:	22395	Cinta Maju	Sitio-Tio	Kab.	Samosir	Sumatera Utara	,\
    824	:	22395	Holbung	Sitio-Tio	Kab.	Samosir	Sumatera Utara	,\
    825	:	22395	Janji Raja	Sitio-Tio	Kab.	Samosir	Sumatera Utara	,\
    826	:	22395	Sabulan	Sitio-Tio	Kab.	Samosir	Sumatera Utara	,\
    827	:	22395	Tamba Dolok	Sitio-Tio	Kab.	Samosir	Sumatera Utara	,\
    828	:	22219	Panji Dabutar (Bako)	Sitinjo	Kab.	Dairi	Sumatera Utara	,\
    829	:	22219	Sitinjo	Sitinjo	Kab.	Dairi	Sumatera Utara	,\
    830	:	22219	Sitinjo I	Sitinjo	Kab.	Dairi	Sumatera Utara	,\
    831	:	22219	Sitinjo II	Sitinjo	Kab.	Dairi	Sumatera Utara	,\
    832	:	22272	Cikaok	Sitellu Tali Urang Julu	Kab.	Pakpak Bharat	Sumatera Utara	,\
    833	:	22272	Lae Langge Namuseng	Sitellu Tali Urang Julu	Kab.	Pakpak Bharat	Sumatera Utara	,\
    834	:	22272	Pardomuan	Sitellu Tali Urang Julu	Kab.	Pakpak Bharat	Sumatera Utara	,\
    835	:	22272	Silima Kuta	Sitellu Tali Urang Julu	Kab.	Pakpak Bharat	Sumatera Utara	,\
    836	:	22272	Ulu Merah	Sitellu Tali Urang Julu	Kab.	Pakpak Bharat	Sumatera Utara	,\
    837	:	22272	Bandar Baru	Sitellu Tali Urang Jehe	Kab.	Pakpak Bharat	Sumatera Utara	,\
    838	:	22272	Kaban Tengah	Sitellu Tali Urang Jehe	Kab.	Pakpak Bharat	Sumatera Utara	,\
    839	:	22272	Maholida	Sitellu Tali Urang Jehe	Kab.	Pakpak Bharat	Sumatera Utara	,\
    840	:	22272	Malum	Sitellu Tali Urang Jehe	Kab.	Pakpak Bharat	Sumatera Utara	,\
    841	:	22272	Mbinalun	Sitellu Tali Urang Jehe	Kab.	Pakpak Bharat	Sumatera Utara	,\
    842	:	22272	Perjaga	Sitellu Tali Urang Jehe	Kab.	Pakpak Bharat	Sumatera Utara	,\
    843	:	22272	Perolihen	Sitellu Tali Urang Jehe	Kab.	Pakpak Bharat	Sumatera Utara	,\
    844	:	22272	Simberuna	Sitellu Tali Urang Jehe	Kab.	Pakpak Bharat	Sumatera Utara	,\
    845	:	22272	Tanjung Meriah	Sitellu Tali Urang Jehe	Kab.	Pakpak Bharat	Sumatera Utara	,\
    846	:	22272	Tanjung Mulia	Sitellu Tali Urang Jehe	Kab.	Pakpak Bharat	Sumatera Utara	,\
    847	:	22611	Bonandolok	Sitahuis	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    848	:	22611	Mardame	Sitahuis	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    849	:	22611	Naga Timbul	Sitahuis	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    850	:	22611	Nauli	Sitahuis	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    851	:	22611	Rampa	Sitahuis	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    852	:	22611	Simaninggir	Sitahuis	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    853	:	22863	Balowondrate	Sirombu	Kab.	Nias Barat	Sumatera Utara	,\
    854	:	22863	Bawasawa	Sirombu	Kab.	Nias Barat	Sumatera Utara	,\
    855	:	22863	Bawosaloo	Sirombu	Kab.	Nias Barat	Sumatera Utara	,\
    856	:	22863	Fadoro	Sirombu	Kab.	Nias Barat	Sumatera Utara	,\
    857	:	22863	Gunung Cahaya	Sirombu	Kab.	Nias Barat	Sumatera Utara	,\
    858	:	22863	Halamona	Sirombu	Kab.	Nias Barat	Sumatera Utara	,\
    859	:	22863	Hanofa	Sirombu	Kab.	Nias Barat	Sumatera Utara	,\
    860	:	22863	Hilimberua	Sirombu	Kab.	Nias Barat	Sumatera Utara	,\
    861	:	22863	Hinako	Sirombu	Kab.	Nias Barat	Sumatera Utara	,\
    862	:	22863	Imana	Sirombu	Kab.	Nias Barat	Sumatera Utara	,\
    863	:	22863	Kafo Kafo	Sirombu	Kab.	Nias Barat	Sumatera Utara	,\
    864	:	22863	Lahawa	Sirombu	Kab.	Nias Barat	Sumatera Utara	,\
    865	:	22863	Lahusa	Sirombu	Kab.	Nias Barat	Sumatera Utara	,\
    866	:	22863	Ombolata	Sirombu	Kab.	Nias Barat	Sumatera Utara	,\
    867	:	22863	Orahili	Sirombu	Kab.	Nias Barat	Sumatera Utara	,\
    868	:	22863	Pulau Bogi	Sirombu	Kab.	Nias Barat	Sumatera Utara	,\
    869	:	22863	Sinene Eto	Sirombu	Kab.	Nias Barat	Sumatera Utara	,\
    870	:	22863	Sirombu	Sirombu	Kab.	Nias Barat	Sumatera Utara	,\
    871	:	22863	Sisobandrao	Sirombu	Kab.	Nias Barat	Sumatera Utara	,\
    872	:	22863	Tetehosi	Sirombu	Kab.	Nias Barat	Sumatera Utara	,\
    873	:	22863	Togideu	Sirombu	Kab.	Nias Barat	Sumatera Utara	,\
    874	:	22863	Togim Bogi	Sirombu	Kab.	Nias Barat	Sumatera Utara	,\
    875	:	22863	Tugala	Sirombu	Kab.	Nias Barat	Sumatera Utara	,\
    876	:	22863	Tugalagawu	Sirombu	Kab.	Nias Barat	Sumatera Utara	,\
    877	:	22863	Tuwa Tuwa	Sirombu	Kab.	Nias Barat	Sumatera Utara	,\
    878	:	20772	Aman Damai/Dame	Sirapit (Serapit)	Kab.	Langkat	Sumatera Utara	,\
    879	:	20773	Gunung Tinggi	Sirapit (Serapit)	Kab.	Langkat	Sumatera Utara	,\
    880	:	20774	Perkebunan Amaltani	Sirapit (Serapit)	Kab.	Langkat	Sumatera Utara	,\
    881	:	20773	Pulau Semikat	Sirapit (Serapit)	Kab.	Langkat	Sumatera Utara	,\
    882	:	20774	Sebertung	Sirapit (Serapit)	Kab.	Langkat	Sumatera Utara	,\
    883	:	20773	Serapit	Sirapit (Serapit)	Kab.	Langkat	Sumatera Utara	,\
    884	:	20773	Sidorejo	Sirapit (Serapit)	Kab.	Langkat	Sumatera Utara	,\
    885	:	20772	Suka Pulung	Sirapit (Serapit)	Kab.	Langkat	Sumatera Utara	,\
    886	:	20774	Sumber Jaya	Sirapit (Serapit)	Kab.	Langkat	Sumatera Utara	,\
    887	:	20772	Tanjung Keriahan/Keriahen	Sirapit (Serapit)	Kab.	Langkat	Sumatera Utara	,\
    888	:	22565	Bajamas	Sirandorung	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    889	:	22565	Masnauli	Sirandorung	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    890	:	22565	Muara Ore	Sirandorung	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    891	:	22565	Pardomuan	Sirandorung	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    892	:	22565	Sampang Maruhur	Sirandorung	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    893	:	22565	Sigodung	Sirandorung	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    894	:	22565	Simpang Tiga Lae Bingke	Sirandorung	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    895	:	22565	Siordang	Sirandorung	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    896	:	22452	Huta Raja	Sipoholon	Kab.	Tapanuli Utara	Sumatera Utara	,\
    897	:	22452	Huta Raja Hasundutan	Sipoholon	Kab.	Tapanuli Utara	Sumatera Utara	,\
    898	:	22452	Hutauruk	Sipoholon	Kab.	Tapanuli Utara	Sumatera Utara	,\
    899	:	22452	Hutauruk Hasundutan (Hutaraja Simanungkalit)	Sipoholon	Kab.	Tapanuli Utara	Sumatera Utara	,\
    900	:	22452	Lobusingkam	Sipoholon	Kab.	Tapanuli Utara	Sumatera Utara	,\
    901	:	22452	Pagar Batu	Sipoholon	Kab.	Tapanuli Utara	Sumatera Utara	,\
    902	:	22452	Rura Julu Dolok	Sipoholon	Kab.	Tapanuli Utara	Sumatera Utara	,\
    903	:	22452	Rura Julu Toruan	Sipoholon	Kab.	Tapanuli Utara	Sumatera Utara	,\
    904	:	22452	Simanungkalit	Sipoholon	Kab.	Tapanuli Utara	Sumatera Utara	,\
    905	:	22452	Sipahutar	Sipoholon	Kab.	Tapanuli Utara	Sumatera Utara	,\
    906	:	22452	Sipoholon	Sipoholon	Kab.	Tapanuli Utara	Sumatera Utara	,\
    907	:	22452	Situmeang Habinsaran	Sipoholon	Kab.	Tapanuli Utara	Sumatera Utara	,\
    908	:	22452	Situmeang Hasundutan	Sipoholon	Kab.	Tapanuli Utara	Sumatera Utara	,\
    909	:	22452	Tapian Nauli	Sipoholon	Kab.	Tapanuli Utara	Sumatera Utara	,\
    910	:	20992	Baja Dolok	Sipispis	Kab.	Serdang Bedagai	Sumatera Utara	,\
    911	:	20992	Bartong	Sipispis	Kab.	Serdang Bedagai	Sumatera Utara	,\
    912	:	20992	Buluh Duri	Sipispis	Kab.	Serdang Bedagai	Sumatera Utara	,\
    913	:	20992	Damak Kurat	Sipispis	Kab.	Serdang Bedagai	Sumatera Utara	,\
    914	:	20992	Gunung Manako	Sipispis	Kab.	Serdang Bedagai	Sumatera Utara	,\
    915	:	20992	Gunung Pane	Sipispis	Kab.	Serdang Bedagai	Sumatera Utara	,\
    916	:	20992	Mariah Nagur	Sipispis	Kab.	Serdang Bedagai	Sumatera Utara	,\
    917	:	20992	Marjanji	Sipispis	Kab.	Serdang Bedagai	Sumatera Utara	,\
    918	:	20992	Marubun	Sipispis	Kab.	Serdang Bedagai	Sumatera Utara	,\
    919	:	20992	Naga Raja	Sipispis	Kab.	Serdang Bedagai	Sumatera Utara	,\
    920	:	20992	Nagur Pane	Sipispis	Kab.	Serdang Bedagai	Sumatera Utara	,\
    921	:	20992	Parlambean	Sipispis	Kab.	Serdang Bedagai	Sumatera Utara	,\
    922	:	20992	Pispis	Sipispis	Kab.	Serdang Bedagai	Sumatera Utara	,\
    923	:	20992	Rimbun	Sipispis	Kab.	Serdang Bedagai	Sumatera Utara	,\
    924	:	20992	Serbananti	Sipispis	Kab.	Serdang Bedagai	Sumatera Utara	,\
    925	:	20992	Sibarau (Sibangu)	Sipispis	Kab.	Serdang Bedagai	Sumatera Utara	,\
    926	:	20992	Silau Padang	Sipispis	Kab.	Serdang Bedagai	Sumatera Utara	,\
    927	:	20992	Simalas	Sipispis	Kab.	Serdang Bedagai	Sumatera Utara	,\
    928	:	20992	Sipispis	Sipispis	Kab.	Serdang Bedagai	Sumatera Utara	,\
    929	:	20992	Tinokkah	Sipispis	Kab.	Serdang Bedagai	Sumatera Utara	,\
    930	:	22742	Aek Batang Paya	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    931	:	22742	Bagas Lombang	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    932	:	22742	Bagas Nagodang III	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    933	:	22742	Baringin	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    934	:	22742	Barnang/Barnag Koling	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    935	:	22742	Batang Tura	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    936	:	22742	Batang Tura Julu	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    937	:	22742	Batu Satail	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    938	:	22742	Bulu Mario	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    939	:	22742	Bunga Bondar	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    940	:	22742	Dolok Sordang	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    941	:	22742	Dolok Sordang Julu	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    942	:	22742	Gadu	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    943	:	22742	Hasang Marsada	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    944	:	22742	Huta Suhut I	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    945	:	22742	Janji Mauli	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    946	:	22742	Kilang Papan	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    947	:	22742	Luat Lombang	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    948	:	22742	Marsada	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    949	:	22742	Padang Bujur	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    950	:	22742	Pahae Aek Sagala	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    951	:	22742	Panaungan	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    952	:	22742	Pangaribuan	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    953	:	22742	Pangurabaan	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    954	:	22742	Paran Dolok Mardomu	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    955	:	22742	Paran Julu	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    956	:	22742	Paran Padang	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    957	:	22742	Parau Sorat	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    958	:	22742	Pargarutan	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    959	:	22742	Pasar Sipirok	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    960	:	22742	Ramba Sihosur	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    961	:	22742	Saba Batang Miha	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    962	:	22742	Sampean	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    963	:	22742	Sarogodung	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    964	:	22742	Siala Gundi	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    965	:	22742	Sialaman	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    966	:	22742	Sibadoar	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    967	:	22742	Simaninggir	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    968	:	22742	Sipirok Godang	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    969	:	22742	Situmba	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    970	:	22742	Situmba Julu	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    971	:	22742	Somba Tolang	Sipirok	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    972	:	22471	Aek Nauli I	Sipahutar	Kab.	Tapanuli Utara	Sumatera Utara	,\
    973	:	22471	Aek Nauli II	Sipahutar	Kab.	Tapanuli Utara	Sumatera Utara	,\
    974	:	22471	Aek Nauli III	Sipahutar	Kab.	Tapanuli Utara	Sumatera Utara	,\
    975	:	22471	Aek Nauli IV	Sipahutar	Kab.	Tapanuli Utara	Sumatera Utara	,\
    976	:	22471	Onan Runggu I	Sipahutar	Kab.	Tapanuli Utara	Sumatera Utara	,\
    977	:	22471	Onan Runggu II	Sipahutar	Kab.	Tapanuli Utara	Sumatera Utara	,\
    978	:	22471	Onan Runggu III	Sipahutar	Kab.	Tapanuli Utara	Sumatera Utara	,\
    979	:	22471	Onan Runggu IV	Sipahutar	Kab.	Tapanuli Utara	Sumatera Utara	,\
    980	:	22471	Sabungan Nihuta I	Sipahutar	Kab.	Tapanuli Utara	Sumatera Utara	,\
    981	:	22471	Sabungan Nihuta II	Sipahutar	Kab.	Tapanuli Utara	Sumatera Utara	,\
    982	:	22471	Sabungan Nihuta III	Sipahutar	Kab.	Tapanuli Utara	Sumatera Utara	,\
    983	:	22471	Sabungan Nihuta IV	Sipahutar	Kab.	Tapanuli Utara	Sumatera Utara	,\
    984	:	22471	Sabungan Nihuta V	Sipahutar	Kab.	Tapanuli Utara	Sumatera Utara	,\
    985	:	22471	Siabal Abal I	Sipahutar	Kab.	Tapanuli Utara	Sumatera Utara	,\
    986	:	22471	Siabal Abal II	Sipahutar	Kab.	Tapanuli Utara	Sumatera Utara	,\
    987	:	22471	Siabal Abal III	Sipahutar	Kab.	Tapanuli Utara	Sumatera Utara	,\
    988	:	22471	Siabal Abal IV	Sipahutar	Kab.	Tapanuli Utara	Sumatera Utara	,\
    989	:	22471	Sipahutar I	Sipahutar	Kab.	Tapanuli Utara	Sumatera Utara	,\
    990	:	22471	Sipahutar II	Sipahutar	Kab.	Tapanuli Utara	Sumatera Utara	,\
    991	:	22471	Sipahutar III	Sipahutar	Kab.	Tapanuli Utara	Sumatera Utara	,\
    992	:	22471	Tapian Nauli I	Sipahutar	Kab.	Tapanuli Utara	Sumatera Utara	,\
    993	:	22471	Tapian Nauli II	Sipahutar	Kab.	Tapanuli Utara	Sumatera Utara	,\
    994	:	22471	Tapian Nauli III	Sipahutar	Kab.	Tapanuli Utara	Sumatera Utara	,\
    995	:	22988	Airapa	Sinunukan	Kab.	Mandailing Natal	Sumatera Utara	,\
    996	:	22988	Banjar Aur Utara	Sinunukan	Kab.	Mandailing Natal	Sumatera Utara	,\
    997	:	22988	Bintungan Bejangkar Baru	Sinunukan	Kab.	Mandailing Natal	Sumatera Utara	,\
    998	:	22988	Kampung Kapas II	Sinunukan	Kab.	Mandailing Natal	Sumatera Utara	,\
    999	:	22988	Sinunukan I	Sinunukan	Kab.	Mandailing Natal	Sumatera Utara	,\
    1000	:	22988	Sinunukan II	Sinunukan	Kab.	Mandailing Natal	Sumatera Utara	,\
    1001	:	22988	Sinunukan III	Sinunukan	Kab.	Mandailing Natal	Sumatera Utara	,\
    1002	:	22988	Sinunukan IV	Sinunukan	Kab.	Mandailing Natal	Sumatera Utara	,\
    1003	:	20582	Bah Bah Buntu	Sinembah Tanjung Muda Hulu	Kab.	Deli Serdang	Sumatera Utara	,\
    1004	:	20582	Durian Empat Mbelang	Sinembah Tanjung Muda Hulu	Kab.	Deli Serdang	Sumatera Utara	,\
    1005	:	20582	Durin Tinggung	Sinembah Tanjung Muda Hulu	Kab.	Deli Serdang	Sumatera Utara	,\
    1006	:	20582	Gunung Manumpak A	Sinembah Tanjung Muda Hulu	Kab.	Deli Serdang	Sumatera Utara	,\
    1007	:	20582	Gunung Manumpak B	Sinembah Tanjung Muda Hulu	Kab.	Deli Serdang	Sumatera Utara	,\
    1008	:	20582	Kuta Mbelin	Sinembah Tanjung Muda Hulu	Kab.	Deli Serdang	Sumatera Utara	,\
    1009	:	20582	Liang Muda	Sinembah Tanjung Muda Hulu	Kab.	Deli Serdang	Sumatera Utara	,\
    1010	:	20582	Liang Pematang	Sinembah Tanjung Muda Hulu	Kab.	Deli Serdang	Sumatera Utara	,\
    1011	:	20582	Ranggitgit	Sinembah Tanjung Muda Hulu	Kab.	Deli Serdang	Sumatera Utara	,\
    1012	:	20582	Rumah Lengo	Sinembah Tanjung Muda Hulu	Kab.	Deli Serdang	Sumatera Utara	,\
    1013	:	20582	Rumah Rih	Sinembah Tanjung Muda Hulu	Kab.	Deli Serdang	Sumatera Utara	,\
    1014	:	20582	Rumah Sumbul	Sinembah Tanjung Muda Hulu	Kab.	Deli Serdang	Sumatera Utara	,\
    1015	:	20582	Sibunga-Bunga Hilir	Sinembah Tanjung Muda Hulu	Kab.	Deli Serdang	Sumatera Utara	,\
    1016	:	20582	Sipinggan	Sinembah Tanjung Muda Hulu	Kab.	Deli Serdang	Sumatera Utara	,\
    1017	:	20582	Tanah Gara Hulu	Sinembah Tanjung Muda Hulu	Kab.	Deli Serdang	Sumatera Utara	,\
    1018	:	20582	Tanjung Bangku (Bampu)	Sinembah Tanjung Muda Hulu	Kab.	Deli Serdang	Sumatera Utara	,\
    1019	:	20582	Tanjung Muda	Sinembah Tanjung Muda Hulu	Kab.	Deli Serdang	Sumatera Utara	,\
    1020	:	20582	Tanjung Raja	Sinembah Tanjung Muda Hulu	Kab.	Deli Serdang	Sumatera Utara	,\
    1021	:	20582	Tanjung Timur	Sinembah Tanjung Muda Hulu	Kab.	Deli Serdang	Sumatera Utara	,\
    1022	:	20582	Tiga Juhar	Sinembah Tanjung Muda Hulu	Kab.	Deli Serdang	Sumatera Utara	,\
    1023	:	20363	Gunung Rintis	Sinembah Tanjung Muda Hilir	Kab.	Deli Serdang	Sumatera Utara	,\
    1024	:	20363	Juma/Jumma Tombak	Sinembah Tanjung Muda Hilir	Kab.	Deli Serdang	Sumatera Utara	,\
    1025	:	20363	Kuta Jurung	Sinembah Tanjung Muda Hilir	Kab.	Deli Serdang	Sumatera Utara	,\
    1026	:	20363	Lau Barus Baru	Sinembah Tanjung Muda Hilir	Kab.	Deli Serdang	Sumatera Utara	,\
    1027	:	20363	Lau Rakit	Sinembah Tanjung Muda Hilir	Kab.	Deli Serdang	Sumatera Utara	,\
    1028	:	20363	Lau Rempah	Sinembah Tanjung Muda Hilir	Kab.	Deli Serdang	Sumatera Utara	,\
    1029	:	20363	Limau Mungkur	Sinembah Tanjung Muda Hilir	Kab.	Deli Serdang	Sumatera Utara	,\
    1030	:	20363	Negara Beringin/Bringin	Sinembah Tanjung Muda Hilir	Kab.	Deli Serdang	Sumatera Utara	,\
    1031	:	20363	Penungkiren	Sinembah Tanjung Muda Hilir	Kab.	Deli Serdang	Sumatera Utara	,\
    1032	:	20363	Rambai	Sinembah Tanjung Muda Hilir	Kab.	Deli Serdang	Sumatera Utara	,\
    1033	:	20363	Siguci	Sinembah Tanjung Muda Hilir	Kab.	Deli Serdang	Sumatera Utara	,\
    1034	:	20363	Sumbul	Sinembah Tanjung Muda Hilir	Kab.	Deli Serdang	Sumatera Utara	,\
    1035	:	20363	Tadukan Raga	Sinembah Tanjung Muda Hilir	Kab.	Deli Serdang	Sumatera Utara	,\
    1036	:	20363	Tala Peta	Sinembah Tanjung Muda Hilir	Kab.	Deli Serdang	Sumatera Utara	,\
    1037	:	20363	Telun Kenas	Sinembah Tanjung Muda Hilir	Kab.	Deli Serdang	Sumatera Utara	,\
    1038	:	22881	Gobo	Simuk	Kab.	Nias Selatan	Sumatera Utara	,\
    1039	:	22881	Gobo Baru	Simuk	Kab.	Nias Selatan	Sumatera Utara	,\
    1040	:	22881	Gondia	Simuk	Kab.	Nias Selatan	Sumatera Utara	,\
    1041	:	22881	Maufa	Simuk	Kab.	Nias Selatan	Sumatera Utara	,\
    1042	:	22881	Silina	Simuk	Kab.	Nias Selatan	Sumatera Utara	,\
    1043	:	22881	Silina Baru	Simuk	Kab.	Nias Selatan	Sumatera Utara	,\
    1044	:	21271	Anjung Gadang	Simpang Empat	Kab.	Asahan	Sumatera Utara	,\
    1045	:	22153	Beganding	Simpang Empat	Kab.	Karo	Sumatera Utara	,\
    1046	:	22153	Berastepu	Simpang Empat	Kab.	Karo	Sumatera Utara	,\
    1047	:	22153	Bulan Baru	Simpang Empat	Kab.	Karo	Sumatera Utara	,\
    1048	:	22153	Gajah	Simpang Empat	Kab.	Karo	Sumatera Utara	,\
    1049	:	22153	Gamber	Simpang Empat	Kab.	Karo	Sumatera Utara	,\
    1050	:	22153	Jeraya	Simpang Empat	Kab.	Karo	Sumatera Utara	,\
    1051	:	22153	Kuta Tengah	Simpang Empat	Kab.	Karo	Sumatera Utara	,\
    1052	:	22153	Lingga	Simpang Empat	Kab.	Karo	Sumatera Utara	,\
    1053	:	22153	Lingga Julu	Simpang Empat	Kab.	Karo	Sumatera Utara	,\
    1054	:	22153	Nang Belawan	Simpang Empat	Kab.	Karo	Sumatera Utara	,\
    1055	:	22153	Ndokum Siroga	Simpang Empat	Kab.	Karo	Sumatera Utara	,\
    1056	:	21271	Perkebunan Hessa	Simpang Empat	Kab.	Asahan	Sumatera Utara	,\
    1057	:	21271	Perkebunan Suka Raja	Simpang Empat	Kab.	Asahan	Sumatera Utara	,\
    1058	:	22153	Perteguhen	Simpang Empat	Kab.	Karo	Sumatera Utara	,\
    1059	:	22153	Pintu Besi	Simpang Empat	Kab.	Karo	Sumatera Utara	,\
    1060	:	21271	Sei Dua Hulu	Simpang Empat	Kab.	Asahan	Sumatera Utara	,\
    1061	:	21271	Sei/Sungai Lama	Simpang Empat	Kab.	Asahan	Sumatera Utara	,\
    1062	:	22153	Serumbia	Simpang Empat	Kab.	Karo	Sumatera Utara	,\
    1063	:	21271	Silomlom	Simpang Empat	Kab.	Asahan	Sumatera Utara	,\
    1064	:	21271	Simpang Empat	Simpang Empat	Kab.	Asahan	Sumatera Utara	,\
    1065	:	21271	Sipaku Area	Simpang Empat	Kab.	Asahan	Sumatera Utara	,\
    1066	:	22153	Surbakti	Simpang Empat	Kab.	Karo	Sumatera Utara	,\
    1067	:	22153	Tiga Pancur	Simpang Empat	Kab.	Karo	Sumatera Utara	,\
    1068	:	22153	Torong	Simpang Empat	Kab.	Karo	Sumatera Utara	,\
    1069	:	22395	Ambarita	Simanindo	Kab.	Samosir	Sumatera Utara	,\
    1070	:	22395	Cinta Dame	Simanindo	Kab.	Samosir	Sumatera Utara	,\
    1071	:	22395	Dosroha	Simanindo	Kab.	Samosir	Sumatera Utara	,\
    1072	:	22395	Garoga	Simanindo	Kab.	Samosir	Sumatera Utara	,\
    1073	:	22395	Huta Ginjang	Simanindo	Kab.	Samosir	Sumatera Utara	,\
    1074	:	22395	Maduma	Simanindo	Kab.	Samosir	Sumatera Utara	,\
    1075	:	22395	Martoba	Simanindo	Kab.	Samosir	Sumatera Utara	,\
    1076	:	22395	Parbalohan	Simanindo	Kab.	Samosir	Sumatera Utara	,\
    1077	:	22395	Pardomuan	Simanindo	Kab.	Samosir	Sumatera Utara	,\
    1078	:	22395	Parmonangan	Simanindo	Kab.	Samosir	Sumatera Utara	,\
    1079	:	22395	Sihusapi	Simanindo	Kab.	Samosir	Sumatera Utara	,\
    1080	:	22395	Simanindo Sangkal	Simanindo	Kab.	Samosir	Sumatera Utara	,\
    1081	:	22395	Simarmata	Simanindo	Kab.	Samosir	Sumatera Utara	,\
    1082	:	22395	Tanjungan	Simanindo	Kab.	Samosir	Sumatera Utara	,\
    1083	:	22395	Tomok	Simanindo	Kab.	Samosir	Sumatera Utara	,\
    1084	:	22395	Tuktuk Siadong	Simanindo	Kab.	Samosir	Sumatera Utara	,\
    1085	:	22466	Aek Nabara	Simangumban	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1086	:	22466	Dolok Sanggul	Simangumban	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1087	:	22466	Dolok Saut	Simangumban	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1088	:	22466	Lobu Sihim	Simangumban	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1089	:	22466	Pardomuan	Simangumban	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1090	:	22466	Silosung	Simangumban	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1091	:	22466	Simangumban Jae	Simangumban	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1092	:	22466	Simangumban Julu	Simangumban	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1093	:	22747	Aek Raru	Simangambat	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1094	:	22747	Gunung Manaon Sim	Simangambat	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1095	:	22747	Gunung Manaon Ub	Simangambat	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1096	:	22747	Huta Baringin	Simangambat	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1097	:	22747	Huta Baru	Simangambat	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1098	:	22747	Huta Pasir	Simangambat	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1099	:	22747	Huta Raja	Simangambat	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1100	:	22747	Jabi-Jabi	Simangambat	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1101	:	22747	Jambu Tonang	Simangambat	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1102	:	22747	Janji Matogu Sim	Simangambat	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1103	:	22747	Kosik Putih	Simangambat	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1104	:	22747	Labuhan Jurung	Simangambat	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1105	:	22747	Langkimat	Simangambat	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1106	:	22747	Mananti	Simangambat	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1107	:	22747	Manare Tua	Simangambat	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1108	:	22747	Mandasip	Simangambat	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1109	:	22747	Marlaung	Simangambat	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1110	:	22747	Martujuan	Simangambat	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1111	:	22747	Paran Padang	Simangambat	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1112	:	22747	Paran Tonga Sim	Simangambat	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1113	:	22747	Pasar Lancat Ub (Pasir Lancat Julu)	Simangambat	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1114	:	22747	Paya Bahung Ub (Lb/An)	Simangambat	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1115	:	22747	Sigagan	Simangambat	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1116	:	22747	Simangambat Jae	Simangambat	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1117	:	22747	Simangambat Julu	Simangambat	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1118	:	22747	Sionggoton	Simangambat	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1119	:	22747	Tanjung Botung	Simangambat	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1120	:	22747	Tanjung Maria	Simangambat	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1121	:	22747	Tobing Tinggi Ub	Simangambat	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1122	:	22747	Ujung Batu Jae	Simangambat	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1123	:	22747	Ujung Batu Julu	Simangambat	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1124	:	22747	Ujung Gading Jae	Simangambat	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1125	:	22747	Ujung Gading Julu	Simangambat	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1126	:	22747	Ulok/Ulak Tano	Simangambat	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1127	:	21157	Bah Sarimah	Silou Kahean	Kab.	Simalungun	Sumatera Utara	,\
    1128	:	21157	Bandar Maruhur	Silou Kahean	Kab.	Simalungun	Sumatera Utara	,\
    1129	:	21157	Bandar Nagori	Silou Kahean	Kab.	Simalungun	Sumatera Utara	,\
    1130	:	21157	Buttu Bayu	Silou Kahean	Kab.	Simalungun	Sumatera Utara	,\
    1131	:	21157	Damaritang	Silou Kahean	Kab.	Simalungun	Sumatera Utara	,\
    1132	:	21157	Dolok Marawa	Silou Kahean	Kab.	Simalungun	Sumatera Utara	,\
    1133	:	21157	Dolok Saribu Bangun	Silou Kahean	Kab.	Simalungun	Sumatera Utara	,\
    1134	:	21157	Mariah Buttu	Silou Kahean	Kab.	Simalungun	Sumatera Utara	,\
    1135	:	21157	Nagori Tani	Silou Kahean	Kab.	Simalungun	Sumatera Utara	,\
    1136	:	21157	Negeri Dolok	Silou Kahean	Kab.	Simalungun	Sumatera Utara	,\
    1137	:	21157	Pardomuan Bandar	Silou Kahean	Kab.	Simalungun	Sumatera Utara	,\
    1138	:	21157	Pardomuan Tongah	Silou Kahean	Kab.	Simalungun	Sumatera Utara	,\
    1139	:	21157	Silau/Silou Dunia	Silou Kahean	Kab.	Simalungun	Sumatera Utara	,\
    1140	:	21157	Silau/Silou Paribuan	Silou Kahean	Kab.	Simalungun	Sumatera Utara	,\
    1141	:	21157	Simanabun	Silou Kahean	Kab.	Simalungun	Sumatera Utara	,\
    1142	:	21157	Sinasih	Silou Kahean	Kab.	Simalungun	Sumatera Utara	,\
    1143	:	20984	Batu Masagi	Silinda	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1144	:	20984	Demak/Damak Gelugur	Silinda	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1145	:	20984	Kulasar	Silinda	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1146	:	20984	Pagar Manik	Silinda	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1147	:	20984	Pamah	Silinda	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1148	:	20984	Silinda	Silinda	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1149	:	20984	Sungai Buaya	Silinda	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1150	:	20984	Tapak Meriah	Silinda	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1151	:	20984	Tarean	Silinda	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1152	:	21167	Bangun Mariah/Meriah	Silimakuta	Kab.	Simalungun	Sumatera Utara	,\
    1153	:	21167	Purba Sinombah	Silimakuta	Kab.	Simalungun	Sumatera Utara	,\
    1154	:	21167	Purba Tua	Silimakuta	Kab.	Simalungun	Sumatera Utara	,\
    1155	:	21167	Purba Tua Baru	Silimakuta	Kab.	Simalungun	Sumatera Utara	,\
    1156	:	21167	Saribu Dolok	Silimakuta	Kab.	Simalungun	Sumatera Utara	,\
    1157	:	21167	Silimakuta	Silimakuta	Kab.	Simalungun	Sumatera Utara	,\
    1158	:	21167	Sinar Baru	Silimakuta	Kab.	Simalungun	Sumatera Utara	,\
    1159	:	22262	Bakal Gajah	Silima Pungga-Pungga	Kab.	Dairi	Sumatera Utara	,\
    1160	:	22262	Bongkaras	Silima Pungga-Pungga	Kab.	Dairi	Sumatera Utara	,\
    1161	:	22262	Bonian	Silima Pungga-Pungga	Kab.	Dairi	Sumatera Utara	,\
    1162	:	22262	Lae Ambat	Silima Pungga-Pungga	Kab.	Dairi	Sumatera Utara	,\
    1163	:	22262	Lae Panginuman	Silima Pungga-Pungga	Kab.	Dairi	Sumatera Utara	,\
    1164	:	22262	Lae Rambong	Silima Pungga-Pungga	Kab.	Dairi	Sumatera Utara	,\
    1165	:	22262	Longkotan	Silima Pungga-Pungga	Kab.	Dairi	Sumatera Utara	,\
    1166	:	22262	Palipi	Silima Pungga-Pungga	Kab.	Dairi	Sumatera Utara	,\
    1167	:	22262	Parongil	Silima Pungga-Pungga	Kab.	Dairi	Sumatera Utara	,\
    1168	:	22262	Polling Anak-Anak	Silima Pungga-Pungga	Kab.	Dairi	Sumatera Utara	,\
    1169	:	22262	Siboras	Silima Pungga-Pungga	Kab.	Dairi	Sumatera Utara	,\
    1170	:	22262	Siratah	Silima Pungga-Pungga	Kab.	Dairi	Sumatera Utara	,\
    1171	:	22262	Sumbari	Silima Pungga-Pungga	Kab.	Dairi	Sumatera Utara	,\
    1172	:	22262	Tungtung Batu	Silima Pungga-Pungga	Kab.	Dairi	Sumatera Utara	,\
    1173	:	22262	Urik Belin	Silima Pungga-Pungga	Kab.	Dairi	Sumatera Utara	,\
    1174	:	21263	Bangun Sari	Silau Laut	Kab.	Asahan	Sumatera Utara	,\
    1175	:	21263	Lubuk Palas	Silau Laut	Kab.	Asahan	Sumatera Utara	,\
    1176	:	21263	Silo Baru	Silau Laut	Kab.	Asahan	Sumatera Utara	,\
    1177	:	21263	Silo Bonto	Silau Laut	Kab.	Asahan	Sumatera Utara	,\
    1178	:	21263	Silo Lama	Silau Laut	Kab.	Asahan	Sumatera Utara	,\
    1179	:	21461	Aek Goti	Silangkitang	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    1180	:	21461	Binanga Dua	Silangkitang	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    1181	:	21461	Mandala Sena	Silangkitang	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    1182	:	21461	Rintis	Silangkitang	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    1183	:	21461	Suka Dame	Silangkitang	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    1184	:	21461	Ulumahuam	Silangkitang	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    1185	:	22281	Paropo	Silahi Sabungan	Kab.	Dairi	Sumatera Utara	,\
    1186	:	22281	Silalahi I	Silahi Sabungan	Kab.	Dairi	Sumatera Utara	,\
    1187	:	22281	Silalahi II	Silahi Sabungan	Kab.	Dairi	Sumatera Utara	,\
    1188	:	22281	Silalahi III	Silahi Sabungan	Kab.	Dairi	Sumatera Utara	,\
    1189	:	22382	Dalihan Natolu	Silaen	Kab.	Toba Samosir	Sumatera Utara	,\
    1190	:	22382	Huta Gurgur I	Silaen	Kab.	Toba Samosir	Sumatera Utara	,\
    1191	:	22382	Huta Gurgur II	Silaen	Kab.	Toba Samosir	Sumatera Utara	,\
    1192	:	22382	Huta Namora	Silaen	Kab.	Toba Samosir	Sumatera Utara	,\
    1193	:	22382	Hutagaol Sihujur	Silaen	Kab.	Toba Samosir	Sumatera Utara	,\
    1194	:	22382	Lumban Dolok	Silaen	Kab.	Toba Samosir	Sumatera Utara	,\
    1195	:	22382	Marbulang	Silaen	Kab.	Toba Samosir	Sumatera Utara	,\
    1196	:	22382	Meranti Barat	Silaen	Kab.	Toba Samosir	Sumatera Utara	,\
    1197	:	22382	Napitupulu	Silaen	Kab.	Toba Samosir	Sumatera Utara	,\
    1198	:	22382	Natolutali	Silaen	Kab.	Toba Samosir	Sumatera Utara	,\
    1199	:	22382	Ombur	Silaen	Kab.	Toba Samosir	Sumatera Utara	,\
    1200	:	22382	Panindi	Silaen	Kab.	Toba Samosir	Sumatera Utara	,\
    1201	:	22382	Pardomuan	Silaen	Kab.	Toba Samosir	Sumatera Utara	,\
    1202	:	22382	Parsambilan	Silaen	Kab.	Toba Samosir	Sumatera Utara	,\
    1203	:	22382	Pintu Batu	Silaen	Kab.	Toba Samosir	Sumatera Utara	,\
    1204	:	22382	Sibide	Silaen	Kab.	Toba Samosir	Sumatera Utara	,\
    1205	:	22382	Sibide Barat	Silaen	Kab.	Toba Samosir	Sumatera Utara	,\
    1206	:	22382	Sigodang Tua	Silaen	Kab.	Toba Samosir	Sumatera Utara	,\
    1207	:	22382	Silaen	Silaen	Kab.	Toba Samosir	Sumatera Utara	,\
    1208	:	22382	Simanobak	Silaen	Kab.	Toba Samosir	Sumatera Utara	,\
    1209	:	22382	Sinta Dame (Cinta Damai)	Silaen	Kab.	Toba Samosir	Sumatera Utara	,\
    1210	:	22382	Siringkiron	Silaen	Kab.	Toba Samosir	Sumatera Utara	,\
    1211	:	22382	Sitorang I	Silaen	Kab.	Toba Samosir	Sumatera Utara	,\
    1212	:	22457	Batu Nagajar	Sijama Polang	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    1213	:	22457	Bonan Dolok I	Sijama Polang	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    1214	:	22457	Bonan Dolok II	Sijama Polang	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    1215	:	22457	Hutaginjang	Sijama Polang	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    1216	:	22457	Nagurguran	Sijama Polang	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    1217	:	22457	Sanggaran I	Sijama Polang	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    1218	:	22457	Siborboron	Sijama Polang	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    1219	:	22457	Sibuntuon	Sijama Polang	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    1220	:	22457	Sigulok	Sijama Polang	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    1221	:	22457	Sitapongan	Sijama Polang	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    1222	:	22755	Aek Goti	Sihapas Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    1223	:	22755	Balangka	Sihapas Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    1224	:	22755	Gulangan	Sihapas Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    1225	:	22755	Lubuk Gonting	Sihapas Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    1226	:	22755	Padang Hasior Dolok	Sihapas Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    1227	:	22755	Padang Hasior Lombang	Sihapas Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    1228	:	22755	Paran Dolok	Sihapas Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    1229	:	22755	Silenjeng	Sihapas Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    1230	:	22755	Simaninggir	Sihapas Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    1231	:	22755	Sitada Tada	Sihapas Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    1232	:	22755	Tanjung Morang	Sihapas Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    1233	:	22755	Ujung Gading	Sihapas Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    1234	:	22755	Ujung Padang	Sihapas Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    1235	:	22381	Banua Huta	Sigumpar	Kab.	Toba Samosir	Sumatera Utara	,\
    1236	:	22381	Dolok Jior	Sigumpar	Kab.	Toba Samosir	Sumatera Utara	,\
    1237	:	22381	Maju	Sigumpar	Kab.	Toba Samosir	Sumatera Utara	,\
    1238	:	22381	Marsangap	Sigumpar	Kab.	Toba Samosir	Sumatera Utara	,\
    1239	:	22381	Nauli	Sigumpar	Kab.	Toba Samosir	Sumatera Utara	,\
    1240	:	22381	Sigumpar	Sigumpar	Kab.	Toba Samosir	Sumatera Utara	,\
    1241	:	22381	Sigumpar Barat	Sigumpar	Kab.	Toba Samosir	Sumatera Utara	,\
    1242	:	22381	Sigumpar Dangsina	Sigumpar	Kab.	Toba Samosir	Sumatera Utara	,\
    1243	:	22381	Sigumpar Julu	Sigumpar	Kab.	Toba Samosir	Sumatera Utara	,\
    1244	:	22381	Situa-Tua	Sigumpar	Kab.	Toba Samosir	Sumatera Utara	,\
    1245	:	22272	Kuta Jungak	Siempat Rube	Kab.	Pakpak Bharat	Sumatera Utara	,\
    1246	:	22272	Mungkur	Siempat Rube	Kab.	Pakpak Bharat	Sumatera Utara	,\
    1247	:	22272	Siempat Rube I	Siempat Rube	Kab.	Pakpak Bharat	Sumatera Utara	,\
    1248	:	22272	Siempat Rube II	Siempat Rube	Kab.	Pakpak Bharat	Sumatera Utara	,\
    1249	:	22272	Siempat Rube IV	Siempat Rube	Kab.	Pakpak Bharat	Sumatera Utara	,\
    1250	:	22272	Traju	Siempat Rube	Kab.	Pakpak Bharat	Sumatera Utara	,\
    1251	:	22254	Bakal Julu	Siempat Nempu Hulu	Kab.	Dairi	Sumatera Utara	,\
    1252	:	22254	Gunung Meriah	Siempat Nempu Hulu	Kab.	Dairi	Sumatera Utara	,\
    1253	:	22254	Kuta Tengah	Siempat Nempu Hulu	Kab.	Dairi	Sumatera Utara	,\
    1254	:	22254	Lae Nuaha	Siempat Nempu Hulu	Kab.	Dairi	Sumatera Utara	,\
    1255	:	22254	Pandan	Siempat Nempu Hulu	Kab.	Dairi	Sumatera Utara	,\
    1256	:	22254	Pangaribuan	Siempat Nempu Hulu	Kab.	Dairi	Sumatera Utara	,\
    1257	:	22254	Sigambir Gambir	Siempat Nempu Hulu	Kab.	Dairi	Sumatera Utara	,\
    1258	:	22254	Silumboyah	Siempat Nempu Hulu	Kab.	Dairi	Sumatera Utara	,\
    1259	:	22254	Sipoltong	Siempat Nempu Hulu	Kab.	Dairi	Sumatera Utara	,\
    1260	:	22254	Sungai Raya	Siempat Nempu Hulu	Kab.	Dairi	Sumatera Utara	,\
    1261	:	22254	Tambahan	Siempat Nempu Hulu	Kab.	Dairi	Sumatera Utara	,\
    1262	:	22254	Tualang	Siempat Nempu Hulu	Kab.	Dairi	Sumatera Utara	,\
    1263	:	22263	Jambur Indonesia	Siempat Nempu Hilir	Kab.	Dairi	Sumatera Utara	,\
    1264	:	22263	Janji	Siempat Nempu Hilir	Kab.	Dairi	Sumatera Utara	,\
    1265	:	22263	Lae Itam	Siempat Nempu Hilir	Kab.	Dairi	Sumatera Utara	,\
    1266	:	22263	Lae Luhung	Siempat Nempu Hilir	Kab.	Dairi	Sumatera Utara	,\
    1267	:	22263	Lae Markelang	Siempat Nempu Hilir	Kab.	Dairi	Sumatera Utara	,\
    1268	:	22263	Lae Saring	Siempat Nempu Hilir	Kab.	Dairi	Sumatera Utara	,\
    1269	:	22263	Pardomuan	Siempat Nempu Hilir	Kab.	Dairi	Sumatera Utara	,\
    1270	:	22263	Simungun	Siempat Nempu Hilir	Kab.	Dairi	Sumatera Utara	,\
    1271	:	22263	Sopobutar	Siempat Nempu Hilir	Kab.	Dairi	Sumatera Utara	,\
    1272	:	22261	Adian Nangka	Siempat Nempu	Kab.	Dairi	Sumatera Utara	,\
    1273	:	22261	Bunturaja	Siempat Nempu	Kab.	Dairi	Sumatera Utara	,\
    1274	:	22261	Gomit	Siempat Nempu	Kab.	Dairi	Sumatera Utara	,\
    1275	:	22261	Huta Imbaru	Siempat Nempu	Kab.	Dairi	Sumatera Utara	,\
    1276	:	22261	Juma Siulok	Siempat Nempu	Kab.	Dairi	Sumatera Utara	,\
    1277	:	22261	Juma Teguh	Siempat Nempu	Kab.	Dairi	Sumatera Utara	,\
    1278	:	22261	Jumantuang	Siempat Nempu	Kab.	Dairi	Sumatera Utara	,\
    1279	:	22261	Sihorbo	Siempat Nempu	Kab.	Dairi	Sumatera Utara	,\
    1280	:	22261	Sinampang	Siempat Nempu	Kab.	Dairi	Sumatera Utara	,\
    1281	:	22261	Soban	Siempat Nempu	Kab.	Dairi	Sumatera Utara	,\
    1282	:	22261	Sosor Lontung	Siempat Nempu	Kab.	Dairi	Sumatera Utara	,\
    1283	:	22874	Hilidohona	Sidua`ori	Kab.	Nias Selatan	Sumatera Utara	,\
    1284	:	22874	Hililaora	Sidua`ori	Kab.	Nias Selatan	Sumatera Utara	,\
    1285	:	22874	Hilisao`oto	Sidua`ori	Kab.	Nias Selatan	Sumatera Utara	,\
    1286	:	22874	Hilizanuwo	Sidua`ori	Kab.	Nias Selatan	Sumatera Utara	,\
    1287	:	22874	Hoya	Sidua`ori	Kab.	Nias Selatan	Sumatera Utara	,\
    1288	:	22874	Mondrowe	Sidua`ori	Kab.	Nias Selatan	Sumatera Utara	,\
    1289	:	22874	Na`ai	Sidua`ori	Kab.	Nias Selatan	Sumatera Utara	,\
    1290	:	22874	Olanori	Sidua`ori	Kab.	Nias Selatan	Sumatera Utara	,\
    1291	:	22874	Taluzusua	Sidua`ori	Kab.	Nias Selatan	Sumatera Utara	,\
    1292	:	22874	Uluidanoduo	Sidua`ori	Kab.	Nias Selatan	Sumatera Utara	,\
    1293	:	22874	Umbu Sohahua	Sidua`ori	Kab.	Nias Selatan	Sumatera Utara	,\
    1294	:	22212	Batang Beruh	Sidikalang	Kab.	Dairi	Sumatera Utara	,\
    1295	:	22215	Belang Malum	Sidikalang	Kab.	Dairi	Sumatera Utara	,\
    1296	:	22219	Bintang	Sidikalang	Kab.	Dairi	Sumatera Utara	,\
    1297	:	22217	Bintang Hulu	Sidikalang	Kab.	Dairi	Sumatera Utara	,\
    1298	:	22211	Huta Rakjat	Sidikalang	Kab.	Dairi	Sumatera Utara	,\
    1299	:	22213	Kalang	Sidikalang	Kab.	Dairi	Sumatera Utara	,\
    1300	:	22218	Kalang Simbara	Sidikalang	Kab.	Dairi	Sumatera Utara	,\
    1301	:	22214	Kuta Gambir	Sidikalang	Kab.	Dairi	Sumatera Utara	,\
    1302	:	22216	Sidiangkat	Sidikalang	Kab.	Dairi	Sumatera Utara	,\
    1303	:	22211	Sidikalang Kota	Sidikalang	Kab.	Dairi	Sumatera Utara	,\
    1304	:	21171	Ambarisan	Sidamanik	Kab.	Simalungun	Sumatera Utara	,\
    1305	:	21171	Bah Biak	Sidamanik	Kab.	Simalungun	Sumatera Utara	,\
    1306	:	21171	Bah Butong 1	Sidamanik	Kab.	Simalungun	Sumatera Utara	,\
    1307	:	21171	Bah Butong 2	Sidamanik	Kab.	Simalungun	Sumatera Utara	,\
    1308	:	21171	Bahal Gajah	Sidamanik	Kab.	Simalungun	Sumatera Utara	,\
    1309	:	21171	Birong Ulu Manriah	Sidamanik	Kab.	Simalungun	Sumatera Utara	,\
    1310	:	21171	Kebun Sayur Bah Butong	Sidamanik	Kab.	Simalungun	Sumatera Utara	,\
    1311	:	21171	Manik Hataran	Sidamanik	Kab.	Simalungun	Sumatera Utara	,\
    1312	:	21171	Manik Maraja	Sidamanik	Kab.	Simalungun	Sumatera Utara	,\
    1313	:	21171	Mekar Sidamanik	Sidamanik	Kab.	Simalungun	Sumatera Utara	,\
    1314	:	21171	Sarimatondang	Sidamanik	Kab.	Simalungun	Sumatera Utara	,\
    1315	:	21171	Sidamanik	Sidamanik	Kab.	Simalungun	Sumatera Utara	,\
    1316	:	21171	Tiga Bolon	Sidamanik	Kab.	Simalungun	Sumatera Utara	,\
    1317	:	22474	Bahal Batu I	Siborong-Borong	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1318	:	22474	Bahal Batu II	Siborong-Borong	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1319	:	22474	Bahal Batu III	Siborong-Borong	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1320	:	22474	Hutabulu	Siborong-Borong	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1321	:	22474	Lobu Siregar I	Siborong-Borong	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1322	:	22474	Lobu Siregar II	Siborong-Borong	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1323	:	22474	Lumban Tonga Tonga	Siborong-Borong	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1324	:	22474	Paniaran	Siborong-Borong	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1325	:	22474	Parik Sabungan	Siborong-Borong	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1326	:	22474	Pasar Siborong Borong	Siborong-Borong	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1327	:	22474	Pohan Jae	Siborong-Borong	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1328	:	22474	Pohan Julu	Siborong-Borong	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1329	:	22474	Pohan Tonga	Siborong-Borong	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1330	:	22474	Siaro	Siborong-Borong	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1331	:	22474	Siborong-Borong I	Siborong-Borong	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1332	:	22474	Siborong-Borong II	Siborong-Borong	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1333	:	22474	Sigumbang	Siborong-Borong	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1334	:	22474	Silait-Lait	Siborong-Borong	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1335	:	22474	Sitabotabo	Siborong-Borong	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1336	:	22474	Sitabotabo Toruan	Siborong-Borong	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1337	:	22474	Sitampurung	Siborong-Borong	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1338	:	22511	Angin Nauli	Sibolga Utara	Kota	Sibolga	Sumatera Utara	,\
    1339	:	22514	Huta Barangan	Sibolga Utara	Kota	Sibolga	Sumatera Utara	,\
    1340	:	22512	Huta Tonga Tonga	Sibolga Utara	Kota	Sibolga	Sumatera Utara	,\
    1341	:	22513	Sibolga Ilir	Sibolga Utara	Kota	Sibolga	Sumatera Utara	,\
    1342	:	22513	Simaremare	Sibolga Utara	Kota	Sibolga	Sumatera Utara	,\
    1343	:	22533	Aek Habil	Sibolga Selatan	Kota	Sibolga	Sumatera Utara	,\
    1344	:	22536	Aek Manis	Sibolga Selatan	Kota	Sibolga	Sumatera Utara	,\
    1345	:	22537	Aek Muara Pinang	Sibolga Selatan	Kota	Sibolga	Sumatera Utara	,\
    1346	:	22538	Aek Parombunan	Sibolga Selatan	Kota	Sibolga	Sumatera Utara	,\
    1347	:	22535	Pancuran Bambu	Sibolga Sambas	Kota	Sibolga	Sumatera Utara	,\
    1348	:	22532	Pancuran Dewa	Sibolga Sambas	Kota	Sibolga	Sumatera Utara	,\
    1349	:	22531	Pancuran Kerambil	Sibolga Sambas	Kota	Sibolga	Sumatera Utara	,\
    1350	:	22534	Pancuran Pinang	Sibolga Sambas	Kota	Sibolga	Sumatera Utara	,\
    1351	:	22521	Kota Baringin (Beringin)	Sibolga Kota	Kota	Sibolga	Sumatera Utara	,\
    1352	:	22524	Pancuran Gerobak	Sibolga Kota	Kota	Sibolga	Sumatera Utara	,\
    1353	:	22522	Pasar Baru	Sibolga Kota	Kota	Sibolga	Sumatera Utara	,\
    1354	:	22523	Pasar Belakang	Sibolga Kota	Kota	Sibolga	Sumatera Utara	,\
    1355	:	20357	Bandar Baru	Sibolangit	Kab.	Deli Serdang	Sumatera Utara	,\
    1356	:	20357	Batu Layang	Sibolangit	Kab.	Deli Serdang	Sumatera Utara	,\
    1357	:	20357	Batu Mbelin	Sibolangit	Kab.	Deli Serdang	Sumatera Utara	,\
    1358	:	20357	Bengkurung	Sibolangit	Kab.	Deli Serdang	Sumatera Utara	,\
    1359	:	20357	Betimus Baru	Sibolangit	Kab.	Deli Serdang	Sumatera Utara	,\
    1360	:	20357	Bingkawan	Sibolangit	Kab.	Deli Serdang	Sumatera Utara	,\
    1361	:	20357	Buah Nabar	Sibolangit	Kab.	Deli Serdang	Sumatera Utara	,\
    1362	:	20357	Bukum	Sibolangit	Kab.	Deli Serdang	Sumatera Utara	,\
    1363	:	20357	Buluh Awar	Sibolangit	Kab.	Deli Serdang	Sumatera Utara	,\
    1364	:	20357	Cinta Rakyat	Sibolangit	Kab.	Deli Serdang	Sumatera Utara	,\
    1365	:	20357	Durin Serugun	Sibolangit	Kab.	Deli Serdang	Sumatera Utara	,\
    1366	:	20357	Ketangkuhen	Sibolangit	Kab.	Deli Serdang	Sumatera Utara	,\
    1367	:	20357	Kuala	Sibolangit	Kab.	Deli Serdang	Sumatera Utara	,\
    1368	:	20357	Martelu	Sibolangit	Kab.	Deli Serdang	Sumatera Utara	,\
    1369	:	20357	Negri Gugung	Sibolangit	Kab.	Deli Serdang	Sumatera Utara	,\
    1370	:	20357	Puang Aja	Sibolangit	Kab.	Deli Serdang	Sumatera Utara	,\
    1371	:	20357	Rambung Baru	Sibolangit	Kab.	Deli Serdang	Sumatera Utara	,\
    1372	:	20357	Rumah Kinangkung Sp	Sibolangit	Kab.	Deli Serdang	Sumatera Utara	,\
    1373	:	20357	Rumah Pil-Pil	Sibolangit	Kab.	Deli Serdang	Sumatera Utara	,\
    1374	:	20357	Rumah Sumbul	Sibolangit	Kab.	Deli Serdang	Sumatera Utara	,\
    1375	:	20357	Sala Bulan	Sibolangit	Kab.	Deli Serdang	Sumatera Utara	,\
    1376	:	20357	Sayum Sabah	Sibolangit	Kab.	Deli Serdang	Sumatera Utara	,\
    1377	:	20357	Sembahe	Sibolangit	Kab.	Deli Serdang	Sumatera Utara	,\
    1378	:	20357	Sibolangit	Sibolangit	Kab.	Deli Serdang	Sumatera Utara	,\
    1379	:	20357	Sikeben	Sibolangit	Kab.	Deli Serdang	Sumatera Utara	,\
    1380	:	20357	Suka Maju	Sibolangit	Kab.	Deli Serdang	Sumatera Utara	,\
    1381	:	20357	Suka Makmur	Sibolangit	Kab.	Deli Serdang	Sumatera Utara	,\
    1382	:	20357	Tambunen	Sibolangit	Kab.	Deli Serdang	Sumatera Utara	,\
    1383	:	20357	Tanjung Beringin	Sibolangit	Kab.	Deli Serdang	Sumatera Utara	,\
    1384	:	20357	Ujung Deleng	Sibolangit	Kab.	Deli Serdang	Sumatera Utara	,\
    1385	:	22654	Anggoli	Sibabangun	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    1386	:	22654	Hutagurgur	Sibabangun	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    1387	:	22654	Mombang Boru	Sibabangun	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    1388	:	22654	Muara Sibuntuon	Sibabangun	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    1389	:	22654	Sibabangun	Sibabangun	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    1390	:	22654	Sibio Bio	Sibabangun	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    1391	:	22654	Simanosor	Sibabangun	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    1392	:	22417	Enda Portibi	Siatas Barita	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1393	:	22417	Lobuhole	Siatas Barita	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1394	:	22417	Lumban Siagian Jae	Siatas Barita	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1395	:	22417	Lumban Siagian Julu	Siatas Barita	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1396	:	22419	Pansur Napitu	Siatas Barita	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1397	:	22418	Sangkaran	Siatas Barita	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1398	:	22417	Si Raja Hutagalung	Siatas Barita	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1399	:	22417	Sidagal	Siatas Barita	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1400	:	22417	Simanampang	Siatas Barita	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1401	:	22417	Simorangkir Habinsaran	Siatas Barita	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1402	:	22417	Simorangkir Julu	Siatas Barita	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1403	:	22418	Sitompul	Siatas Barita	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1404	:	21142	Bane	Siantar Utara	Kota	Pematang Siantar	Sumatera Utara	,\
    1405	:	21145	Baru	Siantar Utara	Kota	Pematang Siantar	Sumatera Utara	,\
    1406	:	21147	Kahean	Siantar Utara	Kota	Pematang Siantar	Sumatera Utara	,\
    1407	:	21143	Martoba	Siantar Utara	Kota	Pematang Siantar	Sumatera Utara	,\
    1408	:	21144	Melayu	Siantar Utara	Kota	Pematang Siantar	Sumatera Utara	,\
    1409	:	21141	Sigulang Gulang I	Siantar Utara	Kota	Pematang Siantar	Sumatera Utara	,\
    1410	:	21146	Sukadame	Siantar Utara	Kota	Pematang Siantar	Sumatera Utara	,\
    1411	:	21136	Asuhan	Siantar Timur	Kota	Pematang Siantar	Sumatera Utara	,\
    1412	:	21134	Kebun Sayur	Siantar Timur	Kota	Pematang Siantar	Sumatera Utara	,\
    1413	:	21135	Merdeka	Siantar Timur	Kota	Pematang Siantar	Sumatera Utara	,\
    1414	:	21132	Pahlawan	Siantar Timur	Kota	Pematang Siantar	Sumatera Utara	,\
    1415	:	21131	Pardomuan	Siantar Timur	Kota	Pematang Siantar	Sumatera Utara	,\
    1416	:	21139	Siopat Suhu	Siantar Timur	Kota	Pematang Siantar	Sumatera Utara	,\
    1417	:	21133	Tomuan	Siantar Timur	Kota	Pematang Siantar	Sumatera Utara	,\
    1418	:	21139	Bah Kapul	Siantar Sitalasari	Kota	Pematang Siantar	Sumatera Utara	,\
    1419	:	21139	Bah Sorma	Siantar Sitalasari	Kota	Pematang Siantar	Sumatera Utara	,\
    1420	:	21137	Bukit Sofa/Shofa	Siantar Sitalasari	Kota	Pematang Siantar	Sumatera Utara	,\
    1421	:	21137	Gurilla	Siantar Sitalasari	Kota	Pematang Siantar	Sumatera Utara	,\
    1422	:	21137	Setia Negara	Siantar Sitalasari	Kota	Pematang Siantar	Sumatera Utara	,\
    1423	:	21126	Aek Nauli	Siantar Selatan	Kota	Pematang Siantar	Sumatera Utara	,\
    1424	:	21122	Karo	Siantar Selatan	Kota	Pematang Siantar	Sumatera Utara	,\
    1425	:	21124	Kristen	Siantar Selatan	Kota	Pematang Siantar	Sumatera Utara	,\
    1426	:	21125	Martimbang	Siantar Selatan	Kota	Pematang Siantar	Sumatera Utara	,\
    1427	:	21121	Simalungun	Siantar Selatan	Kota	Pematang Siantar	Sumatera Utara	,\
    1428	:	21123	Toba	Siantar Selatan	Kota	Pematang Siantar	Sumatera Utara	,\
    1429	:	22384	Narumonda I	Siantar Narumonda	Kab.	Toba Samosir	Sumatera Utara	,\
    1430	:	22384	Narumonda II	Siantar Narumonda	Kab.	Toba Samosir	Sumatera Utara	,\
    1431	:	22384	Narumonda III	Siantar Narumonda	Kab.	Toba Samosir	Sumatera Utara	,\
    1432	:	22384	Narumonda IV	Siantar Narumonda	Kab.	Toba Samosir	Sumatera Utara	,\
    1433	:	22384	Narumonda V	Siantar Narumonda	Kab.	Toba Samosir	Sumatera Utara	,\
    1434	:	22384	Narumonda VI	Siantar Narumonda	Kab.	Toba Samosir	Sumatera Utara	,\
    1435	:	22384	Narumonda VII	Siantar Narumonda	Kab.	Toba Samosir	Sumatera Utara	,\
    1436	:	22384	Narumonda VIII	Siantar Narumonda	Kab.	Toba Samosir	Sumatera Utara	,\
    1437	:	22384	Siantar Dangsina	Siantar Narumonda	Kab.	Toba Samosir	Sumatera Utara	,\
    1438	:	22384	Siantar Sigordang	Siantar Narumonda	Kab.	Toba Samosir	Sumatera Utara	,\
    1439	:	22384	Siantar Sitiotio	Siantar Narumonda	Kab.	Toba Samosir	Sumatera Utara	,\
    1440	:	22384	Siantar Tonga Tonga I	Siantar Narumonda	Kab.	Toba Samosir	Sumatera Utara	,\
    1441	:	22384	Siantar Tonga Tonga II	Siantar Narumonda	Kab.	Toba Samosir	Sumatera Utara	,\
    1442	:	22384	Siantar Tonga-Tonga III	Siantar Narumonda	Kab.	Toba Samosir	Sumatera Utara	,\
    1443	:	21137	Naga Pita	Siantar Martoba	Kota	Pematang Siantar	Sumatera Utara	,\
    1444	:	21137	Pondok Sayur	Siantar Martoba	Kota	Pematang Siantar	Sumatera Utara	,\
    1445	:	21137	Sumber Jaya	Siantar Martoba	Kota	Pematang Siantar	Sumatera Utara	,\
    1446	:	21137	Tambun Nabolon	Siantar Martoba	Kota	Pematang Siantar	Sumatera Utara	,\
    1447	:	21137	Tanjung Pinggir	Siantar Martoba	Kota	Pematang Siantar	Sumatera Utara	,\
    1448	:	21137	Tanjung Tongah	Siantar Martoba	Kota	Pematang Siantar	Sumatera Utara	,\
    1449	:	21128	Marihat Jaya	Siantar Marimbun	Kota	Pematang Siantar	Sumatera Utara	,\
    1450	:	21129	Naga Huta Timur	Siantar Marimbun	Kota	Pematang Siantar	Sumatera Utara	,\
    1451	:	21129	Nagahuta	Siantar Marimbun	Kota	Pematang Siantar	Sumatera Utara	,\
    1452	:	21127	Pematang Marihat	Siantar Marimbun	Kota	Pematang Siantar	Sumatera Utara	,\
    1453	:	21129	Simarimbun	Siantar Marimbun	Kota	Pematang Siantar	Sumatera Utara	,\
    1454	:	21129	Tong Marimbun	Siantar Marimbun	Kota	Pematang Siantar	Sumatera Utara	,\
    1455	:	21129	Baringin Pancur Nauli (Bp Nauli)	Siantar Marihat	Kota	Pematang Siantar	Sumatera Utara	,\
    1456	:	21129	Mekar Nauli	Siantar Marihat	Kota	Pematang Siantar	Sumatera Utara	,\
    1457	:	21128	Pardamean	Siantar Marihat	Kota	Pematang Siantar	Sumatera Utara	,\
    1458	:	21129	Parhorasan Nauli	Siantar Marihat	Kota	Pematang Siantar	Sumatera Utara	,\
    1459	:	21127	Sukamaju	Siantar Marihat	Kota	Pematang Siantar	Sumatera Utara	,\
    1460	:	21128	Sukamakmur	Siantar Marihat	Kota	Pematang Siantar	Sumatera Utara	,\
    1461	:	21128	Sukaraja	Siantar Marihat	Kota	Pematang Siantar	Sumatera Utara	,\
    1462	:	21112	Banjar	Siantar Barat	Kota	Pematang Siantar	Sumatera Utara	,\
    1463	:	21111	Bantan	Siantar Barat	Kota	Pematang Siantar	Sumatera Utara	,\
    1464	:	21118	Dwikora	Siantar Barat	Kota	Pematang Siantar	Sumatera Utara	,\
    1465	:	21117	Proklamasi	Siantar Barat	Kota	Pematang Siantar	Sumatera Utara	,\
    1466	:	21113	Simarito	Siantar Barat	Kota	Pematang Siantar	Sumatera Utara	,\
    1467	:	21114	Sipinggol Pinggol	Siantar Barat	Kota	Pematang Siantar	Sumatera Utara	,\
    1468	:	21115	Teladan **	Siantar Barat	Kota	Pematang Siantar	Sumatera Utara	,\
    1469	:	21116	Timbang Galung	Siantar Barat	Kota	Pematang Siantar	Sumatera Utara	,\
    1470	:	21151	Dolok Hataran	Siantar	Kab.	Simalungun	Sumatera Utara	,\
    1471	:	21151	Dolok Marlawan	Siantar	Kab.	Simalungun	Sumatera Utara	,\
    1472	:	21151	Karang Bangun	Siantar	Kab.	Simalungun	Sumatera Utara	,\
    1473	:	21151	Laras Dua	Siantar	Kab.	Simalungun	Sumatera Utara	,\
    1474	:	21151	Lestari Indah	Siantar	Kab.	Simalungun	Sumatera Utara	,\
    1475	:	21151	Marihat Baris	Siantar	Kab.	Simalungun	Sumatera Utara	,\
    1476	:	21151	Nusa Harapan	Siantar	Kab.	Simalungun	Sumatera Utara	,\
    1477	:	21151	Pantoan Maju	Siantar	Kab.	Simalungun	Sumatera Utara	,\
    1478	:	21151	Pematang Silampuyang	Siantar	Kab.	Simalungun	Sumatera Utara	,\
    1479	:	21151	Pematang Simalungun	Siantar	Kab.	Simalungun	Sumatera Utara	,\
    1480	:	21151	Rambung Merah	Siantar	Kab.	Simalungun	Sumatera Utara	,\
    1481	:	21151	Sejahtera	Siantar	Kab.	Simalungun	Sumatera Utara	,\
    1482	:	21151	Siantar Estate	Siantar	Kab.	Simalungun	Sumatera Utara	,\
    1483	:	21151	Silampuyang	Siantar	Kab.	Simalungun	Sumatera Utara	,\
    1484	:	21151	Silau Malaha	Siantar	Kab.	Simalungun	Sumatera Utara	,\
    1485	:	21151	Silau Manik	Siantar	Kab.	Simalungun	Sumatera Utara	,\
    1486	:	21151	Sitalasari	Siantar	Kab.	Simalungun	Sumatera Utara	,\
    1487	:	22396	Aek Sipitudai	Sianjur Mula-Mula	Kab.	Samosir	Sumatera Utara	,\
    1488	:	22396	Boho	Sianjur Mula-Mula	Kab.	Samosir	Sumatera Utara	,\
    1489	:	22396	Bonan Dolok	Sianjur Mula-Mula	Kab.	Samosir	Sumatera Utara	,\
    1490	:	22396	Ginolat	Sianjur Mula-Mula	Kab.	Samosir	Sumatera Utara	,\
    1491	:	22396	Hasinggaan	Sianjur Mula-Mula	Kab.	Samosir	Sumatera Utara	,\
    1492	:	22396	Huta Ginjang	Sianjur Mula-Mula	Kab.	Samosir	Sumatera Utara	,\
    1493	:	22396	Huta Gurgur	Sianjur Mula-Mula	Kab.	Samosir	Sumatera Utara	,\
    1494	:	22396	Sari Marihit	Sianjur Mula-Mula	Kab.	Samosir	Sumatera Utara	,\
    1495	:	22396	Sianjur Mulamula	Sianjur Mula-Mula	Kab.	Samosir	Sumatera Utara	,\
    1496	:	22396	Siboro	Sianjur Mula-Mula	Kab.	Samosir	Sumatera Utara	,\
    1497	:	22396	Singkam	Sianjur Mula-Mula	Kab.	Samosir	Sumatera Utara	,\
    1498	:	22976	Aek Garut	Siabu	Kab.	Mandailing Natal	Sumatera Utara	,\
    1499	:	22976	Aek Mual	Siabu	Kab.	Mandailing Natal	Sumatera Utara	,\
    1500	:	22976	Bonan Dolok	Siabu	Kab.	Mandailing Natal	Sumatera Utara	,\
    1501	:	22976	Huraba	Siabu	Kab.	Mandailing Natal	Sumatera Utara	,\
    1502	:	22976	Huraba II	Siabu	Kab.	Mandailing Natal	Sumatera Utara	,\
    1503	:	22976	Huta Baringin	Siabu	Kab.	Mandailing Natal	Sumatera Utara	,\
    1504	:	22976	Huta Godang Muda	Siabu	Kab.	Mandailing Natal	Sumatera Utara	,\
    1505	:	22976	Huta Puli	Siabu	Kab.	Mandailing Natal	Sumatera Utara	,\
    1506	:	22976	Huta Raja	Siabu	Kab.	Mandailing Natal	Sumatera Utara	,\
    1507	:	22976	Lumban Dolok	Siabu	Kab.	Mandailing Natal	Sumatera Utara	,\
    1508	:	22976	Lumban Pinasa	Siabu	Kab.	Mandailing Natal	Sumatera Utara	,\
    1509	:	22976	Muara Batang Angkola	Siabu	Kab.	Mandailing Natal	Sumatera Utara	,\
    1510	:	22976	Pintu Padang Jae	Siabu	Kab.	Mandailing Natal	Sumatera Utara	,\
    1511	:	22976	Pintu Padang Julu	Siabu	Kab.	Mandailing Natal	Sumatera Utara	,\
    1512	:	22976	Siabu	Siabu	Kab.	Mandailing Natal	Sumatera Utara	,\
    1513	:	22976	Sibaruang	Siabu	Kab.	Mandailing Natal	Sumatera Utara	,\
    1514	:	22976	Sihepeng	Siabu	Kab.	Mandailing Natal	Sumatera Utara	,\
    1515	:	22976	Simangambat	Siabu	Kab.	Mandailing Natal	Sumatera Utara	,\
    1516	:	22976	Simaninggir	Siabu	Kab.	Mandailing Natal	Sumatera Utara	,\
    1517	:	22976	Sinonoan	Siabu	Kab.	Mandailing Natal	Sumatera Utara	,\
    1518	:	22976	Tangga Bosi	Siabu	Kab.	Mandailing Natal	Sumatera Utara	,\
    1519	:	22976	Tangga Bosi II	Siabu	Kab.	Mandailing Natal	Sumatera Utara	,\
    1520	:	22976	Tangga Bosi III	Siabu	Kab.	Mandailing Natal	Sumatera Utara	,\
    1521	:	22976	Tanjung Sialang	Siabu	Kab.	Mandailing Natal	Sumatera Utara	,\
    1522	:	21261	Bangun Sari	Setia Janji	Kab.	Asahan	Sumatera Utara	,\
    1523	:	21261	Sei Silau Barat	Setia Janji	Kab.	Asahan	Sumatera Utara	,\
    1524	:	21261	Sei Silau Tua	Setia Janji	Kab.	Asahan	Sumatera Utara	,\
    1525	:	21261	Silau Maraja	Setia Janji	Kab.	Asahan	Sumatera Utara	,\
    1526	:	21261	Urung Pane	Setia Janji	Kab.	Asahan	Sumatera Utara	,\
    1527	:	20991	Bah Sidua Dua	Serba Jadi	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1528	:	20991	Karang Tengah	Serba Jadi	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1529	:	20991	Kelapa Bajohor/Bajohom	Serba Jadi	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1530	:	20991	Kwala/Kuala Bali	Serba Jadi	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1531	:	20991	Manggis	Serba Jadi	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1532	:	20991	Pulau Gambar	Serba Jadi	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1533	:	20991	Pulau Tagor	Serba Jadi	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1534	:	20991	Serba Jadi	Serba Jadi	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1535	:	20991	Tambak Cekur	Serba Jadi	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1536	:	20991	Tanjung Harap	Serba Jadi	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1537	:	20762	Bekulap	Selesai	Kab.	Langkat	Sumatera Utara	,\
    1538	:	20762	Kuta Parit	Selesai	Kab.	Langkat	Sumatera Utara	,\
    1539	:	20762	Kwala/Kuala Air Hitam	Selesai	Kab.	Langkat	Sumatera Utara	,\
    1540	:	20762	Lau Mulgap	Selesai	Kab.	Langkat	Sumatera Utara	,\
    1541	:	20762	Mancang	Selesai	Kab.	Langkat	Sumatera Utara	,\
    1542	:	20762	Nambiki	Selesai	Kab.	Langkat	Sumatera Utara	,\
    1543	:	20762	Padang Brahrang	Selesai	Kab.	Langkat	Sumatera Utara	,\
    1544	:	20762	Padang Cermin	Selesai	Kab.	Langkat	Sumatera Utara	,\
    1545	:	20762	Pekan Selesai	Selesai	Kab.	Langkat	Sumatera Utara	,\
    1546	:	20762	Perhiasan	Selesai	Kab.	Langkat	Sumatera Utara	,\
    1547	:	20762	Sei Limbat	Selesai	Kab.	Langkat	Sumatera Utara	,\
    1548	:	20762	Selayang	Selesai	Kab.	Langkat	Sumatera Utara	,\
    1549	:	20762	Selayang Baru	Selesai	Kab.	Langkat	Sumatera Utara	,\
    1550	:	20762	Tanjung Merahe	Selesai	Kab.	Langkat	Sumatera Utara	,\
    1551	:	21465	Batang Nadenggan	Sei/Sungai Kanan	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    1552	:	21465	Hajoran	Sei/Sungai Kanan	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    1553	:	21465	Huta Godang	Sei/Sungai Kanan	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    1554	:	21465	Langga Payung	Sei/Sungai Kanan	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    1555	:	21465	Marsonja	Sei/Sungai Kanan	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    1556	:	21465	Parimburan	Sei/Sungai Kanan	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    1557	:	21465	Sabungan	Sei/Sungai Kanan	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    1558	:	21465	Sampean	Sei/Sungai Kanan	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    1559	:	21465	Ujung Gading	Sei/Sungai Kanan	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    1560	:	21344	Keramat Kubah	Sei Tualang Raso	Kota	Tanjung Balai	Sumatera Utara	,\
    1561	:	21342	Muara Sentosa	Sei Tualang Raso	Kota	Tanjung Balai	Sumatera Utara	,\
    1562	:	21341	Pasar Baru	Sei Tualang Raso	Kota	Tanjung Balai	Sumatera Utara	,\
    1563	:	21345	Sei Raja	Sei Tualang Raso	Kota	Tanjung Balai	Sumatera Utara	,\
    1564	:	21343	Sumber Sari	Sei Tualang Raso	Kota	Tanjung Balai	Sumatera Utara	,\
    1565	:	21257	Brohol	Sei Suka	Kab.	Batu Bara	Sumatera Utara	,\
    1566	:	21257	Dwi Sri	Sei Suka	Kab.	Batu Bara	Sumatera Utara	,\
    1567	:	21257	Kandangan	Sei Suka	Kab.	Batu Bara	Sumatera Utara	,\
    1568	:	21257	Kwala/Kuala Indah	Sei Suka	Kab.	Batu Bara	Sumatera Utara	,\
    1569	:	21257	Kwala/Kuala Tanjung	Sei Suka	Kab.	Batu Bara	Sumatera Utara	,\
    1570	:	21257	Laut Tador	Sei Suka	Kab.	Batu Bara	Sumatera Utara	,\
    1571	:	21257	Mekar Sari	Sei Suka	Kab.	Batu Bara	Sumatera Utara	,\
    1572	:	21257	Pelanggiran Laut Tador	Sei Suka	Kab.	Batu Bara	Sumatera Utara	,\
    1573	:	21257	Pematang Jering	Sei Suka	Kab.	Batu Bara	Sumatera Utara	,\
    1574	:	21257	Pematang Kuning	Sei Suka	Kab.	Batu Bara	Sumatera Utara	,\
    1575	:	21257	Perkebunan Sipare-Pare	Sei Suka	Kab.	Batu Bara	Sumatera Utara	,\
    1576	:	21257	Perkebunan Tanjung Kasau	Sei Suka	Kab.	Batu Bara	Sumatera Utara	,\
    1577	:	21257	Sei Simujur	Sei Suka	Kab.	Batu Bara	Sumatera Utara	,\
    1578	:	21257	Sei Suka Deras	Sei Suka	Kab.	Batu Bara	Sumatera Utara	,\
    1579	:	21257	Simodong	Sei Suka	Kab.	Batu Bara	Sumatera Utara	,\
    1580	:	21257	Simpang Kopi	Sei Suka	Kab.	Batu Bara	Sumatera Utara	,\
    1581	:	21257	Tanjung Kasau	Sei Suka	Kab.	Batu Bara	Sumatera Utara	,\
    1582	:	21257	Tanjung Prapat/Parapat	Sei Suka	Kab.	Batu Bara	Sumatera Utara	,\
    1583	:	21257	Tanjung Seri	Sei Suka	Kab.	Batu Bara	Sumatera Utara	,\
    1584	:	21257	Tanjunggading	Sei Suka	Kab.	Batu Bara	Sumatera Utara	,\
    1585	:	20995	Cempedak Lobang	Sei Rampah	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1586	:	20995	Firdaus	Sei Rampah	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1587	:	20995	Firdaus Estate	Sei Rampah	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1588	:	20995	Pematang Ganjang	Sei Rampah	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1589	:	20995	Pematang Pelintahan	Sei Rampah	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1590	:	20995	Pergulaan	Sei Rampah	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1591	:	20995	Rambung Estate	Sei Rampah	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1592	:	20995	Rambung Sialang Hilir	Sei Rampah	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1593	:	20995	Rambung Sialang Hulu	Sei Rampah	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1594	:	20995	Rambung Sialang Tengah	Sei Rampah	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1595	:	20995	Sei Parit	Sei Rampah	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1596	:	20995	Sei Rampah	Sei Rampah	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1597	:	20995	Sei Rejo	Sei Rampah	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1598	:	20995	Silau Rakyat	Sei Rampah	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1599	:	20995	Simpang Empat	Sei Rampah	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1600	:	20995	Sinah Kasih	Sei Rampah	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1601	:	20995	Tanah Raja	Sei Rampah	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1602	:	20773	Alur Dua	Sei Lepan	Kab.	Langkat	Sumatera Utara	,\
    1603	:	20773	Alur Dua Baru	Sei Lepan	Kab.	Langkat	Sumatera Utara	,\
    1604	:	20773	Harapan Baru	Sei Lepan	Kab.	Langkat	Sumatera Utara	,\
    1605	:	20773	Harapan Jaya	Sei Lepan	Kab.	Langkat	Sumatera Utara	,\
    1606	:	20773	Harapan Maju	Sei Lepan	Kab.	Langkat	Sumatera Utara	,\
    1607	:	20773	Harapan Makmur	Sei Lepan	Kab.	Langkat	Sumatera Utara	,\
    1608	:	20773	Lama	Sei Lepan	Kab.	Langkat	Sumatera Utara	,\
    1609	:	20773	Lama Baru	Sei Lepan	Kab.	Langkat	Sumatera Utara	,\
    1610	:	20773	Mekar Makmur	Sei Lepan	Kab.	Langkat	Sumatera Utara	,\
    1611	:	20773	Puraka I Pertamina	Sei Lepan	Kab.	Langkat	Sumatera Utara	,\
    1612	:	20773	Puraka II	Sei Lepan	Kab.	Langkat	Sumatera Utara	,\
    1613	:	20773	Sei Bilah Barat	Sei Lepan	Kab.	Langkat	Sumatera Utara	,\
    1614	:	20773	Sei Bilah Timur	Sei Lepan	Kab.	Langkat	Sumatera Utara	,\
    1615	:	20773	Telaga Said	Sei Lepan	Kab.	Langkat	Sumatera Utara	,\
    1616	:	21381	Sarang Helang	Sei Kepayang Timur	Kab.	Asahan	Sumatera Utara	,\
    1617	:	21381	Sei Lunang	Sei Kepayang Timur	Kab.	Asahan	Sumatera Utara	,\
    1618	:	21381	Sei Pasir	Sei Kepayang Timur	Kab.	Asahan	Sumatera Utara	,\
    1619	:	21381	Sei Sembilang	Sei Kepayang Timur	Kab.	Asahan	Sumatera Utara	,\
    1620	:	21381	Sei Tempurung	Sei Kepayang Timur	Kab.	Asahan	Sumatera Utara	,\
    1621	:	21381	Sei Jawi-Jawi	Sei Kepayang Barat	Kab.	Asahan	Sumatera Utara	,\
    1622	:	21381	Sei Kepayang Kiri	Sei Kepayang Barat	Kab.	Asahan	Sumatera Utara	,\
    1623	:	21381	Sei Lendir	Sei Kepayang Barat	Kab.	Asahan	Sumatera Utara	,\
    1624	:	21381	Sei Nangka	Sei Kepayang Barat	Kab.	Asahan	Sumatera Utara	,\
    1625	:	21381	Sei Serindan	Sei Kepayang Barat	Kab.	Asahan	Sumatera Utara	,\
    1626	:	21381	Sei Tualang Pandau	Sei Kepayang Barat	Kab.	Asahan	Sumatera Utara	,\
    1627	:	21381	Bangun Baru	Sei Kepayang	Kab.	Asahan	Sumatera Utara	,\
    1628	:	21381	Perbangunan	Sei Kepayang	Kab.	Asahan	Sumatera Utara	,\
    1629	:	21381	Pertahanan	Sei Kepayang	Kab.	Asahan	Sumatera Utara	,\
    1630	:	21381	Sei Kepayang Kanan	Sei Kepayang	Kab.	Asahan	Sumatera Utara	,\
    1631	:	21381	Sei Kepayang Tengah	Sei Kepayang	Kab.	Asahan	Sumatera Utara	,\
    1632	:	21381	Sei Paham	Sei Kepayang	Kab.	Asahan	Sumatera Utara	,\
    1633	:	21272	Bahung Sibatu-Batu	Sei Dadap	Kab.	Asahan	Sumatera Utara	,\
    1634	:	21272	Pasiran	Sei Dadap	Kab.	Asahan	Sumatera Utara	,\
    1635	:	21272	Perkebunan Sei Dadap I-II	Sei Dadap	Kab.	Asahan	Sumatera Utara	,\
    1636	:	21272	Perkebunan Sei Dadap III-IV	Sei Dadap	Kab.	Asahan	Sumatera Utara	,\
    1637	:	21272	Sei Alim Hasak	Sei Dadap	Kab.	Asahan	Sumatera Utara	,\
    1638	:	21272	Sei Kamah Baru	Sei Dadap	Kab.	Asahan	Sumatera Utara	,\
    1639	:	21272	Sei Kamah I	Sei Dadap	Kab.	Asahan	Sumatera Utara	,\
    1640	:	21272	Sei Kamah II	Sei Dadap	Kab.	Asahan	Sumatera Utara	,\
    1641	:	21272	Tanjung Alam	Sei Dadap	Kab.	Asahan	Sumatera Utara	,\
    1642	:	21272	Tanjung Asri	Sei Dadap	Kab.	Asahan	Sumatera Utara	,\
    1643	:	20771	Belinteng	Sei Binge (Bingai)	Kab.	Langkat	Sumatera Utara	,\
    1644	:	20771	Durian Lingga	Sei Binge (Bingai)	Kab.	Langkat	Sumatera Utara	,\
    1645	:	20771	Gunung Ambat	Sei Binge (Bingai)	Kab.	Langkat	Sumatera Utara	,\
    1646	:	20771	Kwala Mencirim	Sei Binge (Bingai)	Kab.	Langkat	Sumatera Utara	,\
    1647	:	20771	Mekar Jaya	Sei Binge (Bingai)	Kab.	Langkat	Sumatera Utara	,\
    1648	:	20771	Namu Ukur Selatan	Sei Binge (Bingai)	Kab.	Langkat	Sumatera Utara	,\
    1649	:	20771	Namu Ukur Utara	Sei Binge (Bingai)	Kab.	Langkat	Sumatera Utara	,\
    1650	:	20771	Pasar IV Namu/Namo Terasi	Sei Binge (Bingai)	Kab.	Langkat	Sumatera Utara	,\
    1651	:	20771	Pasar VI Kwala Mencirim	Sei Binge (Bingai)	Kab.	Langkat	Sumatera Utara	,\
    1652	:	20771	Pasar VIII Namu Terasi	Sei Binge (Bingai)	Kab.	Langkat	Sumatera Utara	,\
    1653	:	20771	Pekan Sawah	Sei Binge (Bingai)	Kab.	Langkat	Sumatera Utara	,\
    1654	:	20771	Purwobinangun	Sei Binge (Bingai)	Kab.	Langkat	Sumatera Utara	,\
    1655	:	20771	Rumah Galuh	Sei Binge (Bingai)	Kab.	Langkat	Sumatera Utara	,\
    1656	:	20771	Simpang Kuta Buluh	Sei Binge (Bingai)	Kab.	Langkat	Sumatera Utara	,\
    1657	:	20771	Tanjung Gunung	Sei Binge (Bingai)	Kab.	Langkat	Sumatera Utara	,\
    1658	:	20771	Telaga	Sei Binge (Bingai)	Kab.	Langkat	Sumatera Utara	,\
    1659	:	20995	Bakaran Batu	Sei Bamban	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1660	:	20995	Gempolan	Sei Bamban	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1661	:	20995	Penggalangan	Sei Bamban	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1662	:	20995	Pon (Kampung Pon)	Sei Bamban	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1663	:	20995	Rampah Estate	Sei Bamban	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1664	:	20995	Sei Bamban	Sei Bamban	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1665	:	20995	Sei Bamban Estate	Sei Bamban	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1666	:	20995	Sei Belutu	Sei Bamban	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1667	:	20995	Sei Buluh Estate	Sei Bamban	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1668	:	20995	Suka Damai	Sei Bamban	Kab.	Serdang Bedagai	Sumatera Utara	,\
    1669	:	21252	Benteng Jaya	Sei Balai	Kab.	Batu Bara	Sumatera Utara	,\
    1670	:	21252	Durian	Sei Balai	Kab.	Batu Bara	Sumatera Utara	,\
    1671	:	21252	Kwala Sikasim	Sei Balai	Kab.	Batu Bara	Sumatera Utara	,\
    1672	:	21252	Mekar Baru	Sei Balai	Kab.	Batu Bara	Sumatera Utara	,\
    1673	:	21252	Mekar Mulio	Sei Balai	Kab.	Batu Bara	Sumatera Utara	,\
    1674	:	21252	Perjuangan	Sei Balai	Kab.	Batu Bara	Sumatera Utara	,\
    1675	:	21252	Perkebunan Sei Balai	Sei Balai	Kab.	Batu Bara	Sumatera Utara	,\
    1676	:	21252	Perkebunan Sei Bejangkar	Sei Balai	Kab.	Batu Bara	Sumatera Utara	,\
    1677	:	21252	Sei Balai	Sei Balai	Kab.	Batu Bara	Sumatera Utara	,\
    1678	:	21252	Siajam	Sei Balai	Kab.	Batu Bara	Sumatera Utara	,\
    1679	:	21252	Sidomulio	Sei Balai	Kab.	Batu Bara	Sumatera Utara	,\
    1680	:	21252	Suka Ramai	Sei Balai	Kab.	Batu Bara	Sumatera Utara	,\
    1681	:	21252	Suko Rejo	Sei Balai	Kab.	Batu Bara	Sumatera Utara	,\
    1682	:	21252	Tanah Timbul	Sei Balai	Kab.	Batu Bara	Sumatera Utara	,\
    1683	:	20855	Cinta Raja	Secanggang	Kab.	Langkat	Sumatera Utara	,\
    1684	:	20855	Hinai Kiri	Secanggang	Kab.	Langkat	Sumatera Utara	,\
    1685	:	20855	Jaring Halus	Secanggang	Kab.	Langkat	Sumatera Utara	,\
    1686	:	20855	Karang Anyar	Secanggang	Kab.	Langkat	Sumatera Utara	,\
    1687	:	20855	Karang Gading	Secanggang	Kab.	Langkat	Sumatera Utara	,\
    1688	:	20855	Kebun Kelapa	Secanggang	Kab.	Langkat	Sumatera Utara	,\
    1689	:	20855	Kepala Sungai	Secanggang	Kab.	Langkat	Sumatera Utara	,\
    1690	:	20855	Kwala Besar	Secanggang	Kab.	Langkat	Sumatera Utara	,\
    1691	:	20855	Pantai Gading	Secanggang	Kab.	Langkat	Sumatera Utara	,\
    1692	:	20855	Perkotaan	Secanggang	Kab.	Langkat	Sumatera Utara	,\
    1693	:	20855	Secanggang	Secanggang	Kab.	Langkat	Sumatera Utara	,\
    1694	:	20855	Selotong	Secanggang	Kab.	Langkat	Sumatera Utara	,\
    1695	:	20855	Suka Mulia	Secanggang	Kab.	Langkat	Sumatera Utara	,\
    1696	:	20855	Sungai Ular	Secanggang	Kab.	Langkat	Sumatera Utara	,\
    1697	:	20855	Tanjung Ibus	Secanggang	Kab.	Langkat	Sumatera Utara	,\
    1698	:	20855	Telaga Jernih	Secanggang	Kab.	Langkat	Sumatera Utara	,\
    1699	:	20855	Teluk	Secanggang	Kab.	Langkat	Sumatera Utara	,\
    1700	:	22774	Aek Badak Jae	Sayur Matinggi	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1701	:	22774	Aek Badak Julu	Sayur Matinggi	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1702	:	22774	Aek Libung	Sayur Matinggi	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1703	:	22774	Aek Raja	Sayur Matinggi	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1704	:	22774	Bange	Sayur Matinggi	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1705	:	22774	Bulu Gading	Sayur Matinggi	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1706	:	22774	Huta Pardomuan	Sayur Matinggi	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1707	:	22774	Janji Mauli Baringin	Sayur Matinggi	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1708	:	22774	Lumban Huayan	Sayur Matinggi	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1709	:	22774	Mondang	Sayur Matinggi	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1710	:	22774	Samonggal Parmonangan	Sayur Matinggi	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1711	:	22774	Sayur Matinggi	Sayur Matinggi	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1712	:	22774	Sialang	Sayur Matinggi	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1713	:	22774	Silaiya	Sayur Matinggi	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1714	:	22774	Silaiya Tanjung Leuk	Sayur Matinggi	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1715	:	22774	Simpang Tolang	Sayur Matinggi	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1716	:	22774	Sipange Godang	Sayur Matinggi	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1717	:	22774	Sipange Julu	Sayur Matinggi	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1718	:	22774	Sipange Siunjam	Sayur Matinggi	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1719	:	22774	Tolang Jae	Sayur Matinggi	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1720	:	22774	Tolang Julu	Sayur Matinggi	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1721	:	22852	Hiliduruwa	Sawo	Kab.	Nias Utara	Sumatera Utara	,\
    1722	:	22852	Lasara Sawo	Sawo	Kab.	Nias Utara	Sumatera Utara	,\
    1723	:	22852	Ombolata Sawo	Sawo	Kab.	Nias Utara	Sumatera Utara	,\
    1724	:	22852	Onozitoli Sawo	Sawo	Kab.	Nias Utara	Sumatera Utara	,\
    1725	:	22852	Sanawuyu	Sawo	Kab.	Nias Utara	Sumatera Utara	,\
    1726	:	22852	Sawo	Sawo	Kab.	Nias Utara	Sumatera Utara	,\
    1727	:	22852	Seriwau	Sawo	Kab.	Nias Utara	Sumatera Utara	,\
    1728	:	22852	Sifahandro	Sawo	Kab.	Nias Utara	Sumatera Utara	,\
    1729	:	22852	Sisarahili Teluk Siabang	Sawo	Kab.	Nias Utara	Sumatera Utara	,\
    1730	:	22852	Teluk Bengkuang	Sawo	Kab.	Nias Utara	Sumatera Utara	,\
    1731	:	20811	Alur Gadung	Sawit Seberang	Kab.	Langkat	Sumatera Utara	,\
    1732	:	20811	Alur Melati	Sawit Seberang	Kab.	Langkat	Sumatera Utara	,\
    1733	:	20811	Mekar Sawit	Sawit Seberang	Kab.	Langkat	Sumatera Utara	,\
    1734	:	20811	Sawit Hulu	Sawit Seberang	Kab.	Langkat	Sumatera Utara	,\
    1735	:	20811	Sawit Seberang	Sawit Seberang	Kab.	Langkat	Sumatera Utara	,\
    1736	:	20811	Sei Litur Tasik	Sawit Seberang	Kab.	Langkat	Sumatera Utara	,\
    1737	:	20811	Simpang Tiga	Sawit Seberang	Kab.	Langkat	Sumatera Utara	,\
    1738	:	22611	Pasir Bidang	Sarudik	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    1739	:	22616	Pondok Batu	Sarudik	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    1740	:	22616	Sarudik	Sarudik	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    1741	:	22616	Sibuluan Nalambok	Sarudik	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    1742	:	22616	Sipan	Sarudik	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    1743	:	20773	Adin Tengah	Salapian	Kab.	Langkat	Sumatera Utara	,\
    1744	:	20773	Lau Gugur	Salapian	Kab.	Langkat	Sumatera Utara	,\
    1745	:	20773	Lau Tepu	Salapian	Kab.	Langkat	Sumatera Utara	,\
    1746	:	20773	Minta Kasih	Salapian	Kab.	Langkat	Sumatera Utara	,\
    1747	:	20773	Naman Jahe	Salapian	Kab.	Langkat	Sumatera Utara	,\
    1748	:	20773	Pama/Pamah Tambunan	Salapian	Kab.	Langkat	Sumatera Utara	,\
    1749	:	20773	Panco Warno	Salapian	Kab.	Langkat	Sumatera Utara	,\
    1750	:	20773	Pancur Ido	Salapian	Kab.	Langkat	Sumatera Utara	,\
    1751	:	20773	Parangguam	Salapian	Kab.	Langkat	Sumatera Utara	,\
    1752	:	20773	Perkebunan Bandar Telu	Salapian	Kab.	Langkat	Sumatera Utara	,\
    1753	:	20773	Perkebunan Gelugur Langkat	Salapian	Kab.	Langkat	Sumatera Utara	,\
    1754	:	20773	Perkebunan Tambunan	Salapian	Kab.	Langkat	Sumatera Utara	,\
    1755	:	20773	Perkebunan Tanjung Keliling	Salapian	Kab.	Langkat	Sumatera Utara	,\
    1756	:	20773	Tanjung Langkat	Salapian	Kab.	Langkat	Sumatera Utara	,\
    1757	:	20773	Turangi	Salapian	Kab.	Langkat	Sumatera Utara	,\
    1758	:	20773	Ujung Bandar	Salapian	Kab.	Langkat	Sumatera Utara	,\
    1759	:	20773	Ujung Terang	Salapian	Kab.	Langkat	Sumatera Utara	,\
    1760	:	22272	Boangmanalu Salak	Salak	Kab.	Pakpak Bharat	Sumatera Utara	,\
    1761	:	22272	Kuta Tinggi	Salak	Kab.	Pakpak Bharat	Sumatera Utara	,\
    1762	:	22272	Penanggalan Binanga Boang	Salak	Kab.	Pakpak Bharat	Sumatera Utara	,\
    1763	:	22272	Salak I	Salak	Kab.	Pakpak Bharat	Sumatera Utara	,\
    1764	:	22272	Salak II	Salak	Kab.	Pakpak Bharat	Sumatera Utara	,\
    1765	:	22272	Sibongkaras	Salak	Kab.	Pakpak Bharat	Sumatera Utara	,\
    1766	:	22758	Aek Simotung	Saipar Dolok Hole	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1767	:	22758	Barumun Tua (Baringin Tua)	Saipar Dolok Hole	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1768	:	22758	Batang Parsuluman	Saipar Dolok Hole	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1769	:	22758	Damparan Haunatas	Saipar Dolok Hole	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1770	:	22758	Galanggang	Saipar Dolok Hole	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1771	:	22758	Huta Hombang	Saipar Dolok Hole	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1772	:	22758	Huta Pohan	Saipar Dolok Hole	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1773	:	22758	Padang Mandailing Garugur	Saipar Dolok Hole	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1774	:	22758	Parau Sorat Sitabo-Tabo	Saipar Dolok Hole	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1775	:	22758	Pasar Simangambat	Saipar Dolok Hole	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1776	:	22758	Pasar Sipagimbar	Saipar Dolok Hole	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1777	:	22758	Pintu Padang Mandalasena	Saipar Dolok Hole	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1778	:	22758	Purbasinomba Sena	Saipar Dolok Hole	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1779	:	22758	Saut Banua Simanosor	Saipar Dolok Hole	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1780	:	22758	Sidapdap Simanosor	Saipar Dolok Hole	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1781	:	22758	Silangkitang Tambiski	Saipar Dolok Hole	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1782	:	22758	Simangambat Godang	Saipar Dolok Hole	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1783	:	22758	Somba Debata Purba	Saipar Dolok Hole	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1784	:	22758	Sunge Sigiring Giring	Saipar Dolok Hole	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1785	:	22758	Ulu Mamis Situnggaling	Saipar Dolok Hole	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    1786	:	22392	Lintongnihuta	Ronggur Nihuta	Kab.	Samosir	Sumatera Utara	,\
    1787	:	22392	Paraduan	Ronggur Nihuta	Kab.	Samosir	Sumatera Utara	,\
    1788	:	22392	Ronggur Nihuta	Ronggur Nihuta	Kab.	Samosir	Sumatera Utara	,\
    1789	:	22392	Sabungan Nihuta	Ronggur Nihuta	Kab.	Samosir	Sumatera Utara	,\
    1790	:	22392	Salaon Dolok	Ronggur Nihuta	Kab.	Samosir	Sumatera Utara	,\
    1791	:	22392	Salaon Toba	Ronggur Nihuta	Kab.	Samosir	Sumatera Utara	,\
    1792	:	22392	Salaon Tonga Tonga	Ronggur Nihuta	Kab.	Samosir	Sumatera Utara	,\
    1793	:	22392	Sijambur	Ronggur Nihuta	Kab.	Samosir	Sumatera Utara	,\
    1794	:	21156	Amborokan Pane Raya	Raya Kahean	Kab.	Simalungun	Sumatera Utara	,\
    1795	:	21156	Bah Bulian	Raya Kahean	Kab.	Simalungun	Sumatera Utara	,\
    1796	:	21156	Bah Tonang	Raya Kahean	Kab.	Simalungun	Sumatera Utara	,\
    1797	:	21156	Bangun Raya	Raya Kahean	Kab.	Simalungun	Sumatera Utara	,\
    1798	:	21156	Durian Banggal	Raya Kahean	Kab.	Simalungun	Sumatera Utara	,\
    1799	:	21156	Gunung Datas	Raya Kahean	Kab.	Simalungun	Sumatera Utara	,\
    1800	:	21156	Panduman	Raya Kahean	Kab.	Simalungun	Sumatera Utara	,\
    1801	:	21156	Puli Buah	Raya Kahean	Kab.	Simalungun	Sumatera Utara	,\
    1802	:	21156	Sambosar Raya	Raya Kahean	Kab.	Simalungun	Sumatera Utara	,\
    1803	:	21156	Sindar Raya	Raya Kahean	Kab.	Simalungun	Sumatera Utara	,\
    1804	:	21156	Sorba Dolog	Raya Kahean	Kab.	Simalungun	Sumatera Utara	,\
    1805	:	21162	Bah Bolon	Raya	Kab.	Simalungun	Sumatera Utara	,\
    1806	:	21162	Bahapal Raya	Raya	Kab.	Simalungun	Sumatera Utara	,\
    1807	:	21162	Dalig Raya	Raya	Kab.	Simalungun	Sumatera Utara	,\
    1808	:	21162	Dolok Huluan	Raya	Kab.	Simalungun	Sumatera Utara	,\
    1809	:	21162	Merek Raya	Raya	Kab.	Simalungun	Sumatera Utara	,\
    1810	:	21162	Pematang Raya	Raya	Kab.	Simalungun	Sumatera Utara	,\
    1811	:	21162	Raya Bayu	Raya	Kab.	Simalungun	Sumatera Utara	,\
    1812	:	21162	Raya Huluan	Raya	Kab.	Simalungun	Sumatera Utara	,\
    1813	:	21162	Raya Usang	Raya	Kab.	Simalungun	Sumatera Utara	,\
    1814	:	21162	Siporkas	Raya	Kab.	Simalungun	Sumatera Utara	,\
    1815	:	21162	Sondi Raya	Raya	Kab.	Simalungun	Sumatera Utara	,\
    1816	:	21264	Panca Arga	Rawang Panca Arga	Kab.	Asahan	Sumatera Utara	,\
    1817	:	21264	Pondok Bungur	Rawang Panca Arga	Kab.	Asahan	Sumatera Utara	,\
    1818	:	21264	Rawang Baru	Rawang Panca Arga	Kab.	Asahan	Sumatera Utara	,\
    1819	:	21264	Rawang Lama	Rawang Panca Arga	Kab.	Asahan	Sumatera Utara	,\
    1820	:	21264	Rawang Pasar IV	Rawang Panca Arga	Kab.	Asahan	Sumatera Utara	,\
    1821	:	21264	Rawang Pasar V	Rawang Panca Arga	Kab.	Asahan	Sumatera Utara	,\
    1822	:	21264	Rawang Pasar VI	Rawang Panca Arga	Kab.	Asahan	Sumatera Utara	,\
    1823	:	22983	Bangun Saroha	Ranto Baek/Baik	Kab.	Mandailing Natal	Sumatera Utara	,\
    1824	:	22983	Banjar Maga	Ranto Baek/Baik	Kab.	Mandailing Natal	Sumatera Utara	,\
    1825	:	22983	Gonting	Ranto Baek/Baik	Kab.	Mandailing Natal	Sumatera Utara	,\
    1826	:	22983	Huta Baringin	Ranto Baek/Baik	Kab.	Mandailing Natal	Sumatera Utara	,\
    1827	:	22983	Huta Nauli	Ranto Baek/Baik	Kab.	Mandailing Natal	Sumatera Utara	,\
    1828	:	22983	Huta Raja	Ranto Baek/Baik	Kab.	Mandailing Natal	Sumatera Utara	,\
    1829	:	22983	Lubuk Kancah	Ranto Baek/Baik	Kab.	Mandailing Natal	Sumatera Utara	,\
    1830	:	22983	Manisak	Ranto Baek/Baik	Kab.	Mandailing Natal	Sumatera Utara	,\
    1831	:	22983	Muara Bangko	Ranto Baek/Baik	Kab.	Mandailing Natal	Sumatera Utara	,\
    1832	:	22983	Ranto Nalinjang	Ranto Baek/Baik	Kab.	Mandailing Natal	Sumatera Utara	,\
    1833	:	22983	Ranto Panjang	Ranto Baek/Baik	Kab.	Mandailing Natal	Sumatera Utara	,\
    1834	:	22983	Sampuran	Ranto Baek/Baik	Kab.	Mandailing Natal	Sumatera Utara	,\
    1835	:	22983	Simaninggir	Ranto Baek/Baik	Kab.	Mandailing Natal	Sumatera Utara	,\
    1836	:	22983	Simpang Talap	Ranto Baek/Baik	Kab.	Mandailing Natal	Sumatera Utara	,\
    1837	:	22983	Tandikek	Ranto Baek/Baik	Kab.	Mandailing Natal	Sumatera Utara	,\
    1838	:	21419	Aek Paing	Rantau Utara	Kab.	Labuhan Batu	Sumatera Utara	,\
    1839	:	21416	Bina Raga (Rinaraga)	Rantau Utara	Kab.	Labuhan Batu	Sumatera Utara	,\
    1840	:	21417	Cendana	Rantau Utara	Kab.	Labuhan Batu	Sumatera Utara	,\
    1841	:	21418	Kartini	Rantau Utara	Kab.	Labuhan Batu	Sumatera Utara	,\
    1842	:	21414	Padang Bulan	Rantau Utara	Kab.	Labuhan Batu	Sumatera Utara	,\
    1843	:	21411	Padang Matingi	Rantau Utara	Kab.	Labuhan Batu	Sumatera Utara	,\
    1844	:	21419	Pulo Padang	Rantau Utara	Kab.	Labuhan Batu	Sumatera Utara	,\
    1845	:	21412	Rantauprapat	Rantau Utara	Kab.	Labuhan Batu	Sumatera Utara	,\
    1846	:	21414	Sirandorung	Rantau Utara	Kab.	Labuhan Batu	Sumatera Utara	,\
    1847	:	21413	Siringo-Ringo	Rantau Utara	Kab.	Labuhan Batu	Sumatera Utara	,\
    1848	:	21421	Bakaran Batu	Rantau Selatan	Kab.	Labuhan Batu	Sumatera Utara	,\
    1849	:	21427	Danobale	Rantau Selatan	Kab.	Labuhan Batu	Sumatera Utara	,\
    1850	:	21423	Lobu Sona	Rantau Selatan	Kab.	Labuhan Batu	Sumatera Utara	,\
    1851	:	21426	Perdamean	Rantau Selatan	Kab.	Labuhan Batu	Sumatera Utara	,\
    1852	:	21424	Sidorejo	Rantau Selatan	Kab.	Labuhan Batu	Sumatera Utara	,\
    1853	:	21425	Sigambal	Rantau Selatan	Kab.	Labuhan Batu	Sumatera Utara	,\
    1854	:	21428	Sioldengan	Rantau Selatan	Kab.	Labuhan Batu	Sumatera Utara	,\
    1855	:	21422	Ujung Bandar	Rantau Selatan	Kab.	Labuhan Batu	Sumatera Utara	,\
    1856	:	21429	Urung Kompas	Rantau Selatan	Kab.	Labuhan Batu	Sumatera Utara	,\
    1857	:	20611	Karya Jaya	Rambutan	Kota	Tebing Tinggi	Sumatera Utara	,\
    1858	:	20614	Lalang	Rambutan	Kota	Tebing Tinggi	Sumatera Utara	,\
    1859	:	20616	Mekar Sentosa	Rambutan	Kota	Tebing Tinggi	Sumatera Utara	,\
    1860	:	20614	Rantau Laban	Rambutan	Kota	Tebing Tinggi	Sumatera Utara	,\
    1861	:	20616	Sri Padang	Rambutan	Kota	Tebing Tinggi	Sumatera Utara	,\
    1862	:	20616	Tanjung Marulak	Rambutan	Kota	Tebing Tinggi	Sumatera Utara	,\
    1863	:	20616	Tanjung Marulak Hilir	Rambutan	Kota	Tebing Tinggi	Sumatera Utara	,\
    1864	:	21274	Batu Anam	Rahuning	Kab.	Asahan	Sumatera Utara	,\
    1865	:	21274	Gunung Melayu	Rahuning	Kab.	Asahan	Sumatera Utara	,\
    1866	:	21274	Perkebunan Aek Nagaga	Rahuning	Kab.	Asahan	Sumatera Utara	,\
    1867	:	21274	Perkebunan Gunung Melayu	Rahuning	Kab.	Asahan	Sumatera Utara	,\
    1868	:	21274	Rahuning	Rahuning	Kab.	Asahan	Sumatera Utara	,\
    1869	:	21274	Rahuning I	Rahuning	Kab.	Asahan	Sumatera Utara	,\
    1870	:	21274	Rahuning II	Rahuning	Kab.	Asahan	Sumatera Utara	,\
    1871	:	22465	Bonani Dolok	Purbatua	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1872	:	22465	Huta Nagodang	Purbatua	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1873	:	22465	Janji Nauli	Purbatua	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1874	:	22465	Pardomuan Janji Angkola	Purbatua	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1875	:	22465	Parsaoran Janji Angkola	Purbatua	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1876	:	22465	Purbatua	Purbatua	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1877	:	22465	Robean	Purbatua	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1878	:	22465	Selamat	Purbatua	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1879	:	22465	Sibulan Bulan	Purbatua	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1880	:	22465	Sidua Bahal	Purbatua	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1881	:	22465	Sitolu Ompu (Bahal)	Purbatua	Kab.	Tapanuli Utara	Sumatera Utara	,\
    1882	:	21165	Hinalang (Kinalang)	Purba	Kab.	Simalungun	Sumatera Utara	,\
    1883	:	21165	Huta Raja	Purba	Kab.	Simalungun	Sumatera Utara	,\
    1884	:	21165	Pematang Purba	Purba	Kab.	Simalungun	Sumatera Utara	,\
    1885	:	21165	Purba Dolog	Purba	Kab.	Simalungun	Sumatera Utara	,\
    1886	:	21165	Purba Sipinggan	Purba	Kab.	Simalungun	Sumatera Utara	,\
    1887	:	21165	Purba Tengah/Tongah	Purba	Kab.	Simalungun	Sumatera Utara	,\
    1888	:	21165	Seribu Jadi	Purba	Kab.	Simalungun	Sumatera Utara	,\
    1889	:	21165	Tanoh/Tano Tinggir	Purba	Kab.	Simalungun	Sumatera Utara	,\
    1890	:	21165	Tiga Runggu	Purba	Kab.	Simalungun	Sumatera Utara	,\
    1891	:	21165	Urung Purba	Purba	Kab.	Simalungun	Sumatera Utara	,\
    1892	:	22994	Handel	Puncak Sorik Marapi/Merapi	Kab.	Mandailing Natal	Sumatera Utara	,\
    1893	:	22994	Huta Barat	Puncak Sorik Marapi/Merapi	Kab.	Mandailing Natal	Sumatera Utara	,\
    1894	:	22994	Huta Lombang	Puncak Sorik Marapi/Merapi	Kab.	Mandailing Natal	Sumatera Utara	,\
    1895	:	22994	Hutabaringin Julu	Puncak Sorik Marapi/Merapi	Kab.	Mandailing Natal	Sumatera Utara	,\
    1896	:	22994	Hutanamale	Puncak Sorik Marapi/Merapi	Kab.	Mandailing Natal	Sumatera Utara	,\
    1897	:	22994	Hutatinggi	Puncak Sorik Marapi/Merapi	Kab.	Mandailing Natal	Sumatera Utara	,\
    1898	:	22994	Purba Julu	Puncak Sorik Marapi/Merapi	Kab.	Mandailing Natal	Sumatera Utara	,\
    1899	:	22994	Sibanggor Jae	Puncak Sorik Marapi/Merapi	Kab.	Mandailing Natal	Sumatera Utara	,\
    1900	:	22994	Sibanggor Julu	Puncak Sorik Marapi/Merapi	Kab.	Mandailing Natal	Sumatera Utara	,\
    1901	:	22994	Sibanggor Tonga	Puncak Sorik Marapi/Merapi	Kab.	Mandailing Natal	Sumatera Utara	,\
    1902	:	21264	Bunut Seberang	Pulo Bandring	Kab.	Asahan	Sumatera Utara	,\
    1903	:	21264	Gedangan	Pulo Bandring	Kab.	Asahan	Sumatera Utara	,\
    1904	:	21264	Perhutaan Silau	Pulo Bandring	Kab.	Asahan	Sumatera Utara	,\
    1905	:	21264	Pulo Bandring	Pulo Bandring	Kab.	Asahan	Sumatera Utara	,\
    1906	:	21264	Sidomulyo	Pulo Bandring	Kab.	Asahan	Sumatera Utara	,\
    1907	:	21264	Suka Damai	Pulo Bandring	Kab.	Asahan	Sumatera Utara	,\
    1908	:	21264	Suka Damai Barat	Pulo Bandring	Kab.	Asahan	Sumatera Utara	,\
    1909	:	21264	Suka Makmur	Pulo Bandring	Kab.	Asahan	Sumatera Utara	,\
    1910	:	21264	Taman Sari	Pulo Bandring	Kab.	Asahan	Sumatera Utara	,\
    1911	:	21264	Tanah Rakyat	Pulo Bandring	Kab.	Asahan	Sumatera Utara	,\
    1912	:	22881	Afore Gobo	Pulau-Pulau Batu Utara	Kab.	Nias Selatan	Sumatera Utara	,\
    1913	:	22881	Bale-Bale	Pulau-Pulau Batu Utara	Kab.	Nias Selatan	Sumatera Utara	,\
    1914	:	22881	Bale-Bale Sibohou	Pulau-Pulau Batu Utara	Kab.	Nias Selatan	Sumatera Utara	,\
    1915	:	22881	Limo Biang	Pulau-Pulau Batu Utara	Kab.	Nias Selatan	Sumatera Utara	,\
    1916	:	22881	Majino Lorang	Pulau-Pulau Batu Utara	Kab.	Nias Selatan	Sumatera Utara	,\
    1917	:	22881	Memong	Pulau-Pulau Batu Utara	Kab.	Nias Selatan	Sumatera Utara	,\
    1918	:	22881	Merit Baru	Pulau-Pulau Batu Utara	Kab.	Nias Selatan	Sumatera Utara	,\
    1919	:	22881	Siofa Banua Lorang	Pulau-Pulau Batu Utara	Kab.	Nias Selatan	Sumatera Utara	,\
    1920	:	22881	Siofa Banua Marit	Pulau-Pulau Batu Utara	Kab.	Nias Selatan	Sumatera Utara	,\
    1921	:	22881	Teluk Limo	Pulau-Pulau Batu Utara	Kab.	Nias Selatan	Sumatera Utara	,\
    1922	:	22881	Wawa	Pulau-Pulau Batu Utara	Kab.	Nias Selatan	Sumatera Utara	,\
    1923	:	22881	Ziabiang	Pulau-Pulau Batu Utara	Kab.	Nias Selatan	Sumatera Utara	,\
    1924	:	22881	Adam	Pulau-Pulau Batu Timur	Kab.	Nias Selatan	Sumatera Utara	,\
    1925	:	22881	Bais	Pulau-Pulau Batu Timur	Kab.	Nias Selatan	Sumatera Utara	,\
    1926	:	22881	Bais Baru	Pulau-Pulau Batu Timur	Kab.	Nias Selatan	Sumatera Utara	,\
    1927	:	22881	Labara	Pulau-Pulau Batu Timur	Kab.	Nias Selatan	Sumatera Utara	,\
    1928	:	22881	Labuan Bajau	Pulau-Pulau Batu Timur	Kab.	Nias Selatan	Sumatera Utara	,\
    1929	:	22881	Labuan Hiu / Hiyu	Pulau-Pulau Batu Timur	Kab.	Nias Selatan	Sumatera Utara	,\
    1930	:	22881	Labuan Rima	Pulau-Pulau Batu Timur	Kab.	Nias Selatan	Sumatera Utara	,\
    1931	:	22881	Labuan Rima Baru	Pulau-Pulau Batu Timur	Kab.	Nias Selatan	Sumatera Utara	,\
    1932	:	22881	Lambak	Pulau-Pulau Batu Timur	Kab.	Nias Selatan	Sumatera Utara	,\
    1933	:	22881	Mahang Labara	Pulau-Pulau Batu Timur	Kab.	Nias Selatan	Sumatera Utara	,\
    1934	:	22881	Bawolawindra	Pulau-Pulau Batu Barat	Kab.	Nias Selatan	Sumatera Utara	,\
    1935	:	22881	Bawositora	Pulau-Pulau Batu Barat	Kab.	Nias Selatan	Sumatera Utara	,\
    1936	:	22881	Bintuang	Pulau-Pulau Batu Barat	Kab.	Nias Selatan	Sumatera Utara	,\
    1937	:	22881	Fuge	Pulau-Pulau Batu Barat	Kab.	Nias Selatan	Sumatera Utara	,\
    1938	:	22881	Hayo	Pulau-Pulau Batu Barat	Kab.	Nias Selatan	Sumatera Utara	,\
    1939	:	22881	Hilizamorogotano	Pulau-Pulau Batu Barat	Kab.	Nias Selatan	Sumatera Utara	,\
    1940	:	22881	Luaha Idanopono	Pulau-Pulau Batu Barat	Kab.	Nias Selatan	Sumatera Utara	,\
    1941	:	22881	Sibaranun	Pulau-Pulau Batu Barat	Kab.	Nias Selatan	Sumatera Utara	,\
    1942	:	22881	Sigese	Pulau-Pulau Batu Barat	Kab.	Nias Selatan	Sumatera Utara	,\
    1943	:	22881	Balogia	Pulau-Pulau Batu	Kab.	Nias Selatan	Sumatera Utara	,\
    1944	:	22881	Baruyu Lasara	Pulau-Pulau Batu	Kab.	Nias Selatan	Sumatera Utara	,\
    1945	:	22881	Bawo Ama Helato	Pulau-Pulau Batu	Kab.	Nias Selatan	Sumatera Utara	,\
    1946	:	22881	Bawo Omasio	Pulau-Pulau Batu	Kab.	Nias Selatan	Sumatera Utara	,\
    1947	:	22881	Bawodobara	Pulau-Pulau Batu	Kab.	Nias Selatan	Sumatera Utara	,\
    1948	:	22881	Hili Amo Dula	Pulau-Pulau Batu	Kab.	Nias Selatan	Sumatera Utara	,\
    1949	:	22881	Hiliotalua	Pulau-Pulau Batu	Kab.	Nias Selatan	Sumatera Utara	,\
    1950	:	22881	Koto	Pulau-Pulau Batu	Kab.	Nias Selatan	Sumatera Utara	,\
    1951	:	22881	Lasonde	Pulau-Pulau Batu	Kab.	Nias Selatan	Sumatera Utara	,\
    1952	:	22881	Loboi	Pulau-Pulau Batu	Kab.	Nias Selatan	Sumatera Utara	,\
    1953	:	22881	Onaya	Pulau-Pulau Batu	Kab.	Nias Selatan	Sumatera Utara	,\
    1954	:	22881	Orahili	Pulau-Pulau Batu	Kab.	Nias Selatan	Sumatera Utara	,\
    1955	:	22881	Pasar Pulau Telo	Pulau-Pulau Batu	Kab.	Nias Selatan	Sumatera Utara	,\
    1956	:	22881	Rapa Rapa Melayu	Pulau-Pulau Batu	Kab.	Nias Selatan	Sumatera Utara	,\
    1957	:	22881	Sebuasi	Pulau-Pulau Batu	Kab.	Nias Selatan	Sumatera Utara	,\
    1958	:	22881	Siduaewali	Pulau-Pulau Batu	Kab.	Nias Selatan	Sumatera Utara	,\
    1959	:	22881	Sifitu Ewali	Pulau-Pulau Batu	Kab.	Nias Selatan	Sumatera Utara	,\
    1960	:	22881	Silimaewali	Pulau-Pulau Batu	Kab.	Nias Selatan	Sumatera Utara	,\
    1961	:	22881	Simaluaya	Pulau-Pulau Batu	Kab.	Nias Selatan	Sumatera Utara	,\
    1962	:	22881	Sinauru	Pulau-Pulau Batu	Kab.	Nias Selatan	Sumatera Utara	,\
    1963	:	22881	Siofa Ewali	Pulau-Pulau Batu	Kab.	Nias Selatan	Sumatera Utara	,\
    1964	:	22881	Sisarahili	Pulau-Pulau Batu	Kab.	Nias Selatan	Sumatera Utara	,\
    1965	:	21273	Bangun	Pulau Rakyat	Kab.	Asahan	Sumatera Utara	,\
    1966	:	21273	Baru	Pulau Rakyat	Kab.	Asahan	Sumatera Utara	,\
    1967	:	21273	Manis	Pulau Rakyat	Kab.	Asahan	Sumatera Utara	,\
    1968	:	21273	Ofa Padang Mahondang	Pulau Rakyat	Kab.	Asahan	Sumatera Utara	,\
    1969	:	21273	Orika	Pulau Rakyat	Kab.	Asahan	Sumatera Utara	,\
    1970	:	21273	Padang Mahondang	Pulau Rakyat	Kab.	Asahan	Sumatera Utara	,\
    1971	:	21273	Persatuan	Pulau Rakyat	Kab.	Asahan	Sumatera Utara	,\
    1972	:	21273	Pulau Rakyat Pekan	Pulau Rakyat	Kab.	Asahan	Sumatera Utara	,\
    1973	:	21273	Pulau Rakyat Tua	Pulau Rakyat	Kab.	Asahan	Sumatera Utara	,\
    1974	:	21273	Sei Piring	Pulau Rakyat	Kab.	Asahan	Sumatera Utara	,\
    1975	:	21273	Tunggul Empat Lima (45)	Pulau Rakyat	Kab.	Asahan	Sumatera Utara	,\
    1976	:	22741	Aek Haruya	Portibi	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1977	:	22741	Aek Siala	Portibi	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1978	:	22741	Aek Torop	Portibi	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1979	:	22741	Aloban	Portibi	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1980	:	22741	Bahal	Portibi	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1981	:	22741	Balakka Torop (Balangka Torop)	Portibi	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1982	:	22741	Bangkudu (Bakkudu)	Portibi	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1983	:	22741	Bara	Portibi	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1984	:	22741	Guma Rupu Lama	Portibi	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1985	:	22741	Gumarupu Baru	Portibi	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1986	:	22741	Gunung Baringin	Portibi	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1987	:	22741	Gunung Manaon	Portibi	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1988	:	22741	Gunung Martua	Portibi	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1989	:	22741	Hadungdung	Portibi	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1990	:	22741	Hotang Sasa	Portibi	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1991	:	22741	Janji Matogu	Portibi	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1992	:	22741	Lantosan I	Portibi	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1993	:	22741	Mangaledang	Portibi	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1994	:	22741	Mangaledang Lama	Portibi	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1995	:	22741	Muara Sigama	Portibi	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1996	:	22741	Napa Halas	Portibi	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1997	:	22741	Napa Lombang	Portibi	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1998	:	22741	Padang Manjoir	Portibi	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    1999	:	22741	Parsarmaan (Parsamaan)	Portibi	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2000	:	22741	Pasir Pinang	Portibi	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2001	:	22741	Pijor Koling	Portibi	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2002	:	22741	Portibi Jae	Portibi	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2003	:	22741	Portibi Julu	Portibi	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2004	:	22741	Purba Tua Dolok	Portibi	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2005	:	22741	Rondaman Dolok (Ronda Mandolok)	Portibi	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2006	:	22741	Rondaman Lombang (Ronda Manlombang)	Portibi	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2007	:	22741	Sigama Napa Halas/Alas	Portibi	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2008	:	22741	Sihambeng	Portibi	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2009	:	22741	Simandi Angin	Portibi	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2010	:	22741	Sipirok	Portibi	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2011	:	22741	Sitopayan	Portibi	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2012	:	22741	Tanjung Salamat/Selamat	Portibi	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2013	:	22741	Torluk Muara Dolok	Portibi	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2014	:	22384	Amborgang	Porsea	Kab.	Toba Samosir	Sumatera Utara	,\
    2015	:	22384	Gala Gala Pangkailan	Porsea	Kab.	Toba Samosir	Sumatera Utara	,\
    2016	:	22384	Lumban Gurning	Porsea	Kab.	Toba Samosir	Sumatera Utara	,\
    2017	:	22384	Nalela	Porsea	Kab.	Toba Samosir	Sumatera Utara	,\
    2018	:	22384	Parparean I	Porsea	Kab.	Toba Samosir	Sumatera Utara	,\
    2019	:	22384	Parparean II	Porsea	Kab.	Toba Samosir	Sumatera Utara	,\
    2020	:	22384	Parparean III	Porsea	Kab.	Toba Samosir	Sumatera Utara	,\
    2021	:	22384	Parparean IV	Porsea	Kab.	Toba Samosir	Sumatera Utara	,\
    2022	:	22384	Pasar Porsea	Porsea	Kab.	Toba Samosir	Sumatera Utara	,\
    2023	:	22384	Patane I	Porsea	Kab.	Toba Samosir	Sumatera Utara	,\
    2024	:	22384	Patane II	Porsea	Kab.	Toba Samosir	Sumatera Utara	,\
    2025	:	22384	Patane III	Porsea	Kab.	Toba Samosir	Sumatera Utara	,\
    2026	:	22384	Patane IV	Porsea	Kab.	Toba Samosir	Sumatera Utara	,\
    2027	:	22384	Patane V	Porsea	Kab.	Toba Samosir	Sumatera Utara	,\
    2028	:	22384	Raut Bosi	Porsea	Kab.	Toba Samosir	Sumatera Utara	,\
    2029	:	22384	Silamosik I	Porsea	Kab.	Toba Samosir	Sumatera Utara	,\
    2030	:	22384	Simpang Sigura-Gura	Porsea	Kab.	Toba Samosir	Sumatera Utara	,\
    2031	:	22457	Aek Nauli I	Pollung	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2032	:	22457	Aek Nauli II	Pollung	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2033	:	22457	Huta Julu	Pollung	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2034	:	22457	Huta Paung	Pollung	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2035	:	22457	Huta Paung Utara	Pollung	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2036	:	22457	Pandumaan	Pollung	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2037	:	22457	Pansur Batu	Pollung	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2038	:	22457	Pardomuan	Pollung	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2039	:	22457	Parsingguran I	Pollung	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2040	:	22457	Parsingguran II	Pollung	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2041	:	22457	Pollung	Pollung	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2042	:	22457	Ria-Ria	Pollung	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2043	:	22457	Sipitu Huta	Pollung	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2044	:	22384	Ambar Halim	Pintu Pohan Meranti	Kab.	Toba Samosir	Sumatera Utara	,\
    2045	:	22384	Halado	Pintu Pohan Meranti	Kab.	Toba Samosir	Sumatera Utara	,\
    2046	:	22384	Meranti Tengah	Pintu Pohan Meranti	Kab.	Toba Samosir	Sumatera Utara	,\
    2047	:	22384	Meranti Timur	Pintu Pohan Meranti	Kab.	Toba Samosir	Sumatera Utara	,\
    2048	:	22384	Meranti Utara	Pintu Pohan Meranti	Kab.	Toba Samosir	Sumatera Utara	,\
    2049	:	22384	Pintu Pohan	Pintu Pohan Meranti	Kab.	Toba Samosir	Sumatera Utara	,\
    2050	:	22384	Pintu Pohan Dolok	Pintu Pohan Meranti	Kab.	Toba Samosir	Sumatera Utara	,\
    2051	:	22654	Gunung Marijo	Pinangsori	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    2052	:	22654	Parjalihotan Baru	Pinangsori	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    2053	:	22654	Pinang Baru	Pinangsori	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    2054	:	22654	Pinangsori	Pinangsori	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    2055	:	22654	Sihaporas	Pinangsori	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    2056	:	22654	Sitonong Bangun	Pinangsori	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    2057	:	22654	Toga Basir	Pinangsori	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    2058	:	22271	Aornakan I	Pergetteng Getteng Sengkut	Kab.	Pakpak Bharat	Sumatera Utara	,\
    2059	:	22271	Aornakan II	Pergetteng Getteng Sengkut	Kab.	Pakpak Bharat	Sumatera Utara	,\
    2060	:	22271	Kecupak I	Pergetteng Getteng Sengkut	Kab.	Pakpak Bharat	Sumatera Utara	,\
    2061	:	22271	Kecupak II	Pergetteng Getteng Sengkut	Kab.	Pakpak Bharat	Sumatera Utara	,\
    2062	:	22271	Simerpara	Pergetteng Getteng Sengkut	Kab.	Pakpak Bharat	Sumatera Utara	,\
    2063	:	20371	Amplas	Percut Sei Tuan	Kab.	Deli Serdang	Sumatera Utara	,\
    2064	:	20371	Bandar Khalifah (Klippa)	Percut Sei Tuan	Kab.	Deli Serdang	Sumatera Utara	,\
    2065	:	20371	Bandar Khalipah Kebon	Percut Sei Tuan	Kab.	Deli Serdang	Sumatera Utara	,\
    2066	:	20371	Bandar Setia	Percut Sei Tuan	Kab.	Deli Serdang	Sumatera Utara	,\
    2067	:	20371	Cinta Damai (Dame)	Percut Sei Tuan	Kab.	Deli Serdang	Sumatera Utara	,\
    2068	:	20371	Cinta Rakyat	Percut Sei Tuan	Kab.	Deli Serdang	Sumatera Utara	,\
    2069	:	20371	Kenangan	Percut Sei Tuan	Kab.	Deli Serdang	Sumatera Utara	,\
    2070	:	20371	Kenangan Baru	Percut Sei Tuan	Kab.	Deli Serdang	Sumatera Utara	,\
    2071	:	20371	Kolam	Percut Sei Tuan	Kab.	Deli Serdang	Sumatera Utara	,\
    2072	:	20371	Laut Dendang	Percut Sei Tuan	Kab.	Deli Serdang	Sumatera Utara	,\
    2073	:	20371	Medan Estate	Percut Sei Tuan	Kab.	Deli Serdang	Sumatera Utara	,\
    2074	:	20371	Pematang Lalang	Percut Sei Tuan	Kab.	Deli Serdang	Sumatera Utara	,\
    2075	:	20371	Percut	Percut Sei Tuan	Kab.	Deli Serdang	Sumatera Utara	,\
    2076	:	20371	Saentis	Percut Sei Tuan	Kab.	Deli Serdang	Sumatera Utara	,\
    2077	:	20371	Sampali	Percut Sei Tuan	Kab.	Deli Serdang	Sumatera Utara	,\
    2078	:	20371	Sei Rotan	Percut Sei Tuan	Kab.	Deli Serdang	Sumatera Utara	,\
    2079	:	20371	Sumber Rejo Timur	Percut Sei Tuan	Kab.	Deli Serdang	Sumatera Utara	,\
    2080	:	20371	Tanjung Rejo	Percut Sei Tuan	Kab.	Deli Serdang	Sumatera Utara	,\
    2081	:	20371	Tanjung Selamat	Percut Sei Tuan	Kab.	Deli Serdang	Sumatera Utara	,\
    2082	:	20371	Tembung	Percut Sei Tuan	Kab.	Deli Serdang	Sumatera Utara	,\
    2083	:	20986	Adolina	Perbaungan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2084	:	20986	Batang Terap	Perbaungan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2085	:	20986	Bengkel	Perbaungan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2086	:	20986	Cinta Air	Perbaungan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2087	:	20986	Citaman Jernih	Perbaungan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2088	:	20986	Deli Muda Ilir	Perbaungan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2089	:	20986	Deli Muda Ulu	Perbaungan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2090	:	20986	Jambur Pulau	Perbaungan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2091	:	20986	Kesatuan	Perbaungan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2092	:	20986	Kota Galuh	Perbaungan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2093	:	20986	Lidah Tanah	Perbaungan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2094	:	20986	Lubuk Bayas	Perbaungan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2095	:	20986	Lubuk Cemara	Perbaungan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2096	:	20986	Lubuk Dendang	Perbaungan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2097	:	20986	Lubuk Rotan	Perbaungan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2098	:	20986	Melati Dua	Perbaungan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2099	:	20986	Melati Satu	Perbaungan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2100	:	20986	Pematang Sijonam	Perbaungan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2101	:	20986	Pematang Tatal	Perbaungan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2102	:	20986	Sei/Sungai Buluh	Perbaungan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2103	:	20986	Sei/Sungai Naga Lawan	Perbaungan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2104	:	20986	Sei/Sungai Sijenggi	Perbaungan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2105	:	20986	Simpang Tiga Pekan	Perbaungan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2106	:	20986	Suka Beras	Perbaungan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2107	:	20986	Suka Jadi	Perbaungan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2108	:	20986	Tanah Merah	Perbaungan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2109	:	20986	Tanjung Buluh	Perbaungan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2110	:	20986	Tualang	Perbaungan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2111	:	21167	Mardinding	Pematang Silima Huta	Kab.	Simalungun	Sumatera Utara	,\
    2112	:	21167	Naga Mariah	Pematang Silima Huta	Kab.	Simalungun	Sumatera Utara	,\
    2113	:	21167	Naga Saribu	Pematang Silima Huta	Kab.	Simalungun	Sumatera Utara	,\
    2114	:	21167	Saribujandi/Saribu Janji	Pematang Silima Huta	Kab.	Simalungun	Sumatera Utara	,\
    2115	:	21167	Siboras	Pematang Silima Huta	Kab.	Simalungun	Sumatera Utara	,\
    2116	:	21167	Silimakuta Barat	Pematang Silima Huta	Kab.	Simalungun	Sumatera Utara	,\
    2117	:	21167	Ujung Mariah	Pematang Silima Huta	Kab.	Simalungun	Sumatera Utara	,\
    2118	:	21167	Ujung Saribu	Pematang Silima Huta	Kab.	Simalungun	Sumatera Utara	,\
    2119	:	21186	Bandar Manik	Pematang Sidamanik	Kab.	Simalungun	Sumatera Utara	,\
    2120	:	21186	Gorak	Pematang Sidamanik	Kab.	Simalungun	Sumatera Utara	,\
    2121	:	21186	Jorlang Huluan	Pematang Sidamanik	Kab.	Simalungun	Sumatera Utara	,\
    2122	:	21186	Pematang Sidamanik	Pematang Sidamanik	Kab.	Simalungun	Sumatera Utara	,\
    2123	:	21186	Pematang Tambun Raya	Pematang Sidamanik	Kab.	Simalungun	Sumatera Utara	,\
    2124	:	21186	Sait Buttu Saribu	Pematang Sidamanik	Kab.	Simalungun	Sumatera Utara	,\
    2125	:	21186	Sarimattin	Pematang Sidamanik	Kab.	Simalungun	Sumatera Utara	,\
    2126	:	21186	Sihaporas	Pematang Sidamanik	Kab.	Simalungun	Sumatera Utara	,\
    2127	:	21186	Simantin	Pematang Sidamanik	Kab.	Simalungun	Sumatera Utara	,\
    2128	:	21186	Sipolha Horisan	Pematang Sidamanik	Kab.	Simalungun	Sumatera Utara	,\
    2129	:	20858	Damar Condong	Pematang Jaya	Kab.	Langkat	Sumatera Utara	,\
    2130	:	20858	Limau Mungkur	Pematang Jaya	Kab.	Langkat	Sumatera Utara	,\
    2131	:	20858	Pematang Tengah	Pematang Jaya	Kab.	Langkat	Sumatera Utara	,\
    2132	:	20858	Perkebunan Damar Condong	Pematang Jaya	Kab.	Langkat	Sumatera Utara	,\
    2133	:	20858	Perkebunan Perapen	Pematang Jaya	Kab.	Langkat	Sumatera Utara	,\
    2134	:	20859	Salahaji	Pematang Jaya	Kab.	Langkat	Sumatera Utara	,\
    2135	:	20859	Serang Jaya	Pematang Jaya	Kab.	Langkat	Sumatera Utara	,\
    2136	:	20859	Serang Jaya Hilir	Pematang Jaya	Kab.	Langkat	Sumatera Utara	,\
    2137	:	21186	Bandar Manis	Pematang Bandar	Kab.	Simalungun	Sumatera Utara	,\
    2138	:	21186	Kandangan	Pematang Bandar	Kab.	Simalungun	Sumatera Utara	,\
    2139	:	21186	Kerasaan I	Pematang Bandar	Kab.	Simalungun	Sumatera Utara	,\
    2140	:	21186	Kerasaan II	Pematang Bandar	Kab.	Simalungun	Sumatera Utara	,\
    2141	:	21186	Mariah Bandar	Pematang Bandar	Kab.	Simalungun	Sumatera Utara	,\
    2142	:	21186	Pardomuan Nauli	Pematang Bandar	Kab.	Simalungun	Sumatera Utara	,\
    2143	:	21186	Pematang Bandar	Pematang Bandar	Kab.	Simalungun	Sumatera Utara	,\
    2144	:	21186	Purba Ganda	Pematang Bandar	Kab.	Simalungun	Sumatera Utara	,\
    2145	:	21186	Purwosari	Pematang Bandar	Kab.	Simalungun	Sumatera Utara	,\
    2146	:	21186	Talun Madear	Pematang Bandar	Kab.	Simalungun	Sumatera Utara	,\
    2147	:	21186	Talun Rejo	Pematang Bandar	Kab.	Simalungun	Sumatera Utara	,\
    2148	:	21186	Wonorejo	Pematang Bandar	Kab.	Simalungun	Sumatera Utara	,\
    2149	:	20986	Bengabing	Pegajahan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2150	:	20986	Bingkat	Pegajahan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2151	:	20986	Jati Mulyo	Pegajahan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2152	:	20986	Karang Anyar	Pegajahan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2153	:	20986	Lestari Dadi	Pegajahan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2154	:	20986	Melati Kebon/Kebun	Pegajahan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2155	:	20986	Pegajahan	Pegajahan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2156	:	20986	Pondok Tengah	Pegajahan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2157	:	20986	Putuaran/Petuaran Ilir	Pegajahan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2158	:	20986	Putuaran/Petuaran Ulu	Pegajahan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2159	:	20986	Senah/Sennah	Pegajahan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2160	:	20986	Sukasari	Pegajahan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2161	:	20986	Tanjung Putus	Pegajahan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2162	:	22283	Bandar Huta Usang	Pegagan Hilir	Kab.	Dairi	Sumatera Utara	,\
    2163	:	22283	Bukittinggi	Pegagan Hilir	Kab.	Dairi	Sumatera Utara	,\
    2164	:	22283	Laksa	Pegagan Hilir	Kab.	Dairi	Sumatera Utara	,\
    2165	:	22283	Lingga Raja	Pegagan Hilir	Kab.	Dairi	Sumatera Utara	,\
    2166	:	22283	Onan Lama	Pegagan Hilir	Kab.	Dairi	Sumatera Utara	,\
    2167	:	22283	Simanduma	Pegagan Hilir	Kab.	Dairi	Sumatera Utara	,\
    2168	:	22283	Tanjung Saluksuk	Pegagan Hilir	Kab.	Dairi	Sumatera Utara	,\
    2169	:	22154	Batukarang	Payung	Kab.	Karo	Sumatera Utara	,\
    2170	:	22154	Cimbang	Payung	Kab.	Karo	Sumatera Utara	,\
    2171	:	22154	Gurukinayan	Payung	Kab.	Karo	Sumatera Utara	,\
    2172	:	22154	Payung	Payung	Kab.	Karo	Sumatera Utara	,\
    2173	:	22154	Rimokayu	Payung	Kab.	Karo	Sumatera Utara	,\
    2174	:	22154	Selandi	Payung	Kab.	Karo	Sumatera Utara	,\
    2175	:	22154	Suka Meriah	Payung	Kab.	Karo	Sumatera Utara	,\
    2176	:	22154	Ujung Payung	Payung	Kab.	Karo	Sumatera Utara	,\
    2177	:	20361	Lantasan Baru	Patumbak	Kab.	Deli Serdang	Sumatera Utara	,\
    2178	:	20361	Lantasan Lama	Patumbak	Kab.	Deli Serdang	Sumatera Utara	,\
    2179	:	20361	Marindal Dua	Patumbak	Kab.	Deli Serdang	Sumatera Utara	,\
    2180	:	20361	Marindal Satu	Patumbak	Kab.	Deli Serdang	Sumatera Utara	,\
    2181	:	20361	Patumbak Dua	Patumbak	Kab.	Deli Serdang	Sumatera Utara	,\
    2182	:	20361	Patumbak Kampung	Patumbak	Kab.	Deli Serdang	Sumatera Utara	,\
    2183	:	20361	Patumbak Satu	Patumbak	Kab.	Deli Serdang	Sumatera Utara	,\
    2184	:	20361	Sigara Gara	Patumbak	Kab.	Deli Serdang	Sumatera Utara	,\
    2185	:	22563	Aek Nadua	Pasaribu Tobing	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    2186	:	22563	Makmur	Pasaribu Tobing	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    2187	:	22563	Pasaribu Tobing	Pasaribu Tobing	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    2188	:	22563	Sidaling	Pasaribu Tobing	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    2189	:	22563	Simargarap	Pasaribu Tobing	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    2190	:	22563	Sipakpahi	Pasaribu Tobing	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    2191	:	22563	Suga-Suga (Hutagodang)	Pasaribu Tobing	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    2192	:	22563	Suka Maju	Pasaribu Tobing	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    2193	:	22453	Aek Raja	Parmonangan	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2194	:	22453	Batu Arimo	Parmonangan	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2195	:	22453	Horison Ranggigit	Parmonangan	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2196	:	22453	Hutajulu	Parmonangan	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2197	:	22453	Hutajulu Parbalik/Purbalik	Parmonangan	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2198	:	22453	Hutatinggi	Parmonangan	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2199	:	22453	Hutatua	Parmonangan	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2200	:	22453	Lobusunut	Parmonangan	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2201	:	22453	Manalu	Parmonangan	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2202	:	22453	Manalu Dolok	Parmonangan	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2203	:	22453	Manalu Purba	Parmonangan	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2204	:	22453	Pertengahan	Parmonangan	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2205	:	22453	Purba Dolok	Parmonangan	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2206	:	22453	Sisordak	Parmonangan	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2207	:	22384	Banjar Ganjang	Parmaksian	Kab.	Toba Samosir	Sumatera Utara	,\
    2208	:	22384	Bius Gu Barat	Parmaksian	Kab.	Toba Samosir	Sumatera Utara	,\
    2209	:	22384	Dolok Nauli	Parmaksian	Kab.	Toba Samosir	Sumatera Utara	,\
    2210	:	22384	Jonggi Manulus	Parmaksian	Kab.	Toba Samosir	Sumatera Utara	,\
    2211	:	22384	Lumban Huala	Parmaksian	Kab.	Toba Samosir	Sumatera Utara	,\
    2212	:	22384	Lumban Manurung	Parmaksian	Kab.	Toba Samosir	Sumatera Utara	,\
    2213	:	22384	Lumban Sitorus	Parmaksian	Kab.	Toba Samosir	Sumatera Utara	,\
    2214	:	22384	Pangombusan	Parmaksian	Kab.	Toba Samosir	Sumatera Utara	,\
    2215	:	22384	Siantar Utara	Parmaksian	Kab.	Toba Samosir	Sumatera Utara	,\
    2216	:	22384	Tangga Batu I	Parmaksian	Kab.	Toba Samosir	Sumatera Utara	,\
    2217	:	22384	Tangga Batu II	Parmaksian	Kab.	Toba Samosir	Sumatera Utara	,\
    2218	:	22456	Baringin	Parlilitan	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2219	:	22456	Baringin Natam	Parlilitan	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2220	:	22456	Janji Hutanapa	Parlilitan	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2221	:	22456	Pusuk I	Parlilitan	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2222	:	22456	Pusuk II Simaninggir	Parlilitan	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2223	:	22456	Sihotang Hasugian Dolok I	Parlilitan	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2224	:	22456	Sihotang Hasugian Dolok II	Parlilitan	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2225	:	22456	Sihotang Hasugian Habinsaran	Parlilitan	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2226	:	22456	Sihotang Hasugian Tonga	Parlilitan	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2227	:	22456	Simataniari	Parlilitan	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2228	:	22456	Sionom Hudon Julu	Parlilitan	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2229	:	22456	Sionom Hudon Runggu	Parlilitan	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2230	:	22456	Sionom Hudon Selatan	Parlilitan	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2231	:	22456	Sionom Hudon Sibulbulon	Parlilitan	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2232	:	22456	Sionom Hudon Timur	Parlilitan	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2233	:	22456	Sionom Hudon Timur II	Parlilitan	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2234	:	22456	Sionom Hudon Tonga	Parlilitan	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2235	:	22456	Sionom Hudon Toruan	Parlilitan	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2236	:	22456	Sionom Hudon Utara	Parlilitan	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2237	:	22456	Sionom Hudon VII	Parlilitan	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2238	:	22282	Bangun	Parbuluan	Kab.	Dairi	Sumatera Utara	,\
    2239	:	22282	Lae Hole	Parbuluan	Kab.	Dairi	Sumatera Utara	,\
    2240	:	22282	Parbuluan I	Parbuluan	Kab.	Dairi	Sumatera Utara	,\
    2241	:	22282	Parbuluan II	Parbuluan	Kab.	Dairi	Sumatera Utara	,\
    2242	:	22282	Parbuluan III	Parbuluan	Kab.	Dairi	Sumatera Utara	,\
    2243	:	22282	Parbuluan IV	Parbuluan	Kab.	Dairi	Sumatera Utara	,\
    2244	:	22282	Parbuluan V	Parbuluan	Kab.	Dairi	Sumatera Utara	,\
    2245	:	22282	Parbuluan VI	Parbuluan	Kab.	Dairi	Sumatera Utara	,\
    2246	:	22475	Lobu Tolong	Paranginan	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2247	:	22475	Lobutolong Habinsaran	Paranginan	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2248	:	22475	Lumban Barat	Paranginan	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2249	:	22475	Lumban Sialaman	Paranginan	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2250	:	22475	Lumban Sianturi	Paranginan	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2251	:	22475	Paranginan Selatan	Paranginan	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2252	:	22475	Paranginan Utara	Paranginan	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2253	:	22475	Pearung	Paranginan	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2254	:	22475	Pearung Silali	Paranginan	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2255	:	22475	Siboru Torop	Paranginan	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2256	:	22475	Sihonongan	Paranginan	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2257	:	22978	Beringin/Baringin Jaya	Panyabungan Utara	Kab.	Mandailing Natal	Sumatera Utara	,\
    2258	:	22978	Binanga	Panyabungan Utara	Kab.	Mandailing Natal	Sumatera Utara	,\
    2259	:	22978	Huta Dame	Panyabungan Utara	Kab.	Mandailing Natal	Sumatera Utara	,\
    2260	:	22978	Hutabargot Simalang	Panyabungan Utara	Kab.	Mandailing Natal	Sumatera Utara	,\
    2261	:	22978	Hutanaingkan	Panyabungan Utara	Kab.	Mandailing Natal	Sumatera Utara	,\
    2262	:	22978	Jambur Padang Matinggi	Panyabungan Utara	Kab.	Mandailing Natal	Sumatera Utara	,\
    2263	:	22978	Kampung Baru	Panyabungan Utara	Kab.	Mandailing Natal	Sumatera Utara	,\
    2264	:	22978	Mompang Jae	Panyabungan Utara	Kab.	Mandailing Natal	Sumatera Utara	,\
    2265	:	22978	Mompang Julu	Panyabungan Utara	Kab.	Mandailing Natal	Sumatera Utara	,\
    2266	:	22978	Rumbio	Panyabungan Utara	Kab.	Mandailing Natal	Sumatera Utara	,\
    2267	:	22978	Simanondong	Panyabungan Utara	Kab.	Mandailing Natal	Sumatera Utara	,\
    2268	:	22978	Sopo Sorik	Panyabungan Utara	Kab.	Mandailing Natal	Sumatera Utara	,\
    2269	:	22978	Sukaramai	Panyabungan Utara	Kab.	Mandailing Natal	Sumatera Utara	,\
    2270	:	22978	Tanjung Mompang	Panyabungan Utara	Kab.	Mandailing Natal	Sumatera Utara	,\
    2271	:	22978	Tor Banua Raja	Panyabungan Utara	Kab.	Mandailing Natal	Sumatera Utara	,\
    2272	:	22912	Aek Nabara	Panyabungan Timur	Kab.	Mandailing Natal	Sumatera Utara	,\
    2273	:	22912	Banjar Lancat	Panyabungan Timur	Kab.	Mandailing Natal	Sumatera Utara	,\
    2274	:	22912	Gunung Baringin	Panyabungan Timur	Kab.	Mandailing Natal	Sumatera Utara	,\
    2275	:	22912	Huta Bangun	Panyabungan Timur	Kab.	Mandailing Natal	Sumatera Utara	,\
    2276	:	22912	Huta Rimbaru Gb	Panyabungan Timur	Kab.	Mandailing Natal	Sumatera Utara	,\
    2277	:	22912	Huta Tinggi	Panyabungan Timur	Kab.	Mandailing Natal	Sumatera Utara	,\
    2278	:	22912	Padang Laru	Panyabungan Timur	Kab.	Mandailing Natal	Sumatera Utara	,\
    2279	:	22912	Pagur	Panyabungan Timur	Kab.	Mandailing Natal	Sumatera Utara	,\
    2280	:	22912	Pardomuan	Panyabungan Timur	Kab.	Mandailing Natal	Sumatera Utara	,\
    2281	:	22912	Parmompang	Panyabungan Timur	Kab.	Mandailing Natal	Sumatera Utara	,\
    2282	:	22912	Ranto Natas	Panyabungan Timur	Kab.	Mandailing Natal	Sumatera Utara	,\
    2283	:	22912	Sirangkap	Panyabungan Timur	Kab.	Mandailing Natal	Sumatera Utara	,\
    2284	:	22912	Tanjung	Panyabungan Timur	Kab.	Mandailing Natal	Sumatera Utara	,\
    2285	:	22912	Tanjung Julu	Panyabungan Timur	Kab.	Mandailing Natal	Sumatera Utara	,\
    2286	:	22912	Tebing Tinggi	Panyabungan Timur	Kab.	Mandailing Natal	Sumatera Utara	,\
    2287	:	22952	Aek Ngali	Panyabungan Selatan	Kab.	Mandailing Natal	Sumatera Utara	,\
    2288	:	22952	Hayuraja	Panyabungan Selatan	Kab.	Mandailing Natal	Sumatera Utara	,\
    2289	:	22952	Hutaraja Hutajulu	Panyabungan Selatan	Kab.	Mandailing Natal	Sumatera Utara	,\
    2290	:	22952	Hutarimbaru	Panyabungan Selatan	Kab.	Mandailing Natal	Sumatera Utara	,\
    2291	:	22952	Kayu Laut	Panyabungan Selatan	Kab.	Mandailing Natal	Sumatera Utara	,\
    2292	:	22952	Lumban Dolok	Panyabungan Selatan	Kab.	Mandailing Natal	Sumatera Utara	,\
    2293	:	22952	Pagaran Gala-Gala	Panyabungan Selatan	Kab.	Mandailing Natal	Sumatera Utara	,\
    2294	:	22952	Roburan Dolok	Panyabungan Selatan	Kab.	Mandailing Natal	Sumatera Utara	,\
    2295	:	22952	Roburan Lombang	Panyabungan Selatan	Kab.	Mandailing Natal	Sumatera Utara	,\
    2296	:	22952	Tano Bato	Panyabungan Selatan	Kab.	Mandailing Natal	Sumatera Utara	,\
    2297	:	22912	Adian Jior	Panyabungan Kota	Kab.	Mandailing Natal	Sumatera Utara	,\
    2298	:	22912	Aek Banir	Panyabungan Kota	Kab.	Mandailing Natal	Sumatera Utara	,\
    2299	:	22912	Aek Mata	Panyabungan Kota	Kab.	Mandailing Natal	Sumatera Utara	,\
    2300	:	22912	Darussalam	Panyabungan Kota	Kab.	Mandailing Natal	Sumatera Utara	,\
    2301	:	22912	Gunung Barani	Panyabungan Kota	Kab.	Mandailing Natal	Sumatera Utara	,\
    2302	:	22912	Gunung Manaon	Panyabungan Kota	Kab.	Mandailing Natal	Sumatera Utara	,\
    2303	:	22918	Gunung Tua Jae	Panyabungan Kota	Kab.	Mandailing Natal	Sumatera Utara	,\
    2304	:	22918	Gunung Tua Julu	Panyabungan Kota	Kab.	Mandailing Natal	Sumatera Utara	,\
    2305	:	22918	Gunung Tua Labuan Pasir	Panyabungan Kota	Kab.	Mandailing Natal	Sumatera Utara	,\
    2306	:	22918	Gunung Tua Tonga	Panyabungan Kota	Kab.	Mandailing Natal	Sumatera Utara	,\
    2307	:	22912	Huta Lombang Lubis	Panyabungan Kota	Kab.	Mandailing Natal	Sumatera Utara	,\
    2308	:	22918	Ipar Bondar	Panyabungan Kota	Kab.	Mandailing Natal	Sumatera Utara	,\
    2309	:	22912	Kampung Padang	Panyabungan Kota	Kab.	Mandailing Natal	Sumatera Utara	,\
    2310	:	22919	Kayu Jati	Panyabungan Kota	Kab.	Mandailing Natal	Sumatera Utara	,\
    2311	:	22919	Kota Siantar	Panyabungan Kota	Kab.	Mandailing Natal	Sumatera Utara	,\
    2312	:	22912	Lumban Pasir	Panyabungan Kota	Kab.	Mandailing Natal	Sumatera Utara	,\
    2313	:	22912	Manyabar	Panyabungan Kota	Kab.	Mandailing Natal	Sumatera Utara	,\
    2314	:	22912	Pagaran Tonga	Panyabungan Kota	Kab.	Mandailing Natal	Sumatera Utara	,\
    2315	:	22912	Panyabungan I	Panyabungan Kota	Kab.	Mandailing Natal	Sumatera Utara	,\
    2316	:	22913	Panyabungan II	Panyabungan Kota	Kab.	Mandailing Natal	Sumatera Utara	,\
    2317	:	22911	Panyabungan III	Panyabungan Kota	Kab.	Mandailing Natal	Sumatera Utara	,\
    2318	:	22917	Panyabungan Jae	Panyabungan Kota	Kab.	Mandailing Natal	Sumatera Utara	,\
    2319	:	22916	Panyabungan Julu	Panyabungan Kota	Kab.	Mandailing Natal	Sumatera Utara	,\
    2320	:	22916	Panyabungan Tonga	Panyabungan Kota	Kab.	Mandailing Natal	Sumatera Utara	,\
    2321	:	22912	Parbangunan / Perbangunan	Panyabungan Kota	Kab.	Mandailing Natal	Sumatera Utara	,\
    2322	:	22916	Pasar Hilir	Panyabungan Kota	Kab.	Mandailing Natal	Sumatera Utara	,\
    2323	:	22915	Pidoli Dolok	Panyabungan Kota	Kab.	Mandailing Natal	Sumatera Utara	,\
    2324	:	22915	Pidoli Lombang	Panyabungan Kota	Kab.	Mandailing Natal	Sumatera Utara	,\
    2325	:	22912	Salambue	Panyabungan Kota	Kab.	Mandailing Natal	Sumatera Utara	,\
    2326	:	22912	Sarak Matua	Panyabungan Kota	Kab.	Mandailing Natal	Sumatera Utara	,\
    2327	:	22912	Sigalapang Julu	Panyabungan Kota	Kab.	Mandailing Natal	Sumatera Utara	,\
    2328	:	22912	Siobon	Panyabungan Kota	Kab.	Mandailing Natal	Sumatera Utara	,\
    2329	:	22912	Sipapaga	Panyabungan Kota	Kab.	Mandailing Natal	Sumatera Utara	,\
    2330	:	22912	Sopo Batu	Panyabungan Kota	Kab.	Mandailing Natal	Sumatera Utara	,\
    2331	:	22911	Barbaran	Panyabungan Barat	Kab.	Mandailing Natal	Sumatera Utara	,\
    2332	:	22911	Barbaran Jae	Panyabungan Barat	Kab.	Mandailing Natal	Sumatera Utara	,\
    2333	:	22911	Batang Gadis	Panyabungan Barat	Kab.	Mandailing Natal	Sumatera Utara	,\
    2334	:	22911	Huta Baringin	Panyabungan Barat	Kab.	Mandailing Natal	Sumatera Utara	,\
    2335	:	22911	Huta Tonga BB	Panyabungan Barat	Kab.	Mandailing Natal	Sumatera Utara	,\
    2336	:	22911	Longat	Panyabungan Barat	Kab.	Mandailing Natal	Sumatera Utara	,\
    2337	:	22911	Ruding	Panyabungan Barat	Kab.	Mandailing Natal	Sumatera Utara	,\
    2338	:	22911	Saba Jior	Panyabungan Barat	Kab.	Mandailing Natal	Sumatera Utara	,\
    2339	:	22911	Sirambas	Panyabungan Barat	Kab.	Mandailing Natal	Sumatera Utara	,\
    2340	:	20553	Bagan Serdang	Pantai Labu	Kab.	Deli Serdang	Sumatera Utara	,\
    2341	:	20553	Binjai Bakung	Pantai Labu	Kab.	Deli Serdang	Sumatera Utara	,\
    2342	:	20553	Denai Kuala	Pantai Labu	Kab.	Deli Serdang	Sumatera Utara	,\
    2343	:	20553	Denai Lama	Pantai Labu	Kab.	Deli Serdang	Sumatera Utara	,\
    2344	:	20553	Denai Sarang Burung	Pantai Labu	Kab.	Deli Serdang	Sumatera Utara	,\
    2345	:	20553	Durian	Pantai Labu	Kab.	Deli Serdang	Sumatera Utara	,\
    2346	:	20553	Kelambir	Pantai Labu	Kab.	Deli Serdang	Sumatera Utara	,\
    2347	:	20553	Kubah Sentang	Pantai Labu	Kab.	Deli Serdang	Sumatera Utara	,\
    2348	:	20553	Paluh Sebaji	Pantai Labu	Kab.	Deli Serdang	Sumatera Utara	,\
    2349	:	20553	Pantai Labu Baru	Pantai Labu	Kab.	Deli Serdang	Sumatera Utara	,\
    2350	:	20553	Pantai Labu Pekan	Pantai Labu	Kab.	Deli Serdang	Sumatera Utara	,\
    2351	:	20553	Pematang Biara	Pantai Labu	Kab.	Deli Serdang	Sumatera Utara	,\
    2352	:	20553	Perkebunan Ramonia (Ramunia)	Pantai Labu	Kab.	Deli Serdang	Sumatera Utara	,\
    2353	:	20553	Ramonia I (Ramunia Satu)	Pantai Labu	Kab.	Deli Serdang	Sumatera Utara	,\
    2354	:	20553	Ramonia II (Ramunia Dua)	Pantai Labu	Kab.	Deli Serdang	Sumatera Utara	,\
    2355	:	20553	Rantau Panjang	Pantai Labu	Kab.	Deli Serdang	Sumatera Utara	,\
    2356	:	20553	Regemuk	Pantai Labu	Kab.	Deli Serdang	Sumatera Utara	,\
    2357	:	20553	Sei Tuan	Pantai Labu	Kab.	Deli Serdang	Sumatera Utara	,\
    2358	:	20553	Tengah (Kampung Tengah)	Pantai Labu	Kab.	Deli Serdang	Sumatera Utara	,\
    2359	:	20987	Ara Payung	Pantai Cermin	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2360	:	20987	Besar 2 Terjun	Pantai Cermin	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2361	:	20987	Celawan	Pantai Cermin	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2362	:	20987	Kota Pari	Pantai Cermin	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2363	:	20987	Kuala Lama	Pantai Cermin	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2364	:	20987	Lubuk Saban	Pantai Cermin	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2365	:	20987	Naga Kisar	Pantai Cermin	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2366	:	20987	Pantai Cermin Kanan	Pantai Cermin	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2367	:	20987	Pantai Cermin Kiri	Pantai Cermin	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2368	:	20987	Pematang Kasih	Pantai Cermin	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2369	:	20987	Sementara	Pantai Cermin	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2370	:	20987	Ujung Rambung	Pantai Cermin	Kab.	Serdang Bedagai	Sumatera Utara	,\
    2371	:	21165	Banuh Raya	Panombeian Panei	Kab.	Simalungun	Sumatera Utara	,\
    2372	:	21165	Marjandi	Panombeian Panei	Kab.	Simalungun	Sumatera Utara	,\
    2373	:	21165	Marjandi Pisang	Panombeian Panei	Kab.	Simalungun	Sumatera Utara	,\
    2374	:	21165	Nagori Bosar	Panombeian Panei	Kab.	Simalungun	Sumatera Utara	,\
    2375	:	21165	Panombeian	Panombeian Panei	Kab.	Simalungun	Sumatera Utara	,\
    2376	:	21165	Pematang Pane	Panombeian Panei	Kab.	Simalungun	Sumatera Utara	,\
    2377	:	21165	Pematang Panombeian	Panombeian Panei	Kab.	Simalungun	Sumatera Utara	,\
    2378	:	21165	Simbolon Tengkoh	Panombeian Panei	Kab.	Simalungun	Sumatera Utara	,\
    2379	:	21165	Simpang Panei	Panombeian Panei	Kab.	Simalungun	Sumatera Utara	,\
    2380	:	21165	Talun Kondot	Panombeian Panei	Kab.	Simalungun	Sumatera Utara	,\
    2381	:	22392	Aek Nauli	Pangururan	Kab.	Samosir	Sumatera Utara	,\
    2382	:	22392	Huta Bolon	Pangururan	Kab.	Samosir	Sumatera Utara	,\
    2383	:	22392	Huta Namora	Pangururan	Kab.	Samosir	Sumatera Utara	,\
    2384	:	22392	Huta Tinggi	Pangururan	Kab.	Samosir	Sumatera Utara	,\
    2385	:	22392	Lumban Pinggol	Pangururan	Kab.	Samosir	Sumatera Utara	,\
    2386	:	22392	Lumban Suhi Suhi Dolok	Pangururan	Kab.	Samosir	Sumatera Utara	,\
    2387	:	22392	Lumban Suhi Suhi Toruan	Pangururan	Kab.	Samosir	Sumatera Utara	,\
    2388	:	22392	Panampangan	Pangururan	Kab.	Samosir	Sumatera Utara	,\
    2389	:	22392	Parbaba Dolok	Pangururan	Kab.	Samosir	Sumatera Utara	,\
    2390	:	22392	Pardomuan I	Pangururan	Kab.	Samosir	Sumatera Utara	,\
    2391	:	22392	Pardomuan Nauli	Pangururan	Kab.	Samosir	Sumatera Utara	,\
    2392	:	22392	Pardugul	Pangururan	Kab.	Samosir	Sumatera Utara	,\
    2393	:	22392	Parhorasan	Pangururan	Kab.	Samosir	Sumatera Utara	,\
    2394	:	22392	Parlondut	Pangururan	Kab.	Samosir	Sumatera Utara	,\
    2395	:	22392	Parmonangan	Pangururan	Kab.	Samosir	Sumatera Utara	,\
    2396	:	22392	Parsaoran I	Pangururan	Kab.	Samosir	Sumatera Utara	,\
    2397	:	22396	Pasar Pangururan	Pangururan	Kab.	Samosir	Sumatera Utara	,\
    2398	:	22392	Pintu Sona	Pangururan	Kab.	Samosir	Sumatera Utara	,\
    2399	:	22392	Rianiate	Pangururan	Kab.	Samosir	Sumatera Utara	,\
    2400	:	22392	Saitnihuta	Pangururan	Kab.	Samosir	Sumatera Utara	,\
    2401	:	22392	Sialanguan	Pangururan	Kab.	Samosir	Sumatera Utara	,\
    2402	:	22392	Sianting Anting	Pangururan	Kab.	Samosir	Sumatera Utara	,\
    2403	:	22392	Sinabulan	Pangururan	Kab.	Samosir	Sumatera Utara	,\
    2404	:	22392	Siogung Ogung	Pangururan	Kab.	Samosir	Sumatera Utara	,\
    2405	:	22392	Siopat Sosor	Pangururan	Kab.	Samosir	Sumatera Utara	,\
    2406	:	22392	Sitoluhuta	Pangururan	Kab.	Samosir	Sumatera Utara	,\
    2407	:	22392	Situngkir	Pangururan	Kab.	Samosir	Sumatera Utara	,\
    2408	:	22392	Tanjung Bunga	Pangururan	Kab.	Samosir	Sumatera Utara	,\
    2409	:	21462	Kampung Padang	Pangkatan	Kab.	Labuhan Batu	Sumatera Utara	,\
    2410	:	21462	Pangkatan (Kampung Pangkatan)	Pangkatan	Kab.	Labuhan Batu	Sumatera Utara	,\
    2411	:	21462	Perkebunan Pangkatan	Pangkatan	Kab.	Labuhan Batu	Sumatera Utara	,\
    2412	:	21462	Sennah (Kampung Sennah)	Pangkatan	Kab.	Labuhan Batu	Sumatera Utara	,\
    2413	:	21462	Sidorukun	Pangkatan	Kab.	Labuhan Batu	Sumatera Utara	,\
    2414	:	21462	Tanjung Harapan	Pangkatan	Kab.	Labuhan Batu	Sumatera Utara	,\
    2415	:	21462	Tebing Tinggi Pangkatan	Pangkatan	Kab.	Labuhan Batu	Sumatera Utara	,\
    2416	:	20858	Alur Cempedak	Pangkalan Susu	Kab.	Langkat	Sumatera Utara	,\
    2417	:	20858	Beras Basah	Pangkalan Susu	Kab.	Langkat	Sumatera Utara	,\
    2418	:	20858	Bukit Jengkol	Pangkalan Susu	Kab.	Langkat	Sumatera Utara	,\
    2419	:	20858	Pangkalan Siata	Pangkalan Susu	Kab.	Langkat	Sumatera Utara	,\
    2420	:	20858	Paya Tampak	Pangkalan Susu	Kab.	Langkat	Sumatera Utara	,\
    2421	:	20858	Pintu Air	Pangkalan Susu	Kab.	Langkat	Sumatera Utara	,\
    2422	:	20858	Pulau Kampai	Pangkalan Susu	Kab.	Langkat	Sumatera Utara	,\
    2423	:	20858	Pulau Sembilan	Pangkalan Susu	Kab.	Langkat	Sumatera Utara	,\
    2424	:	20858	Sei/Sungai Meran	Pangkalan Susu	Kab.	Langkat	Sumatera Utara	,\
    2425	:	20858	Sei/Sungai Siur	Pangkalan Susu	Kab.	Langkat	Sumatera Utara	,\
    2426	:	20858	Tanjung Pasir	Pangkalan Susu	Kab.	Langkat	Sumatera Utara	,\
    2427	:	22472	Batu Nadua	Pangaribuan	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2428	:	22472	Batumanumpak	Pangaribuan	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2429	:	22472	Godung Borotan	Pangaribuan	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2430	:	22472	Harianja	Pangaribuan	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2431	:	22472	Lumban Sinaga Simatupang	Pangaribuan	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2432	:	22472	Lumban Siregar	Pangaribuan	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2433	:	22472	Najumambe	Pangaribuan	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2434	:	22472	Padang Parsadaan	Pangaribuan	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2435	:	22472	Pakpahan	Pangaribuan	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2436	:	22472	Pansurnatolu	Pangaribuan	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2437	:	22472	Parlombuan	Pangaribuan	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2438	:	22472	Parratusan	Pangaribuan	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2439	:	22472	Parsibarungan	Pangaribuan	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2440	:	22472	Parsorminan I	Pangaribuan	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2441	:	22472	Purbatua	Pangaribuan	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2442	:	22472	Rahut Bosi	Pangaribuan	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2443	:	22472	Sampagul	Pangaribuan	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2444	:	22472	Sibingke	Pangaribuan	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2445	:	22472	Sigotom Julu	Pangaribuan	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2446	:	22472	Silantom Jae	Pangaribuan	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2447	:	22472	Silantom Julu	Pangaribuan	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2448	:	22472	Silantom Tonga	Pangaribuan	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2449	:	21161	Bah Bolon Tongah	Panei	Kab.	Simalungun	Sumatera Utara	,\
    2450	:	21161	Bangun Dasmariah	Panei	Kab.	Simalungun	Sumatera Utara	,\
    2451	:	21161	Bangun Rakyat	Panei	Kab.	Simalungun	Sumatera Utara	,\
    2452	:	21161	Janggir Leto	Panei	Kab.	Simalungun	Sumatera Utara	,\
    2453	:	21161	Mekar Sari Raya	Panei	Kab.	Simalungun	Sumatera Utara	,\
    2454	:	21161	Panei Tongah	Panei	Kab.	Simalungun	Sumatera Utara	,\
    2455	:	21161	Siborna	Panei	Kab.	Simalungun	Sumatera Utara	,\
    2456	:	21161	Sigodang	Panei	Kab.	Simalungun	Sumatera Utara	,\
    2457	:	21161	Sigodang Barat	Panei	Kab.	Simalungun	Sumatera Utara	,\
    2458	:	21161	Simantin Pane Dame	Panei	Kab.	Simalungun	Sumatera Utara	,\
    2459	:	21161	Simpang Pane Raya	Panei	Kab.	Simalungun	Sumatera Utara	,\
    2460	:	21161	Simpang Raya Dasma	Panei	Kab.	Simalungun	Sumatera Utara	,\
    2461	:	21161	Sipoldas	Panei	Kab.	Simalungun	Sumatera Utara	,\
    2462	:	22613	Aek Sitio Tio	Pandan	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    2463	:	22613	Aek Tolang	Pandan	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    2464	:	22612	Hajoran	Pandan	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    2465	:	22616	Kalangan	Pandan	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    2466	:	22615	Lubuk Tukko	Pandan	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    2467	:	22611	Pandan	Pandan	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    2468	:	22614	Sibuluan Indah	Pandan	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    2469	:	22616	Sibuluan Nauli	Pandan	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    2470	:	22616	Sibuluan Raya	Pandan	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    2471	:	20353	Baru (Desa Baru)	Pancur Batu	Kab.	Deli Serdang	Sumatera Utara	,\
    2472	:	20353	Bintang Meriah	Pancur Batu	Kab.	Deli Serdang	Sumatera Utara	,\
    2473	:	20353	Dorin Tonggal (Durin Tunggal)	Pancur Batu	Kab.	Deli Serdang	Sumatera Utara	,\
    2474	:	20353	Durian Jangak	Pancur Batu	Kab.	Deli Serdang	Sumatera Utara	,\
    2475	:	20353	Durin Simbelang A	Pancur Batu	Kab.	Deli Serdang	Sumatera Utara	,\
    2476	:	20353	Gunung Tinggi	Pancur Batu	Kab.	Deli Serdang	Sumatera Utara	,\
    2477	:	20353	Hulu (Kampung Hulu)	Pancur Batu	Kab.	Deli Serdang	Sumatera Utara	,\
    2478	:	20353	Lama	Pancur Batu	Kab.	Deli Serdang	Sumatera Utara	,\
    2479	:	20353	Namo Bintang	Pancur Batu	Kab.	Deli Serdang	Sumatera Utara	,\
    2480	:	20353	Namo Riam	Pancur Batu	Kab.	Deli Serdang	Sumatera Utara	,\
    2481	:	20353	Namo Rih	Pancur Batu	Kab.	Deli Serdang	Sumatera Utara	,\
    2482	:	20353	Namo Simpur	Pancur Batu	Kab.	Deli Serdang	Sumatera Utara	,\
    2483	:	20353	Pertampilan (Pertampilen)	Pancur Batu	Kab.	Deli Serdang	Sumatera Utara	,\
    2484	:	20353	Perumnas Simalingkar	Pancur Batu	Kab.	Deli Serdang	Sumatera Utara	,\
    2485	:	20353	Salam Tani	Pancur Batu	Kab.	Deli Serdang	Sumatera Utara	,\
    2486	:	20353	Sei Glugur (Gelugur)	Pancur Batu	Kab.	Deli Serdang	Sumatera Utara	,\
    2487	:	20353	Sembahe Baru	Pancur Batu	Kab.	Deli Serdang	Sumatera Utara	,\
    2488	:	20353	Simalingkar A	Pancur Batu	Kab.	Deli Serdang	Sumatera Utara	,\
    2489	:	20353	Sugou (Sugau)	Pancur Batu	Kab.	Deli Serdang	Sumatera Utara	,\
    2490	:	20353	Suka Raya	Pancur Batu	Kab.	Deli Serdang	Sumatera Utara	,\
    2491	:	20353	Tanjung Anom	Pancur Batu	Kab.	Deli Serdang	Sumatera Utara	,\
    2492	:	20353	Tengah (Kampung Tengah)	Pancur Batu	Kab.	Deli Serdang	Sumatera Utara	,\
    2493	:	20353	Tiang Layar	Pancur Batu	Kab.	Deli Serdang	Sumatera Utara	,\
    2494	:	20353	Tuntungan I	Pancur Batu	Kab.	Deli Serdang	Sumatera Utara	,\
    2495	:	20353	Tuntungan II	Pancur Batu	Kab.	Deli Serdang	Sumatera Utara	,\
    2496	:	21472	Bagan Bilah	Panai Tengah	Kab.	Labuhan Batu	Sumatera Utara	,\
    2497	:	21472	Labuhan Bilik	Panai Tengah	Kab.	Labuhan Batu	Sumatera Utara	,\
    2498	:	21472	Pasar Tiga	Panai Tengah	Kab.	Labuhan Batu	Sumatera Utara	,\
    2499	:	21472	Sei Merdeka	Panai Tengah	Kab.	Labuhan Batu	Sumatera Utara	,\
    2500	:	21472	Sei Nahodaris	Panai Tengah	Kab.	Labuhan Batu	Sumatera Utara	,\
    2501	:	21472	Sei Plancang	Panai Tengah	Kab.	Labuhan Batu	Sumatera Utara	,\
    2502	:	21472	Sei Rakyat	Panai Tengah	Kab.	Labuhan Batu	Sumatera Utara	,\
    2503	:	21472	Sei Siati/Siarti	Panai Tengah	Kab.	Labuhan Batu	Sumatera Utara	,\
    2504	:	21472	Selat Beting	Panai Tengah	Kab.	Labuhan Batu	Sumatera Utara	,\
    2505	:	21472	Telaga Suka	Panai Tengah	Kab.	Labuhan Batu	Sumatera Utara	,\
    2506	:	21471	Ajamu (Perkebunan IV Ajamu)	Panai Hulu	Kab.	Labuhan Batu	Sumatera Utara	,\
    2507	:	21471	Cinta Makmur	Panai Hulu	Kab.	Labuhan Batu	Sumatera Utara	,\
    2508	:	21471	Maranti/Meranti Paham	Panai Hulu	Kab.	Labuhan Batu	Sumatera Utara	,\
    2509	:	21471	Sei Sentosa	Panai Hulu	Kab.	Labuhan Batu	Sumatera Utara	,\
    2510	:	21471	Sijawijawi (Sei Jawi Jawi)	Panai Hulu	Kab.	Labuhan Batu	Sumatera Utara	,\
    2511	:	21471	Tanjung Sarang Elang	Panai Hulu	Kab.	Labuhan Batu	Sumatera Utara	,\
    2512	:	21471	Teluk Sentosa	Panai Hulu	Kab.	Labuhan Batu	Sumatera Utara	,\
    2513	:	21473	Sei Baru	Panai Hilir	Kab.	Labuhan Batu	Sumatera Utara	,\
    2514	:	21473	Sei Berombang	Panai Hilir	Kab.	Labuhan Batu	Sumatera Utara	,\
    2515	:	21473	Sei Lumut	Panai Hilir	Kab.	Labuhan Batu	Sumatera Utara	,\
    2516	:	21473	Sei Penggantungan	Panai Hilir	Kab.	Labuhan Batu	Sumatera Utara	,\
    2517	:	21473	Sei Sakat	Panai Hilir	Kab.	Labuhan Batu	Sumatera Utara	,\
    2518	:	21473	Sei Sanggul	Panai Hilir	Kab.	Labuhan Batu	Sumatera Utara	,\
    2519	:	21473	Sei Tawar	Panai Hilir	Kab.	Labuhan Batu	Sumatera Utara	,\
    2520	:	21473	Wonosari	Panai Hilir	Kab.	Labuhan Batu	Sumatera Utara	,\
    2521	:	22393	Gorat Pallombuan	Palipi	Kab.	Samosir	Sumatera Utara	,\
    2522	:	22393	Hatoguan	Palipi	Kab.	Samosir	Sumatera Utara	,\
    2523	:	22393	Huta Ginjang	Palipi	Kab.	Samosir	Sumatera Utara	,\
    2524	:	22393	Palipi	Palipi	Kab.	Samosir	Sumatera Utara	,\
    2525	:	22393	Pardomuan Nauli	Palipi	Kab.	Samosir	Sumatera Utara	,\
    2526	:	22393	Parsaoran Urat	Palipi	Kab.	Samosir	Sumatera Utara	,\
    2527	:	22393	Saor Nauli Hatoguan	Palipi	Kab.	Samosir	Sumatera Utara	,\
    2528	:	22393	Sigaol Marbun	Palipi	Kab.	Samosir	Sumatera Utara	,\
    2529	:	22393	Sigaol Simbolon	Palipi	Kab.	Samosir	Sumatera Utara	,\
    2530	:	22393	Simbolon Purba	Palipi	Kab.	Samosir	Sumatera Utara	,\
    2531	:	22393	Suhut Nihuta Pardomuan	Palipi	Kab.	Samosir	Sumatera Utara	,\
    2532	:	22393	Urat II	Palipi	Kab.	Samosir	Sumatera Utara	,\
    2533	:	22393	Urat Timur	Palipi	Kab.	Samosir	Sumatera Utara	,\
    2534	:	22455	Ambobi Paranginan	Pakkat	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2535	:	22455	Banuarea	Pakkat	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2536	:	22455	Hauagong	Pakkat	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2537	:	22455	Karya	Pakkat	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2538	:	22455	Lumban Tonga-Tonga	Pakkat	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2539	:	22455	Manalu	Pakkat	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2540	:	22455	Pakkat Hauagong	Pakkat	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2541	:	22455	Panggugunan	Pakkat	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2542	:	22455	Parmonangan	Pakkat	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2543	:	22455	Peadungdung	Pakkat	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2544	:	22455	Pulo Godang	Pakkat	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2545	:	22455	Purba Baringin	Pakkat	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2546	:	22455	Purba Bersatu	Pakkat	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2547	:	22455	Purba Sianjur	Pakkat	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2548	:	22455	Rura Aek Sopang	Pakkat	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2549	:	22455	Rura Tanjung	Pakkat	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2550	:	22455	Siambaton	Pakkat	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2551	:	22455	Siambaton Pahae	Pakkat	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2552	:	22455	Sijarango	Pakkat	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2553	:	22455	Sijarango I	Pakkat	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2554	:	22455	Sipagabu	Pakkat	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2555	:	22455	Tukka Dolok	Pakkat	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2556	:	22998	Huta Gambir	Pakantan	Kab.	Mandailing Natal	Sumatera Utara	,\
    2557	:	22998	Huta Julu	Pakantan	Kab.	Mandailing Natal	Sumatera Utara	,\
    2558	:	22998	Huta Lancat	Pakantan	Kab.	Mandailing Natal	Sumatera Utara	,\
    2559	:	22998	Huta Padang	Pakantan	Kab.	Mandailing Natal	Sumatera Utara	,\
    2560	:	22998	Huta Toras	Pakantan	Kab.	Mandailing Natal	Sumatera Utara	,\
    2561	:	22998	Pakantan Dolok	Pakantan	Kab.	Mandailing Natal	Sumatera Utara	,\
    2562	:	22998	Pakantan Lombang	Pakantan	Kab.	Mandailing Natal	Sumatera Utara	,\
    2563	:	22998	Silogun	Pakantan	Kab.	Mandailing Natal	Sumatera Utara	,\
    2564	:	22463	Huta Barat	Pahae Julu	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2565	:	22463	Janji Matogu	Pahae Julu	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2566	:	22463	Lobu Pining	Pahae Julu	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2567	:	22463	Lontung Dolok	Pahae Julu	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2568	:	22463	Lumban Dolok	Pahae Julu	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2569	:	22463	Lumban Gaol	Pahae Julu	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2570	:	22463	Lumban Garaga	Pahae Julu	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2571	:	22463	Lumban Jaean	Pahae Julu	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2572	:	22463	Lumban Tonga	Pahae Julu	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2573	:	22463	Onan Hasang	Pahae Julu	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2574	:	22463	Pangurdotan	Pahae Julu	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2575	:	22463	Pantis	Pahae Julu	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2576	:	22463	Sibaganding	Pahae Julu	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2577	:	22463	Simanampang	Pahae Julu	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2578	:	22463	Simardangiang	Pahae Julu	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2579	:	22463	Simasom	Pahae Julu	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2580	:	22463	Simasom Toruan	Pahae Julu	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2581	:	22463	Simataniari	Pahae Julu	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2582	:	22463	Sitoluama	Pahae Julu	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2583	:	22465	Nahornop Marsada	Pahae Jae	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2584	:	22465	Pardamean Nainggolan	Pahae Jae	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2585	:	22465	Pardomuan Nainggolan	Pahae Jae	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2586	:	22465	Parsaoran Nainggolan	Pahae Jae	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2587	:	22465	Parsaoran Samosir	Pahae Jae	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2588	:	22465	Sarulla (Pasar Sarulla)	Pahae Jae	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2589	:	22465	Setia	Pahae Jae	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2590	:	22465	Sigurung Gurung	Pahae Jae	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2591	:	22465	Silangkitang	Pahae Jae	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2592	:	22465	Siopat Bahal	Pahae Jae	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2593	:	22465	Sitolu Ompu	Pahae Jae	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2594	:	22465	Sukamaju	Pahae Jae	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2595	:	22465	Tordolok Nauli	Pahae Jae	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2596	:	22271	Lae Mbentar	Pagindar	Kab.	Pakpak Bharat	Sumatera Utara	,\
    2597	:	22271	Napatalun Perlambuken	Pagindar	Kab.	Pakpak Bharat	Sumatera Utara	,\
    2598	:	22271	Pagindar	Pagindar	Kab.	Pakpak Bharat	Sumatera Utara	,\
    2599	:	22271	Sibagindar	Pagindar	Kab.	Pakpak Bharat	Sumatera Utara	,\
    2600	:	22458	Banua Luhu	Pagaran	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2601	:	22458	Dolok Saribu	Pagaran	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2602	:	22458	Hasibuan	Pagaran	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2603	:	22458	Lubis	Pagaran	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2604	:	22458	Lumban Ina Ina	Pagaran	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2605	:	22458	Lumban Julu	Pagaran	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2606	:	22458	Lumban Motung	Pagaran	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2607	:	22458	Lumban Silintong	Pagaran	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2608	:	22458	Pagaran	Pagaran	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2609	:	22458	Parhorboan	Pagaran	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2610	:	22458	Sibaragas	Pagaran	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2611	:	22458	Simamora Hasibuan	Pagaran	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2612	:	22458	Sipultak	Pagaran	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2613	:	22458	Sipultak Dolok	Pagaran	Kab.	Tapanuli Utara	Sumatera Utara	,\
    2614	:	20551	Bandar Dolok	Pagar Merbau	Kab.	Deli Serdang	Sumatera Utara	,\
    2615	:	20551	Jati Baru (Sidoarjo I)	Pagar Merbau	Kab.	Deli Serdang	Sumatera Utara	,\
    2616	:	20551	Jati Rejo	Pagar Merbau	Kab.	Deli Serdang	Sumatera Utara	,\
    2617	:	20551	Pagar Merbau I	Pagar Merbau	Kab.	Deli Serdang	Sumatera Utara	,\
    2618	:	20551	Pagar Merbau II	Pagar Merbau	Kab.	Deli Serdang	Sumatera Utara	,\
    2619	:	20551	Pasar Miring (Sidoarjo Satu Psr Miring)	Pagar Merbau	Kab.	Deli Serdang	Sumatera Utara	,\
    2620	:	20551	Perbarakan	Pagar Merbau	Kab.	Deli Serdang	Sumatera Utara	,\
    2621	:	20551	Purwodadi	Pagar Merbau	Kab.	Deli Serdang	Sumatera Utara	,\
    2622	:	20551	Sidodadi Batu Delapan	Pagar Merbau	Kab.	Deli Serdang	Sumatera Utara	,\
    2623	:	20551	Suka Mulia	Pagar Merbau	Kab.	Deli Serdang	Sumatera Utara	,\
    2624	:	20551	Sukamandi Hilir	Pagar Merbau	Kab.	Deli Serdang	Sumatera Utara	,\
    2625	:	20551	Sukamandi Hulu	Pagar Merbau	Kab.	Deli Serdang	Sumatera Utara	,\
    2626	:	20551	Sumberejo	Pagar Merbau	Kab.	Deli Serdang	Sumatera Utara	,\
    2627	:	20551	Tanjung Garbus II	Pagar Merbau	Kab.	Deli Serdang	Sumatera Utara	,\
    2628	:	20551	Tanjung Garbus Kampung	Pagar Merbau	Kab.	Deli Serdang	Sumatera Utara	,\
    2629	:	20551	Tanjung Mulia	Pagar Merbau	Kab.	Deli Serdang	Sumatera Utara	,\
    2630	:	20852	Banjar Jaya	Padang Tualang	Kab.	Langkat	Sumatera Utara	,\
    2631	:	20852	Besilam	Padang Tualang	Kab.	Langkat	Sumatera Utara	,\
    2632	:	20852	Bukit Sari	Padang Tualang	Kab.	Langkat	Sumatera Utara	,\
    2633	:	20852	Buluh Telang	Padang Tualang	Kab.	Langkat	Sumatera Utara	,\
    2634	:	20852	Jati Sari	Padang Tualang	Kab.	Langkat	Sumatera Utara	,\
    2635	:	20852	Kwala Pesilam (Kuala Besilam)	Padang Tualang	Kab.	Langkat	Sumatera Utara	,\
    2636	:	20852	Padang Tualang	Padang Tualang	Kab.	Langkat	Sumatera Utara	,\
    2637	:	20852	Serapuh Abc	Padang Tualang	Kab.	Langkat	Sumatera Utara	,\
    2638	:	20852	Suka Ramai	Padang Tualang	Kab.	Langkat	Sumatera Utara	,\
    2639	:	20852	Tanjung Putus	Padang Tualang	Kab.	Langkat	Sumatera Utara	,\
    2640	:	20852	Tanjung Selamat	Padang Tualang	Kab.	Langkat	Sumatera Utara	,\
    2641	:	20852	Tebing Tanjung Selamat	Padang Tualang	Kab.	Langkat	Sumatera Utara	,\
    2642	:	22716	Batang Ayumi Jae	Padang Sidempuan Utara (Padangsidimpuan)	Kota	Padang Sidempuan	Sumatera Utara	,\
    2643	:	22711	Batang Ayumi Julu	Padang Sidempuan Utara (Padangsidimpuan)	Kota	Padang Sidempuan	Sumatera Utara	,\
    2644	:	22711	Bincar	Padang Sidempuan Utara (Padangsidimpuan)	Kota	Padang Sidempuan	Sumatera Utara	,\
    2645	:	22712	Bonan Dolok	Padang Sidempuan Utara (Padangsidimpuan)	Kota	Padang Sidempuan	Sumatera Utara	,\
    2646	:	22711	Kantin	Padang Sidempuan Utara (Padangsidimpuan)	Kota	Padang Sidempuan	Sumatera Utara	,\
    2647	:	22711	Kayu Ombun	Padang Sidempuan Utara (Padangsidimpuan)	Kota	Padang Sidempuan	Sumatera Utara	,\
    2648	:	22713	Losung Batu	Padang Sidempuan Utara (Padangsidimpuan)	Kota	Padang Sidempuan	Sumatera Utara	,\
    2649	:	22714	Panyanggar	Padang Sidempuan Utara (Padangsidimpuan)	Kota	Padang Sidempuan	Sumatera Utara	,\
    2650	:	22715	Sadabuan	Padang Sidempuan Utara (Padangsidimpuan)	Kota	Padang Sidempuan	Sumatera Utara	,\
    2651	:	22716	Tano Bato	Padang Sidempuan Utara (Padangsidimpuan)	Kota	Padang Sidempuan	Sumatera Utara	,\
    2652	:	22711	Timbangan	Padang Sidempuan Utara (Padangsidimpuan)	Kota	Padang Sidempuan	Sumatera Utara	,\
    2653	:	22716	Tobat	Padang Sidempuan Utara (Padangsidimpuan)	Kota	Padang Sidempuan	Sumatera Utara	,\
    2654	:	22715	Wek I	Padang Sidempuan Utara (Padangsidimpuan)	Kota	Padang Sidempuan	Sumatera Utara	,\
    2655	:	22718	Wek II	Padang Sidempuan Utara (Padangsidimpuan)	Kota	Padang Sidempuan	Sumatera Utara	,\
    2656	:	22719	Wek III	Padang Sidempuan Utara (Padangsidimpuan)	Kota	Padang Sidempuan	Sumatera Utara	,\
    2657	:	22719	Wek IV	Padang Sidempuan Utara (Padangsidimpuan)	Kota	Padang Sidempuan	Sumatera Utara	,\
    2658	:	22733	Goti	Padang Sidempuan Tenggara	Kota	Padang Sidempuan	Sumatera Utara	,\
    2659	:	22733	Huta Koje Pijor Koling	Padang Sidempuan Tenggara	Kota	Padang Sidempuan	Sumatera Utara	,\
    2660	:	22733	Huta Limbong	Padang Sidempuan Tenggara	Kota	Padang Sidempuan	Sumatera Utara	,\
    2661	:	22733	Huta Lombang	Padang Sidempuan Tenggara	Kota	Padang Sidempuan	Sumatera Utara	,\
    2662	:	22733	Huta Padang	Padang Sidempuan Tenggara	Kota	Padang Sidempuan	Sumatera Utara	,\
    2663	:	22733	Labuhan Labo	Padang Sidempuan Tenggara	Kota	Padang Sidempuan	Sumatera Utara	,\
    2664	:	22733	Labuhan Rasoki	Padang Sidempuan Tenggara	Kota	Padang Sidempuan	Sumatera Utara	,\
    2665	:	22733	Manegen	Padang Sidempuan Tenggara	Kota	Padang Sidempuan	Sumatera Utara	,\
    2666	:	22733	Manunggang Jae	Padang Sidempuan Tenggara	Kota	Padang Sidempuan	Sumatera Utara	,\
    2667	:	22733	Manunggang Julu	Padang Sidempuan Tenggara	Kota	Padang Sidempuan	Sumatera Utara	,\
    2668	:	22733	Palopat (Pal IV) Pijor Koling	Padang Sidempuan Tenggara	Kota	Padang Sidempuan	Sumatera Utara	,\
    2669	:	22733	Perkebunan Pijor Koling	Padang Sidempuan Tenggara	Kota	Padang Sidempuan	Sumatera Utara	,\
    2670	:	22733	Pijor Koling	Padang Sidempuan Tenggara	Kota	Padang Sidempuan	Sumatera Utara	,\
    2671	:	22733	Purbatua Pijor Koling	Padang Sidempuan Tenggara	Kota	Padang Sidempuan	Sumatera Utara	,\
    2672	:	22733	Salambue	Padang Sidempuan Tenggara	Kota	Padang Sidempuan	Sumatera Utara	,\
    2673	:	22733	Sigulang	Padang Sidempuan Tenggara	Kota	Padang Sidempuan	Sumatera Utara	,\
    2674	:	22733	Sihitang	Padang Sidempuan Tenggara	Kota	Padang Sidempuan	Sumatera Utara	,\
    2675	:	22733	Tarutung Baru	Padang Sidempuan Tenggara	Kota	Padang Sidempuan	Sumatera Utara	,\
    2676	:	22726	Aek Tampang	Padang Sidempuan Selatan	Kota	Padang Sidempuan	Sumatera Utara	,\
    2677	:	22721	Hanopan	Padang Sidempuan Selatan	Kota	Padang Sidempuan	Sumatera Utara	,\
    2678	:	22722	Losung	Padang Sidempuan Selatan	Kota	Padang Sidempuan	Sumatera Utara	,\
    2679	:	22727	Padang Matinggi	Padang Sidempuan Selatan	Kota	Padang Sidempuan	Sumatera Utara	,\
    2680	:	22727	Padang Matinggi Lestari	Padang Sidempuan Selatan	Kota	Padang Sidempuan	Sumatera Utara	,\
    2681	:	22721	Sidangkal	Padang Sidempuan Selatan	Kota	Padang Sidempuan	Sumatera Utara	,\
    2682	:	22728	Silandit	Padang Sidempuan Selatan	Kota	Padang Sidempuan	Sumatera Utara	,\
    2683	:	22723	Sitamiang	Padang Sidempuan Selatan	Kota	Padang Sidempuan	Sumatera Utara	,\
    2684	:	22723	Sitamiang Baru	Padang Sidempuan Selatan	Kota	Padang Sidempuan	Sumatera Utara	,\
    2685	:	22725	Ujung Padang	Padang Sidempuan Selatan	Kota	Padang Sidempuan	Sumatera Utara	,\
    2686	:	22723	Wek V	Padang Sidempuan Selatan	Kota	Padang Sidempuan	Sumatera Utara	,\
    2687	:	22724	Wek VI	Padang Sidempuan Selatan	Kota	Padang Sidempuan	Sumatera Utara	,\
    2688	:	22753	Huta Padang	Padang Sidempuan Hutaimbaru	Kota	Padang Sidempuan	Sumatera Utara	,\
    2689	:	22753	Hutaimbaru	Padang Sidempuan Hutaimbaru	Kota	Padang Sidempuan	Sumatera Utara	,\
    2690	:	22753	Lembah Lubuk Manik	Padang Sidempuan Hutaimbaru	Kota	Padang Sidempuan	Sumatera Utara	,\
    2691	:	22753	Lubuk Raya	Padang Sidempuan Hutaimbaru	Kota	Padang Sidempuan	Sumatera Utara	,\
    2692	:	22753	Palopat Maria	Padang Sidempuan Hutaimbaru	Kota	Padang Sidempuan	Sumatera Utara	,\
    2693	:	22753	Partihaman Saroha	Padang Sidempuan Hutaimbaru	Kota	Padang Sidempuan	Sumatera Utara	,\
    2694	:	22753	Sabungan Jae	Padang Sidempuan Hutaimbaru	Kota	Padang Sidempuan	Sumatera Utara	,\
    2695	:	22753	Sabungan Sipabangun	Padang Sidempuan Hutaimbaru	Kota	Padang Sidempuan	Sumatera Utara	,\
    2696	:	22753	Singali	Padang Sidempuan Hutaimbaru	Kota	Padang Sidempuan	Sumatera Utara	,\
    2697	:	22753	Tinjoman Lama	Padang Sidempuan Hutaimbaru	Kota	Padang Sidempuan	Sumatera Utara	,\
    2698	:	22733	Aek Bayur	Padang Sidempuan Batunadua	Kota	Padang Sidempuan	Sumatera Utara	,\
    2699	:	22733	Aek Najaji	Padang Sidempuan Batunadua	Kota	Padang Sidempuan	Sumatera Utara	,\
    2700	:	22733	Aek Tuhul	Padang Sidempuan Batunadua	Kota	Padang Sidempuan	Sumatera Utara	,\
    2701	:	22733	Bargot Topong	Padang Sidempuan Batunadua	Kota	Padang Sidempuan	Sumatera Utara	,\
    2702	:	22733	Baruas	Padang Sidempuan Batunadua	Kota	Padang Sidempuan	Sumatera Utara	,\
    2703	:	22733	Batang Bahal	Padang Sidempuan Batunadua	Kota	Padang Sidempuan	Sumatera Utara	,\
    2704	:	22733	Batunadua Jae	Padang Sidempuan Batunadua	Kota	Padang Sidempuan	Sumatera Utara	,\
    2705	:	22733	Batunadua Julu	Padang Sidempuan Batunadua	Kota	Padang Sidempuan	Sumatera Utara	,\
    2706	:	22733	Gunung Hasahatan	Padang Sidempuan Batunadua	Kota	Padang Sidempuan	Sumatera Utara	,\
    2707	:	22733	Pudun Jae	Padang Sidempuan Batunadua	Kota	Padang Sidempuan	Sumatera Utara	,\
    2708	:	22733	Pudun Julu	Padang Sidempuan Batunadua	Kota	Padang Sidempuan	Sumatera Utara	,\
    2709	:	22733	Purwodadi	Padang Sidempuan Batunadua	Kota	Padang Sidempuan	Sumatera Utara	,\
    2710	:	22733	Siloting	Padang Sidempuan Batunadua	Kota	Padang Sidempuan	Sumatera Utara	,\
    2711	:	22733	Simirik	Padang Sidempuan Batunadua	Kota	Padang Sidempuan	Sumatera Utara	,\
    2712	:	22733	Ujung Gurab	Padang Sidempuan Batunadua	Kota	Padang Sidempuan	Sumatera Utara	,\
    2713	:	22733	Batu Layan	Padang Sidempuan Angkola Julu	Kota	Padang Sidempuan	Sumatera Utara	,\
    2714	:	22733	Joring Lombang	Padang Sidempuan Angkola Julu	Kota	Padang Sidempuan	Sumatera Utara	,\
    2715	:	22733	Joring Natobang	Padang Sidempuan Angkola Julu	Kota	Padang Sidempuan	Sumatera Utara	,\
    2716	:	22733	Mompang	Padang Sidempuan Angkola Julu	Kota	Padang Sidempuan	Sumatera Utara	,\
    2717	:	22733	Pintu Langit Jae	Padang Sidempuan Angkola Julu	Kota	Padang Sidempuan	Sumatera Utara	,\
    2718	:	22733	Rimba Soping	Padang Sidempuan Angkola Julu	Kota	Padang Sidempuan	Sumatera Utara	,\
    2719	:	22733	Simasom	Padang Sidempuan Angkola Julu	Kota	Padang Sidempuan	Sumatera Utara	,\
    2720	:	22733	Simatohir	Padang Sidempuan Angkola Julu	Kota	Padang Sidempuan	Sumatera Utara	,\
    2721	:	20625	Bandarsono	Padang Hulu	Kota	Tebing Tinggi	Sumatera Utara	,\
    2722	:	20622	Lubuk Baru	Padang Hulu	Kota	Tebing Tinggi	Sumatera Utara	,\
    2723	:	20624	Lubuk Raya	Padang Hulu	Kota	Tebing Tinggi	Sumatera Utara	,\
    2724	:	20623	Pabatu	Padang Hulu	Kota	Tebing Tinggi	Sumatera Utara	,\
    2725	:	20624	Padang Merbau	Padang Hulu	Kota	Tebing Tinggi	Sumatera Utara	,\
    2726	:	20624	Persiakan	Padang Hulu	Kota	Tebing Tinggi	Sumatera Utara	,\
    2727	:	20624	Tualang	Padang Hulu	Kota	Tebing Tinggi	Sumatera Utara	,\
    2728	:	20634	Bagelen	Padang Hilir	Kota	Tebing Tinggi	Sumatera Utara	,\
    2729	:	20636	Damar Sari	Padang Hilir	Kota	Tebing Tinggi	Sumatera Utara	,\
    2730	:	20636	Deblod Sundoro	Padang Hilir	Kota	Tebing Tinggi	Sumatera Utara	,\
    2731	:	20636	Satria	Padang Hilir	Kota	Tebing Tinggi	Sumatera Utara	,\
    2732	:	20631	Tambangan	Padang Hilir	Kota	Tebing Tinggi	Sumatera Utara	,\
    2733	:	20636	Tambangan Hulu	Padang Hilir	Kota	Tebing Tinggi	Sumatera Utara	,\
    2734	:	20631	Tebing Tinggi	Padang Hilir	Kota	Tebing Tinggi	Sumatera Utara	,\
    2735	:	22753	Aek Bargot	Padang Bolak Julu	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2736	:	22753	Balakka (Balangka)	Padang Bolak Julu	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2737	:	22753	Balimbing Jae	Padang Bolak Julu	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2738	:	22753	Balimbing Julu	Padang Bolak Julu	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2739	:	22753	Batu Gana	Padang Bolak Julu	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2740	:	22753	Batu Rancang	Padang Bolak Julu	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2741	:	22753	Gariang	Padang Bolak Julu	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2742	:	22753	Hasambi	Padang Bolak Julu	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2743	:	22753	Lantosan II	Padang Bolak Julu	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2744	:	22753	Padang Baruas	Padang Bolak Julu	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2745	:	22753	Padang Bujur	Padang Bolak Julu	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2746	:	22753	Pamuntaran	Padang Bolak Julu	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2747	:	22753	Pancur Pangko	Padang Bolak Julu	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2748	:	22753	Paran Gadung	Padang Bolak Julu	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2749	:	22753	Paran Nangka	Padang Bolak Julu	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2750	:	22753	Parupuk Jae	Padang Bolak Julu	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2751	:	22753	Parupuk Julu	Padang Bolak Julu	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2752	:	22753	Sialang	Padang Bolak Julu	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2753	:	22753	Sipupus Lombang	Padang Bolak Julu	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2754	:	22753	Sitanggoru	Padang Bolak Julu	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2755	:	22753	Siunggam Dolok	Padang Bolak Julu	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2756	:	22753	Sobar	Padang Bolak Julu	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2757	:	22753	Ubar	Padang Bolak Julu	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2758	:	22753	Aek Bayur	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2759	:	22753	Aek Gambir	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2760	:	22753	Aek Jangkang	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2761	:	22753	Aek Suhat	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2762	:	22753	Aek Tolang	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2763	:	22753	Ambasang Natigor	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2764	:	22753	Bangun Purba	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2765	:	22753	Batang Baruhar Jae	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2766	:	22753	Batang Baruhar Julu	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2767	:	22753	Batang Pane I	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2768	:	22753	Batang Pane II	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2769	:	22753	Batang Pane III	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2770	:	22753	Batu Mamak	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2771	:	22753	Batu Sundung	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2772	:	22753	Batu Tambun	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2773	:	22753	Batu Tunggal	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2774	:	22753	Botung	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2775	:	22753	Bukit Raya Sedang / Sordang	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2776	:	22753	Dolok Sae	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2777	:	22753	Garoga	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2778	:	22753	Garonggang	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2779	:	22753	Gulangan	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2780	:	22753	Gunung Manaon II	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2781	:	22753	Gunung Tua Baru	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2782	:	22753	Gunung Tua Jae	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2783	:	22753	Gunung Tua Julu	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2784	:	22753	Gunung Tua Tonga	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2785	:	22753	Hajoran	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2786	:	22753	Hambiri Boding	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2787	:	22753	Huta Lombang	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2788	:	22753	Hutaimbaru II	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2789	:	22753	Liang Hasona/Asona	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2790	:	22753	Losung Batu	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2791	:	22753	Lubuk Torop	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2792	:	22753	Mananti (Marenti)	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2793	:	22753	Mandi Angin Dolok	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2794	:	22753	Mandi Angin Lombang	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2795	:	22753	Mompang/Mempang II	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2796	:	22753	Nabongal (Nabonggal)	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2797	:	22753	Naga Saribu	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2798	:	22753	Napa Gadung Laut	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2799	:	22753	Padang Garugur	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2800	:	22753	Pagaran Singkam	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2801	:	22753	Pagaran Tonga	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2802	:	22753	Paran/Parang Padang	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2803	:	22753	Parlimbatan	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2804	:	22753	Pasar Gunung Tua	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2805	:	22753	Purba Sinomba	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2806	:	22753	Purba Tua	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2807	:	22753	Rahunning/Rahuning Jae	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2808	:	22753	Rampa Jae	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2809	:	22753	Rampa Julu	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2810	:	22753	Saba Bangunan	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2811	:	22753	Saba Sitahul Tahul	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2812	:	22753	Sampuran	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2813	:	22753	Sibagasi	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2814	:	22753	Sibatang Kayu	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2815	:	22753	Sidikkat (Sidingkat)	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2816	:	22753	Sigama	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2817	:	22753	Sigama Ujung Gading	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2818	:	22753	Sigimbal	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2819	:	22753	Sihapas Hapas	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2820	:	22753	Sihodahoda	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2821	:	22753	Simaninggir	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2822	:	22753	Simanosor	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2823	:	22753	Simasi	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2824	:	22753	Simbolon	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2825	:	22753	Siombob	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2826	:	22753	Siunggam Jae	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2827	:	22753	Siunggam Julu	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2828	:	22753	Siunggam Tonga	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2829	:	22753	Sosopan	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2830	:	22753	Sunge Durian	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2831	:	22753	Sunge Orosan	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2832	:	22753	Sunge Tolang	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2833	:	22753	Tangga Tangga Hambeng	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2834	:	22753	Tanjung Marulak	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2835	:	22753	Tanjung Toram	Padang Bolak	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    2836	:	22864	Fadoro`ewo	Onohazumba	Kab.	Nias Selatan	Sumatera Utara	,\
    2837	:	22864	Helefanikha	Onohazumba	Kab.	Nias Selatan	Sumatera Utara	,\
    2838	:	22864	Hiliweto	Onohazumba	Kab.	Nias Selatan	Sumatera Utara	,\
    2839	:	22864	La`uso	Onohazumba	Kab.	Nias Selatan	Sumatera Utara	,\
    2840	:	22864	Onohazumba	Onohazumba	Kab.	Nias Selatan	Sumatera Utara	,\
    2841	:	22864	Orahili Huruna	Onohazumba	Kab.	Nias Selatan	Sumatera Utara	,\
    2842	:	22864	Sisarahili Oyo	Onohazumba	Kab.	Nias Selatan	Sumatera Utara	,\
    2843	:	22864	Sisobahili Huruna	Onohazumba	Kab.	Nias Selatan	Sumatera Utara	,\
    2844	:	22864	Soroma`asi	Onohazumba	Kab.	Nias Selatan	Sumatera Utara	,\
    2845	:	22864	Tetehosi	Onohazumba	Kab.	Nias Selatan	Sumatera Utara	,\
    2846	:	22391	Harian	Onan Runggu	Kab.	Samosir	Sumatera Utara	,\
    2847	:	22394	Huta Hotang	Onan Runggu	Kab.	Samosir	Sumatera Utara	,\
    2848	:	22394	Janji Matogu	Onan Runggu	Kab.	Samosir	Sumatera Utara	,\
    2849	:	22394	Onan Runggu	Onan Runggu	Kab.	Samosir	Sumatera Utara	,\
    2850	:	22394	Pakpahan	Onan Runggu	Kab.	Samosir	Sumatera Utara	,\
    2851	:	22394	Pardomuan	Onan Runggu	Kab.	Samosir	Sumatera Utara	,\
    2852	:	22394	Rinabolak	Onan Runggu	Kab.	Samosir	Sumatera Utara	,\
    2853	:	22394	Silima Lombu	Onan Runggu	Kab.	Samosir	Sumatera Utara	,\
    2854	:	22394	Sipira	Onan Runggu	Kab.	Samosir	Sumatera Utara	,\
    2855	:	22394	Sitamiang	Onan Runggu	Kab.	Samosir	Sumatera Utara	,\
    2856	:	22394	Sitinjak	Onan Runggu	Kab.	Samosir	Sumatera Utara	,\
    2857	:	22394	Tambun Sungkean	Onan Runggu	Kab.	Samosir	Sumatera Utara	,\
    2858	:	22454	Aek Godang	Onan Ganjang	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2859	:	22454	Batu Nagodang Siatas	Onan Ganjang	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2860	:	22454	Hutajulu	Onan Ganjang	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2861	:	22454	Janji Nagodang	Onan Ganjang	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2862	:	22454	Onan Ganjang	Onan Ganjang	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2863	:	22454	Parbotihan	Onan Ganjang	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2864	:	22454	Parnapa	Onan Ganjang	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2865	:	22454	Sampetua	Onan Ganjang	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2866	:	22454	Sanggaran II	Onan Ganjang	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2867	:	22454	Sibuluan	Onan Ganjang	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2868	:	22454	Sigalogo	Onan Ganjang	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2869	:	22454	Sihikkit	Onan Ganjang	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    2870	:	22864	Balohili O`o`u	O`o`u (Oou)	Kab.	Nias Selatan	Sumatera Utara	,\
    2871	:	22864	Bawosalo`o Bawoluo	O`o`u (Oou)	Kab.	Nias Selatan	Sumatera Utara	,\
    2872	:	22864	Hilimbowo	O`o`u (Oou)	Kab.	Nias Selatan	Sumatera Utara	,\
    2873	:	22864	Hilimbuasi	O`o`u (Oou)	Kab.	Nias Selatan	Sumatera Utara	,\
    2874	:	22864	Hilinamozihono	O`o`u (Oou)	Kab.	Nias Selatan	Sumatera Utara	,\
    2875	:	22864	Hilinamozihono Moale	O`o`u (Oou)	Kab.	Nias Selatan	Sumatera Utara	,\
    2876	:	22864	Hilioru dua	O`o`u (Oou)	Kab.	Nias Selatan	Sumatera Utara	,\
    2877	:	22864	Lolomaya	O`o`u (Oou)	Kab.	Nias Selatan	Sumatera Utara	,\
    2878	:	22864	Simandraolo / Simandaolo	O`o`u (Oou)	Kab.	Nias Selatan	Sumatera Utara	,\
    2879	:	22864	Simandraolo O`ou	O`o`u (Oou)	Kab.	Nias Selatan	Sumatera Utara	,\
    2880	:	22864	Suka Maju	O`o`u (Oou)	Kab.	Nias Selatan	Sumatera Utara	,\
    2881	:	22987	Balimbing	Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    2882	:	22987	Bintuas	Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    2883	:	22987	Bonda Kase	Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    2884	:	22987	Buburan	Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    2885	:	22987	Kampung Sawah	Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    2886	:	22987	Panggarutan	Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    2887	:	22987	Pardamean Baru	Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    2888	:	22987	Pasar I Natal	Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    2889	:	22987	Pasar II Natal	Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    2890	:	22987	Pasar III Natal	Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    2891	:	22987	Pasar IV Natal	Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    2892	:	22987	Pasar VI Natal	Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    2893	:	22987	Patiluban Hilir	Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    2894	:	22987	Patiluban Mudik	Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    2895	:	22987	Perkebunan Patiluban	Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    2896	:	22987	Rukun Jaya	Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    2897	:	22987	Setia Karya	Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    2898	:	22987	Sikara Kara	Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    2899	:	22987	Sikara Kara I	Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    2900	:	22987	Sikara Kara II	Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    2901	:	22987	Sikara Kara III	Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    2902	:	22987	Sikara Kara IV	Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    2903	:	22987	Sinunukan V	Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    2904	:	22987	Sundutan Tigo	Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    2905	:	22987	Taluk	Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    2906	:	22987	Tegal Sari	Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    2907	:	22987	Tunas Karya	Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    2908	:	22383	Batu Manumpak	Nassau	Kab.	Toba Samosir	Sumatera Utara	,\
    2909	:	22383	Cinta Damai	Nassau	Kab.	Toba Samosir	Sumatera Utara	,\
    2910	:	22383	Liat Tondung	Nassau	Kab.	Toba Samosir	Sumatera Utara	,\
    2911	:	22383	Lumban Rau Tengah	Nassau	Kab.	Toba Samosir	Sumatera Utara	,\
    2912	:	22383	Lumban Rau Tenggara	Nassau	Kab.	Toba Samosir	Sumatera Utara	,\
    2913	:	22383	Lumban Rau Timur	Nassau	Kab.	Toba Samosir	Sumatera Utara	,\
    2914	:	22383	Lumban Rau Utara	Nassau	Kab.	Toba Samosir	Sumatera Utara	,\
    2915	:	22383	Napajoriho	Nassau	Kab.	Toba Samosir	Sumatera Utara	,\
    2916	:	22383	Siantarasa	Nassau	Kab.	Toba Samosir	Sumatera Utara	,\
    2917	:	22383	Sipagabu	Nassau	Kab.	Toba Samosir	Sumatera Utara	,\
    2918	:	22816	Banua Sibohou	Namohalu Esiwa	Kab.	Nias Utara	Sumatera Utara	,\
    2919	:	22816	Berua	Namohalu Esiwa	Kab.	Nias Utara	Sumatera Utara	,\
    2920	:	22816	Dahana Hiligodu	Namohalu Esiwa	Kab.	Nias Utara	Sumatera Utara	,\
    2921	:	22816	Esiwa	Namohalu Esiwa	Kab.	Nias Utara	Sumatera Utara	,\
    2922	:	22816	Hilibanua	Namohalu Esiwa	Kab.	Nias Utara	Sumatera Utara	,\
    2923	:	22816	Lasara	Namohalu Esiwa	Kab.	Nias Utara	Sumatera Utara	,\
    2924	:	22816	Namohalu	Namohalu Esiwa	Kab.	Nias Utara	Sumatera Utara	,\
    2925	:	22816	Orahili	Namohalu Esiwa	Kab.	Nias Utara	Sumatera Utara	,\
    2926	:	22816	Sisarahili	Namohalu Esiwa	Kab.	Nias Utara	Sumatera Utara	,\
    2927	:	22817	Sisobahili	Namohalu Esiwa	Kab.	Nias Utara	Sumatera Utara	,\
    2928	:	22816	Tuhenakhe I	Namohalu Esiwa	Kab.	Nias Utara	Sumatera Utara	,\
    2929	:	20356	Batu Gemuk	Namo Rambe	Kab.	Deli Serdang	Sumatera Utara	,\
    2930	:	20356	Batu Mbelin	Namo Rambe	Kab.	Deli Serdang	Sumatera Utara	,\
    2931	:	20356	Batu Penjemuran	Namo Rambe	Kab.	Deli Serdang	Sumatera Utara	,\
    2932	:	20356	Batu Rejo	Namo Rambe	Kab.	Deli Serdang	Sumatera Utara	,\
    2933	:	20356	Bekukul	Namo Rambe	Kab.	Deli Serdang	Sumatera Utara	,\
    2934	:	20356	Cinta Rakyat	Namo Rambe	Kab.	Deli Serdang	Sumatera Utara	,\
    2935	:	20356	Deli Tua	Namo Rambe	Kab.	Deli Serdang	Sumatera Utara	,\
    2936	:	20356	Gunung Berita	Namo Rambe	Kab.	Deli Serdang	Sumatera Utara	,\
    2937	:	20356	Gunung Klawas (Kelawas)	Namo Rambe	Kab.	Deli Serdang	Sumatera Utara	,\
    2938	:	20356	Jaba	Namo Rambe	Kab.	Deli Serdang	Sumatera Utara	,\
    2939	:	20356	Jati Kusuma (Kesuma)	Namo Rambe	Kab.	Deli Serdang	Sumatera Utara	,\
    2940	:	20356	Kuala Simeme	Namo Rambe	Kab.	Deli Serdang	Sumatera Utara	,\
    2941	:	20356	Kuta Tengah	Namo Rambe	Kab.	Deli Serdang	Sumatera Utara	,\
    2942	:	20356	Kuta Tuala (Tualah)	Namo Rambe	Kab.	Deli Serdang	Sumatera Utara	,\
    2943	:	20356	Lau Mulgap	Namo Rambe	Kab.	Deli Serdang	Sumatera Utara	,\
    2944	:	20356	Lubang Ido	Namo Rambe	Kab.	Deli Serdang	Sumatera Utara	,\
    2945	:	20356	Namo Batang	Namo Rambe	Kab.	Deli Serdang	Sumatera Utara	,\
    2946	:	20356	Namo Landur	Namo Rambe	Kab.	Deli Serdang	Sumatera Utara	,\
    2947	:	20356	Namo Mbarao (Mbaru)	Namo Rambe	Kab.	Deli Serdang	Sumatera Utara	,\
    2948	:	20356	Namo Mbelin	Namo Rambe	Kab.	Deli Serdang	Sumatera Utara	,\
    2949	:	20356	Namo Mungkur (Rimo Mungkur)	Namo Rambe	Kab.	Deli Serdang	Sumatera Utara	,\
    2950	:	20356	Namo Pakam	Namo Rambe	Kab.	Deli Serdang	Sumatera Utara	,\
    2951	:	20356	Namo Pinang	Namo Rambe	Kab.	Deli Serdang	Sumatera Utara	,\
    2952	:	20356	Namo Rambe	Namo Rambe	Kab.	Deli Serdang	Sumatera Utara	,\
    2953	:	20356	Rumah Keben	Namo Rambe	Kab.	Deli Serdang	Sumatera Utara	,\
    2954	:	20356	Rumah Mbacang	Namo Rambe	Kab.	Deli Serdang	Sumatera Utara	,\
    2955	:	20356	Salang Tungir	Namo Rambe	Kab.	Deli Serdang	Sumatera Utara	,\
    2956	:	20356	Silue Lue	Namo Rambe	Kab.	Deli Serdang	Sumatera Utara	,\
    2957	:	20356	Sudi Rejo	Namo Rambe	Kab.	Deli Serdang	Sumatera Utara	,\
    2958	:	20356	Suka Mulia Hilir	Namo Rambe	Kab.	Deli Serdang	Sumatera Utara	,\
    2959	:	20356	Suka Mulia Hulu	Namo Rambe	Kab.	Deli Serdang	Sumatera Utara	,\
    2960	:	20356	Tangkahan	Namo Rambe	Kab.	Deli Serdang	Sumatera Utara	,\
    2961	:	20356	Tanjung Selamat	Namo Rambe	Kab.	Deli Serdang	Sumatera Utara	,\
    2962	:	20356	Timbang Lawan	Namo Rambe	Kab.	Deli Serdang	Sumatera Utara	,\
    2963	:	20356	Ujung Labuhen	Namo Rambe	Kab.	Deli Serdang	Sumatera Utara	,\
    2964	:	20356	Uruk Gedang	Namo Rambe	Kab.	Deli Serdang	Sumatera Utara	,\
    2965	:	22153	Bekerah	Nama Teran	Kab.	Karo	Sumatera Utara	,\
    2966	:	22153	Gung Pinto	Nama Teran	Kab.	Karo	Sumatera Utara	,\
    2967	:	22153	Kebayaken	Nama Teran	Kab.	Karo	Sumatera Utara	,\
    2968	:	22153	Kuta Gugung	Nama Teran	Kab.	Karo	Sumatera Utara	,\
    2969	:	22153	Kuta Mbelin	Nama Teran	Kab.	Karo	Sumatera Utara	,\
    2970	:	22153	Kuta Rayat	Nama Teran	Kab.	Karo	Sumatera Utara	,\
    2971	:	22153	Kuta Tonggal	Nama Teran	Kab.	Karo	Sumatera Utara	,\
    2972	:	22153	Naman	Nama Teran	Kab.	Karo	Sumatera Utara	,\
    2973	:	22153	Ndeskati	Nama Teran	Kab.	Karo	Sumatera Utara	,\
    2974	:	22153	Sigarang Garang	Nama Teran	Kab.	Karo	Sumatera Utara	,\
    2975	:	22153	Simacem	Nama Teran	Kab.	Karo	Sumatera Utara	,\
    2976	:	22153	Suka Nalu	Nama Teran	Kab.	Karo	Sumatera Utara	,\
    2977	:	22153	Suka Ndebi	Nama Teran	Kab.	Karo	Sumatera Utara	,\
    2978	:	22153	Sukatepu	Nama Teran	Kab.	Karo	Sumatera Utara	,\
    2979	:	22394	Huta Rihit	Nainggolan	Kab.	Samosir	Sumatera Utara	,\
    2980	:	22394	Nainggolan	Nainggolan	Kab.	Samosir	Sumatera Utara	,\
    2981	:	22394	Pananggangan	Nainggolan	Kab.	Samosir	Sumatera Utara	,\
    2982	:	22394	Pangaloan	Nainggolan	Kab.	Samosir	Sumatera Utara	,\
    2983	:	22394	Parhusip III	Nainggolan	Kab.	Samosir	Sumatera Utara	,\
    2984	:	22394	Pasaran I	Nainggolan	Kab.	Samosir	Sumatera Utara	,\
    2985	:	22394	Pasaran Parsaoran	Nainggolan	Kab.	Samosir	Sumatera Utara	,\
    2986	:	22394	Sibonor Ompuratus	Nainggolan	Kab.	Samosir	Sumatera Utara	,\
    2987	:	22394	Sinaga Uruk Pandiangan	Nainggolan	Kab.	Samosir	Sumatera Utara	,\
    2988	:	22394	Sipinggan Lumban Siantar	Nainggolan	Kab.	Samosir	Sumatera Utara	,\
    2989	:	22394	Siruma Hombar	Nainggolan	Kab.	Samosir	Sumatera Utara	,\
    2990	:	22394	Toguan Galung	Nainggolan	Kab.	Samosir	Sumatera Utara	,\
    2991	:	22977	Banua Rakyat	Naga Juang	Kab.	Mandailing Natal	Sumatera Utara	,\
    2992	:	22977	Banua Simanosor	Naga Juang	Kab.	Mandailing Natal	Sumatera Utara	,\
    2993	:	22977	Humbang I	Naga Juang	Kab.	Mandailing Natal	Sumatera Utara	,\
    2994	:	22977	Sayur Matua	Naga Juang	Kab.	Mandailing Natal	Sumatera Utara	,\
    2995	:	22977	Tambiski	Naga Juang	Kab.	Mandailing Natal	Sumatera Utara	,\
    2996	:	21454	Aek Kota Batu	Na IX-X	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    2997	:	21454	Bangun Rejo	Na IX-X	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    2998	:	21454	Batu Tunggal	Na IX-X	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    2999	:	21454	Hatapang	Na IX-X	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3000	:	21454	Kampung Pajak	Na IX-X	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3001	:	21454	Meranti Omas	Na IX-X	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3002	:	21454	Pasang Lela	Na IX-X	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3003	:	21454	Pematang	Na IX-X	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3004	:	21454	Perkebunan Berangir	Na IX-X	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3005	:	21454	Pulo Jantan	Na IX-X	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3006	:	21454	Silumajang	Na IX-X	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3007	:	21454	Simpang Marbau	Na IX-X	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3008	:	21454	Sungai Raja	Na IX-X	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3009	:	22161	Bandar Meriah	Munte	Kab.	Karo	Sumatera Utara	,\
    3010	:	22161	Barung Kersap	Munte	Kab.	Karo	Sumatera Utara	,\
    3011	:	22161	Biak Nampe	Munte	Kab.	Karo	Sumatera Utara	,\
    3012	:	22161	Buluh Naman	Munte	Kab.	Karo	Sumatera Utara	,\
    3013	:	22161	Gunung Manumpak	Munte	Kab.	Karo	Sumatera Utara	,\
    3014	:	22161	Gunung Saribu	Munte	Kab.	Karo	Sumatera Utara	,\
    3015	:	22161	Gurubenua	Munte	Kab.	Karo	Sumatera Utara	,\
    3016	:	22161	Kabantua	Munte	Kab.	Karo	Sumatera Utara	,\
    3017	:	22161	Kineppen	Munte	Kab.	Karo	Sumatera Utara	,\
    3018	:	22161	Kutagerat	Munte	Kab.	Karo	Sumatera Utara	,\
    3019	:	22161	Kutambaru	Munte	Kab.	Karo	Sumatera Utara	,\
    3020	:	22161	Kutasuah	Munte	Kab.	Karo	Sumatera Utara	,\
    3021	:	22161	Munthe	Munte	Kab.	Karo	Sumatera Utara	,\
    3022	:	22161	Nageri	Munte	Kab.	Karo	Sumatera Utara	,\
    3023	:	22161	Parimbalang	Munte	Kab.	Karo	Sumatera Utara	,\
    3024	:	22161	Pertumbungen	Munte	Kab.	Karo	Sumatera Utara	,\
    3025	:	22161	Sarimunte	Munte	Kab.	Karo	Sumatera Utara	,\
    3026	:	22161	Sarinembah	Munte	Kab.	Karo	Sumatera Utara	,\
    3027	:	22161	Selakkar	Munte	Kab.	Karo	Sumatera Utara	,\
    3028	:	22161	Singgamanik	Munte	Kab.	Karo	Sumatera Utara	,\
    3029	:	22161	Sukarame	Munte	Kab.	Karo	Sumatera Utara	,\
    3030	:	22161	Tanjung Beringin	Munte	Kab.	Karo	Sumatera Utara	,\
    3031	:	22998	Bandar Panjang	Muara Sipongi	Kab.	Mandailing Natal	Sumatera Utara	,\
    3032	:	22998	Bandar Panjang Tuo	Muara Sipongi	Kab.	Mandailing Natal	Sumatera Utara	,\
    3033	:	22998	Kampung Pinang	Muara Sipongi	Kab.	Mandailing Natal	Sumatera Utara	,\
    3034	:	22998	Koto Baringin	Muara Sipongi	Kab.	Mandailing Natal	Sumatera Utara	,\
    3035	:	22998	Limau Manis	Muara Sipongi	Kab.	Mandailing Natal	Sumatera Utara	,\
    3036	:	22998	Pasar Muara Sipongi	Muara Sipongi	Kab.	Mandailing Natal	Sumatera Utara	,\
    3037	:	22998	Ranjo Batu	Muara Sipongi	Kab.	Mandailing Natal	Sumatera Utara	,\
    3038	:	22998	Sibinail	Muara Sipongi	Kab.	Mandailing Natal	Sumatera Utara	,\
    3039	:	22998	Simpang Mandepo	Muara Sipongi	Kab.	Mandailing Natal	Sumatera Utara	,\
    3040	:	22998	Tamiang Mudo	Muara Sipongi	Kab.	Mandailing Natal	Sumatera Utara	,\
    3041	:	22998	Tanjung Alai	Muara Sipongi	Kab.	Mandailing Natal	Sumatera Utara	,\
    3042	:	22738	Bandar Hapinis	Muara Batang Toru	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    3043	:	22738	Huta Raja	Muara Batang Toru	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    3044	:	22738	Muara Ampolu	Muara Batang Toru	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    3045	:	22738	Muara Manompas	Muara Batang Toru	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    3046	:	22738	Muara Upu	Muara Batang Toru	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    3047	:	22738	Pardamean	Muara Batang Toru	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    3048	:	22738	Tarapung Raya	Muara Batang Toru	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    3049	:	22989	Batu Mundam	Muara Batang Gadis	Kab.	Mandailing Natal	Sumatera Utara	,\
    3050	:	22989	Huta Imbaru	Muara Batang Gadis	Kab.	Mandailing Natal	Sumatera Utara	,\
    3051	:	22989	Lubuk Kapundung	Muara Batang Gadis	Kab.	Mandailing Natal	Sumatera Utara	,\
    3052	:	22989	Lubuk Kapundung II	Muara Batang Gadis	Kab.	Mandailing Natal	Sumatera Utara	,\
    3053	:	22989	Manuncang	Muara Batang Gadis	Kab.	Mandailing Natal	Sumatera Utara	,\
    3054	:	22989	Panunggulan	Muara Batang Gadis	Kab.	Mandailing Natal	Sumatera Utara	,\
    3055	:	22989	Pasar II Singkuang	Muara Batang Gadis	Kab.	Mandailing Natal	Sumatera Utara	,\
    3056	:	22989	Rantau Panjang	Muara Batang Gadis	Kab.	Mandailing Natal	Sumatera Utara	,\
    3057	:	22989	Sale Baru	Muara Batang Gadis	Kab.	Mandailing Natal	Sumatera Utara	,\
    3058	:	22989	Sikapas	Muara Batang Gadis	Kab.	Mandailing Natal	Sumatera Utara	,\
    3059	:	22989	Singkuang I (Pasar I Singkuang)	Muara Batang Gadis	Kab.	Mandailing Natal	Sumatera Utara	,\
    3060	:	22989	Tabuyung	Muara Batang Gadis	Kab.	Mandailing Natal	Sumatera Utara	,\
    3061	:	22989	Tagilang Julu	Muara Batang Gadis	Kab.	Mandailing Natal	Sumatera Utara	,\
    3062	:	22476	Aritonang	Muara	Kab.	Tapanuli Utara	Sumatera Utara	,\
    3063	:	22476	Bariba Niaek	Muara	Kab.	Tapanuli Utara	Sumatera Utara	,\
    3064	:	22476	Batu Binumbun	Muara	Kab.	Tapanuli Utara	Sumatera Utara	,\
    3065	:	22476	Dolok Martumbur	Muara	Kab.	Tapanuli Utara	Sumatera Utara	,\
    3066	:	22476	Huta Ginjang	Muara	Kab.	Tapanuli Utara	Sumatera Utara	,\
    3067	:	22476	Huta Lontung	Muara	Kab.	Tapanuli Utara	Sumatera Utara	,\
    3068	:	22476	Huta Nagodang	Muara	Kab.	Tapanuli Utara	Sumatera Utara	,\
    3069	:	22476	Papande	Muara	Kab.	Tapanuli Utara	Sumatera Utara	,\
    3070	:	22476	Sampuran	Muara	Kab.	Tapanuli Utara	Sumatera Utara	,\
    3071	:	22476	Sibandang	Muara	Kab.	Tapanuli Utara	Sumatera Utara	,\
    3072	:	22476	Silali Toruan	Muara	Kab.	Tapanuli Utara	Sumatera Utara	,\
    3073	:	22476	Silando	Muara	Kab.	Tapanuli Utara	Sumatera Utara	,\
    3074	:	22476	Simatupang	Muara	Kab.	Tapanuli Utara	Sumatera Utara	,\
    3075	:	22476	Sitanggor	Muara	Kab.	Tapanuli Utara	Sumatera Utara	,\
    3076	:	22476	Unte Mungkur	Muara	Kab.	Tapanuli Utara	Sumatera Utara	,\
    3077	:	22862	Gunung Baru	Moro`o	Kab.	Nias Barat	Sumatera Utara	,\
    3078	:	22862	Hili Soromi	Moro`o	Kab.	Nias Barat	Sumatera Utara	,\
    3079	:	22862	Hili Waele	Moro`o	Kab.	Nias Barat	Sumatera Utara	,\
    3080	:	22862	Hilifadolo	Moro`o	Kab.	Nias Barat	Sumatera Utara	,\
    3081	:	22862	Hiliwaloo II	Moro`o	Kab.	Nias Barat	Sumatera Utara	,\
    3082	:	22862	Lasara Bahili	Moro`o	Kab.	Nias Barat	Sumatera Utara	,\
    3083	:	22862	Onozalukhu You	Moro`o	Kab.	Nias Barat	Sumatera Utara	,\
    3084	:	22862	Sidua Hili	Moro`o	Kab.	Nias Barat	Sumatera Utara	,\
    3085	:	22862	Sitolu Banua Fadoro	Moro`o	Kab.	Nias Barat	Sumatera Utara	,\
    3086	:	22862	Sitolu Ewali	Moro`o	Kab.	Nias Barat	Sumatera Utara	,\
    3087	:	22173	Ajinembah	Merek	Kab.	Karo	Sumatera Utara	,\
    3088	:	22173	Bandar Tongging	Merek	Kab.	Karo	Sumatera Utara	,\
    3089	:	22173	Dokan	Merek	Kab.	Karo	Sumatera Utara	,\
    3090	:	22173	Garingging	Merek	Kab.	Karo	Sumatera Utara	,\
    3091	:	22173	Kodon-Kodon	Merek	Kab.	Karo	Sumatera Utara	,\
    3092	:	22173	Merek	Merek	Kab.	Karo	Sumatera Utara	,\
    3093	:	22173	Mulia Rakyat	Merek	Kab.	Karo	Sumatera Utara	,\
    3094	:	22173	Nagalingga	Merek	Kab.	Karo	Sumatera Utara	,\
    3095	:	22173	Nagara	Merek	Kab.	Karo	Sumatera Utara	,\
    3096	:	22173	Negeri Tongging	Merek	Kab.	Karo	Sumatera Utara	,\
    3097	:	22173	Pancur Batu	Merek	Kab.	Karo	Sumatera Utara	,\
    3098	:	22173	Pangambaten	Merek	Kab.	Karo	Sumatera Utara	,\
    3099	:	22173	Pertibi Lama	Merek	Kab.	Karo	Sumatera Utara	,\
    3100	:	22173	Pertibitembe	Merek	Kab.	Karo	Sumatera Utara	,\
    3101	:	22173	Regaji	Merek	Kab.	Karo	Sumatera Utara	,\
    3102	:	22173	Sibolangit	Merek	Kab.	Karo	Sumatera Utara	,\
    3103	:	22173	Situnggaling	Merek	Kab.	Karo	Sumatera Utara	,\
    3104	:	22173	Sukamandi	Merek	Kab.	Karo	Sumatera Utara	,\
    3105	:	22173	Tongging	Merek	Kab.	Karo	Sumatera Utara	,\
    3106	:	22153	Cinta Rayat	Merdeka	Kab.	Karo	Sumatera Utara	,\
    3107	:	22153	Deram	Merdeka	Kab.	Karo	Sumatera Utara	,\
    3108	:	22153	Gongsol	Merdeka	Kab.	Karo	Sumatera Utara	,\
    3109	:	22153	Jaranguda	Merdeka	Kab.	Karo	Sumatera Utara	,\
    3110	:	22153	Merdeka	Merdeka	Kab.	Karo	Sumatera Utara	,\
    3111	:	22153	Sada Perarih	Merdeka	Kab.	Karo	Sumatera Utara	,\
    3112	:	22153	Semangat	Merdeka	Kab.	Karo	Sumatera Utara	,\
    3113	:	22153	Semangat Gunung	Merdeka	Kab.	Karo	Sumatera Utara	,\
    3114	:	22153	Ujung Teran	Merdeka	Kab.	Karo	Sumatera Utara	,\
    3115	:	21264	Air Putih	Meranti	Kab.	Asahan	Sumatera Utara	,\
    3116	:	21264	Gajah	Meranti	Kab.	Asahan	Sumatera Utara	,\
    3117	:	21264	Meranti	Meranti	Kab.	Asahan	Sumatera Utara	,\
    3118	:	21264	Perkebunan Sei Balai (Baleh)	Meranti	Kab.	Asahan	Sumatera Utara	,\
    3119	:	21264	Sei Beluru	Meranti	Kab.	Asahan	Sumatera Utara	,\
    3120	:	21264	Serdang	Meranti	Kab.	Asahan	Sumatera Utara	,\
    3121	:	21264	Sukajadi	Meranti	Kab.	Asahan	Sumatera Utara	,\
    3122	:	21258	Aek Nauli	Medang Deras	Kab.	Batu Bara	Sumatera Utara	,\
    3123	:	21258	Cengkering Pekan	Medang Deras	Kab.	Batu Bara	Sumatera Utara	,\
    3124	:	21258	Durian	Medang Deras	Kab.	Batu Bara	Sumatera Utara	,\
    3125	:	21258	Lalang	Medang Deras	Kab.	Batu Bara	Sumatera Utara	,\
    3126	:	21258	Mandarsah	Medang Deras	Kab.	Batu Bara	Sumatera Utara	,\
    3127	:	21258	Medang	Medang Deras	Kab.	Batu Bara	Sumatera Utara	,\
    3128	:	21258	Medang Baru	Medang Deras	Kab.	Batu Bara	Sumatera Utara	,\
    3129	:	21258	Nenas Siam	Medang Deras	Kab.	Batu Bara	Sumatera Utara	,\
    3130	:	21258	Pagurawan	Medang Deras	Kab.	Batu Bara	Sumatera Utara	,\
    3131	:	21258	Pakam	Medang Deras	Kab.	Batu Bara	Sumatera Utara	,\
    3132	:	21258	Pakam Raya	Medang Deras	Kab.	Batu Bara	Sumatera Utara	,\
    3133	:	21258	Pakam Raya Selatan	Medang Deras	Kab.	Batu Bara	Sumatera Utara	,\
    3134	:	21258	Pangkalan Dodek	Medang Deras	Kab.	Batu Bara	Sumatera Utara	,\
    3135	:	21258	Pangkalan Dodek Baru	Medang Deras	Kab.	Batu Bara	Sumatera Utara	,\
    3136	:	21258	Pematang Cengkering	Medang Deras	Kab.	Batu Bara	Sumatera Utara	,\
    3137	:	21258	Pematang Nibung	Medang Deras	Kab.	Batu Bara	Sumatera Utara	,\
    3138	:	21258	Sei Buah Keras	Medang Deras	Kab.	Batu Bara	Sumatera Utara	,\
    3139	:	21258	Sei Raja	Medang Deras	Kab.	Batu Bara	Sumatera Utara	,\
    3140	:	21258	Sei Rakyat	Medang Deras	Kab.	Batu Bara	Sumatera Utara	,\
    3141	:	21258	Sidomulyo	Medang Deras	Kab.	Batu Bara	Sumatera Utara	,\
    3142	:	21258	Tanjung Sigoni	Medang Deras	Kab.	Batu Bara	Sumatera Utara	,\
    3143	:	20136	Kemenangan Tani	Medan Tuntungan	Kota	Medan	Sumatera Utara	,\
    3144	:	20138	Ladang Bambu	Medan Tuntungan	Kota	Medan	Sumatera Utara	,\
    3145	:	20136	Lau Cih	Medan Tuntungan	Kota	Medan	Sumatera Utara	,\
    3146	:	20141	Mangga	Medan Tuntungan	Kota	Medan	Sumatera Utara	,\
    3147	:	20136	Namu Gajah	Medan Tuntungan	Kota	Medan	Sumatera Utara	,\
    3148	:	20137	Sidomulyo	Medan Tuntungan	Kota	Medan	Sumatera Utara	,\
    3149	:	20135	Simalingkar B	Medan Tuntungan	Kota	Medan	Sumatera Utara	,\
    3150	:	20135	Simpang Selayang	Medan Tuntungan	Kota	Medan	Sumatera Utara	,\
    3151	:	20134	Tanjung Selamat	Medan Tuntungan	Kota	Medan	Sumatera Utara	,\
    3152	:	20235	Durian	Medan Timur	Kota	Medan	Sumatera Utara	,\
    3153	:	20235	Gaharu	Medan Timur	Kota	Medan	Sumatera Utara	,\
    3154	:	20231	Gang Buntu	Medan Timur	Kota	Medan	Sumatera Utara	,\
    3155	:	20238	Glugur Darat I	Medan Timur	Kota	Medan	Sumatera Utara	,\
    3156	:	20238	Glugur Darat II	Medan Timur	Kota	Medan	Sumatera Utara	,\
    3157	:	20231	Perintis	Medan Timur	Kota	Medan	Sumatera Utara	,\
    3158	:	20239	Pulo Brayan Bengkel	Medan Timur	Kota	Medan	Sumatera Utara	,\
    3159	:	20239	Pulo Brayan Bengkel Baru	Medan Timur	Kota	Medan	Sumatera Utara	,\
    3160	:	20239	Pulo Brayan Darat I	Medan Timur	Kota	Medan	Sumatera Utara	,\
    3161	:	20239	Pulo Brayan Darat II	Medan Timur	Kota	Medan	Sumatera Utara	,\
    3162	:	20234	Sidodadi	Medan Timur	Kota	Medan	Sumatera Utara	,\
    3163	:	20223	Bandar Selamat	Medan Tembung	Kota	Medan	Sumatera Utara	,\
    3164	:	20224	Bantan	Medan Tembung	Kota	Medan	Sumatera Utara	,\
    3165	:	20224	Bantan Timur	Medan Tembung	Kota	Medan	Sumatera Utara	,\
    3166	:	20221	Indra Kasih	Medan Tembung	Kota	Medan	Sumatera Utara	,\
    3167	:	20222	Sidorejo	Medan Tembung	Kota	Medan	Sumatera Utara	,\
    3168	:	20222	Sidorejo Hilir	Medan Tembung	Kota	Medan	Sumatera Utara	,\
    3169	:	20225	Tembung	Medan Tembung	Kota	Medan	Sumatera Utara	,\
    3170	:	20121	Babura Sunggal	Medan Sunggal	Kota	Medan	Sumatera Utara	,\
    3171	:	20127	Lalang	Medan Sunggal	Kota	Medan	Sumatera Utara	,\
    3172	:	20122	Sei Sikambing B	Medan Sunggal	Kota	Medan	Sumatera Utara	,\
    3173	:	20122	Simpang Tanjung	Medan Sunggal	Kota	Medan	Sumatera Utara	,\
    3174	:	20128	Sunggal	Medan Sunggal	Kota	Medan	Sumatera Utara	,\
    3175	:	20122	Tanjung Rejo	Medan Sunggal	Kota	Medan	Sumatera Utara	,\
    3176	:	20133	Asam Kumbang	Medan Selayang	Kota	Medan	Sumatera Utara	,\
    3177	:	20131	Beringin	Medan Selayang	Kota	Medan	Sumatera Utara	,\
    3178	:	20131	Padang Bulan Selayang I	Medan Selayang	Kota	Medan	Sumatera Utara	,\
    3179	:	20131	Padang Bulan Selayang II	Medan Selayang	Kota	Medan	Sumatera Utara	,\
    3180	:	20132	Sempakata	Medan Selayang	Kota	Medan	Sumatera Utara	,\
    3181	:	20132	Tanjung Sari	Medan Selayang	Kota	Medan	Sumatera Utara	,\
    3182	:	20152	Anggrung	Medan Polonia	Kota	Medan	Sumatera Utara	,\
    3183	:	20152	Madras Hulu	Medan Polonia	Kota	Medan	Sumatera Utara	,\
    3184	:	20157	Polonia	Medan Polonia	Kota	Medan	Sumatera Utara	,\
    3185	:	20157	Sari Rejo	Medan Polonia	Kota	Medan	Sumatera Utara	,\
    3186	:	20157	Suka Damai	Medan Polonia	Kota	Medan	Sumatera Utara	,\
    3187	:	20112	Petisah Tengah	Medan Petisah	Kota	Medan	Sumatera Utara	,\
    3188	:	20118	Sei Putih Barat	Medan Petisah	Kota	Medan	Sumatera Utara	,\
    3189	:	20118	Sei Putih Tengah	Medan Petisah	Kota	Medan	Sumatera Utara	,\
    3190	:	20118	Sei Putih Timur I	Medan Petisah	Kota	Medan	Sumatera Utara	,\
    3191	:	20118	Sei Putih Timur II	Medan Petisah	Kota	Medan	Sumatera Utara	,\
    3192	:	20119	Sei Sikambing D	Medan Petisah	Kota	Medan	Sumatera Utara	,\
    3193	:	20113	Sekip	Medan Petisah	Kota	Medan	Sumatera Utara	,\
    3194	:	20233	Pahlawan	Medan Perjuangan	Kota	Medan	Sumatera Utara	,\
    3195	:	20232	Pandau Hilir	Medan Perjuangan	Kota	Medan	Sumatera Utara	,\
    3196	:	20233	Sei Kera Hulu	Medan Perjuangan	Kota	Medan	Sumatera Utara	,\
    3197	:	20233	Sei Kerah Hilir I	Medan Perjuangan	Kota	Medan	Sumatera Utara	,\
    3198	:	20233	Sei Kerah Hilir II	Medan Perjuangan	Kota	Medan	Sumatera Utara	,\
    3199	:	20236	Sidorame Barat I	Medan Perjuangan	Kota	Medan	Sumatera Utara	,\
    3200	:	20236	Sidorame Barat II	Medan Perjuangan	Kota	Medan	Sumatera Utara	,\
    3201	:	20236	Sidorame Timur	Medan Perjuangan	Kota	Medan	Sumatera Utara	,\
    3202	:	20237	Tegal Rejo	Medan Perjuangan	Kota	Medan	Sumatera Utara	,\
    3203	:	20254	Labuhan Deli	Medan Marelan	Kota	Medan	Sumatera Utara	,\
    3204	:	20250	Paya Pasir	Medan Marelan	Kota	Medan	Sumatera Utara	,\
    3205	:	20255	Rengas Pulau	Medan Marelan	Kota	Medan	Sumatera Utara	,\
    3206	:	20245	Tanah Enam Ratus	Medan Marelan	Kota	Medan	Sumatera Utara	,\
    3207	:	20256	Terjun	Medan Marelan	Kota	Medan	Sumatera Utara	,\
    3208	:	20151	Aur	Medan Maimun	Kota	Medan	Sumatera Utara	,\
    3209	:	20151	Hamdan	Medan Maimun	Kota	Medan	Sumatera Utara	,\
    3210	:	20152	Jati	Medan Maimun	Kota	Medan	Sumatera Utara	,\
    3211	:	20158	Kampung Baru	Medan Maimun	Kota	Medan	Sumatera Utara	,\
    3212	:	20159	Sei Mati	Medan Maimun	Kota	Medan	Sumatera Utara	,\
    3213	:	20159	Suka Raja	Medan Maimun	Kota	Medan	Sumatera Utara	,\
    3214	:	20251	Besar	Medan Labuhan	Kota	Medan	Sumatera Utara	,\
    3215	:	20252	Martubung	Medan Labuhan	Kota	Medan	Sumatera Utara	,\
    3216	:	20524	Nelayan Indah	Medan Labuhan	Kota	Medan	Sumatera Utara	,\
    3217	:	20253	Pekan Labuhan	Medan Labuhan	Kota	Medan	Sumatera Utara	,\
    3218	:	20252	Sei Mati	Medan Labuhan	Kota	Medan	Sumatera Utara	,\
    3219	:	20525	Tangkahan	Medan Labuhan	Kota	Medan	Sumatera Utara	,\
    3220	:	20215	Kota Matsum III	Medan Kota	Kota	Medan	Sumatera Utara	,\
    3221	:	20213	Mesjid	Medan Kota	Kota	Medan	Sumatera Utara	,\
    3222	:	20211	Pandau Hulu I	Medan Kota	Kota	Medan	Sumatera Utara	,\
    3223	:	20212	Pasar Baru	Medan Kota	Kota	Medan	Sumatera Utara	,\
    3224	:	20217	Pasar Merah Barat	Medan Kota	Kota	Medan	Sumatera Utara	,\
    3225	:	20212	Pusat Pasar	Medan Kota	Kota	Medan	Sumatera Utara	,\
    3226	:	20214	Sei Rengas I	Medan Kota	Kota	Medan	Sumatera Utara	,\
    3227	:	20219	Siti Rejo I	Medan Kota	Kota	Medan	Sumatera Utara	,\
    3228	:	20218	Sudi Rejo I	Medan Kota	Kota	Medan	Sumatera Utara	,\
    3229	:	20218	Sudi Rejo II	Medan Kota	Kota	Medan	Sumatera Utara	,\
    3230	:	20217	Teladan Barat	Medan Kota	Kota	Medan	Sumatera Utara	,\
    3231	:	20217	Teladan Timur	Medan Kota	Kota	Medan	Sumatera Utara	,\
    3232	:	20144	Gedung Johor	Medan Johor	Kota	Medan	Sumatera Utara	,\
    3233	:	20145	Kedai Durian	Medan Johor	Kota	Medan	Sumatera Utara	,\
    3234	:	20142	Kwala Bekala	Medan Johor	Kota	Medan	Sumatera Utara	,\
    3235	:	20143	Pangkalan Masyhur	Medan Johor	Kota	Medan	Sumatera Utara	,\
    3236	:	20146	Suka Maju	Medan Johor	Kota	Medan	Sumatera Utara	,\
    3237	:	20146	Titi Kuning	Medan Johor	Kota	Medan	Sumatera Utara	,\
    3238	:	20126	Cinta Damai	Medan Helvetia	Kota	Medan	Sumatera Utara	,\
    3239	:	20123	Dwi Kora	Medan Helvetia	Kota	Medan	Sumatera Utara	,\
    3240	:	20124	Helvetia	Medan Helvetia	Kota	Medan	Sumatera Utara	,\
    3241	:	20124	Helvetia Tengah	Medan Helvetia	Kota	Medan	Sumatera Utara	,\
    3242	:	20124	Helvetia Timur	Medan Helvetia	Kota	Medan	Sumatera Utara	,\
    3243	:	20123	Sei Sikambing C II	Medan Helvetia	Kota	Medan	Sumatera Utara	,\
    3244	:	20125	Tanjung Gusta	Medan Helvetia	Kota	Medan	Sumatera Utara	,\
    3245	:	20228	Binjai	Medan Denai	Kota	Medan	Sumatera Utara	,\
    3246	:	20227	Denai	Medan Denai	Kota	Medan	Sumatera Utara	,\
    3247	:	20228	Medan Tenggara	Medan Denai	Kota	Medan	Sumatera Utara	,\
    3248	:	20226	Tegal Sari Mandala I	Medan Denai	Kota	Medan	Sumatera Utara	,\
    3249	:	20226	Tegal Sari Mandala II	Medan Denai	Kota	Medan	Sumatera Utara	,\
    3250	:	20226	Tegal Sari Mandala III	Medan Denai	Kota	Medan	Sumatera Utara	,\
    3251	:	20243	Kota Bangun	Medan Deli	Kota	Medan	Sumatera Utara	,\
    3252	:	20242	Mabar	Medan Deli	Kota	Medan	Sumatera Utara	,\
    3253	:	20242	Mabar Hilir	Medan Deli	Kota	Medan	Sumatera Utara	,\
    3254	:	20241	Tanjung Mulia	Medan Deli	Kota	Medan	Sumatera Utara	,\
    3255	:	20241	Tanjung Mulia Hilir	Medan Deli	Kota	Medan	Sumatera Utara	,\
    3256	:	20244	Titi Papan	Medan Deli	Kota	Medan	Sumatera Utara	,\
    3257	:	20414	Bagan Deli	Medan Belawan Kota	Kota	Medan	Sumatera Utara	,\
    3258	:	20415	Belawan Bahagia	Medan Belawan Kota	Kota	Medan	Sumatera Utara	,\
    3259	:	20414	Belawan Bahari	Medan Belawan Kota	Kota	Medan	Sumatera Utara	,\
    3260	:	20411	Belawan I	Medan Belawan Kota	Kota	Medan	Sumatera Utara	,\
    3261	:	20412	Belawan II	Medan Belawan Kota	Kota	Medan	Sumatera Utara	,\
    3262	:	20412	Belawan Sicanang	Medan Belawan Kota	Kota	Medan	Sumatera Utara	,\
    3263	:	20154	Babura	Medan Baru	Kota	Medan	Sumatera Utara	,\
    3264	:	20153	Darat	Medan Baru	Kota	Medan	Sumatera Utara	,\
    3265	:	20154	Merdeka	Medan Baru	Kota	Medan	Sumatera Utara	,\
    3266	:	20155	Padang Bulan	Medan Baru	Kota	Medan	Sumatera Utara	,\
    3267	:	20153	Petisah Hulu	Medan Baru	Kota	Medan	Sumatera Utara	,\
    3268	:	20156	Titi Rantai/Rante	Medan Baru	Kota	Medan	Sumatera Utara	,\
    3269	:	20115	Glugur Kota	Medan Barat	Kota	Medan	Sumatera Utara	,\
    3270	:	20117	Karang Berombak	Medan Barat	Kota	Medan	Sumatera Utara	,\
    3271	:	20111	Kesawan	Medan Barat	Kota	Medan	Sumatera Utara	,\
    3272	:	20116	Pulo Brayan Kota	Medan Barat	Kota	Medan	Sumatera Utara	,\
    3273	:	20117	Sei Agul	Medan Barat	Kota	Medan	Sumatera Utara	,\
    3274	:	20114	Silalas	Medan Barat	Kota	Medan	Sumatera Utara	,\
    3275	:	20215	Kota Matsum I	Medan Area	Kota	Medan	Sumatera Utara	,\
    3276	:	20215	Kota Matsum II	Medan Area	Kota	Medan	Sumatera Utara	,\
    3277	:	20215	Kota Matsum IV	Medan Area	Kota	Medan	Sumatera Utara	,\
    3278	:	20211	Pandau Hulu II	Medan Area	Kota	Medan	Sumatera Utara	,\
    3279	:	20217	Pasar Merah Timur	Medan Area	Kota	Medan	Sumatera Utara	,\
    3280	:	20214	Sei Rengas II	Medan Area	Kota	Medan	Sumatera Utara	,\
    3281	:	20214	Sei Rengas Permata	Medan Area	Kota	Medan	Sumatera Utara	,\
    3282	:	20216	Sukaramai I	Medan Area	Kota	Medan	Sumatera Utara	,\
    3283	:	20216	Sukaramai II	Medan Area	Kota	Medan	Sumatera Utara	,\
    3284	:	20216	Tegal Sari I	Medan Area	Kota	Medan	Sumatera Utara	,\
    3285	:	20216	Tegal Sari II	Medan Area	Kota	Medan	Sumatera Utara	,\
    3286	:	20216	Tegal Sari III	Medan Area	Kota	Medan	Sumatera Utara	,\
    3287	:	20229	Amplas	Medan Amplas	Kota	Medan	Sumatera Utara	,\
    3288	:	20149	Bangun Mulia	Medan Amplas	Kota	Medan	Sumatera Utara	,\
    3289	:	20147	Harjosari I	Medan Amplas	Kota	Medan	Sumatera Utara	,\
    3290	:	20147	Harjosari II	Medan Amplas	Kota	Medan	Sumatera Utara	,\
    3291	:	20219	Sitirejo II	Medan Amplas	Kota	Medan	Sumatera Utara	,\
    3292	:	20219	Sitirejo III	Medan Amplas	Kota	Medan	Sumatera Utara	,\
    3293	:	20148	Timbang Deli	Medan Amplas	Kota	Medan	Sumatera Utara	,\
    3294	:	22873	Guigui	Mazo	Kab.	Nias Selatan	Sumatera Utara	,\
    3295	:	22873	Hilimaufa	Mazo	Kab.	Nias Selatan	Sumatera Utara	,\
    3296	:	22873	Hilimbaruzo	Mazo	Kab.	Nias Selatan	Sumatera Utara	,\
    3297	:	22873	Luahandroito	Mazo	Kab.	Nias Selatan	Sumatera Utara	,\
    3298	:	22873	Orahuahili	Mazo	Kab.	Nias Selatan	Sumatera Utara	,\
    3299	:	22873	Siofabanua	Mazo	Kab.	Nias Selatan	Sumatera Utara	,\
    3300	:	22873	Tafulu	Mazo	Kab.	Nias Selatan	Sumatera Utara	,\
    3301	:	22873	Tetegawa`ai	Mazo	Kab.	Nias Selatan	Sumatera Utara	,\
    3302	:	22873	Tetegawa`ai Ehomo	Mazo	Kab.	Nias Selatan	Sumatera Utara	,\
    3303	:	22873	Ulu Mazo	Mazo	Kab.	Nias Selatan	Sumatera Utara	,\
    3304	:	22865	Bawolahusa	Mazino	Kab.	Nias Selatan	Sumatera Utara	,\
    3305	:	22865	Bawolahusa Doli-doli	Mazino	Kab.	Nias Selatan	Sumatera Utara	,\
    3306	:	22865	Hilifondege Hilizoroilawa	Mazino	Kab.	Nias Selatan	Sumatera Utara	,\
    3307	:	22865	Hililaza Hilinawalo Mazino	Mazino	Kab.	Nias Selatan	Sumatera Utara	,\
    3308	:	22865	Hilinawalo Mazino / Mazingo	Mazino	Kab.	Nias Selatan	Sumatera Utara	,\
    3309	:	22865	Hilizalo`otano	Mazino	Kab.	Nias Selatan	Sumatera Utara	,\
    3310	:	22865	Hilizalo`otano Laowo	Mazino	Kab.	Nias Selatan	Sumatera Utara	,\
    3311	:	22865	Hilizalo`otano Larono	Mazino	Kab.	Nias Selatan	Sumatera Utara	,\
    3312	:	22865	Hilizoroilawa	Mazino	Kab.	Nias Selatan	Sumatera Utara	,\
    3313	:	22865	Lawindra	Mazino	Kab.	Nias Selatan	Sumatera Utara	,\
    3314	:	22865	Lolomboli	Mazino	Kab.	Nias Selatan	Sumatera Utara	,\
    3315	:	22165	Bandar Purba	Mardinding	Kab.	Karo	Sumatera Utara	,\
    3316	:	22165	Kuta Pengkih	Mardinding	Kab.	Karo	Sumatera Utara	,\
    3317	:	22165	Lau Kasumpat	Mardinding	Kab.	Karo	Sumatera Utara	,\
    3318	:	22165	Lau Mulgap	Mardinding	Kab.	Karo	Sumatera Utara	,\
    3319	:	22165	Lau Pakam	Mardinding	Kab.	Karo	Sumatera Utara	,\
    3320	:	22165	Lau Pengulu	Mardinding	Kab.	Karo	Sumatera Utara	,\
    3321	:	22165	Lau Solu	Mardinding	Kab.	Karo	Sumatera Utara	,\
    3322	:	22165	Mardingding	Mardinding	Kab.	Karo	Sumatera Utara	,\
    3323	:	22165	Rimo Bunga	Mardinding	Kab.	Karo	Sumatera Utara	,\
    3324	:	22165	Tanjung Pamah	Mardinding	Kab.	Karo	Sumatera Utara	,\
    3325	:	21452	Aek Hitetoras	Marbau	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3326	:	21452	Aek Tapa	Marbau	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3327	:	21452	Babussalam	Marbau	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3328	:	21452	Belongkut	Marbau	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3329	:	21452	Bulung Gihit (Bulungihit)	Marbau	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3330	:	21452	Lobu Rampah	Marbau	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3331	:	21452	Marbau	Marbau	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3332	:	21452	Marbau Selatan	Marbau	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3333	:	21452	Perkebunan Brussel	Marbau	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3334	:	21452	Perkebunan Marbau Selatan	Marbau	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3335	:	21452	Perkebunan Milano	Marbau	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3336	:	21452	Perkebunan Pernantian	Marbau	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3337	:	21452	Pulo Bargot	Marbau	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3338	:	21452	Simpang Empat	Marbau	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3339	:	21452	Sipare Pare Hilir	Marbau	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3340	:	21452	Sipare Pare Tengah	Marbau	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3341	:	21452	Sumber Mulyo	Marbau	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3342	:	21452	Tubiran	Marbau	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3343	:	22738	Aek Nabara	Marancar	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    3344	:	22738	Aek Sabaon	Marancar	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    3345	:	22738	Gapuk Tua	Marancar	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    3346	:	22738	Haunatas	Marancar	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    3347	:	22738	Huraba	Marancar	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    3348	:	22738	Marancar	Marancar	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    3349	:	22738	Marancar Godang	Marancar	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    3350	:	22738	Mombang Boru	Marancar	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    3351	:	22738	Pasar Sempurna	Marancar	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    3352	:	22738	Simaninggir	Marancar	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    3353	:	22738	Sugi Tonga	Marancar	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    3354	:	22738	Tanjung Dolok	Marancar	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    3355	:	22865	Bawogosali	Maniamolo	Kab.	Nias Selatan	Sumatera Utara	,\
    3356	:	22865	Bawohosi Maniamolo	Maniamolo	Kab.	Nias Selatan	Sumatera Utara	,\
    3357	:	22865	Bawomaenamolo	Maniamolo	Kab.	Nias Selatan	Sumatera Utara	,\
    3358	:	22865	Bawosaodano	Maniamolo	Kab.	Nias Selatan	Sumatera Utara	,\
    3359	:	22865	Bonia Hilisimaetano	Maniamolo	Kab.	Nias Selatan	Sumatera Utara	,\
    3360	:	22865	Eho Hilisimaetano	Maniamolo	Kab.	Nias Selatan	Sumatera Utara	,\
    3361	:	22865	Faomasi Hilisimaetano	Maniamolo	Kab.	Nias Selatan	Sumatera Utara	,\
    3362	:	22865	Hiliaurifa Hilisimaetano	Maniamolo	Kab.	Nias Selatan	Sumatera Utara	,\
    3363	:	22865	Hilifalawu	Maniamolo	Kab.	Nias Selatan	Sumatera Utara	,\
    3364	:	22865	Hilimae Namolo	Maniamolo	Kab.	Nias Selatan	Sumatera Utara	,\
    3365	:	22865	Hilisimaetano	Maniamolo	Kab.	Nias Selatan	Sumatera Utara	,\
    3366	:	22865	Idala Jaya	Maniamolo	Kab.	Nias Selatan	Sumatera Utara	,\
    3367	:	22865	Ndraso Hilisimaetano	Maniamolo	Kab.	Nias Selatan	Sumatera Utara	,\
    3368	:	22865	Pekan Hilisimaetano	Maniamolo	Kab.	Nias Selatan	Sumatera Utara	,\
    3369	:	22865	Samadaya Hilisimaetano	Maniamolo	Kab.	Nias Selatan	Sumatera Utara	,\
    3370	:	22865	Soto`o Hilisimaetano	Maniamolo	Kab.	Nias Selatan	Sumatera Utara	,\
    3371	:	22565	Binjohara	Manduamas	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    3372	:	22565	Lae Monong	Manduamas	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    3373	:	22565	Manduamas Lama	Manduamas	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    3374	:	22565	Pagaran Nauli	Manduamas	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    3375	:	22565	Pasar Onan Manduamas	Manduamas	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    3376	:	22565	Saragih	Manduamas	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    3377	:	22565	Sarma Nauli	Manduamas	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    3378	:	22565	Tumba	Manduamas	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    3379	:	22565	Tumba Jae	Manduamas	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    3380	:	22814	Balodano	Mandrehe Utara	Kab.	Nias Barat	Sumatera Utara	,\
    3381	:	22814	Hiambanua	Mandrehe Utara	Kab.	Nias Barat	Sumatera Utara	,\
    3382	:	22814	Hili Mayo	Mandrehe Utara	Kab.	Nias Barat	Sumatera Utara	,\
    3383	:	22814	Hilimbaruzo	Mandrehe Utara	Kab.	Nias Barat	Sumatera Utara	,\
    3384	:	22814	Hilimbowo	Mandrehe Utara	Kab.	Nias Barat	Sumatera Utara	,\
    3385	:	22814	Lahagu	Mandrehe Utara	Kab.	Nias Barat	Sumatera Utara	,\
    3386	:	22814	Lolomboli	Mandrehe Utara	Kab.	Nias Barat	Sumatera Utara	,\
    3387	:	22814	Ononamolo I	Mandrehe Utara	Kab.	Nias Barat	Sumatera Utara	,\
    3388	:	22814	Ononamolo II	Mandrehe Utara	Kab.	Nias Barat	Sumatera Utara	,\
    3389	:	22814	Sihareo	Mandrehe Utara	Kab.	Nias Barat	Sumatera Utara	,\
    3390	:	22814	Taraha	Mandrehe Utara	Kab.	Nias Barat	Sumatera Utara	,\
    3391	:	22814	Tarahoso	Mandrehe Utara	Kab.	Nias Barat	Sumatera Utara	,\
    3392	:	22812	Fadoro Sifulu Banua	Mandrehe Barat	Kab.	Nias Barat	Sumatera Utara	,\
    3393	:	22812	Hilidaura	Mandrehe Barat	Kab.	Nias Barat	Sumatera Utara	,\
    3394	:	22812	Iraonogeba	Mandrehe Barat	Kab.	Nias Barat	Sumatera Utara	,\
    3395	:	22812	Lasara Bagawu	Mandrehe Barat	Kab.	Nias Barat	Sumatera Utara	,\
    3396	:	22812	Lasara Faga	Mandrehe Barat	Kab.	Nias Barat	Sumatera Utara	,\
    3397	:	22812	Lolohia	Mandrehe Barat	Kab.	Nias Barat	Sumatera Utara	,\
    3398	:	22812	Mazingo	Mandrehe Barat	Kab.	Nias Barat	Sumatera Utara	,\
    3399	:	22812	Onolimburaya	Mandrehe Barat	Kab.	Nias Barat	Sumatera Utara	,\
    3400	:	22812	Onolimbuyou	Mandrehe Barat	Kab.	Nias Barat	Sumatera Utara	,\
    3401	:	22812	Ononamolo III	Mandrehe Barat	Kab.	Nias Barat	Sumatera Utara	,\
    3402	:	22812	Orahili Badalu	Mandrehe Barat	Kab.	Nias Barat	Sumatera Utara	,\
    3403	:	22812	Sisarahili II	Mandrehe Barat	Kab.	Nias Barat	Sumatera Utara	,\
    3404	:	22812	Sisobandrao	Mandrehe Barat	Kab.	Nias Barat	Sumatera Utara	,\
    3405	:	22812	Sisobaoho	Mandrehe Barat	Kab.	Nias Barat	Sumatera Utara	,\
    3406	:	22862	Doli-Doli	Mandrehe	Kab.	Nias Barat	Sumatera Utara	,\
    3407	:	22862	Fadoro	Mandrehe	Kab.	Nias Barat	Sumatera Utara	,\
    3408	:	22862	Fadoro Bahili	Mandrehe	Kab.	Nias Barat	Sumatera Utara	,\
    3409	:	22867	Hayo	Mandrehe	Kab.	Nias Barat	Sumatera Utara	,\
    3410	:	22862	Hiliwalo`o I	Mandrehe	Kab.	Nias Barat	Sumatera Utara	,\
    3411	:	22862	Iraono Gambo	Mandrehe	Kab.	Nias Barat	Sumatera Utara	,\
    3412	:	22862	Iriani Gambo	Mandrehe	Kab.	Nias Barat	Sumatera Utara	,\
    3413	:	22862	Lakhena	Mandrehe	Kab.	Nias Barat	Sumatera Utara	,\
    3414	:	22862	Lasara Baene	Mandrehe	Kab.	Nias Barat	Sumatera Utara	,\
    3415	:	22862	Lologolu	Mandrehe	Kab.	Nias Barat	Sumatera Utara	,\
    3416	:	22862	Lolozirugi	Mandrehe	Kab.	Nias Barat	Sumatera Utara	,\
    3417	:	22862	Siana`a	Mandrehe	Kab.	Nias Barat	Sumatera Utara	,\
    3418	:	22862	Simae`asi	Mandrehe	Kab.	Nias Barat	Sumatera Utara	,\
    3419	:	22862	Sisarahili I	Mandrehe	Kab.	Nias Barat	Sumatera Utara	,\
    3420	:	22862	Tetehosi	Mandrehe	Kab.	Nias Barat	Sumatera Utara	,\
    3421	:	22862	Tuhemberua	Mandrehe	Kab.	Nias Barat	Sumatera Utara	,\
    3422	:	22862	Tuho`owo	Mandrehe	Kab.	Nias Barat	Sumatera Utara	,\
    3423	:	22862	Tumori	Mandrehe	Kab.	Nias Barat	Sumatera Utara	,\
    3424	:	22862	Tuwuuna	Mandrehe	Kab.	Nias Barat	Sumatera Utara	,\
    3425	:	22862	ZuzuNdrao	Mandrehe	Kab.	Nias Barat	Sumatera Utara	,\
    3426	:	22852	Atualuo	Ma`u	Kab.	Nias	Sumatera Utara	,\
    3427	:	22852	Balodano	Ma`u	Kab.	Nias	Sumatera Utara	,\
    3428	:	22852	Dekha	Ma`u	Kab.	Nias	Sumatera Utara	,\
    3429	:	22852	Lasara Siwalu Banua	Ma`u	Kab.	Nias	Sumatera Utara	,\
    3430	:	22852	Lewa - Lewa	Ma`u	Kab.	Nias	Sumatera Utara	,\
    3431	:	22852	Lewu Oguru II (Lewuaguru II)	Ma`u	Kab.	Nias	Sumatera Utara	,\
    3432	:	22852	Sihaero III	Ma`u	Kab.	Nias	Sumatera Utara	,\
    3433	:	22852	Sihare`o III Bawosalo`o Berua	Ma`u	Kab.	Nias	Sumatera Utara	,\
    3434	:	22852	Sihare`o III Hilibadalu	Ma`u	Kab.	Nias	Sumatera Utara	,\
    3435	:	22852	Sisarahili Ma U	Ma`u	Kab.	Nias	Sumatera Utara	,\
    3436	:	22852	Tuhemberua	Ma`u	Kab.	Nias	Sumatera Utara	,\
    3437	:	22654	Aek Gambir	Lumut	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    3438	:	22654	Lumut	Lumut	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    3439	:	22654	Lumut Maju	Lumut	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    3440	:	22654	Lumut Nauli	Lumut	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    3441	:	22654	Masundung	Lumut	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    3442	:	22654	Sialogo	Lumut	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    3443	:	22654	Sialogo (Sihalogo)	Lumut	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    3444	:	22386	Aek Natolu Jaya	Lumban Julu	Kab.	Toba Samosir	Sumatera Utara	,\
    3445	:	22386	Hatinggian	Lumban Julu	Kab.	Toba Samosir	Sumatera Utara	,\
    3446	:	22386	Hutanamora	Lumban Julu	Kab.	Toba Samosir	Sumatera Utara	,\
    3447	:	22386	Jangga Dolok	Lumban Julu	Kab.	Toba Samosir	Sumatera Utara	,\
    3448	:	22386	Jangga Toruan	Lumban Julu	Kab.	Toba Samosir	Sumatera Utara	,\
    3449	:	22386	Jonggi Nihuta	Lumban Julu	Kab.	Toba Samosir	Sumatera Utara	,\
    3450	:	22386	Lintong Julu	Lumban Julu	Kab.	Toba Samosir	Sumatera Utara	,\
    3451	:	22386	Pasar Lumban Julu	Lumban Julu	Kab.	Toba Samosir	Sumatera Utara	,\
    3452	:	22386	Sibaruang	Lumban Julu	Kab.	Toba Samosir	Sumatera Utara	,\
    3453	:	22386	Sionggang Selatan	Lumban Julu	Kab.	Toba Samosir	Sumatera Utara	,\
    3454	:	22386	Sionggang Tengah	Lumban Julu	Kab.	Toba Samosir	Sumatera Utara	,\
    3455	:	22386	Sionggang Utara	Lumban Julu	Kab.	Toba Samosir	Sumatera Utara	,\
    3456	:	20511	Bakaran Batu	Lubuk Pakam	Kab.	Deli Serdang	Sumatera Utara	,\
    3457	:	20517	Cemara	Lubuk Pakam	Kab.	Deli Serdang	Sumatera Utara	,\
    3458	:	20511	Lubuk Pakam I-II	Lubuk Pakam	Kab.	Deli Serdang	Sumatera Utara	,\
    3459	:	20512	Lubuk Pakam Pekan	Lubuk Pakam	Kab.	Deli Serdang	Sumatera Utara	,\
    3460	:	20516	Lubuk Pakam Tiga	Lubuk Pakam	Kab.	Deli Serdang	Sumatera Utara	,\
    3461	:	20518	Pagar Jati	Lubuk Pakam	Kab.	Deli Serdang	Sumatera Utara	,\
    3462	:	20515	Pagar Merbau Tiga	Lubuk Pakam	Kab.	Deli Serdang	Sumatera Utara	,\
    3463	:	20513	Paluh Kemiri	Lubuk Pakam	Kab.	Deli Serdang	Sumatera Utara	,\
    3464	:	20518	Pasar Melintang	Lubuk Pakam	Kab.	Deli Serdang	Sumatera Utara	,\
    3465	:	20514	Petapahan	Lubuk Pakam	Kab.	Deli Serdang	Sumatera Utara	,\
    3466	:	20517	Sekip	Lubuk Pakam	Kab.	Deli Serdang	Sumatera Utara	,\
    3467	:	20515	Syahmad	Lubuk Pakam	Kab.	Deli Serdang	Sumatera Utara	,\
    3468	:	20511	Tanjung Garbus	Lubuk Pakam	Kab.	Deli Serdang	Sumatera Utara	,\
    3469	:	22763	Aek Lancat	Lubuk Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    3470	:	22763	Batang Bulu Jae	Lubuk Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    3471	:	22763	Batang Bulu Tanggal	Lubuk Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    3472	:	22763	Batang Tanggal Baru	Lubuk Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    3473	:	22763	Bonal	Lubuk Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    3474	:	22763	Gunung Manobot	Lubuk Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    3475	:	22763	Huta Dolok (Latong)	Lubuk Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    3476	:	22763	Huta Ibus	Lubuk Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    3477	:	22763	Huta Lombang	Lubuk Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    3478	:	22763	Huta Nopan	Lubuk Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    3479	:	22763	Janji Lobi Lima	Lubuk Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    3480	:	22763	Janji Matogu	Lubuk Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    3481	:	22763	Pagaran Jae Batu	Lubuk Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    3482	:	22763	Pagaran Jalu Jalu	Lubuk Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    3483	:	22763	Pagaran Malaka	Lubuk Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    3484	:	22763	Pagaran Mompang	Lubuk Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    3485	:	22763	Pagaran Silindung	Lubuk Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    3486	:	22763	Parsombaan	Lubuk Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    3487	:	22763	Pasar Latong	Lubuk Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    3488	:	22763	Sangkilon	Lubuk Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    3489	:	22763	Siali Ali	Lubuk Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    3490	:	22763	Sihiuk	Lubuk Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    3491	:	22763	Surodingin	Lubuk Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    3492	:	22763	Tangga Bosi	Lubuk Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    3493	:	22851	Baho	Lotu	Kab.	Nias Utara	Sumatera Utara	,\
    3494	:	22851	Dahadano	Lotu	Kab.	Nias Utara	Sumatera Utara	,\
    3495	:	22851	Fadoro Fulolo	Lotu	Kab.	Nias Utara	Sumatera Utara	,\
    3496	:	22851	Hilidundra	Lotu	Kab.	Nias Utara	Sumatera Utara	,\
    3497	:	22851	Hiligeo Afia	Lotu	Kab.	Nias Utara	Sumatera Utara	,\
    3498	:	22851	Hiligodu	Lotu	Kab.	Nias Utara	Sumatera Utara	,\
    3499	:	22851	Lawira I	Lotu	Kab.	Nias Utara	Sumatera Utara	,\
    3500	:	22851	Lawira II	Lotu	Kab.	Nias Utara	Sumatera Utara	,\
    3501	:	22851	Lawira Satua	Lotu	Kab.	Nias Utara	Sumatera Utara	,\
    3502	:	22851	Lolofaoso	Lotu	Kab.	Nias Utara	Sumatera Utara	,\
    3503	:	22851	Lolomboli	Lotu	Kab.	Nias Utara	Sumatera Utara	,\
    3504	:	22851	Lombuzaua	Lotu	Kab.	Nias Utara	Sumatera Utara	,\
    3505	:	22851	Maziaya	Lotu	Kab.	Nias Utara	Sumatera Utara	,\
    3506	:	22864	Amuri	Lolowau	Kab.	Nias Selatan	Sumatera Utara	,\
    3507	:	22864	Bawohosi	Lolowau	Kab.	Nias Selatan	Sumatera Utara	,\
    3508	:	22864	Bawosaloo Siwalawa / Sowalawa	Lolowau	Kab.	Nias Selatan	Sumatera Utara	,\
    3509	:	22864	Botohili	Lolowau	Kab.	Nias Selatan	Sumatera Utara	,\
    3510	:	22864	Hili Fadolo	Lolowau	Kab.	Nias Selatan	Sumatera Utara	,\
    3511	:	22864	Hilikara	Lolowau	Kab.	Nias Selatan	Sumatera Utara	,\
    3512	:	22864	Hilimbowo Siwalawa	Lolowau	Kab.	Nias Selatan	Sumatera Utara	,\
    3513	:	22864	Lolofaoso	Lolowau	Kab.	Nias Selatan	Sumatera Utara	,\
    3514	:	22864	Lolohowa	Lolowau	Kab.	Nias Selatan	Sumatera Utara	,\
    3515	:	22864	Lolomoyo	Lolowau	Kab.	Nias Selatan	Sumatera Utara	,\
    3516	:	22864	Lolowau	Lolowau	Kab.	Nias Selatan	Sumatera Utara	,\
    3517	:	22864	Nituwu Boho	Lolowau	Kab.	Nias Selatan	Sumatera Utara	,\
    3518	:	22864	Samiri	Lolowau	Kab.	Nias Selatan	Sumatera Utara	,\
    3519	:	22864	Sisarahili Ekholo	Lolowau	Kab.	Nias Selatan	Sumatera Utara	,\
    3520	:	22867	Botohili Ndruria	Lolomatua	Kab.	Nias Selatan	Sumatera Utara	,\
    3521	:	22867	Caritas Sogawunasi	Lolomatua	Kab.	Nias Selatan	Sumatera Utara	,\
    3522	:	22867	Ewo	Lolomatua	Kab.	Nias Selatan	Sumatera Utara	,\
    3523	:	22867	Hili Otalua	Lolomatua	Kab.	Nias Selatan	Sumatera Utara	,\
    3524	:	22867	Hilifaondrato	Lolomatua	Kab.	Nias Selatan	Sumatera Utara	,\
    3525	:	22867	Hilisangowola	Lolomatua	Kab.	Nias Selatan	Sumatera Utara	,\
    3526	:	22867	Ko`olotano	Lolomatua	Kab.	Nias Selatan	Sumatera Utara	,\
    3527	:	22867	Koendrafo	Lolomatua	Kab.	Nias Selatan	Sumatera Utara	,\
    3528	:	22867	Lawa-Lawa Luo	Lolomatua	Kab.	Nias Selatan	Sumatera Utara	,\
    3529	:	22867	Orudua Lawa-Lawa Lou	Lolomatua	Kab.	Nias Selatan	Sumatera Utara	,\
    3530	:	22867	Tesikhori	Lolomatua	Kab.	Nias Selatan	Sumatera Utara	,\
    3531	:	22867	Tuhemberua	Lolomatua	Kab.	Nias Selatan	Sumatera Utara	,\
    3532	:	22867	Tumari	Lolomatua	Kab.	Nias Selatan	Sumatera Utara	,\
    3533	:	22875	Ambukha	Lolofitu Moi	Kab.	Nias Barat	Sumatera Utara	,\
    3534	:	22875	Duria	Lolofitu Moi	Kab.	Nias Barat	Sumatera Utara	,\
    3535	:	22875	Hilimbowo Mau	Lolofitu Moi	Kab.	Nias Barat	Sumatera Utara	,\
    3536	:	22875	Hilimbuasi	Lolofitu Moi	Kab.	Nias Barat	Sumatera Utara	,\
    3537	:	22875	Hiliuso	Lolofitu Moi	Kab.	Nias Barat	Sumatera Utara	,\
    3538	:	22875	Lolofitu	Lolofitu Moi	Kab.	Nias Barat	Sumatera Utara	,\
    3539	:	22875	Sisobawino II	Lolofitu Moi	Kab.	Nias Barat	Sumatera Utara	,\
    3540	:	22875	Wango	Lolofitu Moi	Kab.	Nias Barat	Sumatera Utara	,\
    3541	:	22475	Bonan Dolok	Lintong Nihuta	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    3542	:	22475	Dolok Margu (Dolok Marduga)	Lintong Nihuta	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    3543	:	22475	Habeahan	Lintong Nihuta	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    3544	:	22475	Hutasoit	Lintong Nihuta	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    3545	:	22475	Hutasoit II	Lintong Nihuta	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    3546	:	22475	Lobu Tua	Lintong Nihuta	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    3547	:	22475	Naga Saribu I	Lintong Nihuta	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    3548	:	22475	Naga Saribu II	Lintong Nihuta	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    3549	:	22475	Nagasaribu III	Lintong Nihuta	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    3550	:	22475	Nagasaribu IV	Lintong Nihuta	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    3551	:	22475	Nagasaribu V	Lintong Nihuta	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    3552	:	22475	Pargaulan	Lintong Nihuta	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    3553	:	22475	Parulohan	Lintong Nihuta	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    3554	:	22475	Sibuntoan Parpea / Parpean	Lintong Nihuta	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    3555	:	22475	Sibuntuon	Lintong Nihuta	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    3556	:	22475	Sigompul	Lintong Nihuta	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    3557	:	22475	Sigumpar	Lintong Nihuta	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    3558	:	22475	Siharjulu	Lintong Nihuta	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    3559	:	22475	Siponjot	Lintong Nihuta	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    3560	:	22475	Sitio II	Lintong Nihuta	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    3561	:	22475	Sitolu Bahal	Lintong Nihuta	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    3562	:	22475	Tapian Nauli	Lintong Nihuta	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    3563	:	21255	Air Hitam	Limapuluh	Kab.	Batu Bara	Sumatera Utara	,\
    3564	:	21255	Antara	Limapuluh	Kab.	Batu Bara	Sumatera Utara	,\
    3565	:	21255	Barung-Barung	Limapuluh	Kab.	Batu Bara	Sumatera Utara	,\
    3566	:	21255	Bulan-Bulan	Limapuluh	Kab.	Batu Bara	Sumatera Utara	,\
    3567	:	21255	Cahaya Pardomuan	Limapuluh	Kab.	Batu Bara	Sumatera Utara	,\
    3568	:	21255	Empat Negeri	Limapuluh	Kab.	Batu Bara	Sumatera Utara	,\
    3569	:	21255	Gambus Laut	Limapuluh	Kab.	Batu Bara	Sumatera Utara	,\
    3570	:	21255	Guntung	Limapuluh	Kab.	Batu Bara	Sumatera Utara	,\
    3571	:	21255	Gunung Bandung	Limapuluh	Kab.	Batu Bara	Sumatera Utara	,\
    3572	:	21255	Kwala/Kuala Gunung	Limapuluh	Kab.	Batu Bara	Sumatera Utara	,\
    3573	:	21255	Lima Puluh Kota	Limapuluh	Kab.	Batu Bara	Sumatera Utara	,\
    3574	:	21255	Lubuk Besar	Limapuluh	Kab.	Batu Bara	Sumatera Utara	,\
    3575	:	21255	Lubuk Cuik	Limapuluh	Kab.	Batu Bara	Sumatera Utara	,\
    3576	:	21255	Lubuk Hulu	Limapuluh	Kab.	Batu Bara	Sumatera Utara	,\
    3577	:	21255	Mangkai Baru	Limapuluh	Kab.	Batu Bara	Sumatera Utara	,\
    3578	:	21255	Mangkai Lama	Limapuluh	Kab.	Batu Bara	Sumatera Utara	,\
    3579	:	21255	Pasir Permit	Limapuluh	Kab.	Batu Bara	Sumatera Utara	,\
    3580	:	21255	Pematang Panjang	Limapuluh	Kab.	Batu Bara	Sumatera Utara	,\
    3581	:	21255	Pematang Tengah	Limapuluh	Kab.	Batu Bara	Sumatera Utara	,\
    3582	:	21255	Perkebunan Dolok	Limapuluh	Kab.	Batu Bara	Sumatera Utara	,\
    3583	:	21255	Perkebunan Kwala Gunung	Limapuluh	Kab.	Batu Bara	Sumatera Utara	,\
    3584	:	21255	Perkebunan Lima Puluh	Limapuluh	Kab.	Batu Bara	Sumatera Utara	,\
    3585	:	21255	Perkebunan Limau Manis	Limapuluh	Kab.	Batu Bara	Sumatera Utara	,\
    3586	:	21255	Perkebunan Tanah Gambus	Limapuluh	Kab.	Batu Bara	Sumatera Utara	,\
    3587	:	21255	Perkebunan Tanah Itam Hilir	Limapuluh	Kab.	Batu Bara	Sumatera Utara	,\
    3588	:	21255	Perkebunan Tanah Itam Hulu	Limapuluh	Kab.	Batu Bara	Sumatera Utara	,\
    3589	:	21255	Perupuk	Limapuluh	Kab.	Batu Bara	Sumatera Utara	,\
    3590	:	21255	Pulau Sejuk	Limapuluh	Kab.	Batu Bara	Sumatera Utara	,\
    3591	:	21255	Simpang Dolok	Limapuluh	Kab.	Batu Bara	Sumatera Utara	,\
    3592	:	21255	Simpang Gambus	Limapuluh	Kab.	Batu Bara	Sumatera Utara	,\
    3593	:	21255	Sumber Makmur	Limapuluh	Kab.	Batu Bara	Sumatera Utara	,\
    3594	:	21255	Sumber Padi	Limapuluh	Kab.	Batu Bara	Sumatera Utara	,\
    3595	:	21255	Sumber Rejo	Limapuluh	Kab.	Batu Bara	Sumatera Utara	,\
    3596	:	21255	Titi Merah	Limapuluh	Kab.	Batu Bara	Sumatera Utara	,\
    3597	:	21255	Titi Putih	Limapuluh	Kab.	Batu Bara	Sumatera Utara	,\
    3598	:	22994	Aek Marian Mg	Lembah Sorik Merapi	Kab.	Mandailing Natal	Sumatera Utara	,\
    3599	:	22994	Bangun Purba	Lembah Sorik Merapi	Kab.	Mandailing Natal	Sumatera Utara	,\
    3600	:	22994	Maga Dolok	Lembah Sorik Merapi	Kab.	Mandailing Natal	Sumatera Utara	,\
    3601	:	22994	Maga Lombang	Lembah Sorik Merapi	Kab.	Mandailing Natal	Sumatera Utara	,\
    3602	:	22994	Pangkat	Lembah Sorik Merapi	Kab.	Mandailing Natal	Sumatera Utara	,\
    3603	:	22994	Pasar Maga	Lembah Sorik Merapi	Kab.	Mandailing Natal	Sumatera Utara	,\
    3604	:	22994	Purba Baru	Lembah Sorik Merapi	Kab.	Mandailing Natal	Sumatera Utara	,\
    3605	:	22994	Purba Lamo	Lembah Sorik Merapi	Kab.	Mandailing Natal	Sumatera Utara	,\
    3606	:	22994	Sian Tona	Lembah Sorik Merapi	Kab.	Mandailing Natal	Sumatera Utara	,\
    3607	:	22164	Buluh Pancur	Laubaleng	Kab.	Karo	Sumatera Utara	,\
    3608	:	22164	Durin Rugun	Laubaleng	Kab.	Karo	Sumatera Utara	,\
    3609	:	22164	Kinangkong	Laubaleng	Kab.	Karo	Sumatera Utara	,\
    3610	:	22164	Kutambelin	Laubaleng	Kab.	Karo	Sumatera Utara	,\
    3611	:	22164	Lau Baleng	Laubaleng	Kab.	Karo	Sumatera Utara	,\
    3612	:	22164	Lau Peradep	Laubaleng	Kab.	Karo	Sumatera Utara	,\
    3613	:	22164	Lau Peranggunen (Peranggunan)	Laubaleng	Kab.	Karo	Sumatera Utara	,\
    3614	:	22164	Lingga Muda	Laubaleng	Kab.	Karo	Sumatera Utara	,\
    3615	:	22164	Martelu	Laubaleng	Kab.	Karo	Sumatera Utara	,\
    3616	:	22164	Mbal-Mbal Petarum	Laubaleng	Kab.	Karo	Sumatera Utara	,\
    3617	:	22164	Perbulan	Laubaleng	Kab.	Karo	Sumatera Utara	,\
    3618	:	22164	Rambah Tampu	Laubaleng	Kab.	Karo	Sumatera Utara	,\
    3619	:	22164	Tanjung Gunung	Laubaleng	Kab.	Karo	Sumatera Utara	,\
    3620	:	22983	Aek Garinggin	Langga Bayu (Lingga Bayu)	Kab.	Mandailing Natal	Sumatera Utara	,\
    3621	:	22983	Aek Manyuruk	Langga Bayu (Lingga Bayu)	Kab.	Mandailing Natal	Sumatera Utara	,\
    3622	:	22983	Bandar Limabun	Langga Bayu (Lingga Bayu)	Kab.	Mandailing Natal	Sumatera Utara	,\
    3623	:	22983	Batu Gajah	Langga Bayu (Lingga Bayu)	Kab.	Mandailing Natal	Sumatera Utara	,\
    3624	:	22983	Bonca Bayuon	Langga Bayu (Lingga Bayu)	Kab.	Mandailing Natal	Sumatera Utara	,\
    3625	:	22983	Dalan Lidang	Langga Bayu (Lingga Bayu)	Kab.	Mandailing Natal	Sumatera Utara	,\
    3626	:	22983	Kampung Baru	Langga Bayu (Lingga Bayu)	Kab.	Mandailing Natal	Sumatera Utara	,\
    3627	:	22983	Lobung	Langga Bayu (Lingga Bayu)	Kab.	Mandailing Natal	Sumatera Utara	,\
    3628	:	22983	Padang Silojongan	Langga Bayu (Lingga Bayu)	Kab.	Mandailing Natal	Sumatera Utara	,\
    3629	:	22983	Pangkalan	Langga Bayu (Lingga Bayu)	Kab.	Mandailing Natal	Sumatera Utara	,\
    3630	:	22983	Perbatasan	Langga Bayu (Lingga Bayu)	Kab.	Mandailing Natal	Sumatera Utara	,\
    3631	:	22983	Perk. Simpang Gambir	Langga Bayu (Lingga Bayu)	Kab.	Mandailing Natal	Sumatera Utara	,\
    3632	:	22983	Sikumbu	Langga Bayu (Lingga Bayu)	Kab.	Mandailing Natal	Sumatera Utara	,\
    3633	:	22983	Simpang Bajole	Langga Bayu (Lingga Bayu)	Kab.	Mandailing Natal	Sumatera Utara	,\
    3634	:	22983	Simpang Duku	Langga Bayu (Lingga Bayu)	Kab.	Mandailing Natal	Sumatera Utara	,\
    3635	:	22983	Simpang Durian	Langga Bayu (Lingga Bayu)	Kab.	Mandailing Natal	Sumatera Utara	,\
    3636	:	22983	Simpang Gambir	Langga Bayu (Lingga Bayu)	Kab.	Mandailing Natal	Sumatera Utara	,\
    3637	:	22983	Simpang Koje	Langga Bayu (Lingga Bayu)	Kab.	Mandailing Natal	Sumatera Utara	,\
    3638	:	22983	Tangsi Atas	Langga Bayu (Lingga Bayu)	Kab.	Mandailing Natal	Sumatera Utara	,\
    3639	:	22983	Tapus	Langga Bayu (Lingga Bayu)	Kab.	Mandailing Natal	Sumatera Utara	,\
    3640	:	22983	Ulu Torusan	Langga Bayu (Lingga Bayu)	Kab.	Mandailing Natal	Sumatera Utara	,\
    3641	:	22874	Angorudua Balaekha	Lahusa	Kab.	Nias Selatan	Sumatera Utara	,\
    3642	:	22874	Bawolato	Lahusa	Kab.	Nias Selatan	Sumatera Utara	,\
    3643	:	22874	Bawootalua	Lahusa	Kab.	Nias Selatan	Sumatera Utara	,\
    3644	:	22874	Bawozihono	Lahusa	Kab.	Nias Selatan	Sumatera Utara	,\
    3645	:	22874	Golambanua I	Lahusa	Kab.	Nias Selatan	Sumatera Utara	,\
    3646	:	22874	Harenoro	Lahusa	Kab.	Nias Selatan	Sumatera Utara	,\
    3647	:	22874	Hiliabolata	Lahusa	Kab.	Nias Selatan	Sumatera Utara	,\
    3648	:	22874	Hiligambukha	Lahusa	Kab.	Nias Selatan	Sumatera Utara	,\
    3649	:	22874	Hilinawalo Balaekha	Lahusa	Kab.	Nias Selatan	Sumatera Utara	,\
    3650	:	22874	Hiliorudua	Lahusa	Kab.	Nias Selatan	Sumatera Utara	,\
    3651	:	22874	Hilisimaetano	Lahusa	Kab.	Nias Selatan	Sumatera Utara	,\
    3652	:	22874	Hiliwatema	Lahusa	Kab.	Nias Selatan	Sumatera Utara	,\
    3653	:	22874	Hilizomboi	Lahusa	Kab.	Nias Selatan	Sumatera Utara	,\
    3654	:	22874	Lahusa	Lahusa	Kab.	Nias Selatan	Sumatera Utara	,\
    3655	:	22874	Lahusa Satu	Lahusa	Kab.	Nias Selatan	Sumatera Utara	,\
    3656	:	22874	Mogae	Lahusa	Kab.	Nias Selatan	Sumatera Utara	,\
    3657	:	22874	Oikhoda Balaekha	Lahusa	Kab.	Nias Selatan	Sumatera Utara	,\
    3658	:	22874	Orahili Balaekha	Lahusa	Kab.	Nias Selatan	Sumatera Utara	,\
    3659	:	22874	Sarahililaza	Lahusa	Kab.	Nias Selatan	Sumatera Utara	,\
    3660	:	22874	Sinar Baho	Lahusa	Kab.	Nias Selatan	Sumatera Utara	,\
    3661	:	22874	Sinar Baru	Lahusa	Kab.	Nias Selatan	Sumatera Utara	,\
    3662	:	22874	Sobawagoli	Lahusa	Kab.	Nias Selatan	Sumatera Utara	,\
    3663	:	22874	Tetezou (Fetezou)	Lahusa	Kab.	Nias Selatan	Sumatera Utara	,\
    3664	:	22864	Bawozamaiwo	Lahomi (Gahori)	Kab.	Nias Barat	Sumatera Utara	,\
    3665	:	22864	Hiliadulo	Lahomi (Gahori)	Kab.	Nias Barat	Sumatera Utara	,\
    3666	:	22864	Iraonogaila	Lahomi (Gahori)	Kab.	Nias Barat	Sumatera Utara	,\
    3667	:	22864	Lologundre	Lahomi (Gahori)	Kab.	Nias Barat	Sumatera Utara	,\
    3668	:	22864	Lolowau	Lahomi (Gahori)	Kab.	Nias Barat	Sumatera Utara	,\
    3669	:	22864	Ono Limbu	Lahomi (Gahori)	Kab.	Nias Barat	Sumatera Utara	,\
    3670	:	22864	Ono Waembo	Lahomi (Gahori)	Kab.	Nias Barat	Sumatera Utara	,\
    3671	:	22864	Sisobambowo	Lahomi (Gahori)	Kab.	Nias Barat	Sumatera Utara	,\
    3672	:	22864	Sisobaoho	Lahomi (Gahori)	Kab.	Nias Barat	Sumatera Utara	,\
    3673	:	22864	Sitolu Banua	Lahomi (Gahori)	Kab.	Nias Barat	Sumatera Utara	,\
    3674	:	22864	Tiga Serangkai	Lahomi (Gahori)	Kab.	Nias Barat	Sumatera Utara	,\
    3675	:	22851	Laowowaga	Lahewa Timur	Kab.	Nias Utara	Sumatera Utara	,\
    3676	:	22851	Lukhu Lase	Lahewa Timur	Kab.	Nias Utara	Sumatera Utara	,\
    3677	:	22851	Meafu	Lahewa Timur	Kab.	Nias Utara	Sumatera Utara	,\
    3678	:	22851	Muzoi	Lahewa Timur	Kab.	Nias Utara	Sumatera Utara	,\
    3679	:	22851	Tefao	Lahewa Timur	Kab.	Nias Utara	Sumatera Utara	,\
    3680	:	22851	Tetehosi Sorowi	Lahewa Timur	Kab.	Nias Utara	Sumatera Utara	,\
    3681	:	22851	Tugala Lauru	Lahewa Timur	Kab.	Nias Utara	Sumatera Utara	,\
    3682	:	22853	Afia	Lahewa	Kab.	Nias Utara	Sumatera Utara	,\
    3683	:	22853	Balefadoro Tuho	Lahewa	Kab.	Nias Utara	Sumatera Utara	,\
    3684	:	22853	Fadoro Hilihambawa	Lahewa	Kab.	Nias Utara	Sumatera Utara	,\
    3685	:	22853	Fadoro Hilimbowo	Lahewa	Kab.	Nias Utara	Sumatera Utara	,\
    3686	:	22853	Fadoro Sitolu Hili	Lahewa	Kab.	Nias Utara	Sumatera Utara	,\
    3687	:	22853	Hili Gawolo	Lahewa	Kab.	Nias Utara	Sumatera Utara	,\
    3688	:	22853	Hili Goduhoya	Lahewa	Kab.	Nias Utara	Sumatera Utara	,\
    3689	:	22853	Hili Hati	Lahewa	Kab.	Nias Utara	Sumatera Utara	,\
    3690	:	22853	Hilina A	Lahewa	Kab.	Nias Utara	Sumatera Utara	,\
    3691	:	22853	Hilizukhu	Lahewa	Kab.	Nias Utara	Sumatera Utara	,\
    3692	:	22853	Holi	Lahewa	Kab.	Nias Utara	Sumatera Utara	,\
    3693	:	22853	Iraono Lase	Lahewa	Kab.	Nias Utara	Sumatera Utara	,\
    3694	:	22853	Lahewa (Pasar Lahewa)	Lahewa	Kab.	Nias Utara	Sumatera Utara	,\
    3695	:	22853	Lasara	Lahewa	Kab.	Nias Utara	Sumatera Utara	,\
    3696	:	22853	Marafala	Lahewa	Kab.	Nias Utara	Sumatera Utara	,\
    3697	:	22853	Moawo	Lahewa	Kab.	Nias Utara	Sumatera Utara	,\
    3698	:	22853	Ombolata	Lahewa	Kab.	Nias Utara	Sumatera Utara	,\
    3699	:	22853	Onozalukhu	Lahewa	Kab.	Nias Utara	Sumatera Utara	,\
    3700	:	22853	Sifaoroasi	Lahewa	Kab.	Nias Utara	Sumatera Utara	,\
    3701	:	22853	Siheneasi	Lahewa	Kab.	Nias Utara	Sumatera Utara	,\
    3702	:	22853	Sitolu Banua	Lahewa	Kab.	Nias Utara	Sumatera Utara	,\
    3703	:	22381	Aruan	Laguboti	Kab.	Toba Samosir	Sumatera Utara	,\
    3704	:	22381	Gasa Ribu	Laguboti	Kab.	Toba Samosir	Sumatera Utara	,\
    3705	:	22381	Haunatas I	Laguboti	Kab.	Toba Samosir	Sumatera Utara	,\
    3706	:	22381	Haunatas II	Laguboti	Kab.	Toba Samosir	Sumatera Utara	,\
    3707	:	22381	Lumban Bagasan	Laguboti	Kab.	Toba Samosir	Sumatera Utara	,\
    3708	:	22381	Lumban Binanga	Laguboti	Kab.	Toba Samosir	Sumatera Utara	,\
    3709	:	22381	Ompu Raja Hatulian	Laguboti	Kab.	Toba Samosir	Sumatera Utara	,\
    3710	:	22381	Ompu Raja Hutapea	Laguboti	Kab.	Toba Samosir	Sumatera Utara	,\
    3711	:	22381	Ompu Raja Hutapea Timur	Laguboti	Kab.	Toba Samosir	Sumatera Utara	,\
    3712	:	22381	Pardinggaran	Laguboti	Kab.	Toba Samosir	Sumatera Utara	,\
    3713	:	22381	Pardomuan Nauli	Laguboti	Kab.	Toba Samosir	Sumatera Utara	,\
    3714	:	22381	Pasar Lagu Boti	Laguboti	Kab.	Toba Samosir	Sumatera Utara	,\
    3715	:	22381	Pintu Bosi	Laguboti	Kab.	Toba Samosir	Sumatera Utara	,\
    3716	:	22381	Sibarani Nasampulu	Laguboti	Kab.	Toba Samosir	Sumatera Utara	,\
    3717	:	22381	Sibuea	Laguboti	Kab.	Toba Samosir	Sumatera Utara	,\
    3718	:	22381	Sidulang	Laguboti	Kab.	Toba Samosir	Sumatera Utara	,\
    3719	:	22381	Simatibung	Laguboti	Kab.	Toba Samosir	Sumatera Utara	,\
    3720	:	22381	Sintong Marnipi	Laguboti	Kab.	Toba Samosir	Sumatera Utara	,\
    3721	:	22381	Siraja Gorat	Laguboti	Kab.	Toba Samosir	Sumatera Utara	,\
    3722	:	22381	Sitangkola	Laguboti	Kab.	Toba Samosir	Sumatera Utara	,\
    3723	:	22381	Sitoluama	Laguboti	Kab.	Toba Samosir	Sumatera Utara	,\
    3724	:	22381	Tinggir Nipasir	Laguboti	Kab.	Toba Samosir	Sumatera Utara	,\
    3725	:	22381	Ujung Tanduk	Laguboti	Kab.	Toba Samosir	Sumatera Utara	,\
    3726	:	22281	Bulu Duri	Lae Parira	Kab.	Dairi	Sumatera Utara	,\
    3727	:	22281	Kentara	Lae Parira	Kab.	Dairi	Sumatera Utara	,\
    3728	:	22281	Lae Parira	Lae Parira	Kab.	Dairi	Sumatera Utara	,\
    3729	:	22281	Lumban Sihite	Lae Parira	Kab.	Dairi	Sumatera Utara	,\
    3730	:	22281	Lumban Toruan	Lae Parira	Kab.	Dairi	Sumatera Utara	,\
    3731	:	22281	Pandiangan	Lae Parira	Kab.	Dairi	Sumatera Utara	,\
    3732	:	22281	Sempung Polling	Lae Parira	Kab.	Dairi	Sumatera Utara	,\
    3733	:	22281	Sumbul	Lae Parira	Kab.	Dairi	Sumatera Utara	,\
    3734	:	20373	Helvetia	Labuhan Deli	Kab.	Deli Serdang	Sumatera Utara	,\
    3735	:	20373	Karang Gading	Labuhan Deli	Kab.	Deli Serdang	Sumatera Utara	,\
    3736	:	20373	Manunggal	Labuhan Deli	Kab.	Deli Serdang	Sumatera Utara	,\
    3737	:	20373	Pematang Johar	Labuhan Deli	Kab.	Deli Serdang	Sumatera Utara	,\
    3738	:	20373	Telaga Tujuh	Labuhan Deli	Kab.	Deli Serdang	Sumatera Utara	,\
    3739	:	20773	Kaperas	Kutambaru	Kab.	Langkat	Sumatera Utara	,\
    3740	:	20773	Kutagajah	Kutambaru	Kab.	Langkat	Sumatera Utara	,\
    3741	:	20773	Kutambaru	Kutambaru	Kab.	Langkat	Sumatera Utara	,\
    3742	:	20773	Namoteras	Kutambaru	Kab.	Langkat	Sumatera Utara	,\
    3743	:	20773	Perkebunan Marikie	Kutambaru	Kab.	Langkat	Sumatera Utara	,\
    3744	:	20773	Perkebunan Namotongan	Kutambaru	Kab.	Langkat	Sumatera Utara	,\
    3745	:	20773	Rampah	Kutambaru	Kab.	Langkat	Sumatera Utara	,\
    3746	:	20773	Sulkam	Kutambaru	Kab.	Langkat	Sumatera Utara	,\
    3747	:	20354	Kuala Lau Bicik	Kutalimbaru	Kab.	Deli Serdang	Sumatera Utara	,\
    3748	:	20354	Kuta Limbaru	Kutalimbaru	Kab.	Deli Serdang	Sumatera Utara	,\
    3749	:	20354	Lau Bakeri	Kutalimbaru	Kab.	Deli Serdang	Sumatera Utara	,\
    3750	:	20354	Namo Mirik	Kutalimbaru	Kab.	Deli Serdang	Sumatera Utara	,\
    3751	:	20354	Namo Rube Julu	Kutalimbaru	Kab.	Deli Serdang	Sumatera Utara	,\
    3752	:	20354	Pasar X	Kutalimbaru	Kab.	Deli Serdang	Sumatera Utara	,\
    3753	:	20354	Perpanden	Kutalimbaru	Kab.	Deli Serdang	Sumatera Utara	,\
    3754	:	20354	Sampe Gita (Cita)	Kutalimbaru	Kab.	Deli Serdang	Sumatera Utara	,\
    3755	:	20354	Sawit Rejo	Kutalimbaru	Kab.	Deli Serdang	Sumatera Utara	,\
    3756	:	20354	Sei Mencirim	Kutalimbaru	Kab.	Deli Serdang	Sumatera Utara	,\
    3757	:	20354	Silebo Lebo	Kutalimbaru	Kab.	Deli Serdang	Sumatera Utara	,\
    3758	:	20354	Suka Dame	Kutalimbaru	Kab.	Deli Serdang	Sumatera Utara	,\
    3759	:	20354	Suka Makmur	Kutalimbaru	Kab.	Deli Serdang	Sumatera Utara	,\
    3760	:	20354	Suka Rende	Kutalimbaru	Kab.	Deli Serdang	Sumatera Utara	,\
    3761	:	22155	Amburudi (Mburidi)	Kuta Buluh	Kab.	Karo	Sumatera Utara	,\
    3762	:	22155	Bintang Meriah	Kuta Buluh	Kab.	Karo	Sumatera Utara	,\
    3763	:	22155	Buah Raya	Kuta Buluh	Kab.	Karo	Sumatera Utara	,\
    3764	:	22155	Gunung Meriah	Kuta Buluh	Kab.	Karo	Sumatera Utara	,\
    3765	:	22155	Jinabun	Kuta Buluh	Kab.	Karo	Sumatera Utara	,\
    3766	:	22155	Kuta Buluh	Kuta Buluh	Kab.	Karo	Sumatera Utara	,\
    3767	:	22155	Kuta Buluh Gugung	Kuta Buluh	Kab.	Karo	Sumatera Utara	,\
    3768	:	22155	Kuta Male	Kuta Buluh	Kab.	Karo	Sumatera Utara	,\
    3769	:	22155	Lau Buluh	Kuta Buluh	Kab.	Karo	Sumatera Utara	,\
    3770	:	22155	Liang Merdeka	Kuta Buluh	Kab.	Karo	Sumatera Utara	,\
    3771	:	22155	Negeri Jahe	Kuta Buluh	Kab.	Karo	Sumatera Utara	,\
    3772	:	22155	Pola Tebu	Kuta Buluh	Kab.	Karo	Sumatera Utara	,\
    3773	:	22155	Rih Tengah	Kuta Buluh	Kab.	Karo	Sumatera Utara	,\
    3774	:	22155	Siabang Abang	Kuta Buluh	Kab.	Karo	Sumatera Utara	,\
    3775	:	22155	Tanjung Merahe	Kuta Buluh	Kab.	Karo	Sumatera Utara	,\
    3776	:	22155	Ujung Deleng	Kuta Buluh	Kab.	Karo	Sumatera Utara	,\
    3777	:	21457	Bandar Lama	Kualuh Selatan	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3778	:	21457	Damuli Kebun (Perkebunan Damuli)	Kualuh Selatan	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3779	:	21457	Damuli Pekan	Kualuh Selatan	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3780	:	21457	Gunting Saga	Kualuh Selatan	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3781	:	21457	Gunung Melayu	Kualuh Selatan	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3782	:	21457	Hasang	Kualuh Selatan	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3783	:	21457	Lobu Huala	Kualuh Selatan	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3784	:	21457	Sialang Taji	Kualuh Selatan	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3785	:	21457	Siamporik	Kualuh Selatan	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3786	:	21457	Sidua Dua	Kualuh Selatan	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3787	:	21457	Simangalam	Kualuh Selatan	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3788	:	21457	Tanjung Pasir	Kualuh Selatan	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3789	:	21457	Aek Kanopan	Kualuh Hulu	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3790	:	21457	Aek Kanopan Timur	Kualuh Hulu	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3791	:	21457	Kuala Beringin	Kualuh Hulu	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3792	:	21457	Parpaudangan	Kualuh Hulu	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3793	:	21457	Perkebunan Hanna	Kualuh Hulu	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3794	:	21457	Perkebunan Kanopan Ulu	Kualuh Hulu	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3795	:	21457	Perkebunan Labuhan Haji	Kualuh Hulu	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3796	:	21457	Perkebunan Londut	Kualuh Hulu	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3797	:	21457	Perkebunan Mambang/Membang Muda	Kualuh Hulu	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3798	:	21457	Pulo Dogom	Kualuh Hulu	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3799	:	21457	Sono Martani	Kualuh Hulu	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3800	:	21457	Suka Rame	Kualuh Hulu	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3801	:	21457	Suka Rame Baru	Kualuh Hulu	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3802	:	21474	Kampung Mesjid	Kualuh Hilir	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3803	:	21474	Kuala Bangka	Kualuh Hilir	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3804	:	21474	Sei/Sungai Apung	Kualuh Hilir	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3805	:	21474	Sei/Sungai Sentang	Kualuh Hilir	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3806	:	21474	Tanjung Mangedar	Kualuh Hilir	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3807	:	21474	Teluk Binjai	Kualuh Hilir	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3808	:	21474	Teluk Piai	Kualuh Hilir	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3809	:	21475	Air Hitam	Kuala Ledong (Kualuh Leidong)	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3810	:	21475	Kelapa Sebatang	Kuala Ledong (Kualuh Leidong)	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3811	:	21475	Pangkalan Lunang	Kuala Ledong (Kualuh Leidong)	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3812	:	21475	Simandulang	Kuala Ledong (Kualuh Leidong)	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3813	:	21475	Tanjung Leidong	Kuala Ledong (Kualuh Leidong)	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3814	:	21475	Teluk Pulai Dalam	Kuala Ledong (Kualuh Leidong)	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3815	:	21475	Teluk Pulai Luar	Kuala Ledong (Kualuh Leidong)	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    3816	:	20772	Balai Kasih	Kuala	Kab.	Langkat	Sumatera Utara	,\
    3817	:	20772	Bekiung	Kuala	Kab.	Langkat	Sumatera Utara	,\
    3818	:	20772	Bela Rakyat	Kuala	Kab.	Langkat	Sumatera Utara	,\
    3819	:	20772	Beruam	Kuala	Kab.	Langkat	Sumatera Utara	,\
    3820	:	20772	Besadi	Kuala	Kab.	Langkat	Sumatera Utara	,\
    3821	:	20772	Blangkahan/Belangkahan	Kuala	Kab.	Langkat	Sumatera Utara	,\
    3822	:	20772	Dalan Naman (Dalam Daman)	Kuala	Kab.	Langkat	Sumatera Utara	,\
    3823	:	20772	Garunggang	Kuala	Kab.	Langkat	Sumatera Utara	,\
    3824	:	20772	Namo Mbelin	Kuala	Kab.	Langkat	Sumatera Utara	,\
    3825	:	20772	Parit Bindu	Kuala	Kab.	Langkat	Sumatera Utara	,\
    3826	:	20772	Pekan Kuala	Kuala	Kab.	Langkat	Sumatera Utara	,\
    3827	:	20772	Perkebunan Bekiun	Kuala	Kab.	Langkat	Sumatera Utara	,\
    3828	:	20772	Raja Tengah	Kuala	Kab.	Langkat	Sumatera Utara	,\
    3829	:	20772	Sei Penjara	Kuala	Kab.	Langkat	Sumatera Utara	,\
    3830	:	20772	Sido Makmur	Kuala	Kab.	Langkat	Sumatera Utara	,\
    3831	:	20772	Suka Damai	Kuala	Kab.	Langkat	Sumatera Utara	,\
    3832	:	20984	Bandar Bayu	Kotarih	Kab.	Serdang Bedagai	Sumatera Utara	,\
    3833	:	20984	Banjaran Godang	Kotarih	Kab.	Serdang Bedagai	Sumatera Utara	,\
    3834	:	20984	Durian Kondot	Kotarih	Kab.	Serdang Bedagai	Sumatera Utara	,\
    3835	:	20984	Huta Galuh	Kotarih	Kab.	Serdang Bedagai	Sumatera Utara	,\
    3836	:	20984	Kotarih Baru	Kotarih	Kab.	Serdang Bedagai	Sumatera Utara	,\
    3837	:	20984	Kotarih Pekan	Kotarih	Kab.	Serdang Bedagai	Sumatera Utara	,\
    3838	:	20984	Perbahingan	Kotarih	Kab.	Serdang Bedagai	Sumatera Utara	,\
    3839	:	20984	Rubun Dunia	Kotarih	Kab.	Serdang Bedagai	Sumatera Utara	,\
    3840	:	20984	Sei Karih	Kotarih	Kab.	Serdang Bedagai	Sumatera Utara	,\
    3841	:	20984	Sei Ujan-Ujan	Kotarih	Kab.	Serdang Bedagai	Sumatera Utara	,\
    3842	:	20984	Sialtong	Kotarih	Kab.	Serdang Bedagai	Sumatera Utara	,\
    3843	:	22994	Batahan	Kotanopan	Kab.	Mandailing Natal	Sumatera Utara	,\
    3844	:	22994	Botung	Kotanopan	Kab.	Mandailing Natal	Sumatera Utara	,\
    3845	:	22994	Gading Bain	Kotanopan	Kab.	Mandailing Natal	Sumatera Utara	,\
    3846	:	22994	Gunung Tua Ms	Kotanopan	Kab.	Mandailing Natal	Sumatera Utara	,\
    3847	:	22994	Gunung Tua Sm	Kotanopan	Kab.	Mandailing Natal	Sumatera Utara	,\
    3848	:	22994	Husor Tolang (Unsor Tolan)	Kotanopan	Kab.	Mandailing Natal	Sumatera Utara	,\
    3849	:	22994	Huta Baringin Tb	Kotanopan	Kab.	Mandailing Natal	Sumatera Utara	,\
    3850	:	22994	Huta Dangka	Kotanopan	Kab.	Mandailing Natal	Sumatera Utara	,\
    3851	:	22994	Huta Padang Sm	Kotanopan	Kab.	Mandailing Natal	Sumatera Utara	,\
    3852	:	22994	Huta Puli	Kotanopan	Kab.	Mandailing Natal	Sumatera Utara	,\
    3853	:	22994	Huta Pungkut Jae	Kotanopan	Kab.	Mandailing Natal	Sumatera Utara	,\
    3854	:	22994	Huta Pungkut Julu	Kotanopan	Kab.	Mandailing Natal	Sumatera Utara	,\
    3855	:	22994	Huta Pungkut Tonga	Kotanopan	Kab.	Mandailing Natal	Sumatera Utara	,\
    3856	:	22994	Huta Rimbaru Sm	Kotanopan	Kab.	Mandailing Natal	Sumatera Utara	,\
    3857	:	22994	Manambin	Kotanopan	Kab.	Mandailing Natal	Sumatera Utara	,\
    3858	:	22994	Muara Botung	Kotanopan	Kab.	Mandailing Natal	Sumatera Utara	,\
    3859	:	22994	Muara Potan	Kotanopan	Kab.	Mandailing Natal	Sumatera Utara	,\
    3860	:	22994	Muara Pungkut	Kotanopan	Kab.	Mandailing Natal	Sumatera Utara	,\
    3861	:	22994	Muara Saladi	Kotanopan	Kab.	Mandailing Natal	Sumatera Utara	,\
    3862	:	22994	Muara Siambak	Kotanopan	Kab.	Mandailing Natal	Sumatera Utara	,\
    3863	:	22994	Padang Bulan	Kotanopan	Kab.	Mandailing Natal	Sumatera Utara	,\
    3864	:	22994	Pagar Gunung	Kotanopan	Kab.	Mandailing Natal	Sumatera Utara	,\
    3865	:	22994	Pasar Kotanopan	Kotanopan	Kab.	Mandailing Natal	Sumatera Utara	,\
    3866	:	22994	Patialo	Kotanopan	Kab.	Mandailing Natal	Sumatera Utara	,\
    3867	:	22994	Saba Dolok	Kotanopan	Kab.	Mandailing Natal	Sumatera Utara	,\
    3868	:	22994	Sayur Maincat	Kotanopan	Kab.	Mandailing Natal	Sumatera Utara	,\
    3869	:	22994	Sibio-Bio	Kotanopan	Kab.	Mandailing Natal	Sumatera Utara	,\
    3870	:	22994	Simandolan	Kotanopan	Kab.	Mandailing Natal	Sumatera Utara	,\
    3871	:	22994	Simpang Tolang Jae	Kotanopan	Kab.	Mandailing Natal	Sumatera Utara	,\
    3872	:	22994	Simpang Tolang Julu	Kotanopan	Kab.	Mandailing Natal	Sumatera Utara	,\
    3873	:	22994	Singengu Jae	Kotanopan	Kab.	Mandailing Natal	Sumatera Utara	,\
    3874	:	22994	Singengu Julu	Kotanopan	Kab.	Mandailing Natal	Sumatera Utara	,\
    3875	:	22994	Tambang Bustak	Kotanopan	Kab.	Mandailing Natal	Sumatera Utara	,\
    3876	:	22994	Tamiang	Kotanopan	Kab.	Mandailing Natal	Sumatera Utara	,\
    3877	:	22994	Tobang	Kotanopan	Kab.	Mandailing Natal	Sumatera Utara	,\
    3878	:	22994	Ujung Marisi	Kotanopan	Kab.	Mandailing Natal	Sumatera Utara	,\
    3879	:	22994	Usor Tolang	Kotanopan	Kab.	Mandailing Natal	Sumatera Utara	,\
    3880	:	21464	Hadundung	Kota Pinang	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    3881	:	21464	Kota Pinang	Kota Pinang	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    3882	:	21464	Mampang	Kota Pinang	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    3883	:	21464	Pasir Tuntung	Kota Pinang	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    3884	:	21464	Perkebunan Nagodang	Kota Pinang	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    3885	:	21464	Perkebunan Normark	Kota Pinang	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    3886	:	21464	Simatahari	Kota Pinang	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    3887	:	21464	Sisumut	Kota Pinang	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    3888	:	21464	Sosopan	Kota Pinang	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    3889	:	21464	Sungai Rumbia (Perkebunan Sei Rumbia)	Kota Pinang	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    3890	:	22562	Hudopa Nauli	Kolang	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    3891	:	22562	Hurlang Muara Nauli	Kolang	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    3892	:	22562	Kolang Nauli	Kolang	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    3893	:	22562	Makarti Nauli	Kolang	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    3894	:	22562	Pasar Onan Hurlang	Kolang	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    3895	:	22562	Rawa Makmur	Kolang	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    3896	:	22562	Satahi Nauli	Kolang	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    3897	:	22562	Sipakpahi Aek Lobu	Kolang	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    3898	:	22562	Unte Mungkur I	Kolang	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    3899	:	22562	Unte Mungkur II	Kolang	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    3900	:	22562	Unte Mungkur III	Kolang	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    3901	:	22562	Unte Mungkur IV	Kolang	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    3902	:	21221	Gambir Baru	Kisaran Timur Kota	Kab.	Asahan	Sumatera Utara	,\
    3903	:	21229	Karang Anyer	Kisaran Timur Kota	Kab.	Asahan	Sumatera Utara	,\
    3904	:	21227	Kedai Ledang	Kisaran Timur Kota	Kab.	Asahan	Sumatera Utara	,\
    3905	:	21219	Kisaran Naga	Kisaran Timur Kota	Kab.	Asahan	Sumatera Utara	,\
    3906	:	21222	Kisaran Timur	Kisaran Timur Kota	Kab.	Asahan	Sumatera Utara	,\
    3907	:	21221	Lestari	Kisaran Timur Kota	Kab.	Asahan	Sumatera Utara	,\
    3908	:	21223	Mutiara	Kisaran Timur Kota	Kab.	Asahan	Sumatera Utara	,\
    3909	:	21228	Selawan	Kisaran Timur Kota	Kab.	Asahan	Sumatera Utara	,\
    3910	:	21224	Sentang	Kisaran Timur Kota	Kab.	Asahan	Sumatera Utara	,\
    3911	:	21226	Siumbut Baru	Kisaran Timur Kota	Kab.	Asahan	Sumatera Utara	,\
    3912	:	21225	Siumbut-Umbut	Kisaran Timur Kota	Kab.	Asahan	Sumatera Utara	,\
    3913	:	21222	Teladan	Kisaran Timur Kota	Kab.	Asahan	Sumatera Utara	,\
    3914	:	21211	Bunut	Kisaran Barat Kota	Kab.	Asahan	Sumatera Utara	,\
    3915	:	21211	Bunut Barat	Kisaran Barat Kota	Kab.	Asahan	Sumatera Utara	,\
    3916	:	21212	Dadi Mulyo	Kisaran Barat Kota	Kab.	Asahan	Sumatera Utara	,\
    3917	:	21214	Kisaran Barat	Kisaran Barat Kota	Kab.	Asahan	Sumatera Utara	,\
    3918	:	21216	Kisaran Baru	Kisaran Barat Kota	Kab.	Asahan	Sumatera Utara	,\
    3919	:	21215	Kisaran Kota	Kisaran Barat Kota	Kab.	Asahan	Sumatera Utara	,\
    3920	:	21216	Mekar Baru	Kisaran Barat Kota	Kab.	Asahan	Sumatera Utara	,\
    3921	:	21213	Sei Renggas	Kisaran Barat Kota	Kab.	Asahan	Sumatera Utara	,\
    3922	:	21218	Sendang Sari	Kisaran Barat Kota	Kab.	Asahan	Sumatera Utara	,\
    3923	:	21212	Sidodadi	Kisaran Barat Kota	Kab.	Asahan	Sumatera Utara	,\
    3924	:	21217	Sidomukti	Kisaran Barat Kota	Kab.	Asahan	Sumatera Utara	,\
    3925	:	21215	Tebing Kisaran	Kisaran Barat Kota	Kab.	Asahan	Sumatera Utara	,\
    3926	:	21218	Tegal Sari	Kisaran Barat Kota	Kab.	Asahan	Sumatera Utara	,\
    3927	:	22271	Kuta Mariah/Meriah	Kerajaan	Kab.	Pakpak Bharat	Sumatera Utara	,\
    3928	:	22271	Kutadame	Kerajaan	Kab.	Pakpak Bharat	Sumatera Utara	,\
    3929	:	22271	Kutasaga	Kerajaan	Kab.	Pakpak Bharat	Sumatera Utara	,\
    3930	:	22271	Majanggut I	Kerajaan	Kab.	Pakpak Bharat	Sumatera Utara	,\
    3931	:	22271	Majanggut II	Kerajaan	Kab.	Pakpak Bharat	Sumatera Utara	,\
    3932	:	22271	Pardomuan	Kerajaan	Kab.	Pakpak Bharat	Sumatera Utara	,\
    3933	:	22271	Parpulungan/Parpulungen	Kerajaan	Kab.	Pakpak Bharat	Sumatera Utara	,\
    3934	:	22271	Perduhapen	Kerajaan	Kab.	Pakpak Bharat	Sumatera Utara	,\
    3935	:	22271	Sukaramai	Kerajaan	Kab.	Pakpak Bharat	Sumatera Utara	,\
    3936	:	22271	Surung Mersada	Kerajaan	Kab.	Pakpak Bharat	Sumatera Utara	,\
    3937	:	21463	Air Merah	Kampung Rakyat	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    3938	:	21463	Perkebunan Batang Seponggol	Kampung Rakyat	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    3939	:	21463	Perkebunan Perlabian	Kampung Rakyat	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    3940	:	21463	Perkebunan Teluk Panji	Kampung Rakyat	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    3941	:	21463	Perkebunan Tolan (Pekan Tolan)	Kampung Rakyat	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    3942	:	21463	Perkebunan Tolan I/II	Kampung Rakyat	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    3943	:	21463	Perlabian (Kampung Perlabian)	Kampung Rakyat	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    3944	:	21463	Tanjung Medan	Kampung Rakyat	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    3945	:	21463	Tanjung Mulia	Kampung Rakyat	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    3946	:	21463	Tanjung Selamat	Kampung Rakyat	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    3947	:	21463	Teluk Panji (Kampung Teluk Panji)	Kampung Rakyat	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    3948	:	21463	Teluk Panji I	Kampung Rakyat	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    3949	:	21463	Teluk Panji II	Kampung Rakyat	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    3950	:	21463	Teluk Panji III	Kampung Rakyat	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    3951	:	21463	Teluk Panji IV	Kampung Rakyat	Kab.	Labuhan Batu Selatan	Sumatera Utara	,\
    3952	:	22111	Gung Leto	Kabanjahe	Kab.	Karo	Sumatera Utara	,\
    3953	:	22112	Gung Negeri	Kabanjahe	Kab.	Karo	Sumatera Utara	,\
    3954	:	22111	Kaban	Kabanjahe	Kab.	Karo	Sumatera Utara	,\
    3955	:	22111	Kacaribu	Kabanjahe	Kab.	Karo	Sumatera Utara	,\
    3956	:	22113	Kampung Dalam	Kabanjahe	Kab.	Karo	Sumatera Utara	,\
    3957	:	22111	Kandibata	Kabanjahe	Kab.	Karo	Sumatera Utara	,\
    3958	:	22111	Ketaren	Kabanjahe	Kab.	Karo	Sumatera Utara	,\
    3959	:	22114	Lau Cimba	Kabanjahe	Kab.	Karo	Sumatera Utara	,\
    3960	:	22111	Lausimono	Kabanjahe	Kab.	Karo	Sumatera Utara	,\
    3961	:	22115	Padang Mas	Kabanjahe	Kab.	Karo	Sumatera Utara	,\
    3962	:	22111	Rumah Kabanjahe	Kabanjahe	Kab.	Karo	Sumatera Utara	,\
    3963	:	22111	Samura	Kabanjahe	Kab.	Karo	Sumatera Utara	,\
    3964	:	22111	Sumber Mufakat	Kabanjahe	Kab.	Karo	Sumatera Utara	,\
    3965	:	22163	Batu Mamak	Juhar	Kab.	Karo	Sumatera Utara	,\
    3966	:	22163	Bekilang	Juhar	Kab.	Karo	Sumatera Utara	,\
    3967	:	22163	Buluh Pancur	Juhar	Kab.	Karo	Sumatera Utara	,\
    3968	:	22163	Gunung Juhar	Juhar	Kab.	Karo	Sumatera Utara	,\
    3969	:	22163	Jandi (Jandi Meriah)	Juhar	Kab.	Karo	Sumatera Utara	,\
    3970	:	22163	Juhar Ginting	Juhar	Kab.	Karo	Sumatera Utara	,\
    3971	:	22163	Juhar Ginting Sadanioga	Juhar	Kab.	Karo	Sumatera Utara	,\
    3972	:	22163	Juhar Perangin-Angin	Juhar	Kab.	Karo	Sumatera Utara	,\
    3973	:	22163	Juhar Tarigan	Juhar	Kab.	Karo	Sumatera Utara	,\
    3974	:	22163	Keriahen	Juhar	Kab.	Karo	Sumatera Utara	,\
    3975	:	22163	Ketawaren	Juhar	Kab.	Karo	Sumatera Utara	,\
    3976	:	22163	Kidupen	Juhar	Kab.	Karo	Sumatera Utara	,\
    3977	:	22163	Kutagugung	Juhar	Kab.	Karo	Sumatera Utara	,\
    3978	:	22163	Kutambelin	Juhar	Kab.	Karo	Sumatera Utara	,\
    3979	:	22163	Lau Kidupen	Juhar	Kab.	Karo	Sumatera Utara	,\
    3980	:	22163	Lau Lingga	Juhar	Kab.	Karo	Sumatera Utara	,\
    3981	:	22163	Mbetong (Mbetung)	Juhar	Kab.	Karo	Sumatera Utara	,\
    3982	:	22163	Naga	Juhar	Kab.	Karo	Sumatera Utara	,\
    3983	:	22163	Nageri	Juhar	Kab.	Karo	Sumatera Utara	,\
    3984	:	22163	Namosuro	Juhar	Kab.	Karo	Sumatera Utara	,\
    3985	:	22163	Pasar Baru	Juhar	Kab.	Karo	Sumatera Utara	,\
    3986	:	22163	Pernantin	Juhar	Kab.	Karo	Sumatera Utara	,\
    3987	:	22163	Sigenderang	Juhar	Kab.	Karo	Sumatera Utara	,\
    3988	:	22163	Sugihen	Juhar	Kab.	Karo	Sumatera Utara	,\
    3989	:	22163	Sukababo	Juhar	Kab.	Karo	Sumatera Utara	,\
    3990	:	21172	Bah Birong Ulu	Jorlang Hataran	Kab.	Simalungun	Sumatera Utara	,\
    3991	:	21172	Bah Sampuran	Jorlang Hataran	Kab.	Simalungun	Sumatera Utara	,\
    3992	:	21172	Dipar Hataran	Jorlang Hataran	Kab.	Simalungun	Sumatera Utara	,\
    3993	:	21172	Dolok Marlawan	Jorlang Hataran	Kab.	Simalungun	Sumatera Utara	,\
    3994	:	21172	Jorlang Hataran	Jorlang Hataran	Kab.	Simalungun	Sumatera Utara	,\
    3995	:	21172	Kasindir	Jorlang Hataran	Kab.	Simalungun	Sumatera Utara	,\
    3996	:	21172	Panombean Huta Urung	Jorlang Hataran	Kab.	Simalungun	Sumatera Utara	,\
    3997	:	21172	Pinang Ratus	Jorlang Hataran	Kab.	Simalungun	Sumatera Utara	,\
    3998	:	21172	Sibunga Bunga	Jorlang Hataran	Kab.	Simalungun	Sumatera Utara	,\
    3999	:	21172	Tiga Balata	Jorlang Hataran	Kab.	Simalungun	Sumatera Utara	,\
    4000	:	21153	Bah Jambi I	Jawa Maraja Bah Jambi	Kab.	Simalungun	Sumatera Utara	,\
    4001	:	21153	Bah Joga	Jawa Maraja Bah Jambi	Kab.	Simalungun	Sumatera Utara	,\
    4002	:	21153	Bahalat Bayu	Jawa Maraja Bah Jambi	Kab.	Simalungun	Sumatera Utara	,\
    4003	:	21153	Jawa Maraja	Jawa Maraja Bah Jambi	Kab.	Simalungun	Sumatera Utara	,\
    4004	:	21153	Mariah Jambi	Jawa Maraja Bah Jambi	Kab.	Simalungun	Sumatera Utara	,\
    4005	:	21153	Mekar Bahalat	Jawa Maraja Bah Jambi	Kab.	Simalungun	Sumatera Utara	,\
    4006	:	21153	Moho	Jawa Maraja Bah Jambi	Kab.	Simalungun	Sumatera Utara	,\
    4007	:	21153	Tanjung Maraja	Jawa Maraja Bah Jambi	Kab.	Simalungun	Sumatera Utara	,\
    4008	:	22872	Ahedano	Idano Gawo	Kab.	Nias	Sumatera Utara	,\
    4009	:	22872	Awoni Lauso	Idano Gawo	Kab.	Nias	Sumatera Utara	,\
    4010	:	22872	Baruzo	Idano Gawo	Kab.	Nias	Sumatera Utara	,\
    4011	:	22872	Biouti	Idano Gawo	Kab.	Nias	Sumatera Utara	,\
    4012	:	22872	Biouti Timur	Idano Gawo	Kab.	Nias	Sumatera Utara	,\
    4013	:	22872	Bobozioli Loloanaa	Idano Gawo	Kab.	Nias	Sumatera Utara	,\
    4014	:	22872	Bozihona	Idano Gawo	Kab.	Nias	Sumatera Utara	,\
    4015	:	22872	Hili`adulo	Idano Gawo	Kab.	Nias	Sumatera Utara	,\
    4016	:	22872	Hiligogowaya Maliwa`a	Idano Gawo	Kab.	Nias	Sumatera Utara	,\
    4017	:	22872	Hililawae	Idano Gawo	Kab.	Nias	Sumatera Utara	,\
    4018	:	22872	Hilimoasio	Idano Gawo	Kab.	Nias	Sumatera Utara	,\
    4019	:	22872	Hilimoasio Dua	Idano Gawo	Kab.	Nias	Sumatera Utara	,\
    4020	:	22872	Hilinaa Tafuo	Idano Gawo	Kab.	Nias	Sumatera Utara	,\
    4021	:	22872	Hilionozega	Idano Gawo	Kab.	Nias	Sumatera Utara	,\
    4022	:	22872	Laira	Idano Gawo	Kab.	Nias	Sumatera Utara	,\
    4023	:	22872	Laowo Hilimbaruzo	Idano Gawo	Kab.	Nias	Sumatera Utara	,\
    4024	:	22872	Maliwaa	Idano Gawo	Kab.	Nias	Sumatera Utara	,\
    4025	:	22872	Mondrali	Idano Gawo	Kab.	Nias	Sumatera Utara	,\
    4026	:	22872	Oladano	Idano Gawo	Kab.	Nias	Sumatera Utara	,\
    4027	:	22872	Orahili Zuzundrao	Idano Gawo	Kab.	Nias	Sumatera Utara	,\
    4028	:	22872	Otalua	Idano Gawo	Kab.	Nias	Sumatera Utara	,\
    4029	:	22872	Saiwahili Hiliadulo	Idano Gawo	Kab.	Nias	Sumatera Utara	,\
    4030	:	22872	Sandruta	Idano Gawo	Kab.	Nias	Sumatera Utara	,\
    4031	:	22872	Sisobahili Iraonohura	Idano Gawo	Kab.	Nias	Sumatera Utara	,\
    4032	:	22872	Tete Goenaai	Idano Gawo	Kab.	Nias	Sumatera Utara	,\
    4033	:	22872	Tetehosi	Idano Gawo	Kab.	Nias	Sumatera Utara	,\
    4034	:	22872	Tiga Serangkai Maliwa`a	Idano Gawo	Kab.	Nias	Sumatera Utara	,\
    4035	:	22872	Tuhewaebu	Idano Gawo	Kab.	Nias	Sumatera Utara	,\
    4036	:	22774	Ali Aga	Huta Raja Tinggi	Kab.	Padang Lawas	Sumatera Utara	,\
    4037	:	22774	Gunung Mulia	Huta Raja Tinggi	Kab.	Padang Lawas	Sumatera Utara	,\
    4038	:	22774	Huta Raja Tinggi	Huta Raja Tinggi	Kab.	Padang Lawas	Sumatera Utara	,\
    4039	:	22774	Lubuk Bunut	Huta Raja Tinggi	Kab.	Padang Lawas	Sumatera Utara	,\
    4040	:	22774	Mananti Sosa Jae	Huta Raja Tinggi	Kab.	Padang Lawas	Sumatera Utara	,\
    4041	:	22774	Margo Mulia (Pirtrans Sosa IV)	Huta Raja Tinggi	Kab.	Padang Lawas	Sumatera Utara	,\
    4042	:	22774	Mulya Sari	Huta Raja Tinggi	Kab.	Padang Lawas	Sumatera Utara	,\
    4043	:	22774	Pagaran Dolok Sosa Jae	Huta Raja Tinggi	Kab.	Padang Lawas	Sumatera Utara	,\
    4044	:	22774	Panyabungan	Huta Raja Tinggi	Kab.	Padang Lawas	Sumatera Utara	,\
    4045	:	22774	Parmainan	Huta Raja Tinggi	Kab.	Padang Lawas	Sumatera Utara	,\
    4046	:	22774	Pasar Panyabungan	Huta Raja Tinggi	Kab.	Padang Lawas	Sumatera Utara	,\
    4047	:	22774	Payombur (Payaombor)	Huta Raja Tinggi	Kab.	Padang Lawas	Sumatera Utara	,\
    4048	:	22774	Pirtrans Sosa II	Huta Raja Tinggi	Kab.	Padang Lawas	Sumatera Utara	,\
    4049	:	22774	Siabu	Huta Raja Tinggi	Kab.	Padang Lawas	Sumatera Utara	,\
    4050	:	22774	Sibodak Sosa Jae	Huta Raja Tinggi	Kab.	Padang Lawas	Sumatera Utara	,\
    4051	:	22774	Sido Mulyo (Pirtrans Sosa III A)	Huta Raja Tinggi	Kab.	Padang Lawas	Sumatera Utara	,\
    4052	:	22774	Sigala Gala	Huta Raja Tinggi	Kab.	Padang Lawas	Sumatera Utara	,\
    4053	:	22774	Sigalapung	Huta Raja Tinggi	Kab.	Padang Lawas	Sumatera Utara	,\
    4054	:	22774	Simangambat	Huta Raja Tinggi	Kab.	Padang Lawas	Sumatera Utara	,\
    4055	:	22774	Sosa Mulia	Huta Raja Tinggi	Kab.	Padang Lawas	Sumatera Utara	,\
    4056	:	22774	Suka Dame (Pirtrans Sosa III B)	Huta Raja Tinggi	Kab.	Padang Lawas	Sumatera Utara	,\
    4057	:	22774	Sungai Korang	Huta Raja Tinggi	Kab.	Padang Lawas	Sumatera Utara	,\
    4058	:	22774	Tanjung Ale	Huta Raja Tinggi	Kab.	Padang Lawas	Sumatera Utara	,\
    4059	:	22774	Tanjung Baringin	Huta Raja Tinggi	Kab.	Padang Lawas	Sumatera Utara	,\
    4060	:	22774	Tanjung Sari (Pirtrans Sosa Ib)	Huta Raja Tinggi	Kab.	Padang Lawas	Sumatera Utara	,\
    4061	:	22774	Ujung Batu I	Huta Raja Tinggi	Kab.	Padang Lawas	Sumatera Utara	,\
    4062	:	22774	Ujung Batu II	Huta Raja Tinggi	Kab.	Padang Lawas	Sumatera Utara	,\
    4063	:	22774	Ujung Batu III	Huta Raja Tinggi	Kab.	Padang Lawas	Sumatera Utara	,\
    4064	:	22774	Ujung Batu IV	Huta Raja Tinggi	Kab.	Padang Lawas	Sumatera Utara	,\
    4065	:	22774	Ujung Batu V	Huta Raja Tinggi	Kab.	Padang Lawas	Sumatera Utara	,\
    4066	:	22774	Ujung Padang	Huta Raja Tinggi	Kab.	Padang Lawas	Sumatera Utara	,\
    4067	:	21182	Bahal Batu	Huta Bayu Raja	Kab.	Simalungun	Sumatera Utara	,\
    4068	:	21182	Bosar Bayu	Huta Bayu Raja	Kab.	Simalungun	Sumatera Utara	,\
    4069	:	21182	Dolok Sinumbah	Huta Bayu Raja	Kab.	Simalungun	Sumatera Utara	,\
    4070	:	21182	Huta Bayu	Huta Bayu Raja	Kab.	Simalungun	Sumatera Utara	,\
    4071	:	21182	Jawa Baru	Huta Bayu Raja	Kab.	Simalungun	Sumatera Utara	,\
    4072	:	21182	Maligas Bayu	Huta Bayu Raja	Kab.	Simalungun	Sumatera Utara	,\
    4073	:	21182	Mancuk	Huta Bayu Raja	Kab.	Simalungun	Sumatera Utara	,\
    4074	:	21182	Mariah Hombang	Huta Bayu Raja	Kab.	Simalungun	Sumatera Utara	,\
    4075	:	21182	Marihat Mayang	Huta Bayu Raja	Kab.	Simalungun	Sumatera Utara	,\
    4076	:	21182	Pulo Bayu	Huta Bayu Raja	Kab.	Simalungun	Sumatera Utara	,\
    4077	:	21182	Raja Maligas	Huta Bayu Raja	Kab.	Simalungun	Sumatera Utara	,\
    4078	:	21182	Raja Maligas I	Huta Bayu Raja	Kab.	Simalungun	Sumatera Utara	,\
    4079	:	21182	Silak Kidir	Huta Bayu Raja	Kab.	Simalungun	Sumatera Utara	,\
    4080	:	22978	Bangun Sejati	Huta Bargot	Kab.	Mandailing Natal	Sumatera Utara	,\
    4081	:	22978	Huta Bargot Dolok	Huta Bargot	Kab.	Mandailing Natal	Sumatera Utara	,\
    4082	:	22978	Huta Bargot Lombang	Huta Bargot	Kab.	Mandailing Natal	Sumatera Utara	,\
    4083	:	22978	Huta Bargot Nauli	Huta Bargot	Kab.	Mandailing Natal	Sumatera Utara	,\
    4084	:	22978	Huta Bargot Setia	Huta Bargot	Kab.	Mandailing Natal	Sumatera Utara	,\
    4085	:	22978	Hutarimbaru	Huta Bargot	Kab.	Mandailing Natal	Sumatera Utara	,\
    4086	:	22978	Mondan	Huta Bargot	Kab.	Mandailing Natal	Sumatera Utara	,\
    4087	:	22978	Pasar Huta Bargot	Huta Bargot	Kab.	Mandailing Natal	Sumatera Utara	,\
    4088	:	22978	Sayur Maincat	Huta Bargot	Kab.	Mandailing Natal	Sumatera Utara	,\
    4089	:	22867	Bawahosi Huruna	Huruna	Kab.	Nias Selatan	Sumatera Utara	,\
    4090	:	22867	Ehosakhozi	Huruna	Kab.	Nias Selatan	Sumatera Utara	,\
    4091	:	22867	Fadoro Tuhemberua	Huruna	Kab.	Nias Selatan	Sumatera Utara	,\
    4092	:	22867	Hilifalawu	Huruna	Kab.	Nias Selatan	Sumatera Utara	,\
    4093	:	22867	Hilimanawa	Huruna	Kab.	Nias Selatan	Sumatera Utara	,\
    4094	:	22867	Hiliuso	Huruna	Kab.	Nias Selatan	Sumatera Utara	,\
    4095	:	22867	Hilizoliga	Huruna	Kab.	Nias Selatan	Sumatera Utara	,\
    4096	:	22867	Lalimanawa	Huruna	Kab.	Nias Selatan	Sumatera Utara	,\
    4097	:	22867	Luahamofakhe	Huruna	Kab.	Nias Selatan	Sumatera Utara	,\
    4098	:	22867	Mombawa Oladano	Huruna	Kab.	Nias Selatan	Sumatera Utara	,\
    4099	:	22867	Olayama	Huruna	Kab.	Nias Selatan	Sumatera Utara	,\
    4100	:	22867	Sifalago	Huruna	Kab.	Nias Selatan	Sumatera Utara	,\
    4101	:	22867	Sifaoro`asi	Huruna	Kab.	Nias Selatan	Sumatera Utara	,\
    4102	:	22867	Sifaoroasi Huruna	Huruna	Kab.	Nias Selatan	Sumatera Utara	,\
    4103	:	22867	Sisarahili Huruna	Huruna	Kab.	Nias Selatan	Sumatera Utara	,\
    4104	:	22867	Tarewe	Huruna	Kab.	Nias Selatan	Sumatera Utara	,\
    4105	:	22867	Tundrombaho	Huruna	Kab.	Nias Selatan	Sumatera Utara	,\
    4106	:	22742	Binanga Tolu	Huristak	Kab.	Padang Lawas	Sumatera Utara	,\
    4107	:	22742	Bulu Cina	Huristak	Kab.	Padang Lawas	Sumatera Utara	,\
    4108	:	22742	Gala Bonang	Huristak	Kab.	Padang Lawas	Sumatera Utara	,\
    4109	:	22742	Ganal	Huristak	Kab.	Padang Lawas	Sumatera Utara	,\
    4110	:	22742	Gonting Jae	Huristak	Kab.	Padang Lawas	Sumatera Utara	,\
    4111	:	22742	Gonting Julu	Huristak	Kab.	Padang Lawas	Sumatera Utara	,\
    4112	:	22742	Gunung Manaon Hr	Huristak	Kab.	Padang Lawas	Sumatera Utara	,\
    4113	:	22742	Gunung Matinggi	Huristak	Kab.	Padang Lawas	Sumatera Utara	,\
    4114	:	22742	Huristak	Huristak	Kab.	Padang Lawas	Sumatera Utara	,\
    4115	:	22742	Huta Pasir Ulak Tano	Huristak	Kab.	Padang Lawas	Sumatera Utara	,\
    4116	:	22742	Paran Tonga Hr (An)	Huristak	Kab.	Padang Lawas	Sumatera Utara	,\
    4117	:	22742	Pasar Huristak	Huristak	Kab.	Padang Lawas	Sumatera Utara	,\
    4118	:	22742	Pasir Lancat Baru	Huristak	Kab.	Padang Lawas	Sumatera Utara	,\
    4119	:	22742	Pasir Lancat Lama	Huristak	Kab.	Padang Lawas	Sumatera Utara	,\
    4120	:	22742	Pasir Pinang	Huristak	Kab.	Padang Lawas	Sumatera Utara	,\
    4121	:	22742	Paya Bujing	Huristak	Kab.	Padang Lawas	Sumatera Utara	,\
    4122	:	22742	Pulo Barian/Bariang	Huristak	Kab.	Padang Lawas	Sumatera Utara	,\
    4123	:	22742	Ramba	Huristak	Kab.	Padang Lawas	Sumatera Utara	,\
    4124	:	22742	Siala Gundi	Huristak	Kab.	Padang Lawas	Sumatera Utara	,\
    4125	:	22742	Sigading	Huristak	Kab.	Padang Lawas	Sumatera Utara	,\
    4126	:	22742	Sihoda-Hoda (Tarutung)	Huristak	Kab.	Padang Lawas	Sumatera Utara	,\
    4127	:	22742	Sipirok Baru	Huristak	Kab.	Padang Lawas	Sumatera Utara	,\
    4128	:	22742	Tanjung Baringin	Huristak	Kab.	Padang Lawas	Sumatera Utara	,\
    4129	:	22742	Tanjung Morang Hr	Huristak	Kab.	Padang Lawas	Sumatera Utara	,\
    4130	:	22742	Tobing Jae	Huristak	Kab.	Padang Lawas	Sumatera Utara	,\
    4131	:	22742	Tobing Julu	Huristak	Kab.	Padang Lawas	Sumatera Utara	,\
    4132	:	22742	Tobing Tinggi Hr	Huristak	Kab.	Padang Lawas	Sumatera Utara	,\
    4133	:	22733	Aek Godang	Hulu Sihapas	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4134	:	22733	Aek Nauli	Hulu Sihapas	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4135	:	22733	Pangirkiran	Hulu Sihapas	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4136	:	22733	Parmeraan	Hulu Sihapas	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4137	:	22733	Pintu Bosi	Hulu Sihapas	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4138	:	22733	Sampuran Simarloting	Hulu Sihapas	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4139	:	22733	Sidongdong	Hulu Sihapas	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4140	:	22733	Simaninggir	Hulu Sihapas	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4141	:	22733	Sitabar	Hulu Sihapas	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4142	:	22733	Suka Dame	Hulu Sihapas	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4143	:	20854	Baru Pasar VIII (8)	Hinai	Kab.	Langkat	Sumatera Utara	,\
    4144	:	20854	Batu Melenggang	Hinai	Kab.	Langkat	Sumatera Utara	,\
    4145	:	20854	Cempa	Hinai	Kab.	Langkat	Sumatera Utara	,\
    4146	:	20854	Hinai Kanan	Hinai	Kab.	Langkat	Sumatera Utara	,\
    4147	:	20854	Kebun Lada	Hinai	Kab.	Langkat	Sumatera Utara	,\
    4148	:	20854	Muka Paya	Hinai	Kab.	Langkat	Sumatera Utara	,\
    4149	:	20854	Paya Rengas	Hinai	Kab.	Langkat	Sumatera Utara	,\
    4150	:	20854	Perkebunan Tanjung Beringin	Hinai	Kab.	Langkat	Sumatera Utara	,\
    4151	:	20854	Suka Damai	Hinai	Kab.	Langkat	Sumatera Utara	,\
    4152	:	20854	Suka Damai Timur	Hinai	Kab.	Langkat	Sumatera Utara	,\
    4153	:	20854	Suka Jadi	Hinai	Kab.	Langkat	Sumatera Utara	,\
    4154	:	20854	Tamaran	Hinai	Kab.	Langkat	Sumatera Utara	,\
    4155	:	20854	Tanjung Mulia	Hinai	Kab.	Langkat	Sumatera Utara	,\
    4156	:	22864	Anaoma	Hilisalawa`ahe (Hilisalawaahe)	Kab.	Nias Selatan	Sumatera Utara	,\
    4157	:	22864	Berua Siwalawa	Hilisalawa`ahe (Hilisalawaahe)	Kab.	Nias Selatan	Sumatera Utara	,\
    4158	:	22864	Bukitburasi	Hilisalawa`ahe (Hilisalawaahe)	Kab.	Nias Selatan	Sumatera Utara	,\
    4159	:	22864	Hilidulo	Hilisalawa`ahe (Hilisalawaahe)	Kab.	Nias Selatan	Sumatera Utara	,\
    4160	:	22864	Hiligodu	Hilisalawa`ahe (Hilisalawaahe)	Kab.	Nias Selatan	Sumatera Utara	,\
    4161	:	22864	Maluo	Hilisalawa`ahe (Hilisalawaahe)	Kab.	Nias Selatan	Sumatera Utara	,\
    4162	:	22864	Manawadano	Hilisalawa`ahe (Hilisalawaahe)	Kab.	Nias Selatan	Sumatera Utara	,\
    4163	:	22864	Sisobahili Siwalawa	Hilisalawa`ahe (Hilisalawaahe)	Kab.	Nias Selatan	Sumatera Utara	,\
    4164	:	22864	Talio	Hilisalawa`ahe (Hilisalawaahe)	Kab.	Nias Selatan	Sumatera Utara	,\
    4165	:	22864	Umbu`asi	Hilisalawa`ahe (Hilisalawaahe)	Kab.	Nias Selatan	Sumatera Utara	,\
    4166	:	22864	Umbuasi Barat	Hilisalawa`ahe (Hilisalawaahe)	Kab.	Nias Selatan	Sumatera Utara	,\
    4167	:	22864	Bawasalo`o Dao-dao	Hilimegai	Kab.	Nias Selatan	Sumatera Utara	,\
    4168	:	22864	Dao-dao Sowo	Hilimegai	Kab.	Nias Selatan	Sumatera Utara	,\
    4169	:	22864	Hiliadulo	Hilimegai	Kab.	Nias Selatan	Sumatera Utara	,\
    4170	:	22864	Hilitoese	Hilimegai	Kab.	Nias Selatan	Sumatera Utara	,\
    4171	:	22864	Soledua	Hilimegai	Kab.	Nias Selatan	Sumatera Utara	,\
    4172	:	22864	Soledua Dua	Hilimegai	Kab.	Nias Selatan	Sumatera Utara	,\
    4173	:	22864	Soledua Satu	Hilimegai	Kab.	Nias Selatan	Sumatera Utara	,\
    4174	:	22864	Togizita	Hilimegai	Kab.	Nias Selatan	Sumatera Utara	,\
    4175	:	22864	Togozita Satu	Hilimegai	Kab.	Nias Selatan	Sumatera Utara	,\
    4176	:	22864	Tuho Owo	Hilimegai	Kab.	Nias Selatan	Sumatera Utara	,\
    4177	:	22854	Dima	Hiliduho	Kab.	Nias	Sumatera Utara	,\
    4178	:	22854	Fadoro Lauru	Hiliduho	Kab.	Nias	Sumatera Utara	,\
    4179	:	22854	Hiliduho	Hiliduho	Kab.	Nias	Sumatera Utara	,\
    4180	:	22851	Hiligodu Tanoseo	Hiliduho	Kab.	Nias	Sumatera Utara	,\
    4181	:	22854	Lasara Tanose`o	Hiliduho	Kab.	Nias	Sumatera Utara	,\
    4182	:	22854	Ombolalasalo`o	Hiliduho	Kab.	Nias	Sumatera Utara	,\
    4183	:	22854	Ombolata Sisarahili	Hiliduho	Kab.	Nias	Sumatera Utara	,\
    4184	:	22854	Ononamolo I Bot	Hiliduho	Kab.	Nias	Sumatera Utara	,\
    4185	:	22854	Onowaembo Hiligara	Hiliduho	Kab.	Nias	Sumatera Utara	,\
    4186	:	22854	Onozitolidulu	Hiliduho	Kab.	Nias	Sumatera Utara	,\
    4187	:	22854	Silimabanua	Hiliduho	Kab.	Nias	Sumatera Utara	,\
    4188	:	22854	Sinarikhi	Hiliduho	Kab.	Nias	Sumatera Utara	,\
    4189	:	22854	Sisobahili I Tanoseo	Hiliduho	Kab.	Nias	Sumatera Utara	,\
    4190	:	22854	Sisobalauru	Hiliduho	Kab.	Nias	Sumatera Utara	,\
    4191	:	22854	Tanoseo	Hiliduho	Kab.	Nias	Sumatera Utara	,\
    4192	:	22854	Tuhegafoa II	Hiliduho	Kab.	Nias	Sumatera Utara	,\
    4193	:	22851	Awela	Hili Serangkai (Hilisaranggu)	Kab.	Nias	Sumatera Utara	,\
    4194	:	22851	Dahadano Botombawo	Hili Serangkai (Hilisaranggu)	Kab.	Nias	Sumatera Utara	,\
    4195	:	22851	Ehosakhozi	Hili Serangkai (Hilisaranggu)	Kab.	Nias	Sumatera Utara	,\
    4196	:	22851	Fadoro Hunogoa	Hili Serangkai (Hilisaranggu)	Kab.	Nias	Sumatera Utara	,\
    4197	:	22851	Fadoro Lalai	Hili Serangkai (Hilisaranggu)	Kab.	Nias	Sumatera Utara	,\
    4198	:	22851	Fulolo Lalai	Hili Serangkai (Hilisaranggu)	Kab.	Nias	Sumatera Utara	,\
    4199	:	22851	Hilizia Lauru	Hili Serangkai (Hilisaranggu)	Kab.	Nias	Sumatera Utara	,\
    4200	:	22851	Lalai I/II	Hili Serangkai (Hilisaranggu)	Kab.	Nias	Sumatera Utara	,\
    4201	:	22851	Lawa-Lawa	Hili Serangkai (Hilisaranggu)	Kab.	Nias	Sumatera Utara	,\
    4202	:	22851	Lolofaoso	Hili Serangkai (Hilisaranggu)	Kab.	Nias	Sumatera Utara	,\
    4203	:	22851	Lolofaoso Lalai	Hili Serangkai (Hilisaranggu)	Kab.	Nias	Sumatera Utara	,\
    4204	:	22851	Lolowua	Hili Serangkai (Hilisaranggu)	Kab.	Nias	Sumatera Utara	,\
    4205	:	22851	Lolowua Hiliwarasi	Hili Serangkai (Hilisaranggu)	Kab.	Nias	Sumatera Utara	,\
    4206	:	22851	Onombongi	Hili Serangkai (Hilisaranggu)	Kab.	Nias	Sumatera Utara	,\
    4207	:	22851	Orahili Idanoi	Hili Serangkai (Hilisaranggu)	Kab.	Nias	Sumatera Utara	,\
    4208	:	22881	Baruyu Sibohou	Hibala	Kab.	Nias Selatan	Sumatera Utara	,\
    4209	:	22881	Bawonifaoso	Hibala	Kab.	Nias Selatan	Sumatera Utara	,\
    4210	:	22881	Duru	Hibala	Kab.	Nias Selatan	Sumatera Utara	,\
    4211	:	22881	Eho	Hibala	Kab.	Nias Selatan	Sumatera Utara	,\
    4212	:	22881	Hilianombasela	Hibala	Kab.	Nias Selatan	Sumatera Utara	,\
    4213	:	22881	Hilikana	Hibala	Kab.	Nias Selatan	Sumatera Utara	,\
    4214	:	22881	Hilinifaese	Hibala	Kab.	Nias Selatan	Sumatera Utara	,\
    4215	:	22881	Hilioro Dua Tebolo	Hibala	Kab.	Nias Selatan	Sumatera Utara	,\
    4216	:	22881	Hilioro Mao	Hibala	Kab.	Nias Selatan	Sumatera Utara	,\
    4217	:	22881	Lumbui Melayu	Hibala	Kab.	Nias Selatan	Sumatera Utara	,\
    4218	:	22881	Lumbui Nias	Hibala	Kab.	Nias Selatan	Sumatera Utara	,\
    4219	:	22881	Omega	Hibala	Kab.	Nias Selatan	Sumatera Utara	,\
    4220	:	22881	Sepakat	Hibala	Kab.	Nias Selatan	Sumatera Utara	,\
    4221	:	22881	Sialema	Hibala	Kab.	Nias Selatan	Sumatera Utara	,\
    4222	:	22881	Tano Mokinu	Hibala	Kab.	Nias Selatan	Sumatera Utara	,\
    4223	:	22881	Tebolo Melayu	Hibala	Kab.	Nias Selatan	Sumatera Utara	,\
    4224	:	22881	Tuwaso	Hibala	Kab.	Nias Selatan	Sumatera Utara	,\
    4225	:	21174	Bosar Nauli	Hatonduhan	Kab.	Simalungun	Sumatera Utara	,\
    4226	:	21174	Buttu Bayu (Buntu Bayu)	Hatonduhan	Kab.	Simalungun	Sumatera Utara	,\
    4227	:	21174	Buttu Turunan (Buntu Turunan)	Hatonduhan	Kab.	Simalungun	Sumatera Utara	,\
    4228	:	21174	Jawa Tongah	Hatonduhan	Kab.	Simalungun	Sumatera Utara	,\
    4229	:	21174	Jawa Tongah II	Hatonduhan	Kab.	Simalungun	Sumatera Utara	,\
    4230	:	21174	Parhundalian Jawadipar	Hatonduhan	Kab.	Simalungun	Sumatera Utara	,\
    4231	:	21174	Saribu Asih	Hatonduhan	Kab.	Simalungun	Sumatera Utara	,\
    4232	:	21174	Tangga Batu	Hatonduhan	Kab.	Simalungun	Sumatera Utara	,\
    4233	:	21174	Tonduhan	Hatonduhan	Kab.	Simalungun	Sumatera Utara	,\
    4234	:	22391	Dolok Raja	Harian	Kab.	Samosir	Sumatera Utara	,\
    4235	:	22391	Hariara Pohan	Harian	Kab.	Samosir	Sumatera Utara	,\
    4236	:	22391	Janji Martahan	Harian	Kab.	Samosir	Sumatera Utara	,\
    4237	:	22391	Partungko Naginjang	Harian	Kab.	Samosir	Sumatera Utara	,\
    4238	:	22391	Sampur Toba	Harian	Kab.	Samosir	Sumatera Utara	,\
    4239	:	22391	Siparmahan	Harian	Kab.	Samosir	Sumatera Utara	,\
    4240	:	22391	Sosor Dolok	Harian	Kab.	Samosir	Sumatera Utara	,\
    4241	:	22391	Turpuk Limbong	Harian	Kab.	Samosir	Sumatera Utara	,\
    4242	:	22391	Turpuk Malau	Harian	Kab.	Samosir	Sumatera Utara	,\
    4243	:	22391	Turpuk Sagala	Harian	Kab.	Samosir	Sumatera Utara	,\
    4244	:	22391	Turpuk Sihotang	Harian	Kab.	Samosir	Sumatera Utara	,\
    4245	:	21174	Haranggaol	Haranggaol Horison	Kab.	Simalungun	Sumatera Utara	,\
    4246	:	21174	Nagori Purba Harison/Harisan	Haranggaol Horison	Kab.	Simalungun	Sumatera Utara	,\
    4247	:	21174	Nagori Purba Pasir	Haranggaol Horison	Kab.	Simalungun	Sumatera Utara	,\
    4248	:	21174	Nagori Purba Saribu	Haranggaol Horison	Kab.	Simalungun	Sumatera Utara	,\
    4249	:	21174	Nagori Sihalpe	Haranggaol Horison	Kab.	Simalungun	Sumatera Utara	,\
    4250	:	20374	Bulu Cina	Hamparan Perak	Kab.	Deli Serdang	Sumatera Utara	,\
    4251	:	20374	Desa Lama (Kampung Lama)	Hamparan Perak	Kab.	Deli Serdang	Sumatera Utara	,\
    4252	:	20374	Hamparan Perak	Hamparan Perak	Kab.	Deli Serdang	Sumatera Utara	,\
    4253	:	20374	Klambir	Hamparan Perak	Kab.	Deli Serdang	Sumatera Utara	,\
    4254	:	20374	Klambir Lima Kampung	Hamparan Perak	Kab.	Deli Serdang	Sumatera Utara	,\
    4255	:	20374	Klambir Lima Kebon	Hamparan Perak	Kab.	Deli Serdang	Sumatera Utara	,\
    4256	:	20374	Klumpang Kampung	Hamparan Perak	Kab.	Deli Serdang	Sumatera Utara	,\
    4257	:	20374	Klumpang Kebon	Hamparan Perak	Kab.	Deli Serdang	Sumatera Utara	,\
    4258	:	20374	Kota Datar	Hamparan Perak	Kab.	Deli Serdang	Sumatera Utara	,\
    4259	:	20374	Kota Pantang (Rantang)	Hamparan Perak	Kab.	Deli Serdang	Sumatera Utara	,\
    4260	:	20374	Paluh Kurau	Hamparan Perak	Kab.	Deli Serdang	Sumatera Utara	,\
    4261	:	20374	Paluh Manan	Hamparan Perak	Kab.	Deli Serdang	Sumatera Utara	,\
    4262	:	20374	Paya Bakung	Hamparan Perak	Kab.	Deli Serdang	Sumatera Utara	,\
    4263	:	20374	Sei/Sungai Baharu	Hamparan Perak	Kab.	Deli Serdang	Sumatera Utara	,\
    4264	:	20374	Selemak	Hamparan Perak	Kab.	Deli Serdang	Sumatera Utara	,\
    4265	:	20374	Sialang Muda	Hamparan Perak	Kab.	Deli Serdang	Sumatera Utara	,\
    4266	:	20374	Tandam/Tandem Hilir Dua	Hamparan Perak	Kab.	Deli Serdang	Sumatera Utara	,\
    4267	:	20374	Tandam/Tandem Hilir Satu	Hamparan Perak	Kab.	Deli Serdang	Sumatera Utara	,\
    4268	:	20374	Tandam/Tandem Hulu Dua	Hamparan Perak	Kab.	Deli Serdang	Sumatera Utara	,\
    4269	:	20374	Tandam/Tandem Hulu Satu	Hamparan Perak	Kab.	Deli Serdang	Sumatera Utara	,\
    4270	:	22753	Balimbing	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4271	:	22753	Batu Tunggal	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4272	:	22753	Bolatan	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4273	:	22753	Borgot/Bargot Topong Jae	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4274	:	22753	Borgot/Bargot Topong Julu	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4275	:	22753	Gunung Intan	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4276	:	22753	Gunung Manaon III	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4277	:	22753	Halongonan	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4278	:	22753	Hambulo	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4279	:	22753	Hasahatan (Hasatan)	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4280	:	22753	Hiteurat	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4281	:	22753	Huta Baru Nangka	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4282	:	22753	Hutaimbaru	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4283	:	22753	Hutanopan	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4284	:	22753	Japinulik	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4285	:	22753	Mompang I	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4286	:	22753	Napalancat	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4287	:	22753	Pagar Gunung	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4288	:	22753	Pangarambangan	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4289	:	22753	Pangirkiran	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4290	:	22753	Paolan	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4291	:	22753	Paran Honas	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4292	:	22753	Pasir Baru	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4293	:	22753	Rondaman	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4294	:	22753	Rondaman Siburegar	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4295	:	22753	Saba	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4296	:	22753	Sandean Jae	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4297	:	22753	Sandean Julu	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4298	:	22753	Sandean Tonga	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4299	:	22753	Siancimun	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4300	:	22753	Siboru Angin	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4301	:	22753	Sigala-Gala	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4302	:	22753	Silantoyung	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4303	:	22753	Siopuk/Sihopuk Baru	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4304	:	22753	Siopuk/Sihopuk Lama	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4305	:	22753	Sipaho	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4306	:	22753	Sipenggeng	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4307	:	22753	Siringkit Jae	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4308	:	22753	Siringkit Julu	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4309	:	22753	Sitabola	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4310	:	22753	Sitonun (Sitenun)	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4311	:	22753	Situmbaga	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4312	:	22753	Tapus Jae	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4313	:	22753	Ujung Padang	Halongonan	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4314	:	22383	Aek Ulok	Habinsaran	Kab.	Toba Samosir	Sumatera Utara	,\
    4315	:	22383	Batu Nabolon	Habinsaran	Kab.	Toba Samosir	Sumatera Utara	,\
    4316	:	22383	Hitetano (Tite Tano)	Habinsaran	Kab.	Toba Samosir	Sumatera Utara	,\
    4317	:	22383	Lobu Hole	Habinsaran	Kab.	Toba Samosir	Sumatera Utara	,\
    4318	:	22383	Lumban Gaol	Habinsaran	Kab.	Toba Samosir	Sumatera Utara	,\
    4319	:	22383	Lumban Lintong	Habinsaran	Kab.	Toba Samosir	Sumatera Utara	,\
    4320	:	22383	Lumban Pea	Habinsaran	Kab.	Toba Samosir	Sumatera Utara	,\
    4321	:	22383	Lumban Pinasa	Habinsaran	Kab.	Toba Samosir	Sumatera Utara	,\
    4322	:	22383	Lumban Pinasa Saroba	Habinsaran	Kab.	Toba Samosir	Sumatera Utara	,\
    4323	:	22383	Lumban Rau Balik	Habinsaran	Kab.	Toba Samosir	Sumatera Utara	,\
    4324	:	22383	Lumban Rau Barat	Habinsaran	Kab.	Toba Samosir	Sumatera Utara	,\
    4325	:	22383	Lumban Rau Selatan	Habinsaran	Kab.	Toba Samosir	Sumatera Utara	,\
    4326	:	22383	Lumban Ruhap/Ruhaya	Habinsaran	Kab.	Toba Samosir	Sumatera Utara	,\
    4327	:	22383	Pagar Batu	Habinsaran	Kab.	Toba Samosir	Sumatera Utara	,\
    4328	:	22383	Panamparan	Habinsaran	Kab.	Toba Samosir	Sumatera Utara	,\
    4329	:	22383	Pangunjungan	Habinsaran	Kab.	Toba Samosir	Sumatera Utara	,\
    4330	:	22383	Pararungan	Habinsaran	Kab.	Toba Samosir	Sumatera Utara	,\
    4331	:	22383	Parsoburan Barat	Habinsaran	Kab.	Toba Samosir	Sumatera Utara	,\
    4332	:	22383	Parsoburan Tengah	Habinsaran	Kab.	Toba Samosir	Sumatera Utara	,\
    4333	:	22383	Sibuntuon	Habinsaran	Kab.	Toba Samosir	Sumatera Utara	,\
    4334	:	22383	Taon Marisi	Habinsaran	Kab.	Toba Samosir	Sumatera Utara	,\
    4335	:	22383	Tornagodang	Habinsaran	Kab.	Toba Samosir	Sumatera Utara	,\
    4336	:	22851	Afia	Gunungsitoli Utara	Kota	Gunungsitoli	Sumatera Utara	,\
    4337	:	22851	Gawu Gawu Bouso/Bauso	Gunungsitoli Utara	Kota	Gunungsitoli	Sumatera Utara	,\
    4338	:	22851	Hambawa	Gunungsitoli Utara	Kota	Gunungsitoli	Sumatera Utara	,\
    4339	:	22851	Hiligodu Ulu	Gunungsitoli Utara	Kota	Gunungsitoli	Sumatera Utara	,\
    4340	:	22851	Hilimbowo Olora	Gunungsitoli Utara	Kota	Gunungsitoli	Sumatera Utara	,\
    4341	:	22851	Lasara Sowu	Gunungsitoli Utara	Kota	Gunungsitoli	Sumatera Utara	,\
    4342	:	22851	Loloanaa / Lolomoyo	Gunungsitoli Utara	Kota	Gunungsitoli	Sumatera Utara	,\
    4343	:	22851	Olora	Gunungsitoli Utara	Kota	Gunungsitoli	Sumatera Utara	,\
    4344	:	22851	Teluk Belukar	Gunungsitoli Utara	Kota	Gunungsitoli	Sumatera Utara	,\
    4345	:	22851	Tetehosi Afia	Gunungsitoli Utara	Kota	Gunungsitoli	Sumatera Utara	,\
    4346	:	22851	Faekhu	Gunungsitoli Selatan	Kota	Gunungsitoli	Sumatera Utara	,\
    4347	:	22851	Fodo	Gunungsitoli Selatan	Kota	Gunungsitoli	Sumatera Utara	,\
    4348	:	22851	Hiligara	Gunungsitoli Selatan	Kota	Gunungsitoli	Sumatera Utara	,\
    4349	:	22851	Hiligodu Ombolata	Gunungsitoli Selatan	Kota	Gunungsitoli	Sumatera Utara	,\
    4350	:	22851	Lolofaoso Tabaloho	Gunungsitoli Selatan	Kota	Gunungsitoli	Sumatera Utara	,\
    4351	:	22851	Lololakha	Gunungsitoli Selatan	Kota	Gunungsitoli	Sumatera Utara	,\
    4352	:	22851	Lolomboli	Gunungsitoli Selatan	Kota	Gunungsitoli	Sumatera Utara	,\
    4353	:	22851	Luaha Laraga	Gunungsitoli Selatan	Kota	Gunungsitoli	Sumatera Utara	,\
    4354	:	22851	Mazingo Tabaloho	Gunungsitoli Selatan	Kota	Gunungsitoli	Sumatera Utara	,\
    4355	:	22851	Ombolata Simenari (Simanari)	Gunungsitoli Selatan	Kota	Gunungsitoli	Sumatera Utara	,\
    4356	:	22851	Ononamolo I Lot	Gunungsitoli Selatan	Kota	Gunungsitoli	Sumatera Utara	,\
    4357	:	22851	Onozitoli Tabaloho	Gunungsitoli Selatan	Kota	Gunungsitoli	Sumatera Utara	,\
    4358	:	22851	Sihareo I Tabaloho	Gunungsitoli Selatan	Kota	Gunungsitoli	Sumatera Utara	,\
    4359	:	22851	Sisobahili II Tanoseo	Gunungsitoli Selatan	Kota	Gunungsitoli	Sumatera Utara	,\
    4360	:	22851	Tetehosi Ombolata	Gunungsitoli Selatan	Kota	Gunungsitoli	Sumatera Utara	,\
    4361	:	22871	Awaai	Gunungsitoli Idanoi	Kota	Gunungsitoli	Sumatera Utara	,\
    4362	:	22871	Bawodesolo	Gunungsitoli Idanoi	Kota	Gunungsitoli	Sumatera Utara	,\
    4363	:	22871	Binaka	Gunungsitoli Idanoi	Kota	Gunungsitoli	Sumatera Utara	,\
    4364	:	22871	Dahana	Gunungsitoli Idanoi	Kota	Gunungsitoli	Sumatera Utara	,\
    4365	:	22871	Fadoro	Gunungsitoli Idanoi	Kota	Gunungsitoli	Sumatera Utara	,\
    4366	:	22871	Fowa	Gunungsitoli Idanoi	Kota	Gunungsitoli	Sumatera Utara	,\
    4367	:	22871	Helefanikha	Gunungsitoli Idanoi	Kota	Gunungsitoli	Sumatera Utara	,\
    4368	:	22871	Hilihambawa	Gunungsitoli Idanoi	Kota	Gunungsitoli	Sumatera Utara	,\
    4369	:	22871	Hilimbawo Desolo	Gunungsitoli Idanoi	Kota	Gunungsitoli	Sumatera Utara	,\
    4370	:	22871	Hilimbowo Idanoi	Gunungsitoli Idanoi	Kota	Gunungsitoli	Sumatera Utara	,\
    4371	:	22871	Hiliweto Idanoi	Gunungsitoli Idanoi	Kota	Gunungsitoli	Sumatera Utara	,\
    4372	:	22871	Humene	Gunungsitoli Idanoi	Kota	Gunungsitoli	Sumatera Utara	,\
    4373	:	22871	Idanotae	Gunungsitoli Idanoi	Kota	Gunungsitoli	Sumatera Utara	,\
    4374	:	22871	Lewuoguru Idanoi	Gunungsitoli Idanoi	Kota	Gunungsitoli	Sumatera Utara	,\
    4375	:	22871	Loloanaa Idanoi	Gunungsitoli Idanoi	Kota	Gunungsitoli	Sumatera Utara	,\
    4376	:	22871	Ombolata	Gunungsitoli Idanoi	Kota	Gunungsitoli	Sumatera Utara	,\
    4377	:	22871	Onowaembo	Gunungsitoli Idanoi	Kota	Gunungsitoli	Sumatera Utara	,\
    4378	:	22871	Samasi	Gunungsitoli Idanoi	Kota	Gunungsitoli	Sumatera Utara	,\
    4379	:	22871	Sifalaete	Gunungsitoli Idanoi	Kota	Gunungsitoli	Sumatera Utara	,\
    4380	:	22871	Simanaere	Gunungsitoli Idanoi	Kota	Gunungsitoli	Sumatera Utara	,\
    4381	:	22871	Siwalubanua I	Gunungsitoli Idanoi	Kota	Gunungsitoli	Sumatera Utara	,\
    4382	:	22871	Siwalubanua II	Gunungsitoli Idanoi	Kota	Gunungsitoli	Sumatera Utara	,\
    4383	:	22871	Tetehosi I	Gunungsitoli Idanoi	Kota	Gunungsitoli	Sumatera Utara	,\
    4384	:	22871	Tetehosi II	Gunungsitoli Idanoi	Kota	Gunungsitoli	Sumatera Utara	,\
    4385	:	22871	Tuhegeo I	Gunungsitoli Idanoi	Kota	Gunungsitoli	Sumatera Utara	,\
    4386	:	22871	Tuhegeo II	Gunungsitoli Idanoi	Kota	Gunungsitoli	Sumatera Utara	,\
    4387	:	22811	Gada	Gunungsitoli Barat	Kota	Gunungsitoli	Sumatera Utara	,\
    4388	:	22811	Hilinakhe	Gunungsitoli Barat	Kota	Gunungsitoli	Sumatera Utara	,\
    4389	:	22811	Lolomoyo Tuhemberua	Gunungsitoli Barat	Kota	Gunungsitoli	Sumatera Utara	,\
    4390	:	22811	Ononamolo II	Gunungsitoli Barat	Kota	Gunungsitoli	Sumatera Utara	,\
    4391	:	22811	Onozikho	Gunungsitoli Barat	Kota	Gunungsitoli	Sumatera Utara	,\
    4392	:	22811	Orahili Tumori	Gunungsitoli Barat	Kota	Gunungsitoli	Sumatera Utara	,\
    4393	:	22811	Sihareo Siwahili	Gunungsitoli Barat	Kota	Gunungsitoli	Sumatera Utara	,\
    4394	:	22811	Tumori	Gunungsitoli Barat	Kota	Gunungsitoli	Sumatera Utara	,\
    4395	:	22811	Tumori Balohili	Gunungsitoli Barat	Kota	Gunungsitoli	Sumatera Utara	,\
    4396	:	22851	Fadoro Hilimbowo	Gunungsitoli Alo`oa	Kota	Gunungsitoli	Sumatera Utara	,\
    4397	:	22851	Fadoro You	Gunungsitoli Alo`oa	Kota	Gunungsitoli	Sumatera Utara	,\
    4398	:	22851	Irano Lase (Iraono Lase)	Gunungsitoli Alo`oa	Kota	Gunungsitoli	Sumatera Utara	,\
    4399	:	22851	Lololawa	Gunungsitoli Alo`oa	Kota	Gunungsitoli	Sumatera Utara	,\
    4400	:	22851	Nazalou Alo`oa	Gunungsitoli Alo`oa	Kota	Gunungsitoli	Sumatera Utara	,\
    4401	:	22851	Nazalou Lolowua	Gunungsitoli Alo`oa	Kota	Gunungsitoli	Sumatera Utara	,\
    4402	:	22851	Niko`otano Dao	Gunungsitoli Alo`oa	Kota	Gunungsitoli	Sumatera Utara	,\
    4403	:	22851	Orahili Tanose'o	Gunungsitoli Alo'oa	Kota	Gunungsitoli	Sumatera Utara	,\
    4404	:	22851	Tarakhaini	Gunungsitoli Alo`oa	Kota	Gunungsitoli	Sumatera Utara	,\
    4405	:	22811	Bawodesolo (Bawadesolo)	Gunungsitoli	Kota	Gunungsitoli	Sumatera Utara	,\
    4406	:	22811	Boyo	Gunungsitoli	Kota	Gunungsitoli	Sumatera Utara	,\
    4407	:	22811	Dahadano Gawu Gawu	Gunungsitoli	Kota	Gunungsitoli	Sumatera Utara	,\
    4408	:	22811	Dahana Tabaloho	Gunungsitoli	Kota	Gunungsitoli	Sumatera Utara	,\
    4409	:	22811	Fadoro Lasara	Gunungsitoli	Kota	Gunungsitoli	Sumatera Utara	,\
    4410	:	22811	Hili Hao	Gunungsitoli	Kota	Gunungsitoli	Sumatera Utara	,\
    4411	:	22811	Hilimbaruzo	Gunungsitoli	Kota	Gunungsitoli	Sumatera Utara	,\
    4412	:	22811	Hilina A	Gunungsitoli	Kota	Gunungsitoli	Sumatera Utara	,\
    4413	:	22811	Ilir	Gunungsitoli	Kota	Gunungsitoli	Sumatera Utara	,\
    4414	:	22812	Iraonogeba	Gunungsitoli	Kota	Gunungsitoli	Sumatera Utara	,\
    4415	:	22811	Lasara Bahili	Gunungsitoli	Kota	Gunungsitoli	Sumatera Utara	,\
    4416	:	22811	Lolomoyo/Lelewonu Nikootano	Gunungsitoli	Kota	Gunungsitoli	Sumatera Utara	,\
    4417	:	22811	Madolaoli	Gunungsitoli	Kota	Gunungsitoli	Sumatera Utara	,\
    4418	:	22811	Madula	Gunungsitoli	Kota	Gunungsitoli	Sumatera Utara	,\
    4419	:	22811	Miga	Gunungsitoli	Kota	Gunungsitoli	Sumatera Utara	,\
    4420	:	22811	Moawo	Gunungsitoli	Kota	Gunungsitoli	Sumatera Utara	,\
    4421	:	22814	Mudik	Gunungsitoli	Kota	Gunungsitoli	Sumatera Utara	,\
    4422	:	22811	Ombolata Ulu	Gunungsitoli	Kota	Gunungsitoli	Sumatera Utara	,\
    4423	:	22811	Ono Waembo	Gunungsitoli	Kota	Gunungsitoli	Sumatera Utara	,\
    4424	:	22811	Onozitoli Olora	Gunungsitoli	Kota	Gunungsitoli	Sumatera Utara	,\
    4425	:	22811	Onozitoli Sifaoroasi (Siforoasi)	Gunungsitoli	Kota	Gunungsitoli	Sumatera Utara	,\
    4426	:	22811	Pasar Gunung Sitoli	Gunungsitoli	Kota	Gunungsitoli	Sumatera Utara	,\
    4427	:	22811	Saewe	Gunungsitoli	Kota	Gunungsitoli	Sumatera Utara	,\
    4428	:	22812	Saombo	Gunungsitoli	Kota	Gunungsitoli	Sumatera Utara	,\
    4429	:	22811	Sifalaete Tabaloho	Gunungsitoli	Kota	Gunungsitoli	Sumatera Utara	,\
    4430	:	22811	Sifalaete Ulu	Gunungsitoli	Kota	Gunungsitoli	Sumatera Utara	,\
    4431	:	22811	Sihareo II Tabaloho	Gunungsitoli	Kota	Gunungsitoli	Sumatera Utara	,\
    4432	:	22811	Simandraolo	Gunungsitoli	Kota	Gunungsitoli	Sumatera Utara	,\
    4433	:	22811	Sisarahili Gamo	Gunungsitoli	Kota	Gunungsitoli	Sumatera Utara	,\
    4434	:	22811	Sisarahili Sisambalahe	Gunungsitoli	Kota	Gunungsitoli	Sumatera Utara	,\
    4435	:	22811	Sisobahili Tabaloho	Gunungsitoli	Kota	Gunungsitoli	Sumatera Utara	,\
    4436	:	22811	Tuhemberua Ulu	Gunungsitoli	Kota	Gunungsitoli	Sumatera Utara	,\
    4437	:	22251	Batu Gun-Gun	Gunung Sitember	Kab.	Dairi	Sumatera Utara	,\
    4438	:	22251	Bukit Lau Kersik	Gunung Sitember	Kab.	Dairi	Sumatera Utara	,\
    4439	:	22251	Gundaling	Gunung Sitember	Kab.	Dairi	Sumatera Utara	,\
    4440	:	22251	Gunung Sitember	Gunung Sitember	Kab.	Dairi	Sumatera Utara	,\
    4441	:	22251	Kendit Liang	Gunung Sitember	Kab.	Dairi	Sumatera Utara	,\
    4442	:	22251	Lau Lebah	Gunung Sitember	Kab.	Dairi	Sumatera Utara	,\
    4443	:	22251	Rante Besi	Gunung Sitember	Kab.	Dairi	Sumatera Utara	,\
    4444	:	22251	Tupak Raja	Gunung Sitember	Kab.	Dairi	Sumatera Utara	,\
    4445	:	20583	Bintang Meriah	Gunung Meriah	Kab.	Deli Serdang	Sumatera Utara	,\
    4446	:	20583	Gunung Meriah	Gunung Meriah	Kab.	Deli Serdang	Sumatera Utara	,\
    4447	:	20583	Gunung Paribuan	Gunung Meriah	Kab.	Deli Serdang	Sumatera Utara	,\
    4448	:	20583	Gunung Seribu	Gunung Meriah	Kab.	Deli Serdang	Sumatera Utara	,\
    4449	:	20583	Gunung Sinembah	Gunung Meriah	Kab.	Deli Serdang	Sumatera Utara	,\
    4450	:	20583	Kuta Bayu	Gunung Meriah	Kab.	Deli Serdang	Sumatera Utara	,\
    4451	:	20583	Kuta Tengah	Gunung Meriah	Kab.	Deli Serdang	Sumatera Utara	,\
    4452	:	20583	Marjanji Pematang	Gunung Meriah	Kab.	Deli Serdang	Sumatera Utara	,\
    4453	:	20583	Marjanji Tongah	Gunung Meriah	Kab.	Deli Serdang	Sumatera Utara	,\
    4454	:	20583	Pekan Gunung Meriah	Gunung Meriah	Kab.	Deli Serdang	Sumatera Utara	,\
    4455	:	20583	Simompar (Simempar)	Gunung Meriah	Kab.	Deli Serdang	Sumatera Utara	,\
    4456	:	20583	Ujung Meriah	Gunung Meriah	Kab.	Deli Serdang	Sumatera Utara	,\
    4457	:	21174	Bandar Malela	Gunung Maligas	Kab.	Simalungun	Sumatera Utara	,\
    4458	:	21174	Gajing	Gunung Maligas	Kab.	Simalungun	Sumatera Utara	,\
    4459	:	21174	Hutadipar	Gunung Maligas	Kab.	Simalungun	Sumatera Utara	,\
    4460	:	21174	Karang Anyer	Gunung Maligas	Kab.	Simalungun	Sumatera Utara	,\
    4461	:	21174	Karang Rejo	Gunung Maligas	Kab.	Simalungun	Sumatera Utara	,\
    4462	:	21174	Karang Sari	Gunung Maligas	Kab.	Simalungun	Sumatera Utara	,\
    4463	:	21174	Rabuhit	Gunung Maligas	Kab.	Simalungun	Sumatera Utara	,\
    4464	:	21174	Silau Bayu	Gunung Maligas	Kab.	Simalungun	Sumatera Utara	,\
    4465	:	21174	Tumorang	Gunung Maligas	Kab.	Simalungun	Sumatera Utara	,\
    4466	:	21174	Bandar Siantar	Gunung Malela	Kab.	Simalungun	Sumatera Utara	,\
    4467	:	21174	Bangun	Gunung Malela	Kab.	Simalungun	Sumatera Utara	,\
    4468	:	21174	Bukit Maraja	Gunung Malela	Kab.	Simalungun	Sumatera Utara	,\
    4469	:	21174	Dolok Malela	Gunung Malela	Kab.	Simalungun	Sumatera Utara	,\
    4470	:	21174	Lingga	Gunung Malela	Kab.	Simalungun	Sumatera Utara	,\
    4471	:	21174	Margo Muliyo	Gunung Malela	Kab.	Simalungun	Sumatera Utara	,\
    4472	:	21174	Marihat Bukit	Gunung Malela	Kab.	Simalungun	Sumatera Utara	,\
    4473	:	21174	Nagori Malela	Gunung Malela	Kab.	Simalungun	Sumatera Utara	,\
    4474	:	21174	Pematang Asilum	Gunung Malela	Kab.	Simalungun	Sumatera Utara	,\
    4475	:	21174	Pematang Gajing	Gunung Malela	Kab.	Simalungun	Sumatera Utara	,\
    4476	:	21174	Pematang Syahkuda (Sah Kuda)	Gunung Malela	Kab.	Simalungun	Sumatera Utara	,\
    4477	:	21174	Senio	Gunung Malela	Kab.	Simalungun	Sumatera Utara	,\
    4478	:	21174	Serapuh	Gunung Malela	Kab.	Simalungun	Sumatera Utara	,\
    4479	:	21174	Silau Malela	Gunung Malela	Kab.	Simalungun	Sumatera Utara	,\
    4480	:	21174	Silulu	Gunung Malela	Kab.	Simalungun	Sumatera Utara	,\
    4481	:	21174	Syahkuda Bayu (Sah Kuda Bayu)	Gunung Malela	Kab.	Simalungun	Sumatera Utara	,\
    4482	:	22873	Awoni	Gomo	Kab.	Nias Selatan	Sumatera Utara	,\
    4483	:	22873	Balombaruzo Orahua	Gomo	Kab.	Nias Selatan	Sumatera Utara	,\
    4484	:	22873	Buhawa	Gomo	Kab.	Nias Selatan	Sumatera Utara	,\
    4485	:	22873	Damai	Gomo	Kab.	Nias Selatan	Sumatera Utara	,\
    4486	:	22873	Dao-dao Zanuwo Idano Tae	Gomo	Kab.	Nias Selatan	Sumatera Utara	,\
    4487	:	22873	Doli-Doli Idano Tae	Gomo	Kab.	Nias Selatan	Sumatera Utara	,\
    4488	:	22873	Fanedanu Sibohou	Gomo	Kab.	Nias Selatan	Sumatera Utara	,\
    4489	:	22873	Fonedanu	Gomo	Kab.	Nias Selatan	Sumatera Utara	,\
    4490	:	22873	Gununggabungan	Gomo	Kab.	Nias Selatan	Sumatera Utara	,\
    4491	:	22873	Harefa Orahua	Gomo	Kab.	Nias Selatan	Sumatera Utara	,\
    4492	:	22873	Hilialo`oa	Gomo	Kab.	Nias Selatan	Sumatera Utara	,\
    4493	:	22873	Hilianaa Gomo	Gomo	Kab.	Nias Selatan	Sumatera Utara	,\
    4494	:	22873	Hiligabungan	Gomo	Kab.	Nias Selatan	Sumatera Utara	,\
    4495	:	22873	Hilimbowo Idano Tae	Gomo	Kab.	Nias Selatan	Sumatera Utara	,\
    4496	:	22873	Hilisalo`o	Gomo	Kab.	Nias Selatan	Sumatera Utara	,\
    4497	:	22873	Hiliserangkai	Gomo	Kab.	Nias Selatan	Sumatera Utara	,\
    4498	:	22873	Lahusa Idano Tae	Gomo	Kab.	Nias Selatan	Sumatera Utara	,\
    4499	:	22873	Lawa-Lawaluo Gomo	Gomo	Kab.	Nias Selatan	Sumatera Utara	,\
    4500	:	22873	Lawa-Lawaluo Idano Tae	Gomo	Kab.	Nias Selatan	Sumatera Utara	,\
    4501	:	22873	Lolosoni	Gomo	Kab.	Nias Selatan	Sumatera Utara	,\
    4502	:	22873	Orahili Gomo	Gomo	Kab.	Nias Selatan	Sumatera Utara	,\
    4503	:	22873	Orahili Sibohou	Gomo	Kab.	Nias Selatan	Sumatera Utara	,\
    4504	:	22873	Orahua	Gomo	Kab.	Nias Selatan	Sumatera Utara	,\
    4505	:	22873	Sifaoroasi Gomo	Gomo	Kab.	Nias Selatan	Sumatera Utara	,\
    4506	:	22873	Sirahia	Gomo	Kab.	Nias Selatan	Sumatera Utara	,\
    4507	:	22873	Sisarahili Ewo	Gomo	Kab.	Nias Selatan	Sumatera Utara	,\
    4508	:	22873	Sisiwa Ewali	Gomo	Kab.	Nias Selatan	Sumatera Utara	,\
    4509	:	22873	Suka Maju Mohili	Gomo	Kab.	Nias Selatan	Sumatera Utara	,\
    4510	:	22873	Tanoniko`o	Gomo	Kab.	Nias Selatan	Sumatera Utara	,\
    4511	:	22873	Umbu Idano Tae	Gomo	Kab.	Nias Selatan	Sumatera Utara	,\
    4512	:	22873	Umbu Orahua	Gomo	Kab.	Nias Selatan	Sumatera Utara	,\
    4513	:	21174	Girsang	Girsang Sipangan Bolon	Kab.	Simalungun	Sumatera Utara	,\
    4514	:	21174	Parapat	Girsang Sipangan Bolon	Kab.	Simalungun	Sumatera Utara	,\
    4515	:	21174	Sibaganding	Girsang Sipangan Bolon	Kab.	Simalungun	Sumatera Utara	,\
    4516	:	21174	Sipangan Bolon	Girsang Sipangan Bolon	Kab.	Simalungun	Sumatera Utara	,\
    4517	:	21174	Tiga Raja	Girsang Sipangan Bolon	Kab.	Simalungun	Sumatera Utara	,\
    4518	:	22871	Akhelaume	Gido	Kab.	Nias	Sumatera Utara	,\
    4519	:	22871	Hiliotalua	Gido	Kab.	Nias	Sumatera Utara	,\
    4520	:	22871	Hilisebua	Gido	Kab.	Nias	Sumatera Utara	,\
    4521	:	22871	Hiliweto Gido	Gido	Kab.	Nias	Sumatera Utara	,\
    4522	:	22871	Hilizoi	Gido	Kab.	Nias	Sumatera Utara	,\
    4523	:	22871	Ladea	Gido	Kab.	Nias	Sumatera Utara	,\
    4524	:	22871	Ladea Orahua	Gido	Kab.	Nias	Sumatera Utara	,\
    4525	:	22871	Lahemo	Gido	Kab.	Nias	Sumatera Utara	,\
    4526	:	22871	Lasara Idanoi	Gido	Kab.	Nias	Sumatera Utara	,\
    4527	:	22871	Lasela	Gido	Kab.	Nias	Sumatera Utara	,\
    4528	:	22871	Loloanaa Gido	Gido	Kab.	Nias	Sumatera Utara	,\
    4529	:	22871	Lolozasai	Gido	Kab.	Nias	Sumatera Utara	,\
    4530	:	22871	Nifolo`o Lauru	Gido	Kab.	Nias	Sumatera Utara	,\
    4531	:	22871	Olindrawa Sisarahili	Gido	Kab.	Nias	Sumatera Utara	,\
    4532	:	22871	Sirete	Gido	Kab.	Nias	Sumatera Utara	,\
    4533	:	22871	Sisobahili	Gido	Kab.	Nias	Sumatera Utara	,\
    4534	:	22871	Soewe (Saewe)	Gido	Kab.	Nias	Sumatera Utara	,\
    4535	:	22871	Somi	Gido	Kab.	Nias	Sumatera Utara	,\
    4536	:	22871	Somi Botogo`o	Gido	Kab.	Nias	Sumatera Utara	,\
    4537	:	22871	Tulumbaho Salo`o	Gido	Kab.	Nias	Sumatera Utara	,\
    4538	:	22871	Umbu	Gido	Kab.	Nias	Sumatera Utara	,\
    4539	:	20856	Air Hitam	Gebang	Kab.	Langkat	Sumatera Utara	,\
    4540	:	20856	Bukit Mengkirai	Gebang	Kab.	Langkat	Sumatera Utara	,\
    4541	:	20856	Dogang	Gebang	Kab.	Langkat	Sumatera Utara	,\
    4542	:	20856	Kwala Gebang	Gebang	Kab.	Langkat	Sumatera Utara	,\
    4543	:	20856	Padang Langkat	Gebang	Kab.	Langkat	Sumatera Utara	,\
    4544	:	20856	Paluh Manis	Gebang	Kab.	Langkat	Sumatera Utara	,\
    4545	:	20856	Pasar Rawa	Gebang	Kab.	Langkat	Sumatera Utara	,\
    4546	:	20856	Pasiran	Gebang	Kab.	Langkat	Sumatera Utara	,\
    4547	:	20856	Paya Bengkuang	Gebang	Kab.	Langkat	Sumatera Utara	,\
    4548	:	20856	Pekan Gebang	Gebang	Kab.	Langkat	Sumatera Utara	,\
    4549	:	20856	Sangga Lima (Perkebunan Serap)	Gebang	Kab.	Langkat	Sumatera Utara	,\
    4550	:	22473	Aek Tangga	Garoga	Kab.	Tapanuli Utara	Sumatera Utara	,\
    4551	:	22473	Garoga Sibargot	Garoga	Kab.	Tapanuli Utara	Sumatera Utara	,\
    4552	:	22473	Gonting Garoga	Garoga	Kab.	Tapanuli Utara	Sumatera Utara	,\
    4553	:	22473	Gonting Salak	Garoga	Kab.	Tapanuli Utara	Sumatera Utara	,\
    4554	:	22473	Lontung Jae I	Garoga	Kab.	Tapanuli Utara	Sumatera Utara	,\
    4555	:	22473	Lontung Jae II	Garoga	Kab.	Tapanuli Utara	Sumatera Utara	,\
    4556	:	22473	Padang Siandomang	Garoga	Kab.	Tapanuli Utara	Sumatera Utara	,\
    4557	:	22473	Parinsoran Pangorian	Garoga	Kab.	Tapanuli Utara	Sumatera Utara	,\
    4558	:	22473	Parsosoran	Garoga	Kab.	Tapanuli Utara	Sumatera Utara	,\
    4559	:	22473	Sibaganding	Garoga	Kab.	Tapanuli Utara	Sumatera Utara	,\
    4560	:	22473	Sibalanga	Garoga	Kab.	Tapanuli Utara	Sumatera Utara	,\
    4561	:	22473	Simpang Bolon	Garoga	Kab.	Tapanuli Utara	Sumatera Utara	,\
    4562	:	20585	Bandar Kuala	Galang	Kab.	Deli Serdang	Sumatera Utara	,\
    4563	:	20585	Baru Titi Besi	Galang	Kab.	Deli Serdang	Sumatera Utara	,\
    4564	:	20585	Batu Lokong	Galang	Kab.	Deli Serdang	Sumatera Utara	,\
    4565	:	20585	Galang Barat	Galang	Kab.	Deli Serdang	Sumatera Utara	,\
    4566	:	20585	Galang Kota	Galang	Kab.	Deli Serdang	Sumatera Utara	,\
    4567	:	20585	Galang Suka	Galang	Kab.	Deli Serdang	Sumatera Utara	,\
    4568	:	20585	Jaharum A	Galang	Kab.	Deli Serdang	Sumatera Utara	,\
    4569	:	20585	Jaharum B	Galang	Kab.	Deli Serdang	Sumatera Utara	,\
    4570	:	20585	Juhar Baru	Galang	Kab.	Deli Serdang	Sumatera Utara	,\
    4571	:	20585	Kelapa Satu	Galang	Kab.	Deli Serdang	Sumatera Utara	,\
    4572	:	20585	Keramat Gajah	Galang	Kab.	Deli Serdang	Sumatera Utara	,\
    4573	:	20585	Kotangan	Galang	Kab.	Deli Serdang	Sumatera Utara	,\
    4574	:	20585	Kotasan	Galang	Kab.	Deli Serdang	Sumatera Utara	,\
    4575	:	20585	Nogorejo	Galang	Kab.	Deli Serdang	Sumatera Utara	,\
    4576	:	20585	Paku	Galang	Kab.	Deli Serdang	Sumatera Utara	,\
    4577	:	20585	Paya Itik	Galang	Kab.	Deli Serdang	Sumatera Utara	,\
    4578	:	20585	Paya Kuda	Galang	Kab.	Deli Serdang	Sumatera Utara	,\
    4579	:	20585	Paya Sampir	Galang	Kab.	Deli Serdang	Sumatera Utara	,\
    4580	:	20585	Petangguhan	Galang	Kab.	Deli Serdang	Sumatera Utara	,\
    4581	:	20585	Petumbukan	Galang	Kab.	Deli Serdang	Sumatera Utara	,\
    4582	:	20585	Pisang Pala	Galang	Kab.	Deli Serdang	Sumatera Utara	,\
    4583	:	20585	Pulau Tagor Batu	Galang	Kab.	Deli Serdang	Sumatera Utara	,\
    4584	:	20585	Sei Karang	Galang	Kab.	Deli Serdang	Sumatera Utara	,\
    4585	:	20585	Sei Putih	Galang	Kab.	Deli Serdang	Sumatera Utara	,\
    4586	:	20585	Tanah Abang	Galang	Kab.	Deli Serdang	Sumatera Utara	,\
    4587	:	20585	Tanah Merah	Galang	Kab.	Deli Serdang	Sumatera Utara	,\
    4588	:	20585	Tanjung Gusti	Galang	Kab.	Deli Serdang	Sumatera Utara	,\
    4589	:	20585	Tanjung Siporkis	Galang	Kab.	Deli Serdang	Sumatera Utara	,\
    4590	:	20585	Timbang Deli	Galang	Kab.	Deli Serdang	Sumatera Utara	,\
    4591	:	22865	Bawofanayama	Fanayama	Kab.	Nias Selatan	Sumatera Utara	,\
    4592	:	22865	Bawomataluo	Fanayama	Kab.	Nias Selatan	Sumatera Utara	,\
    4593	:	22865	Bawonahono	Fanayama	Kab.	Nias Selatan	Sumatera Utara	,\
    4594	:	22865	Botohili Silambo	Fanayama	Kab.	Nias Selatan	Sumatera Utara	,\
    4595	:	22865	Botohili Sorake	Fanayama	Kab.	Nias Selatan	Sumatera Utara	,\
    4596	:	22865	Botohilisalo`o	Fanayama	Kab.	Nias Selatan	Sumatera Utara	,\
    4597	:	22865	Botohilitano	Fanayama	Kab.	Nias Selatan	Sumatera Utara	,\
    4598	:	22865	Eho Orahili	Fanayama	Kab.	Nias Selatan	Sumatera Utara	,\
    4599	:	22865	Ete Batu	Fanayama	Kab.	Nias Selatan	Sumatera Utara	,\
    4600	:	22865	Hiliamaetaniha	Fanayama	Kab.	Nias Selatan	Sumatera Utara	,\
    4601	:	22865	Hilifarokha	Fanayama	Kab.	Nias Selatan	Sumatera Utara	,\
    4602	:	22865	Hiligito	Fanayama	Kab.	Nias Selatan	Sumatera Utara	,\
    4603	:	22865	Hilikara Maha	Fanayama	Kab.	Nias Selatan	Sumatera Utara	,\
    4604	:	22865	Hiliofonaluo	Fanayama	Kab.	Nias Selatan	Sumatera Utara	,\
    4605	:	22865	Hilisalawa	Fanayama	Kab.	Nias Selatan	Sumatera Utara	,\
    4606	:	22865	Hilizihono	Fanayama	Kab.	Nias Selatan	Sumatera Utara	,\
    4607	:	22865	Hinawalo Fau	Fanayama	Kab.	Nias Selatan	Sumatera Utara	,\
    4608	:	22865	Lagundri	Fanayama	Kab.	Nias Selatan	Sumatera Utara	,\
    4609	:	22865	Lahusa Fau	Fanayama	Kab.	Nias Selatan	Sumatera Utara	,\
    4610	:	22865	Ono Hondro	Fanayama	Kab.	Nias Selatan	Sumatera Utara	,\
    4611	:	22865	Orahili Faomasi	Fanayama	Kab.	Nias Selatan	Sumatera Utara	,\
    4612	:	22865	Orahili Fau	Fanayama	Kab.	Nias Selatan	Sumatera Utara	,\
    4613	:	22865	Siliwulawa	Fanayama	Kab.	Nias Selatan	Sumatera Utara	,\
    4614	:	22865	Siwalawa	Fanayama	Kab.	Nias Selatan	Sumatera Utara	,\
    4615	:	22865	Sondregeasi	Fanayama	Kab.	Nias Selatan	Sumatera Utara	,\
    4616	:	21168	Bawang	Dolok Silau	Kab.	Simalungun	Sumatera Utara	,\
    4617	:	21168	Cingkes	Dolok Silau	Kab.	Simalungun	Sumatera Utara	,\
    4618	:	21168	Dolok Mariah	Dolok Silau	Kab.	Simalungun	Sumatera Utara	,\
    4619	:	21168	Huta Saing	Dolok Silau	Kab.	Simalungun	Sumatera Utara	,\
    4620	:	21168	Mariah Dolok	Dolok Silau	Kab.	Simalungun	Sumatera Utara	,\
    4621	:	21168	Marubun Lokkung	Dolok Silau	Kab.	Simalungun	Sumatera Utara	,\
    4622	:	21168	Paribuan	Dolok Silau	Kab.	Simalungun	Sumatera Utara	,\
    4623	:	21168	Perasmian	Dolok Silau	Kab.	Simalungun	Sumatera Utara	,\
    4624	:	21168	Saran Padang	Dolok Silau	Kab.	Simalungun	Sumatera Utara	,\
    4625	:	21168	Tagur	Dolok Silau	Kab.	Simalungun	Sumatera Utara	,\
    4626	:	22756	Aek Jabut	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4627	:	22756	Aek Kanan	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4628	:	22756	Aek Kundur	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4629	:	22756	Aek Simanat	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4630	:	22756	Batu Hibul	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4631	:	22756	Gadung Holbung	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4632	:	22756	Gonting Bange	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4633	:	22756	Gunung Sormin	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4634	:	22756	Hasahatan	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4635	:	22756	Hatiran	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4636	:	22756	Huta Imbaru Simundol	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4637	:	22756	Janjimanahan Gnt	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4638	:	22756	Karang anyer/Anyar	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4639	:	22756	Kuala Simpang	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4640	:	22756	Malino	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4641	:	22756	Nabundong	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4642	:	22756	Nahulu Jae	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4643	:	22756	Nahulu Julu	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4644	:	22756	Padang Malakka (Balakka)	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4645	:	22756	Padang Matinggi Gnt	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4646	:	22756	Padang Matinggi Simundol	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4647	:	22756	Pamarai (Paramai)	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4648	:	22756	Pamonoran	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4649	:	22756	Panyabungan	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4650	:	22756	Pasang Lela	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4651	:	22756	Pasar Sayur Matinggi	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4652	:	22756	Pasar Simundol	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4653	:	22756	Pinarik	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4654	:	22756	Pulo Liman (Limo)	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4655	:	22756	Saba Bangunan	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4656	:	22756	Salusuhan	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4657	:	22756	Sayur Matinggi	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4658	:	22756	Sigordang	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4659	:	22756	Sihalo-Halo/Sihatubang	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4660	:	22756	Simadihon	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4661	:	22756	Simangambat	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4662	:	22756	Simaninggir Simundol	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4663	:	22756	Simundol	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4664	:	22756	Sipogas A	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4665	:	22756	Sipogas B	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4666	:	22756	Sitonun	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4667	:	22756	Sunut	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4668	:	22756	Tanjung Baru Silaiya	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4669	:	22756	Unte Manis	Dolok Sigompulon	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4670	:	22457	Aek Lung	Dolok Sanggul	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    4671	:	22457	Bonani Onan	Dolok Sanggul	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    4672	:	22457	Dolok Sanggul (Pasar Dolok Sanggul)	Dolok Sanggul	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    4673	:	22457	Huta Gurgur	Dolok Sanggul	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    4674	:	22457	Hutabagasan	Dolok Sanggul	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    4675	:	22457	Hutaraja	Dolok Sanggul	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    4676	:	22457	Janji	Dolok Sanggul	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    4677	:	22457	Lumban Purba	Dolok Sanggul	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    4678	:	22457	Lumban Tobing	Dolok Sanggul	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    4679	:	22457	Matiti I	Dolok Sanggul	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    4680	:	22457	Matiti II	Dolok Sanggul	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    4681	:	22457	Pakkat	Dolok Sanggul	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    4682	:	22457	Parik Sinomba	Dolok Sanggul	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    4683	:	22457	Pasaribu	Dolok Sanggul	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    4684	:	22457	Purba Dolok	Dolok Sanggul	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    4685	:	22457	Purba Manalu	Dolok Sanggul	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    4686	:	22457	Saitnihuta	Dolok Sanggul	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    4687	:	22457	Sampean	Dolok Sanggul	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    4688	:	22457	Sigala Gala (Silaga Laga)	Dolok Sanggul	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    4689	:	22457	Sihite I	Dolok Sanggul	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    4690	:	22457	Sihite II	Dolok Sanggul	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    4691	:	22457	Sileang	Dolok Sanggul	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    4692	:	22457	Simangaronsang	Dolok Sanggul	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    4693	:	22457	Simarigung	Dolok Sanggul	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    4694	:	22457	Sirisirisi	Dolok Sanggul	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    4695	:	22457	Sosor Gonting	Dolok Sanggul	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    4696	:	22457	Sosor Tambok	Dolok Sanggul	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    4697	:	22457	Sosortolong Sihite III	Dolok Sanggul	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    4698	:	21163	Bangun Pane	Dolok Pardamean	Kab.	Simalungun	Sumatera Utara	,\
    4699	:	21163	Butu Bayu Panei Raja	Dolok Pardamean	Kab.	Simalungun	Sumatera Utara	,\
    4700	:	21163	Dolok Saribu	Dolok Pardamean	Kab.	Simalungun	Sumatera Utara	,\
    4701	:	21163	Parik Sabungan	Dolok Pardamean	Kab.	Simalungun	Sumatera Utara	,\
    4702	:	21163	Parjalangan	Dolok Pardamean	Kab.	Simalungun	Sumatera Utara	,\
    4703	:	21163	Sibuntuon	Dolok Pardamean	Kab.	Simalungun	Sumatera Utara	,\
    4704	:	21163	Silabah Jaya	Dolok Pardamean	Kab.	Simalungun	Sumatera Utara	,\
    4705	:	21163	Sinaman Labah	Dolok Pardamean	Kab.	Simalungun	Sumatera Utara	,\
    4706	:	21163	Sirube-rube Gunung Purba	Dolok Pardamean	Kab.	Simalungun	Sumatera Utara	,\
    4707	:	21163	Tigaras	Dolok Pardamean	Kab.	Simalungun	Sumatera Utara	,\
    4708	:	21163	Togu Domu Nauli	Dolok Pardamean	Kab.	Simalungun	Sumatera Utara	,\
    4709	:	21173	Bandar Dolok	Dolok Panribuan	Kab.	Simalungun	Sumatera Utara	,\
    4710	:	21173	Dolok Parmonangan	Dolok Panribuan	Kab.	Simalungun	Sumatera Utara	,\
    4711	:	21173	Dolok Tomuan	Dolok Panribuan	Kab.	Simalungun	Sumatera Utara	,\
    4712	:	21173	Gunung Mariah	Dolok Panribuan	Kab.	Simalungun	Sumatera Utara	,\
    4713	:	21173	Lumban Gorat	Dolok Panribuan	Kab.	Simalungun	Sumatera Utara	,\
    4714	:	21173	Marihat Dolok	Dolok Panribuan	Kab.	Simalungun	Sumatera Utara	,\
    4715	:	21173	Marihat Marsada	Dolok Panribuan	Kab.	Simalungun	Sumatera Utara	,\
    4716	:	21173	Marihat Pondok	Dolok Panribuan	Kab.	Simalungun	Sumatera Utara	,\
    4717	:	21173	Marihat Raja	Dolok Panribuan	Kab.	Simalungun	Sumatera Utara	,\
    4718	:	21173	Negeri Dolok	Dolok Panribuan	Kab.	Simalungun	Sumatera Utara	,\
    4719	:	21173	Pondok Buluh	Dolok Panribuan	Kab.	Simalungun	Sumatera Utara	,\
    4720	:	21173	Siatasan	Dolok Panribuan	Kab.	Simalungun	Sumatera Utara	,\
    4721	:	21173	Tiga Dolok	Dolok Panribuan	Kab.	Simalungun	Sumatera Utara	,\
    4722	:	21173	Ujung Bondar	Dolok Panribuan	Kab.	Simalungun	Sumatera Utara	,\
    4723	:	20993	Afdeling VI Dolok Ilir	Dolok Merawan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4724	:	20993	Afdeling VII Dolok Ilir	Dolok Merawan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4725	:	20993	Bah Damar	Dolok Merawan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4726	:	20993	Bandarawan	Dolok Merawan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4727	:	20993	Dolok Merawan	Dolok Merawan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4728	:	20993	Gunung Para II	Dolok Merawan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4729	:	20993	Kalembak	Dolok Merawan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4730	:	20993	Korajim	Dolok Merawan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4731	:	20993	Limbong	Dolok Merawan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4732	:	20993	Mainu Tengah/Tongah	Dolok Merawan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4733	:	20993	Nagaraja I	Dolok Merawan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4734	:	20993	Pabatu I	Dolok Merawan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4735	:	20993	Pabatu II	Dolok Merawan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4736	:	20993	Pabatu III	Dolok Merawan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4737	:	20993	Pabatu VI	Dolok Merawan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4738	:	20993	Panglong	Dolok Merawan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4739	:	20993	Paretokan (Paritokan)	Dolok Merawan	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4740	:	20991	Aras Panjang	Dolok Masihul	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4741	:	20991	Bah Kerapuh	Dolok Masihul	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4742	:	20991	Baja Ronggi	Dolok Masihul	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4743	:	20991	Bantan	Dolok Masihul	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4744	:	20991	Batu 12	Dolok Masihul	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4745	:	20991	Batu 13	Dolok Masihul	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4746	:	20991	Blok Sepuluh	Dolok Masihul	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4747	:	20991	Bukit Cermin Hilir	Dolok Masihul	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4748	:	20991	Dame	Dolok Masihul	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4749	:	20991	Dolok Manampang	Dolok Masihul	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4750	:	20991	Dolok Sagala	Dolok Masihul	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4751	:	20991	Durian Puloan	Dolok Masihul	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4752	:	20991	Havea	Dolok Masihul	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4753	:	20991	Huta Nauli	Dolok Masihul	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4754	:	20991	Kerapuh	Dolok Masihul	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4755	:	20991	Kota Tengah	Dolok Masihul	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4756	:	20991	Mala Sori	Dolok Masihul	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4757	:	20991	Martebing	Dolok Masihul	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4758	:	20991	Pardomuan	Dolok Masihul	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4759	:	20991	Pekan Dolok Masihul	Dolok Masihul	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4760	:	20991	Pekan Kemis	Dolok Masihul	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4761	:	20991	Pertambatan	Dolok Masihul	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4762	:	20991	Sarang Ginting	Dolok Masihul	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4763	:	20991	Sarang Torop	Dolok Masihul	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4764	:	20991	Silau Merawan	Dolok Masihul	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4765	:	20991	Tanjung Maria	Dolok Masihul	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4766	:	20991	Tegal Sari	Dolok Masihul	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4767	:	20991	Ujung Silau	Dolok Masihul	Kab.	Serdang Bedagai	Sumatera Utara	,\
    4768	:	21155	Bah Tobu	Dolok Batu Nanggar	Kab.	Simalungun	Sumatera Utara	,\
    4769	:	21155	Bahung Huluan	Dolok Batu Nanggar	Kab.	Simalungun	Sumatera Utara	,\
    4770	:	21155	Bahung Kahean	Dolok Batu Nanggar	Kab.	Simalungun	Sumatera Utara	,\
    4771	:	21155	Bandar Selamat	Dolok Batu Nanggar	Kab.	Simalungun	Sumatera Utara	,\
    4772	:	21155	Dolog Kataran (Hataran)	Dolok Batu Nanggar	Kab.	Simalungun	Sumatera Utara	,\
    4773	:	21155	Dolok Ilir Dua	Dolok Batu Nanggar	Kab.	Simalungun	Sumatera Utara	,\
    4774	:	21155	Dolok Ilir Satu	Dolok Batu Nanggar	Kab.	Simalungun	Sumatera Utara	,\
    4775	:	21155	Dolok Mainu	Dolok Batu Nanggar	Kab.	Simalungun	Sumatera Utara	,\
    4776	:	21155	Dolok Merangir Dua	Dolok Batu Nanggar	Kab.	Simalungun	Sumatera Utara	,\
    4777	:	21155	Dolok Merangir Satu	Dolok Batu Nanggar	Kab.	Simalungun	Sumatera Utara	,\
    4778	:	21155	Dolok Tenera	Dolok Batu Nanggar	Kab.	Simalungun	Sumatera Utara	,\
    4779	:	21155	Kahean	Dolok Batu Nanggar	Kab.	Simalungun	Sumatera Utara	,\
    4780	:	21155	Padang Mainu	Dolok Batu Nanggar	Kab.	Simalungun	Sumatera Utara	,\
    4781	:	21155	Serbelawan	Dolok Batu Nanggar	Kab.	Simalungun	Sumatera Utara	,\
    4782	:	21155	Silenduk	Dolok Batu Nanggar	Kab.	Simalungun	Sumatera Utara	,\
    4783	:	22756	Aek Haruaya	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4784	:	22756	Aek Ilung	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4785	:	22756	Aek Rao Tapian Nadenggan	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4786	:	22756	Aek Suhat Jae	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4787	:	22756	Aek Suhut Tr	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4788	:	22756	Aek Sundur	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4789	:	22756	Aek Tangga	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4790	:	22756	Arse	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4791	:	22756	Bahap	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4792	:	22756	Bandar Nauli	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4793	:	22756	Baringin Sil	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4794	:	22756	Baringin Sip	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4795	:	22756	Batu Runding	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4796	:	22756	Binanga Gumbot	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4797	:	22756	Bintais Julu	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4798	:	22756	Bukit Tinggi	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4799	:	22756	Bunut	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4800	:	22756	Dalihan Natolu	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4801	:	22756	Dolok Sanggul	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4802	:	22756	Gumaruntar	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4803	:	22756	Gumbot	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4804	:	22756	Gunung Maria	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4805	:	22756	Gunung Salamat	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4806	:	22756	Huta Baru Sil	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4807	:	22756	Huta Baru Sip	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4808	:	22756	Huta Imbaru Gil	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4809	:	22756	Jambur Batu	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4810	:	22756	Janji Manahan Gul	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4811	:	22756	Janji Manahan Sil	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4812	:	22756	Janji Matogu	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4813	:	22756	Kuala Baringin	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4814	:	22756	Lubuk Godang	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4815	:	22756	Lubuk Kundur	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4816	:	22756	Lubuk Lanjang	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4817	:	22756	Mompang Dolok	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4818	:	22756	Mompang Lombang	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4819	:	22756	Nabonggal	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4820	:	22756	Naga Saribu	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4821	:	22756	Napa Sundali	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4822	:	22756	Pagaran Julu I	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4823	:	22756	Pagaran Julu II	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4824	:	22756	Pagaran Siregar	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4825	:	22756	Panca	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4826	:	22756	Pancaran (Rancaran)	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4827	:	22756	Parigi	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4828	:	22756	Parmeraan/Parmeran	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4829	:	22756	Pasar Sipiongot	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4830	:	22756	Paya Ombik	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4831	:	22756	Pijor Koling	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4832	:	22756	Pintu Padang Merdeka	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4833	:	22756	Purbatua (Purbaba Tua)	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4834	:	22756	Rongkare	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4835	:	22756	Sialan Gundi	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4836	:	22756	Sialang Dolok	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4837	:	22756	Sibanga Panahasahan (Binanga Panosahan)	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4838	:	22756	Sibayo	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4839	:	22756	Sibayo Jae	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4840	:	22756	Sibio-Bio	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4841	:	22756	Sibur Bur	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4842	:	22756	Sigala Gala	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4843	:	22756	Sigambal (Simambal)	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4844	:	22756	Siganyal (Singanyal)	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4845	:	22756	Sigugah	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4846	:	22756	Sijantung Jae	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4847	:	22756	Sijantung Julu	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4848	:	22756	Sijara-Jara	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4849	:	22756	Sijorang	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4850	:	22756	Silangge	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4851	:	22756	Silogo-Logo	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4852	:	22756	Siloung	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4853	:	22756	Simangambat Tua	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4854	:	22756	Simaninggir Sip	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4855	:	22756	Simanosor	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4856	:	22756	Simataniari	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4857	:	22756	Simataniari Jae	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4858	:	22756	Simatorkis	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4859	:	22756	Sinabongan	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4860	:	22756	Sipiongot	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4861	:	22756	Siraga Huta Padang	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4862	:	22756	Siranap	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4863	:	22756	Situmbaga	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4864	:	22756	Sungai Datar	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4865	:	22756	Sungai Pining	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4866	:	22756	Tanjung Baru B	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4867	:	22756	Tanjung Longat	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4868	:	22756	Tarutung Bolak	Dolok	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    4869	:	22171	Bukit	Dolat Rayat	Kab.	Karo	Sumatera Utara	,\
    4870	:	22171	Dolat Rayat	Dolat Rayat	Kab.	Karo	Sumatera Utara	,\
    4871	:	22171	Kubucolia	Dolat Rayat	Kab.	Karo	Sumatera Utara	,\
    4872	:	22171	Melas	Dolat Rayat	Kab.	Karo	Sumatera Utara	,\
    4873	:	22171	Sampun	Dolat Rayat	Kab.	Karo	Sumatera Utara	,\
    4874	:	22171	Sugihen	Dolat Rayat	Kab.	Karo	Sumatera Utara	,\
    4875	:	22171	Ujung Sampun	Dolat Rayat	Kab.	Karo	Sumatera Utara	,\
    4876	:	20355	Deli Tua	Deli Tua	Kab.	Deli Serdang	Sumatera Utara	,\
    4877	:	20355	Deli Tua Barat	Deli Tua	Kab.	Deli Serdang	Sumatera Utara	,\
    4878	:	20355	Deli Tua Timur	Deli Tua	Kab.	Deli Serdang	Sumatera Utara	,\
    4879	:	20355	Kedai Durian	Deli Tua	Kab.	Deli Serdang	Sumatera Utara	,\
    4880	:	20355	Mekar Sari	Deli Tua	Kab.	Deli Serdang	Sumatera Utara	,\
    4881	:	20355	Suka Makmur	Deli Tua	Kab.	Deli Serdang	Sumatera Utara	,\
    4882	:	21367	Bunga Tanjung	Datuk Bandar Timur	Kota	Tanjung Balai	Sumatera Utara	,\
    4883	:	21366	Pulau Simardan	Datuk Bandar Timur	Kota	Tanjung Balai	Sumatera Utara	,\
    4884	:	21364	Selat Lancang	Datuk Bandar Timur	Kota	Tanjung Balai	Sumatera Utara	,\
    4885	:	21364	Selat Tanjung Medan	Datuk Bandar Timur	Kota	Tanjung Balai	Sumatera Utara	,\
    4886	:	21365	Semula Jadi	Datuk Bandar Timur	Kota	Tanjung Balai	Sumatera Utara	,\
    4887	:	21362	Gading	Datuk Bandar	Kota	Tanjung Balai	Sumatera Utara	,\
    4888	:	21369	Pahang	Datuk Bandar	Kota	Tanjung Balai	Sumatera Utara	,\
    4889	:	21368	Pantai Johor	Datuk Bandar	Kota	Tanjung Balai	Sumatera Utara	,\
    4890	:	21361	Sijambi	Datuk Bandar	Kota	Tanjung Balai	Sumatera Utara	,\
    4891	:	21368	Sirantau	Datuk Bandar	Kota	Tanjung Balai	Sumatera Utara	,\
    4892	:	21261	Ambalutu	Buntu Pane	Kab.	Asahan	Sumatera Utara	,\
    4893	:	21261	Buntu Pane	Buntu Pane	Kab.	Asahan	Sumatera Utara	,\
    4894	:	21261	Karya Ambalutu	Buntu Pane	Kab.	Asahan	Sumatera Utara	,\
    4895	:	21261	Lestari	Buntu Pane	Kab.	Asahan	Sumatera Utara	,\
    4896	:	21261	Mekar Sari	Buntu Pane	Kab.	Asahan	Sumatera Utara	,\
    4897	:	21261	Perkebunan Sei Silau	Buntu Pane	Kab.	Asahan	Sumatera Utara	,\
    4898	:	21261	Prapat Janji	Buntu Pane	Kab.	Asahan	Sumatera Utara	,\
    4899	:	21261	Sei Silau Timur	Buntu Pane	Kab.	Asahan	Sumatera Utara	,\
    4900	:	21261	Sionggang	Buntu Pane	Kab.	Asahan	Sumatera Utara	,\
    4901	:	22977	Bange	Bukit Malintang	Kab.	Mandailing Natal	Sumatera Utara	,\
    4902	:	22977	Bange Nauli	Bukit Malintang	Kab.	Mandailing Natal	Sumatera Utara	,\
    4903	:	22977	Huta Bangun	Bukit Malintang	Kab.	Mandailing Natal	Sumatera Utara	,\
    4904	:	22977	Huta Bangun Jae	Bukit Malintang	Kab.	Mandailing Natal	Sumatera Utara	,\
    4905	:	22977	Janji Matogu	Bukit Malintang	Kab.	Mandailing Natal	Sumatera Utara	,\
    4906	:	22977	Lambou Darul Ihsan	Bukit Malintang	Kab.	Mandailing Natal	Sumatera Utara	,\
    4907	:	22977	Malintang Jae	Bukit Malintang	Kab.	Mandailing Natal	Sumatera Utara	,\
    4908	:	22977	Malintang Julu	Bukit Malintang	Kab.	Mandailing Natal	Sumatera Utara	,\
    4909	:	22977	Pasar Baru Malintang	Bukit Malintang	Kab.	Mandailing Natal	Sumatera Utara	,\
    4910	:	22977	Sidojadi	Bukit Malintang	Kab.	Mandailing Natal	Sumatera Utara	,\
    4911	:	22152	Doulu (Daulu)	Brastagi (Berastagi)	Kab.	Karo	Sumatera Utara	,\
    4912	:	22152	Gundaling I	Brastagi (Berastagi)	Kab.	Karo	Sumatera Utara	,\
    4913	:	22152	Gundaling II	Brastagi (Berastagi)	Kab.	Karo	Sumatera Utara	,\
    4914	:	22152	Gurusinga	Brastagi (Berastagi)	Kab.	Karo	Sumatera Utara	,\
    4915	:	22152	Lau Gumba	Brastagi (Berastagi)	Kab.	Karo	Sumatera Utara	,\
    4916	:	22152	Raya	Brastagi (Berastagi)	Kab.	Karo	Sumatera Utara	,\
    4917	:	22152	Rumah Brastagi/Berastagi	Brastagi (Berastagi)	Kab.	Karo	Sumatera Utara	,\
    4918	:	22152	Sempajaya	Brastagi (Berastagi)	Kab.	Karo	Sumatera Utara	,\
    4919	:	22152	Tambak Lau Mulgap I	Brastagi (Berastagi)	Kab.	Karo	Sumatera Utara	,\
    4920	:	22152	Tambak Lau Mulgap II	Brastagi (Berastagi)	Kab.	Karo	Sumatera Utara	,\
    4921	:	20881	Kelantan	Brandan Barat	Kab.	Langkat	Sumatera Utara	,\
    4922	:	20881	Lubuk Kasih	Brandan Barat	Kab.	Langkat	Sumatera Utara	,\
    4923	:	20881	Lubuk Kertang	Brandan Barat	Kab.	Langkat	Sumatera Utara	,\
    4924	:	20881	Pangkalan Batu	Brandan Barat	Kab.	Langkat	Sumatera Utara	,\
    4925	:	20881	Perlis	Brandan Barat	Kab.	Langkat	Sumatera Utara	,\
    4926	:	20881	Sei/Sungai Tualang	Brandan Barat	Kab.	Langkat	Sumatera Utara	,\
    4927	:	20881	Tangkahan Durian	Brandan Barat	Kab.	Langkat	Sumatera Utara	,\
    4928	:	22815	Balohili Botomuzoi	Botomuzoi	Kab.	Nias	Sumatera Utara	,\
    4929	:	22815	Banua Sibohou Botomuzoi	Botomuzoi	Kab.	Nias	Sumatera Utara	,\
    4930	:	22815	Fulolo Botomuzoi	Botomuzoi	Kab.	Nias	Sumatera Utara	,\
    4931	:	22815	Hiliambowo Botomuzoi	Botomuzoi	Kab.	Nias	Sumatera Utara	,\
    4932	:	22815	Hiligodu Botomuzoi	Botomuzoi	Kab.	Nias	Sumatera Utara	,\
    4933	:	22815	Hilimbowo Botomuzoi	Botomuzoi	Kab.	Nias	Sumatera Utara	,\
    4934	:	22815	Hiliwaele I	Botomuzoi	Kab.	Nias	Sumatera Utara	,\
    4935	:	22815	Hiliwaele II	Botomuzoi	Kab.	Nias	Sumatera Utara	,\
    4936	:	22815	Lazara Botomuzoi	Botomuzoi	Kab.	Nias	Sumatera Utara	,\
    4937	:	22815	Lololana`a	Botomuzoi	Kab.	Nias	Sumatera Utara	,\
    4938	:	22815	Mohili Berua Botomuzoi	Botomuzoi	Kab.	Nias	Sumatera Utara	,\
    4939	:	22815	Ola Nori	Botomuzoi	Kab.	Nias	Sumatera Utara	,\
    4940	:	22815	Ononamolo Talafu	Botomuzoi	Kab.	Nias	Sumatera Utara	,\
    4941	:	22815	Simanaere Botomuzoi	Botomuzoi	Kab.	Nias	Sumatera Utara	,\
    4942	:	22815	Sisobahili Dola	Botomuzoi	Kab.	Nias	Sumatera Utara	,\
    4943	:	22815	Talafu	Botomuzoi	Kab.	Nias	Sumatera Utara	,\
    4944	:	22815	Tetehosi Botomuzoi	Botomuzoi	Kab.	Nias	Sumatera Utara	,\
    4945	:	22815	Tuhegafoa I	Botomuzoi	Kab.	Nias	Sumatera Utara	,\
    4946	:	21183	Adil Makmur	Bosar Maligas	Kab.	Simalungun	Sumatera Utara	,\
    4947	:	21183	Boluk	Bosar Maligas	Kab.	Simalungun	Sumatera Utara	,\
    4948	:	21183	Bosar Maligas	Bosar Maligas	Kab.	Simalungun	Sumatera Utara	,\
    4949	:	21183	Dusun Pengkolan	Bosar Maligas	Kab.	Simalungun	Sumatera Utara	,\
    4950	:	21183	Gunung Bayu	Bosar Maligas	Kab.	Simalungun	Sumatera Utara	,\
    4951	:	21183	Marihat Butar	Bosar Maligas	Kab.	Simalungun	Sumatera Utara	,\
    4952	:	21183	Marihat Tanjung	Bosar Maligas	Kab.	Simalungun	Sumatera Utara	,\
    4953	:	21183	Mayang	Bosar Maligas	Kab.	Simalungun	Sumatera Utara	,\
    4954	:	21183	Mekar Rejo	Bosar Maligas	Kab.	Simalungun	Sumatera Utara	,\
    4955	:	21183	Nanggar Bayu	Bosar Maligas	Kab.	Simalungun	Sumatera Utara	,\
    4956	:	21183	Parbutaran	Bosar Maligas	Kab.	Simalungun	Sumatera Utara	,\
    4957	:	21183	Sei Mangkei	Bosar Maligas	Kab.	Simalungun	Sumatera Utara	,\
    4958	:	21183	Sei Torop	Bosar Maligas	Kab.	Simalungun	Sumatera Utara	,\
    4959	:	21183	Sidomulyo	Bosar Maligas	Kab.	Simalungun	Sumatera Utara	,\
    4960	:	21183	Teladan	Bosar Maligas	Kab.	Simalungun	Sumatera Utara	,\
    4961	:	21183	Telun/Talun Saragih	Bosar Maligas	Kab.	Simalungun	Sumatera Utara	,\
    4962	:	21183	Tempel Jaya	Bosar Maligas	Kab.	Simalungun	Sumatera Utara	,\
    4963	:	22873	Balohili Gomo	Boronadu	Kab.	Nias Selatan	Sumatera Utara	,\
    4964	:	22873	Bohalu	Boronadu	Kab.	Nias Selatan	Sumatera Utara	,\
    4965	:	22873	Lewa-Lewa	Boronadu	Kab.	Nias Selatan	Sumatera Utara	,\
    4966	:	22873	Orsedes	Boronadu	Kab.	Nias Selatan	Sumatera Utara	,\
    4967	:	22873	Perjuangan	Boronadu	Kab.	Nias Selatan	Sumatera Utara	,\
    4968	:	22873	Sifalago Gomo	Boronadu	Kab.	Nias Selatan	Sumatera Utara	,\
    4969	:	22873	Siholi	Boronadu	Kab.	Nias Selatan	Sumatera Utara	,\
    4970	:	22873	Sinar Helaowo	Boronadu	Kab.	Nias Selatan	Sumatera Utara	,\
    4971	:	22873	Siraha (Sirahia)	Boronadu	Kab.	Nias Selatan	Sumatera Utara	,\
    4972	:	22873	Tuhegafoa	Boronadu	Kab.	Nias Selatan	Sumatera Utara	,\
    4973	:	22383	Aek Unsim	Bor-Bor	Kab.	Toba Samosir	Sumatera Utara	,\
    4974	:	22383	Hutagurgur	Bor-Bor	Kab.	Toba Samosir	Sumatera Utara	,\
    4975	:	22383	Janji Maria	Bor-Bor	Kab.	Toba Samosir	Sumatera Utara	,\
    4976	:	22383	Lintong	Bor-Bor	Kab.	Toba Samosir	Sumatera Utara	,\
    4977	:	22383	Lumban Sewa	Bor-Bor	Kab.	Toba Samosir	Sumatera Utara	,\
    4978	:	22383	Natu Mingka	Bor-Bor	Kab.	Toba Samosir	Sumatera Utara	,\
    4979	:	22383	Pangururan	Bor-Bor	Kab.	Toba Samosir	Sumatera Utara	,\
    4980	:	22383	Pangururan II	Bor-Bor	Kab.	Toba Samosir	Sumatera Utara	,\
    4981	:	22383	Pangururan III	Bor-Bor	Kab.	Toba Samosir	Sumatera Utara	,\
    4982	:	22383	Pardomuan Nauli	Bor-Bor	Kab.	Toba Samosir	Sumatera Utara	,\
    4983	:	22383	Pasar Borbor	Bor-Bor	Kab.	Toba Samosir	Sumatera Utara	,\
    4984	:	22383	Purba Tua	Bor-Bor	Kab.	Toba Samosir	Sumatera Utara	,\
    4985	:	22383	Rianiate	Bor-Bor	Kab.	Toba Samosir	Sumatera Utara	,\
    4986	:	22383	Riganjang	Bor-Bor	Kab.	Toba Samosir	Sumatera Utara	,\
    4987	:	22383	Simare	Bor-Bor	Kab.	Toba Samosir	Sumatera Utara	,\
    4988	:	22386	Harungguan	Bonatua Lunasi	Kab.	Toba Samosir	Sumatera Utara	,\
    4989	:	22386	Lumban Lobu	Bonatua Lunasi	Kab.	Toba Samosir	Sumatera Utara	,\
    4990	:	22386	Lumban Sangkalan	Bonatua Lunasi	Kab.	Toba Samosir	Sumatera Utara	,\
    4991	:	22386	Naga Timbul	Bonatua Lunasi	Kab.	Toba Samosir	Sumatera Utara	,\
    4992	:	22386	Nagatimbul Timur	Bonatua Lunasi	Kab.	Toba Samosir	Sumatera Utara	,\
    4993	:	22386	Pardolok Lumban Lobu	Bonatua Lunasi	Kab.	Toba Samosir	Sumatera Utara	,\
    4994	:	22386	Partoruan Lumban Lobu	Bonatua Lunasi	Kab.	Toba Samosir	Sumatera Utara	,\
    4995	:	22386	Sibadihon	Bonatua Lunasi	Kab.	Toba Samosir	Sumatera Utara	,\
    4996	:	22386	Sihiong	Bonatua Lunasi	Kab.	Toba Samosir	Sumatera Utara	,\
    4997	:	22386	Silamosik II	Bonatua Lunasi	Kab.	Toba Samosir	Sumatera Utara	,\
    4998	:	22386	Silombu	Bonatua Lunasi	Kab.	Toba Samosir	Sumatera Utara	,\
    4999	:	22386	Sinar Sabungan	Bonatua Lunasi	Kab.	Toba Samosir	Sumatera Utara	,\
    5000	:	20358	Aji Baho	Biru-Biru	Kab.	Deli Serdang	Sumatera Utara	,\
    5001	:	20358	Biru-Biru	Biru-Biru	Kab.	Deli Serdang	Sumatera Utara	,\
    5002	:	20358	Candi Rejo	Biru-Biru	Kab.	Deli Serdang	Sumatera Utara	,\
    5003	:	20358	Kuala Dekah	Biru-Biru	Kab.	Deli Serdang	Sumatera Utara	,\
    5004	:	20358	Kuta Mulyo	Biru-Biru	Kab.	Deli Serdang	Sumatera Utara	,\
    5005	:	20358	Madinding Julu	Biru-Biru	Kab.	Deli Serdang	Sumatera Utara	,\
    5006	:	20358	Mbaruae (Mbaruai)	Biru-Biru	Kab.	Deli Serdang	Sumatera Utara	,\
    5007	:	20358	Namo Suro Baru	Biru-Biru	Kab.	Deli Serdang	Sumatera Utara	,\
    5008	:	20358	Namo Tualang	Biru-Biru	Kab.	Deli Serdang	Sumatera Utara	,\
    5009	:	20358	Penen	Biru-Biru	Kab.	Deli Serdang	Sumatera Utara	,\
    5010	:	20358	Per Ria Ria	Biru-Biru	Kab.	Deli Serdang	Sumatera Utara	,\
    5011	:	20358	Rumah Gerat	Biru-Biru	Kab.	Deli Serdang	Sumatera Utara	,\
    5012	:	20358	Sari Laba Jahe	Biru-Biru	Kab.	Deli Serdang	Sumatera Utara	,\
    5013	:	20358	Selamat (Kampung Selamat)	Biru-Biru	Kab.	Deli Serdang	Sumatera Utara	,\
    5014	:	20358	Sidodadi	Biru-Biru	Kab.	Deli Serdang	Sumatera Utara	,\
    5015	:	20358	Sidomulyo	Biru-Biru	Kab.	Deli Serdang	Sumatera Utara	,\
    5016	:	20358	Tanjung Sena	Biru-Biru	Kab.	Deli Serdang	Sumatera Utara	,\
    5017	:	20984	Bandar Magondang (Nagodang)	Bintang Bayu	Kab.	Serdang Bedagai	Sumatera Utara	,\
    5018	:	20984	Bandar Negeri	Bintang Bayu	Kab.	Serdang Bedagai	Sumatera Utara	,\
    5019	:	20984	Bandar Pinang Kebun/Kebon	Bintang Bayu	Kab.	Serdang Bedagai	Sumatera Utara	,\
    5020	:	20984	Bandar Pinang Rambe	Bintang Bayu	Kab.	Serdang Bedagai	Sumatera Utara	,\
    5021	:	20984	Bintang Bayu	Bintang Bayu	Kab.	Serdang Bedagai	Sumatera Utara	,\
    5022	:	20984	Damak Tolong Buho	Bintang Bayu	Kab.	Serdang Bedagai	Sumatera Utara	,\
    5023	:	20984	Dolok Masango	Bintang Bayu	Kab.	Serdang Bedagai	Sumatera Utara	,\
    5024	:	20984	Gudang Garam	Bintang Bayu	Kab.	Serdang Bedagai	Sumatera Utara	,\
    5025	:	20984	Huta Durian	Bintang Bayu	Kab.	Serdang Bedagai	Sumatera Utara	,\
    5026	:	20984	Kampung Kristen	Bintang Bayu	Kab.	Serdang Bedagai	Sumatera Utara	,\
    5027	:	20984	Marihat Dolok	Bintang Bayu	Kab.	Serdang Bedagai	Sumatera Utara	,\
    5028	:	20984	Panombean	Bintang Bayu	Kab.	Serdang Bedagai	Sumatera Utara	,\
    5029	:	20984	Pergajahan/Pegajahan Hulu	Bintang Bayu	Kab.	Serdang Bedagai	Sumatera Utara	,\
    5030	:	20984	Pergajahan/Pegajahan Kahan	Bintang Bayu	Kab.	Serdang Bedagai	Sumatera Utara	,\
    5031	:	20984	Sarang Ginting Hulu	Bintang Bayu	Kab.	Serdang Bedagai	Sumatera Utara	,\
    5032	:	20984	Sarang Ginting Kahan	Bintang Bayu	Kab.	Serdang Bedagai	Sumatera Utara	,\
    5033	:	20984	Siahap	Bintang Bayu	Kab.	Serdang Bedagai	Sumatera Utara	,\
    5034	:	20984	Ujung Negeri Hulu	Bintang Bayu	Kab.	Serdang Bedagai	Sumatera Utara	,\
    5035	:	20984	Ujung Negeri Kahan	Bintang Bayu	Kab.	Serdang Bedagai	Sumatera Utara	,\
    5036	:	20747	Cengkeh Turi	Binjai Utara	Kota	Binjai	Sumatera Utara	,\
    5037	:	20745	Damai	Binjai Utara	Kota	Binjai	Sumatera Utara	,\
    5038	:	20746	Jati Karya	Binjai Utara	Kota	Binjai	Sumatera Utara	,\
    5039	:	20748	Jati Makmur	Binjai Utara	Kota	Binjai	Sumatera Utara	,\
    5040	:	20741	Jati Negara	Binjai Utara	Kota	Binjai	Sumatera Utara	,\
    5041	:	20749	Jati Utomo	Binjai Utara	Kota	Binjai	Sumatera Utara	,\
    5042	:	20744	Kebun Lada	Binjai Utara	Kota	Binjai	Sumatera Utara	,\
    5043	:	20742	Nangka	Binjai Utara	Kota	Binjai	Sumatera Utara	,\
    5044	:	20743	Pahlawan	Binjai Utara	Kota	Binjai	Sumatera Utara	,\
    5045	:	20736	Dataran Tinggi	Binjai Timur	Kota	Binjai	Sumatera Utara	,\
    5046	:	20733	Mencirim	Binjai Timur	Kota	Binjai	Sumatera Utara	,\
    5047	:	20737	Sumber Karya	Binjai Timur	Kota	Binjai	Sumatera Utara	,\
    5048	:	20735	Sumber Mulyo Rejo	Binjai Timur	Kota	Binjai	Sumatera Utara	,\
    5049	:	20731	Tanah Tinggi	Binjai Timur	Kota	Binjai	Sumatera Utara	,\
    5050	:	20732	Timbang Langkat	Binjai Timur	Kota	Binjai	Sumatera Utara	,\
    5051	:	20734	Tunggurono	Binjai Timur	Kota	Binjai	Sumatera Utara	,\
    5052	:	20728	Bhakti Karya	Binjai Selatan	Kota	Binjai	Sumatera Utara	,\
    5053	:	20724	Binjai Estate	Binjai Selatan	Kota	Binjai	Sumatera Utara	,\
    5054	:	20727	Pujidadi	Binjai Selatan	Kota	Binjai	Sumatera Utara	,\
    5055	:	20723	Rambung Barat	Binjai Selatan	Kota	Binjai	Sumatera Utara	,\
    5056	:	20722	Rambung Dalam	Binjai Selatan	Kota	Binjai	Sumatera Utara	,\
    5057	:	20721	Rambung Timur	Binjai Selatan	Kota	Binjai	Sumatera Utara	,\
    5058	:	20725	Tanah Merah	Binjai Selatan	Kota	Binjai	Sumatera Utara	,\
    5059	:	20726	Tanah Seribu	Binjai Selatan	Kota	Binjai	Sumatera Utara	,\
    5060	:	20715	Berngam	Binjai Kota	Kota	Binjai	Sumatera Utara	,\
    5061	:	20712	Binjai	Binjai Kota	Kota	Binjai	Sumatera Utara	,\
    5062	:	20713	Kartini	Binjai Kota	Kota	Binjai	Sumatera Utara	,\
    5063	:	20711	Pekan Binjai	Binjai Kota	Kota	Binjai	Sumatera Utara	,\
    5064	:	20714	Satria	Binjai Kota	Kota	Binjai	Sumatera Utara	,\
    5065	:	20713	Setia	Binjai Kota	Kota	Binjai	Sumatera Utara	,\
    5066	:	20714	Tangsi	Binjai Kota	Kota	Binjai	Sumatera Utara	,\
    5067	:	20719	Bandar Senembah	Binjai Barat	Kota	Binjai	Sumatera Utara	,\
    5068	:	20717	Limau Mungkur	Binjai Barat	Kota	Binjai	Sumatera Utara	,\
    5069	:	20716	Limau Sundai	Binjai Barat	Kota	Binjai	Sumatera Utara	,\
    5070	:	20718	Payaroba	Binjai Barat	Kota	Binjai	Sumatera Utara	,\
    5071	:	20719	Suka Maju	Binjai Barat	Kota	Binjai	Sumatera Utara	,\
    5072	:	20717	Sukaramai	Binjai Barat	Kota	Binjai	Sumatera Utara	,\
    5073	:	20761	Kwala Begumit	Binjai	Kab.	Langkat	Sumatera Utara	,\
    5074	:	20761	Perdamaina (Perdamean)	Binjai	Kab.	Langkat	Sumatera Utara	,\
    5075	:	20761	Sabi/Sambi Rejo	Binjai	Kab.	Langkat	Sumatera Utara	,\
    5076	:	20761	Sendang Rejo	Binjai	Kab.	Langkat	Sumatera Utara	,\
    5077	:	20761	Sido Mulyo	Binjai	Kab.	Langkat	Sumatera Utara	,\
    5078	:	20761	Suka Makmur	Binjai	Kab.	Langkat	Sumatera Utara	,\
    5079	:	20761	Tanjung Jati	Binjai	Kab.	Langkat	Sumatera Utara	,\
    5080	:	21451	Bandar Tinggi	Bilah Hulu	Kab.	Labuhan Batu	Sumatera Utara	,\
    5081	:	21451	Emplasmen Aek Nabara	Bilah Hulu	Kab.	Labuhan Batu	Sumatera Utara	,\
    5082	:	21451	Gunung Selamat	Bilah Hulu	Kab.	Labuhan Batu	Sumatera Utara	,\
    5083	:	21451	Kampung Dalam	Bilah Hulu	Kab.	Labuhan Batu	Sumatera Utara	,\
    5084	:	21451	Lingga Tiga	Bilah Hulu	Kab.	Labuhan Batu	Sumatera Utara	,\
    5085	:	21451	Meranti	Bilah Hulu	Kab.	Labuhan Batu	Sumatera Utara	,\
    5086	:	21451	N 1/Satu Aek Nabara	Bilah Hulu	Kab.	Labuhan Batu	Sumatera Utara	,\
    5087	:	21451	N 2/Dua Aek Nabara	Bilah Hulu	Kab.	Labuhan Batu	Sumatera Utara	,\
    5088	:	21451	N 3/Tiga Aek Nabara	Bilah Hulu	Kab.	Labuhan Batu	Sumatera Utara	,\
    5089	:	21451	N 4/Empat Aek Nabara	Bilah Hulu	Kab.	Labuhan Batu	Sumatera Utara	,\
    5090	:	21451	N 5/Lima Aek Nabara	Bilah Hulu	Kab.	Labuhan Batu	Sumatera Utara	,\
    5091	:	21451	N 6/Enam Aek Nabara	Bilah Hulu	Kab.	Labuhan Batu	Sumatera Utara	,\
    5092	:	21451	N 7/Tujuh Aek Nabara	Bilah Hulu	Kab.	Labuhan Batu	Sumatera Utara	,\
    5093	:	21451	N 8/Delapan Aek Nabara	Bilah Hulu	Kab.	Labuhan Batu	Sumatera Utara	,\
    5094	:	21451	Pematang Slang (Seleng)	Bilah Hulu	Kab.	Labuhan Batu	Sumatera Utara	,\
    5095	:	21451	Perbaungan	Bilah Hulu	Kab.	Labuhan Batu	Sumatera Utara	,\
    5096	:	21451	Pondok Batu	Bilah Hulu	Kab.	Labuhan Batu	Sumatera Utara	,\
    5097	:	21451	S 1/Satu Aek Nabara	Bilah Hulu	Kab.	Labuhan Batu	Sumatera Utara	,\
    5098	:	21451	S 2/Dua Aek Nabara	Bilah Hulu	Kab.	Labuhan Batu	Sumatera Utara	,\
    5099	:	21451	S 3/Tiga Aek Nabara	Bilah Hulu	Kab.	Labuhan Batu	Sumatera Utara	,\
    5100	:	21451	S 4/Empat Aek Nabara	Bilah Hulu	Kab.	Labuhan Batu	Sumatera Utara	,\
    5101	:	21451	S 5/Lima Aek Nabara	Bilah Hulu	Kab.	Labuhan Batu	Sumatera Utara	,\
    5102	:	21451	S 6/Enam Aek Nabara	Bilah Hulu	Kab.	Labuhan Batu	Sumatera Utara	,\
    5103	:	21451	Tanjung Tiram (Siram)	Bilah Hulu	Kab.	Labuhan Batu	Sumatera Utara	,\
    5104	:	21471	Kampung Bilah	Bilah Hilir	Kab.	Labuhan Batu	Sumatera Utara	,\
    5105	:	21471	Negeri Baru	Bilah Hilir	Kab.	Labuhan Batu	Sumatera Utara	,\
    5106	:	21471	Negeri Lama	Bilah Hilir	Kab.	Labuhan Batu	Sumatera Utara	,\
    5107	:	21471	Negeri Lama Seberang	Bilah Hilir	Kab.	Labuhan Batu	Sumatera Utara	,\
    5108	:	21471	Perkebunan Bilah	Bilah Hilir	Kab.	Labuhan Batu	Sumatera Utara	,\
    5109	:	21471	Perkebunan Negeri Lama	Bilah Hilir	Kab.	Labuhan Batu	Sumatera Utara	,\
    5110	:	21471	Perkebunan Sennah	Bilah Hilir	Kab.	Labuhan Batu	Sumatera Utara	,\
    5111	:	21471	Sei Kasih	Bilah Hilir	Kab.	Labuhan Batu	Sumatera Utara	,\
    5112	:	21471	Sei Tampang	Bilah Hilir	Kab.	Labuhan Batu	Sumatera Utara	,\
    5113	:	21471	Sei Tarolat	Bilah Hilir	Kab.	Labuhan Batu	Sumatera Utara	,\
    5114	:	21471	Selat Besar	Bilah Hilir	Kab.	Labuhan Batu	Sumatera Utara	,\
    5115	:	21471	Sidomulyo	Bilah Hilir	Kab.	Labuhan Batu	Sumatera Utara	,\
    5116	:	21471	Tanjung Haloban	Bilah Hilir	Kab.	Labuhan Batu	Sumatera Utara	,\
    5117	:	21411	Bandar Kumbul	Bilah Barat	Kab.	Labuhan Batu	Sumatera Utara	,\
    5118	:	21411	Janji	Bilah Barat	Kab.	Labuhan Batu	Sumatera Utara	,\
    5119	:	21415	Kampung Baru	Bilah Barat	Kab.	Labuhan Batu	Sumatera Utara	,\
    5120	:	21411	Perkebunan Aek Buru Selatan	Bilah Barat	Kab.	Labuhan Batu	Sumatera Utara	,\
    5121	:	21411	Perkebunan Afdeling I Rantau Prapat	Bilah Barat	Kab.	Labuhan Batu	Sumatera Utara	,\
    5122	:	21411	Perkebunan Afdeling II Rantau Prapat	Bilah Barat	Kab.	Labuhan Batu	Sumatera Utara	,\
    5123	:	21411	Sibargot	Bilah Barat	Kab.	Labuhan Batu	Sumatera Utara	,\
    5124	:	21411	Tanjung Medan	Bilah Barat	Kab.	Labuhan Batu	Sumatera Utara	,\
    5125	:	21411	Tebing Linggahara	Bilah Barat	Kab.	Labuhan Batu	Sumatera Utara	,\
    5126	:	21411	Tebing Linggahara Baru	Bilah Barat	Kab.	Labuhan Batu	Sumatera Utara	,\
    5127	:	20859	Bukit Kubu	Besitang	Kab.	Langkat	Sumatera Utara	,\
    5128	:	20859	Bukit Mas	Besitang	Kab.	Langkat	Sumatera Utara	,\
    5129	:	20859	Bukit Selamat	Besitang	Kab.	Langkat	Sumatera Utara	,\
    5130	:	20859	Halaban	Besitang	Kab.	Langkat	Sumatera Utara	,\
    5131	:	20859	Kampung Lama	Besitang	Kab.	Langkat	Sumatera Utara	,\
    5132	:	20859	Pekan Besitang	Besitang	Kab.	Langkat	Sumatera Utara	,\
    5133	:	20859	Pir Adb Besitang	Besitang	Kab.	Langkat	Sumatera Utara	,\
    5134	:	20859	Sekoci	Besitang	Kab.	Langkat	Sumatera Utara	,\
    5135	:	20859	Suka Jaya	Besitang	Kab.	Langkat	Sumatera Utara	,\
    5136	:	20552	Aras Kabu	Beringin	Kab.	Deli Serdang	Sumatera Utara	,\
    5137	:	20552	Beringin	Beringin	Kab.	Deli Serdang	Sumatera Utara	,\
    5138	:	20552	Emplasmen Kuala Namu	Beringin	Kab.	Deli Serdang	Sumatera Utara	,\
    5139	:	20552	Karang Anyar	Beringin	Kab.	Deli Serdang	Sumatera Utara	,\
    5140	:	20552	Pasar Enam Kuala Namu	Beringin	Kab.	Deli Serdang	Sumatera Utara	,\
    5141	:	20552	Pasar Lima Kebun Kelapa	Beringin	Kab.	Deli Serdang	Sumatera Utara	,\
    5142	:	20552	Serdang	Beringin	Kab.	Deli Serdang	Sumatera Utara	,\
    5143	:	20552	Sidoarjo Dua Ramunia	Beringin	Kab.	Deli Serdang	Sumatera Utara	,\
    5144	:	20552	Sidodadi Ramonia (Ramunia)	Beringin	Kab.	Deli Serdang	Sumatera Utara	,\
    5145	:	20552	Sidourip	Beringin	Kab.	Deli Serdang	Sumatera Utara	,\
    5146	:	20552	Tumpatan	Beringin	Kab.	Deli Serdang	Sumatera Utara	,\
    5147	:	22251	Banjar Toba	Berampu (Brampu)	Kab.	Dairi	Sumatera Utara	,\
    5148	:	22251	Berampu (Brampu)	Berampu (Brampu)	Kab.	Dairi	Sumatera Utara	,\
    5149	:	22251	Karing	Berampu (Brampu)	Kab.	Dairi	Sumatera Utara	,\
    5150	:	22251	Pasi	Berampu (Brampu)	Kab.	Dairi	Sumatera Utara	,\
    5151	:	22251	Sambaliang	Berampu (Brampu)	Kab.	Dairi	Sumatera Utara	,\
    5152	:	22876	Balale Toba'a	Bawolato	Kab.	Nias	Sumatera Utara	,\
    5153	:	22876	Banua Sibohou Silima Ewali	Bawolato	Kab.	Nias	Sumatera Utara	,\
    5154	:	22876	Botohaenga	Bawolato	Kab.	Nias	Sumatera Utara	,\
    5155	:	22851	Dahana Bawolato	Bawolato	Kab.	Nias	Sumatera Utara	,\
    5156	:	22876	Gazamanu	Bawolato	Kab.	Nias	Sumatera Utara	,\
    5157	:	22876	Hilialawa	Bawolato	Kab.	Nias	Sumatera Utara	,\
    5158	:	22876	Hilifaosi	Bawolato	Kab.	Nias	Sumatera Utara	,\
    5159	:	22876	Hiliganoita	Bawolato	Kab.	Nias	Sumatera Utara	,\
    5160	:	22876	Hilihao Cugala	Bawolato	Kab.	Nias	Sumatera Utara	,\
    5161	:	22851	Hilihoru	Bawolato	Kab.	Nias	Sumatera Utara	,\
    5162	:	22876	Hiliwarokha	Bawolato	Kab.	Nias	Sumatera Utara	,\
    5163	:	22876	Hou	Bawolato	Kab.	Nias	Sumatera Utara	,\
    5164	:	22876	Lagasimahe	Bawolato	Kab.	Nias	Sumatera Utara	,\
    5165	:	22876	Orahili	Bawolato	Kab.	Nias	Sumatera Utara	,\
    5166	:	22876	Orahua	Bawolato	Kab.	Nias	Sumatera Utara	,\
    5167	:	22876	Orahua Faondrato	Bawolato	Kab.	Nias	Sumatera Utara	,\
    5168	:	22876	Si'ofaewali Selatan	Bawolato	Kab.	Nias	Sumatera Utara	,\
    5169	:	22876	Sifaoroasi Uluhou	Bawolato	Kab.	Nias	Sumatera Utara	,\
    5170	:	22876	Sindrondro	Bawolato	Kab.	Nias	Sumatera Utara	,\
    5171	:	22876	Siofabanua	Bawolato	Kab.	Nias	Sumatera Utara	,\
    5172	:	22876	Siofaewali	Bawolato	Kab.	Nias	Sumatera Utara	,\
    5173	:	22876	Sisarahili Bawolato	Bawolato	Kab.	Nias	Sumatera Utara	,\
    5174	:	22876	Sitolubanua	Bawolato	Kab.	Nias	Sumatera Utara	,\
    5175	:	22876	Sohoya	Bawolato	Kab.	Nias	Sumatera Utara	,\
    5176	:	22876	Tagaule	Bawolato	Kab.	Nias	Sumatera Utara	,\
    5177	:	22738	Aek Nauli	Batang Toru	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5178	:	22738	Aek Pining	Batang Toru	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5179	:	22738	Batu Horing	Batang Toru	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5180	:	22738	Batu Hula	Batang Toru	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5181	:	22738	Garoga	Batang Toru	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5182	:	22738	Hapesong Baru	Batang Toru	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5183	:	22738	Hapesong Lama	Batang Toru	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5184	:	22738	Huta Godang	Batang Toru	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5185	:	22738	Hutabaru	Batang Toru	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5186	:	22738	Napa	Batang Toru	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5187	:	22738	Padang Lancat	Batang Toru	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5188	:	22738	Perkebunan Batang Toru	Batang Toru	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5189	:	22738	Perkebunan Hapesong	Batang Toru	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5190	:	22738	Sianggunan	Batang Toru	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5191	:	22738	Sigala-Gala (Perkebunan Sigala-gala)	Batang Toru	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5192	:	22738	Sipenggeng	Batang Toru	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5193	:	22738	Sisipa	Batang Toru	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5194	:	22738	Sisoma Jae	Batang Toru	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5195	:	22738	Sumuran	Batang Toru	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5196	:	22738	Telo	Batang Toru	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5197	:	22738	Wek I Batang Toru	Batang Toru	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5198	:	22738	Wek II Batang Toru	Batang Toru	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5199	:	22738	Wek III Batang Toru	Batang Toru	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5200	:	22738	Wek IV Batang Toru	Batang Toru	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5201	:	20852	Batang Serangan	Batang Serangan	Kab.	Langkat	Sumatera Utara	,\
    5202	:	20852	Karya Jadi	Batang Serangan	Kab.	Langkat	Sumatera Utara	,\
    5203	:	20852	Kwala Musam	Batang Serangan	Kab.	Langkat	Sumatera Utara	,\
    5204	:	20852	Namu/Namo Sialang	Batang Serangan	Kab.	Langkat	Sumatera Utara	,\
    5205	:	20852	Paluh Pakih Babussalam	Batang Serangan	Kab.	Langkat	Sumatera Utara	,\
    5206	:	20852	Sei Bamban	Batang Serangan	Kab.	Langkat	Sumatera Utara	,\
    5207	:	20852	Sei Musam	Batang Serangan	Kab.	Langkat	Sumatera Utara	,\
    5208	:	20852	Sei Serdang	Batang Serangan	Kab.	Langkat	Sumatera Utara	,\
    5209	:	22762	Batang Onang Baru	Batang Onang	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    5210	:	22762	Batang Onang Lama	Batang Onang	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    5211	:	22762	Batu Mamak	Batang Onang	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    5212	:	22762	Batu Nanggar	Batang Onang	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    5213	:	22762	Batu Pulut	Batang Onang	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    5214	:	22762	Bonan Dolok	Batang Onang	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    5215	:	22762	Galanggang	Batang Onang	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    5216	:	22762	Gunung Tua Batang Onang	Batang Onang	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    5217	:	22762	Gunung Tua Jati (Tumbujat)	Batang Onang	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    5218	:	22762	Gunung Tua Julu	Batang Onang	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    5219	:	22762	Huta Lambung	Batang Onang	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    5220	:	22762	Janji Manahan	Batang Onang	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    5221	:	22762	Janji Mauli	Batang Onang	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    5222	:	22762	Morang	Batang Onang	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    5223	:	22762	Padang Bujur Baru	Batang Onang	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    5224	:	22762	Padang Garugur	Batang Onang	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    5225	:	22762	Padang Matinggi	Batang Onang	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    5226	:	22762	Pagaran Batu	Batang Onang	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    5227	:	22762	Pangkalan Dolok Julu	Batang Onang	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    5228	:	22762	Pangkalan Dolok Lama	Batang Onang	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    5229	:	22762	Parau Sorat	Batang Onang	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    5230	:	22762	Pasar Matanggor	Batang Onang	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    5231	:	22762	Pasir Ampolu Hepeng	Batang Onang	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    5232	:	22762	Pintu Padang	Batang Onang	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    5233	:	22762	Purba Tua	Batang Onang	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    5234	:	22762	Sayur Matinggi	Batang Onang	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    5235	:	22762	Sayur Matinggi II Julu	Batang Onang	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    5236	:	22762	Simanapang	Batang Onang	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    5237	:	22762	Simangambat Dolok	Batang Onang	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    5238	:	22762	Simaninggir Psm	Batang Onang	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    5239	:	22762	Simardona	Batang Onang	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    5240	:	22762	Tamosu	Batang Onang	Kab.	Padang Lawas Utara	Sumatera Utara	,\
    5241	:	22983	Aek Guo	Batang Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    5242	:	22983	Aek Holbung	Batang Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    5243	:	22983	Aek Manggis	Batang Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    5244	:	22983	Aek Nabara	Batang Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    5245	:	22983	Aek Nangali	Batang Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    5246	:	22983	Ampung Julu	Batang Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    5247	:	22983	Ampung Padang	Batang Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    5248	:	22983	Ampung Siala	Batang Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    5249	:	22983	Bangkelang	Batang Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    5250	:	22983	Banjar Malayu	Batang Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    5251	:	22983	Batu Madinding	Batang Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    5252	:	22983	Bulu Soma	Batang Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    5253	:	22983	Guo Batu	Batang Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    5254	:	22983	Hadangkahan	Batang Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    5255	:	22983	Hatupangan	Batang Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    5256	:	22983	Huta Lobu	Batang Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    5257	:	22983	Lubuk Samba	Batang Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    5258	:	22983	Muara Lampungan	Batang Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    5259	:	22983	Muara Soma	Batang Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    5260	:	22983	Rantobi	Batang Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    5261	:	22983	Rao Rao	Batang Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    5262	:	22983	Simanguntong	Batang Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    5263	:	22983	Sipogu	Batang Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    5264	:	22983	Sopo Tinjak	Batang Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    5265	:	22983	Tarlola	Batang Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    5266	:	22983	Tombang Taluang	Batang Natal	Kab.	Mandailing Natal	Sumatera Utara	,\
    5267	:	22742	Aek Sorik	Batang Lubu Sutam	Kab.	Padang Lawas	Sumatera Utara	,\
    5268	:	22742	Botung	Batang Lubu Sutam	Kab.	Padang Lawas	Sumatera Utara	,\
    5269	:	22742	Gunung Intan	Batang Lubu Sutam	Kab.	Padang Lawas	Sumatera Utara	,\
    5270	:	22742	Gunung Manaon	Batang Lubu Sutam	Kab.	Padang Lawas	Sumatera Utara	,\
    5271	:	22742	Hatongga	Batang Lubu Sutam	Kab.	Padang Lawas	Sumatera Utara	,\
    5272	:	22742	Huta Baru	Batang Lubu Sutam	Kab.	Padang Lawas	Sumatera Utara	,\
    5273	:	22742	Hutanopan	Batang Lubu Sutam	Kab.	Padang Lawas	Sumatera Utara	,\
    5274	:	22742	Manggis	Batang Lubu Sutam	Kab.	Padang Lawas	Sumatera Utara	,\
    5275	:	22742	Muara Malinto Baru	Batang Lubu Sutam	Kab.	Padang Lawas	Sumatera Utara	,\
    5276	:	22742	Muara Malinto Lama	Batang Lubu Sutam	Kab.	Padang Lawas	Sumatera Utara	,\
    5277	:	22742	Muara Tige	Batang Lubu Sutam	Kab.	Padang Lawas	Sumatera Utara	,\
    5278	:	22742	Pagaran Baringin/Beringin	Batang Lubu Sutam	Kab.	Padang Lawas	Sumatera Utara	,\
    5279	:	22742	Pagaran Dolok Pinarik	Batang Lubu Sutam	Kab.	Padang Lawas	Sumatera Utara	,\
    5280	:	22742	Pagaran Manggis	Batang Lubu Sutam	Kab.	Padang Lawas	Sumatera Utara	,\
    5281	:	22742	Pagaran Tayas	Batang Lubu Sutam	Kab.	Padang Lawas	Sumatera Utara	,\
    5282	:	22742	Papaso	Batang Lubu Sutam	Kab.	Padang Lawas	Sumatera Utara	,\
    5283	:	22742	Pinarik	Batang Lubu Sutam	Kab.	Padang Lawas	Sumatera Utara	,\
    5284	:	22742	Rombayan	Batang Lubu Sutam	Kab.	Padang Lawas	Sumatera Utara	,\
    5285	:	22742	Salambue	Batang Lubu Sutam	Kab.	Padang Lawas	Sumatera Utara	,\
    5286	:	22742	Siadam	Batang Lubu Sutam	Kab.	Padang Lawas	Sumatera Utara	,\
    5287	:	22742	Sibodak Papaso	Batang Lubu Sutam	Kab.	Padang Lawas	Sumatera Utara	,\
    5288	:	22742	Siojo	Batang Lubu Sutam	Kab.	Padang Lawas	Sumatera Utara	,\
    5289	:	22742	Tamiang	Batang Lubu Sutam	Kab.	Padang Lawas	Sumatera Utara	,\
    5290	:	22742	Tandalon	Batang Lubu Sutam	Kab.	Padang Lawas	Sumatera Utara	,\
    5291	:	22742	Tangga Batu	Batang Lubu Sutam	Kab.	Padang Lawas	Sumatera Utara	,\
    5292	:	22742	Tanjung Barani	Batang Lubu Sutam	Kab.	Padang Lawas	Sumatera Utara	,\
    5293	:	22742	Tanjung Baru	Batang Lubu Sutam	Kab.	Padang Lawas	Sumatera Utara	,\
    5294	:	22742	Tanjung Botung Pinarik	Batang Lubu Sutam	Kab.	Padang Lawas	Sumatera Utara	,\
    5295	:	20372	Bakaran Batu	Batang Kuis	Kab.	Deli Serdang	Sumatera Utara	,\
    5296	:	20372	Baru (kampung Baru)	Batang Kuis	Kab.	Deli Serdang	Sumatera Utara	,\
    5297	:	20372	Batang Kuis Pekan	Batang Kuis	Kab.	Deli Serdang	Sumatera Utara	,\
    5298	:	20372	Bintang Meriah	Batang Kuis	Kab.	Deli Serdang	Sumatera Utara	,\
    5299	:	20372	Mesjid	Batang Kuis	Kab.	Deli Serdang	Sumatera Utara	,\
    5300	:	20372	Paya Gambar	Batang Kuis	Kab.	Deli Serdang	Sumatera Utara	,\
    5301	:	20372	Sena	Batang Kuis	Kab.	Deli Serdang	Sumatera Utara	,\
    5302	:	20372	Sidodadi	Batang Kuis	Kab.	Deli Serdang	Sumatera Utara	,\
    5303	:	20372	Sugiharjo	Batang Kuis	Kab.	Deli Serdang	Sumatera Utara	,\
    5304	:	20372	Tanjung Sari	Batang Kuis	Kab.	Deli Serdang	Sumatera Utara	,\
    5305	:	20372	Tumpatan Nibung	Batang Kuis	Kab.	Deli Serdang	Sumatera Utara	,\
    5306	:	22773	Aek Gunung	Batang Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5307	:	22773	Aek Nauli	Batang Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5308	:	22773	Bargot Topong	Batang Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5309	:	22773	Basilam Baru	Batang Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5310	:	22773	Benteng Huraba	Batang Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5311	:	22773	Bintuju	Batang Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5312	:	22773	Hurase / Hurare	Batang Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5313	:	22773	Huta Holbung / Holdung	Batang Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5314	:	22773	Huta Padang	Batang Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5315	:	22773	Huta Tonga	Batang Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5316	:	22773	Janji Manaon	Batang Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5317	:	22773	Janji Mauli Mt	Batang Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5318	:	22773	Muara Nauli	Batang Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5319	:	22773	Muara Tais I	Batang Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5320	:	22773	Muara Tais II	Batang Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5321	:	22773	Muara Tais III	Batang Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5322	:	22773	Padang Kahombu	Batang Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5323	:	22773	Pangaribuan	Batang Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5324	:	22773	Pargumbangan	Batang Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5325	:	22773	Pasar Lamo/Lama	Batang Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5326	:	22773	Pasir	Batang Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5327	:	22773	Pintu Padang Raya Dua	Batang Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5328	:	22773	Pintu Padang Raya Satu	Batang Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5329	:	22773	Sibulele	Batang Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5330	:	22773	Sidadi Dua	Batang Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5331	:	22773	Sidadi Julu Satu	Batang Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5332	:	22773	Sigalangan	Batang Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5333	:	22773	Sigulang Losung	Batang Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5334	:	22773	Sijungkit	Batang Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5335	:	22773	Sipangko	Batang Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5336	:	22773	Sitampa	Batang Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5337	:	22773	Sori Madingin Pp	Batang Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5338	:	22773	Sorik	Batang Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5339	:	22773	Sorimadingin	Batang Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5340	:	22773	Tahalak Ujung	Batang Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5341	:	22773	Tatengger	Batang Angkola	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5342	:	22988	Banjar Aur	Batahan	Kab.	Mandailing Natal	Sumatera Utara	,\
    5343	:	22988	Batahan I	Batahan	Kab.	Mandailing Natal	Sumatera Utara	,\
    5344	:	22988	Batahan II	Batahan	Kab.	Mandailing Natal	Sumatera Utara	,\
    5345	:	22988	Batahan III	Batahan	Kab.	Mandailing Natal	Sumatera Utara	,\
    5346	:	22988	Batahan IV	Batahan	Kab.	Mandailing Natal	Sumatera Utara	,\
    5347	:	22988	Batu Sondat	Batahan	Kab.	Mandailing Natal	Sumatera Utara	,\
    5348	:	22988	Bintungan Bejangkar	Batahan	Kab.	Mandailing Natal	Sumatera Utara	,\
    5349	:	22988	Kampung Kapas	Batahan	Kab.	Mandailing Natal	Sumatera Utara	,\
    5350	:	22988	Kampung Kapas I	Batahan	Kab.	Mandailing Natal	Sumatera Utara	,\
    5351	:	22988	Kuala Batahan	Batahan	Kab.	Mandailing Natal	Sumatera Utara	,\
    5352	:	22988	Kubangan Tompek	Batahan	Kab.	Mandailing Natal	Sumatera Utara	,\
    5353	:	22988	Muara Pertemuan	Batahan	Kab.	Mandailing Natal	Sumatera Utara	,\
    5354	:	22988	Pasar Baru Batahan	Batahan	Kab.	Mandailing Natal	Sumatera Utara	,\
    5355	:	22988	Pasar Batahan	Batahan	Kab.	Mandailing Natal	Sumatera Utara	,\
    5356	:	22988	Pulau Tamang	Batahan	Kab.	Mandailing Natal	Sumatera Utara	,\
    5357	:	22988	Sari Kenanga Batahan	Batahan	Kab.	Mandailing Natal	Sumatera Utara	,\
    5358	:	22988	Sinunukan VI	Batahan	Kab.	Mandailing Natal	Sumatera Utara	,\
    5359	:	22564	Huta Ginjang	Barus Utara	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5360	:	22564	Pananggahan	Barus Utara	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5361	:	22564	Parik Sinomba	Barus Utara	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5362	:	22564	Purbatua	Barus Utara	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5363	:	22564	Siharbangan	Barus Utara	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5364	:	22564	Sihorbo	Barus Utara	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5365	:	22172	Barus Jahe	Barus Jahe	Kab.	Karo	Sumatera Utara	,\
    5366	:	22172	Barus Julu	Barus Jahe	Kab.	Karo	Sumatera Utara	,\
    5367	:	22172	Bulan Jahe	Barus Jahe	Kab.	Karo	Sumatera Utara	,\
    5368	:	22172	Bulan Julu	Barus Jahe	Kab.	Karo	Sumatera Utara	,\
    5369	:	22172	Paribun	Barus Jahe	Kab.	Karo	Sumatera Utara	,\
    5370	:	22172	Penampen	Barus Jahe	Kab.	Karo	Sumatera Utara	,\
    5371	:	22172	Persadanta	Barus Jahe	Kab.	Karo	Sumatera Utara	,\
    5372	:	22172	Pertumbuken	Barus Jahe	Kab.	Karo	Sumatera Utara	,\
    5373	:	22172	Rumamis	Barus Jahe	Kab.	Karo	Sumatera Utara	,\
    5374	:	22172	Sarimanis	Barus Jahe	Kab.	Karo	Sumatera Utara	,\
    5375	:	22172	Semangat	Barus Jahe	Kab.	Karo	Sumatera Utara	,\
    5376	:	22172	Serdang	Barus Jahe	Kab.	Karo	Sumatera Utara	,\
    5377	:	22172	Sikab	Barus Jahe	Kab.	Karo	Sumatera Utara	,\
    5378	:	22172	Sinaman	Barus Jahe	Kab.	Karo	Sumatera Utara	,\
    5379	:	22172	Sukajulu	Barus Jahe	Kab.	Karo	Sumatera Utara	,\
    5380	:	22172	Sukanalu	Barus Jahe	Kab.	Karo	Sumatera Utara	,\
    5381	:	22172	Talimbaru	Barus Jahe	Kab.	Karo	Sumatera Utara	,\
    5382	:	22172	Tangkidik	Barus Jahe	Kab.	Karo	Sumatera Utara	,\
    5383	:	22172	Tanjung Barus	Barus Jahe	Kab.	Karo	Sumatera Utara	,\
    5384	:	22564	Aek Dakka	Barus	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5385	:	22564	Bungo Tanjung	Barus	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5386	:	22564	Gabungan Hasang	Barus	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5387	:	22564	Kampung Mudik	Barus	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5388	:	22564	Kampung Solok	Barus	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5389	:	22564	Kedai Gedang	Barus	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5390	:	22564	Kinali	Barus	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5391	:	22564	Padang Masiang	Barus	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5392	:	22564	Pasar Batu Gerigis	Barus	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5393	:	22564	Pasar Terandam	Barus	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5394	:	22564	Patupangan	Barus	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5395	:	22564	Sigambo Gambo	Barus	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5396	:	22564	Ujung Batu	Barus	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5397	:	22755	Aek Siala	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5398	:	22755	Aek Tanduk	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5399	:	22755	Aek Tunjang	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5400	:	22755	Bahal Batu	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5401	:	22755	Bakkudu (Bangkudu)	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5402	:	22755	Bara Batu	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5403	:	22755	Batu Sundung	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5404	:	22755	Binanga	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5405	:	22755	Bire	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5406	:	22755	Gading	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5407	:	22755	Ginduang Batu	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5408	:	22755	Gunung Baringin	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5409	:	22755	Gunung Malintang	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5410	:	22755	Gunung Manaon Ur	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5411	:	22755	Huta Ruhom	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5412	:	22755	Janji Manahan	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5413	:	22755	Janji Matogu Ur	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5414	:	22755	Janji Raja	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5415	:	22755	Manombo	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5416	:	22755	Padang Garugur	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5417	:	22755	Padang Matinggi	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5418	:	22755	Pangirkiran Dolok	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5419	:	22755	Paran Napa Dolok	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5420	:	22755	Paran Napa Jae	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5421	:	22755	Pasar Binanga	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5422	:	22755	Pp Makmur	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5423	:	22755	Sibatu Loting	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5424	:	22755	Sibontar	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5425	:	22755	Siboris Bahal	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5426	:	22755	Siboris Dolok	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5427	:	22755	Siboris Lombang	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5428	:	22755	Sidong-Dong	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5429	:	22755	Sihaborgoan Barum	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5430	:	22755	Sihaborgoan Dalan	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5431	:	22755	Siolip	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5432	:	22755	Siparau	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5433	:	22755	Sisalean	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5434	:	22755	Tandihat	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5435	:	22755	Unte Rudang	Barumun Tengah	Kab.	Padang Lawas	Sumatera Utara	,\
    5436	:	22763	Banua Tonga	Barumun Selatan	Kab.	Padang Lawas	Sumatera Utara	,\
    5437	:	22763	Batang Bulu Baru	Barumun Selatan	Kab.	Padang Lawas	Sumatera Utara	,\
    5438	:	22763	Batang Bulu Lama	Barumun Selatan	Kab.	Padang Lawas	Sumatera Utara	,\
    5439	:	22763	Gunung Barani	Barumun Selatan	Kab.	Padang Lawas	Sumatera Utara	,\
    5440	:	22763	Gunung Intan	Barumun Selatan	Kab.	Padang Lawas	Sumatera Utara	,\
    5441	:	22763	Pagur Satio	Barumun Selatan	Kab.	Padang Lawas	Sumatera Utara	,\
    5442	:	22763	Panarian	Barumun Selatan	Kab.	Padang Lawas	Sumatera Utara	,\
    5443	:	22763	Sayur Mahincat/Maincat	Barumun Selatan	Kab.	Padang Lawas	Sumatera Utara	,\
    5444	:	22763	Sidomulio	Barumun Selatan	Kab.	Padang Lawas	Sumatera Utara	,\
    5445	:	22763	Tanjung Baringin Sim	Barumun Selatan	Kab.	Padang Lawas	Sumatera Utara	,\
    5446	:	22763	Tanjung Purba Baru (Purbatua)	Barumun Selatan	Kab.	Padang Lawas	Sumatera Utara	,\
    5447	:	22763	Arse Simatorkis	Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5448	:	22763	Bangun Raya	Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5449	:	22763	Binabo Jae	Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5450	:	22763	Binabo Julu	Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5451	:	22763	Bulu Sonik	Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5452	:	22763	Handis Julu	Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5453	:	22763	Hasahatan Jae	Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5454	:	22763	Hasahatan Julu	Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5455	:	22763	Hutarimbaru	Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5456	:	22763	Janji Lobi	Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5457	:	22763	Limbong	Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5458	:	22763	Mompang	Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5459	:	22763	Pagaran Baringin	Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5460	:	22763	Pancaukan	Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5461	:	22763	Pasar Sibuhuan	Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5462	:	22763	Purbatua	Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5463	:	22763	Saba Rimba/Riba	Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5464	:	22763	Sabahotang	Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5465	:	22763	Salambue (Sialam Bue)	Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5466	:	22763	Sayur Matua	Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5467	:	22763	Sibuhuan Jae	Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5468	:	22763	Sibuhuan Julu	Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5469	:	22763	Sigorbus Jae	Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5470	:	22763	Sigorbus Julu	Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5471	:	22763	Simaninggir	Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5472	:	22763	Siolip	Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5473	:	22763	Sitarolo Julu	Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5474	:	22763	Tanjung Botung	Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5475	:	22763	Tanjung Durian	Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5476	:	22763	Tano Bato	Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5477	:	20581	Bagerpang	Bangun Purba	Kab.	Deli Serdang	Sumatera Utara	,\
    5478	:	20581	Bah Balua	Bangun Purba	Kab.	Deli Serdang	Sumatera Utara	,\
    5479	:	20581	Bah Perak	Bangun Purba	Kab.	Deli Serdang	Sumatera Utara	,\
    5480	:	20581	Bandar Gunung	Bangun Purba	Kab.	Deli Serdang	Sumatera Utara	,\
    5481	:	20581	Bandar Kuala (Kwala)	Bangun Purba	Kab.	Deli Serdang	Sumatera Utara	,\
    5482	:	20581	Bandar Meriah	Bangun Purba	Kab.	Deli Serdang	Sumatera Utara	,\
    5483	:	20581	Bangun Purba	Bangun Purba	Kab.	Deli Serdang	Sumatera Utara	,\
    5484	:	20581	Bangun Purba Tengah	Bangun Purba	Kab.	Deli Serdang	Sumatera Utara	,\
    5485	:	20581	Batu Gingging	Bangun Purba	Kab.	Deli Serdang	Sumatera Utara	,\
    5486	:	20581	Batu Rata	Bangun Purba	Kab.	Deli Serdang	Sumatera Utara	,\
    5487	:	20581	Cimahi (Cimahe)	Bangun Purba	Kab.	Deli Serdang	Sumatera Utara	,\
    5488	:	20581	Damak Maliho	Bangun Purba	Kab.	Deli Serdang	Sumatera Utara	,\
    5489	:	20581	Geriahan (Greahan)	Bangun Purba	Kab.	Deli Serdang	Sumatera Utara	,\
    5490	:	20581	Mabar	Bangun Purba	Kab.	Deli Serdang	Sumatera Utara	,\
    5491	:	20581	Marambun Barat (Marombun Barat)	Bangun Purba	Kab.	Deli Serdang	Sumatera Utara	,\
    5492	:	20581	Marambun Ujung Jawi	Bangun Purba	Kab.	Deli Serdang	Sumatera Utara	,\
    5493	:	20581	Perguroan (Perguruan)	Bangun Purba	Kab.	Deli Serdang	Sumatera Utara	,\
    5494	:	20581	Rumah Deleng	Bangun Purba	Kab.	Deli Serdang	Sumatera Utara	,\
    5495	:	20581	Sialang	Bangun Purba	Kab.	Deli Serdang	Sumatera Utara	,\
    5496	:	20581	Sibaganding	Bangun Purba	Kab.	Deli Serdang	Sumatera Utara	,\
    5497	:	20581	Suka Luae (Lewei)	Bangun Purba	Kab.	Deli Serdang	Sumatera Utara	,\
    5498	:	20581	Tanjung Purba	Bangun Purba	Kab.	Deli Serdang	Sumatera Utara	,\
    5499	:	20581	Ujung Rambe	Bangun Purba	Kab.	Deli Serdang	Sumatera Utara	,\
    5500	:	20581	Urung Ganjang	Bangun Purba	Kab.	Deli Serdang	Sumatera Utara	,\
    5501	:	21274	Aek Nagali	Bandar Pulau	Kab.	Asahan	Sumatera Utara	,\
    5502	:	21274	Bandar Pulau Pekan	Bandar Pulau	Kab.	Asahan	Sumatera Utara	,\
    5503	:	21274	Buntu Maraja	Bandar Pulau	Kab.	Asahan	Sumatera Utara	,\
    5504	:	21274	Gajah Sakti	Bandar Pulau	Kab.	Asahan	Sumatera Utara	,\
    5505	:	21274	Gonting Malaha	Bandar Pulau	Kab.	Asahan	Sumatera Utara	,\
    5506	:	21274	Gunung Berkat	Bandar Pulau	Kab.	Asahan	Sumatera Utara	,\
    5507	:	21274	Huta Rao	Bandar Pulau	Kab.	Asahan	Sumatera Utara	,\
    5508	:	21274	Padang Pulau	Bandar Pulau	Kab.	Asahan	Sumatera Utara	,\
    5509	:	21274	Perkebunan Aek Tarum	Bandar Pulau	Kab.	Asahan	Sumatera Utara	,\
    5510	:	21274	Perkebunan Padang Pulau	Bandar Pulau	Kab.	Asahan	Sumatera Utara	,\
    5511	:	21262	Bandar Pasir Mandoge	Bandar Pasir Mandoge	Kab.	Asahan	Sumatera Utara	,\
    5512	:	21262	Gotting Sidodadi	Bandar Pasir Mandoge	Kab.	Asahan	Sumatera Utara	,\
    5513	:	21262	Huta Bagasan	Bandar Pasir Mandoge	Kab.	Asahan	Sumatera Utara	,\
    5514	:	21262	Huta Padang	Bandar Pasir Mandoge	Kab.	Asahan	Sumatera Utara	,\
    5515	:	21262	Sei Kopas	Bandar Pasir Mandoge	Kab.	Asahan	Sumatera Utara	,\
    5516	:	21262	Sei Nadoras	Bandar Pasir Mandoge	Kab.	Asahan	Sumatera Utara	,\
    5517	:	21262	Silau Jawa	Bandar Pasir Mandoge	Kab.	Asahan	Sumatera Utara	,\
    5518	:	21262	Suka Makmur	Bandar Pasir Mandoge	Kab.	Asahan	Sumatera Utara	,\
    5519	:	21184	Bandar Masilam	Bandar Masilam	Kab.	Simalungun	Sumatera Utara	,\
    5520	:	21184	Bandar Masilam II	Bandar Masilam	Kab.	Simalungun	Sumatera Utara	,\
    5521	:	21184	Bandar Rejo	Bandar Masilam	Kab.	Simalungun	Sumatera Utara	,\
    5522	:	21184	Bandar Silou	Bandar Masilam	Kab.	Simalungun	Sumatera Utara	,\
    5523	:	21184	Bandar Tinggi	Bandar Masilam	Kab.	Simalungun	Sumatera Utara	,\
    5524	:	21184	Gunung Serawan	Bandar Masilam	Kab.	Simalungun	Sumatera Utara	,\
    5525	:	21184	Lias Baru	Bandar Masilam	Kab.	Simalungun	Sumatera Utara	,\
    5526	:	21184	Panombean Baru	Bandar Masilam	Kab.	Simalungun	Sumatera Utara	,\
    5527	:	21184	Partimbalan	Bandar Masilam	Kab.	Simalungun	Sumatera Utara	,\
    5528	:	20994	Bandar Tengah	Bandar Khalifah	Kab.	Serdang Bedagai	Sumatera Utara	,\
    5529	:	20994	Gelam Sei Sarimah	Bandar Khalifah	Kab.	Serdang Bedagai	Sumatera Utara	,\
    5530	:	20994	Juhar (Kampung Juhar)	Bandar Khalifah	Kab.	Serdang Bedagai	Sumatera Utara	,\
    5531	:	20994	Kayu Besar	Bandar Khalifah	Kab.	Serdang Bedagai	Sumatera Utara	,\
    5532	:	20994	Pekan Bandar Khalipah	Bandar Khalifah	Kab.	Serdang Bedagai	Sumatera Utara	,\
    5533	:	21184	Bah Gunung	Bandar Huluan	Kab.	Simalungun	Sumatera Utara	,\
    5534	:	21184	Bandar Betsy I	Bandar Huluan	Kab.	Simalungun	Sumatera Utara	,\
    5535	:	21184	Bandar Betsy II	Bandar Huluan	Kab.	Simalungun	Sumatera Utara	,\
    5536	:	21184	Bandar Tongah	Bandar Huluan	Kab.	Simalungun	Sumatera Utara	,\
    5537	:	21184	Dolok Parmonangan	Bandar Huluan	Kab.	Simalungun	Sumatera Utara	,\
    5538	:	21184	Laras	Bandar Huluan	Kab.	Simalungun	Sumatera Utara	,\
    5539	:	21184	Naga Jaya I	Bandar Huluan	Kab.	Simalungun	Sumatera Utara	,\
    5540	:	21184	Naga Jaya II	Bandar Huluan	Kab.	Simalungun	Sumatera Utara	,\
    5541	:	21184	Naga Soppa	Bandar Huluan	Kab.	Simalungun	Sumatera Utara	,\
    5542	:	21184	Tanjung Hataran	Bandar Huluan	Kab.	Simalungun	Sumatera Utara	,\
    5543	:	21184	Bah Lias	Bandar	Kab.	Simalungun	Sumatera Utara	,\
    5544	:	21184	Bandar Jawa	Bandar	Kab.	Simalungun	Sumatera Utara	,\
    5545	:	21184	Bandar Pulo	Bandar	Kab.	Simalungun	Sumatera Utara	,\
    5546	:	21184	Bandar Rakyat	Bandar	Kab.	Simalungun	Sumatera Utara	,\
    5547	:	21162	Marihat Bandar	Bandar	Kab.	Simalungun	Sumatera Utara	,\
    5548	:	21184	Nagori Bandar	Bandar	Kab.	Simalungun	Sumatera Utara	,\
    5549	:	21184	Pematang Kerasaan	Bandar	Kab.	Simalungun	Sumatera Utara	,\
    5550	:	21184	Pematang Kerasaan Rejo	Bandar	Kab.	Simalungun	Sumatera Utara	,\
    5551	:	21184	Perdagangan I	Bandar	Kab.	Simalungun	Sumatera Utara	,\
    5552	:	21184	Perdagangan II	Bandar	Kab.	Simalungun	Sumatera Utara	,\
    5553	:	21184	Perdagangan III	Bandar	Kab.	Simalungun	Sumatera Utara	,\
    5554	:	21184	Perlanaan	Bandar	Kab.	Simalungun	Sumatera Utara	,\
    5555	:	21184	Sido Tani	Bandar	Kab.	Simalungun	Sumatera Utara	,\
    5556	:	21184	Sugarang Bayu	Bandar	Kab.	Simalungun	Sumatera Utara	,\
    5557	:	21184	Timbaan	Bandar	Kab.	Simalungun	Sumatera Utara	,\
    5558	:	22312	Aek Bolon Jae	Balige	Kab.	Toba Samosir	Sumatera Utara	,\
    5559	:	22312	Aek Bolon Julu	Balige	Kab.	Toba Samosir	Sumatera Utara	,\
    5560	:	22316	Balige I	Balige	Kab.	Toba Samosir	Sumatera Utara	,\
    5561	:	22316	Balige II	Balige	Kab.	Toba Samosir	Sumatera Utara	,\
    5562	:	22315	Balige III	Balige	Kab.	Toba Samosir	Sumatera Utara	,\
    5563	:	22312	Baru Ara	Balige	Kab.	Toba Samosir	Sumatera Utara	,\
    5564	:	22312	Bonan Dolok I	Balige	Kab.	Toba Samosir	Sumatera Utara	,\
    5565	:	22312	Bonan Dolok II	Balige	Kab.	Toba Samosir	Sumatera Utara	,\
    5566	:	22312	Bonan Dolok III	Balige	Kab.	Toba Samosir	Sumatera Utara	,\
    5567	:	22312	Hinalang Bagasan	Balige	Kab.	Toba Samosir	Sumatera Utara	,\
    5568	:	22312	Huta Bulu Mejan	Balige	Kab.	Toba Samosir	Sumatera Utara	,\
    5569	:	22312	Huta Dame	Balige	Kab.	Toba Samosir	Sumatera Utara	,\
    5570	:	22312	Huta Namora	Balige	Kab.	Toba Samosir	Sumatera Utara	,\
    5571	:	22312	Hutagaol Peatalun (Peatalum)	Balige	Kab.	Toba Samosir	Sumatera Utara	,\
    5572	:	22312	Longat	Balige	Kab.	Toba Samosir	Sumatera Utara	,\
    5573	:	22312	Lumban Bul Bul	Balige	Kab.	Toba Samosir	Sumatera Utara	,\
    5574	:	22314	Lumban Dolok Haume Bange	Balige	Kab.	Toba Samosir	Sumatera Utara	,\
    5575	:	22312	Lumban Gaol	Balige	Kab.	Toba Samosir	Sumatera Utara	,\
    5576	:	22312	Lumban Gorat	Balige	Kab.	Toba Samosir	Sumatera Utara	,\
    5577	:	22312	Lumban Pea	Balige	Kab.	Toba Samosir	Sumatera Utara	,\
    5578	:	22312	Lumban Pea Timur	Balige	Kab.	Toba Samosir	Sumatera Utara	,\
    5579	:	22312	Lumban Silintong	Balige	Kab.	Toba Samosir	Sumatera Utara	,\
    5580	:	22312	Matio	Balige	Kab.	Toba Samosir	Sumatera Utara	,\
    5581	:	22311	Napitupulu Bagasan	Balige	Kab.	Toba Samosir	Sumatera Utara	,\
    5582	:	22312	Paindoan	Balige	Kab.	Toba Samosir	Sumatera Utara	,\
    5583	:	22313	Pardede Onan	Balige	Kab.	Toba Samosir	Sumatera Utara	,\
    5584	:	22312	Parsuratan	Balige	Kab.	Toba Samosir	Sumatera Utara	,\
    5585	:	22312	Sangkar Nihuta	Balige	Kab.	Toba Samosir	Sumatera Utara	,\
    5586	:	22312	Sariburaja Janji Maria	Balige	Kab.	Toba Samosir	Sumatera Utara	,\
    5587	:	22312	Sianipar Sihail Hail	Balige	Kab.	Toba Samosir	Sumatera Utara	,\
    5588	:	22312	Sibola Hotangsas	Balige	Kab.	Toba Samosir	Sumatera Utara	,\
    5589	:	22312	Siboruon	Balige	Kab.	Toba Samosir	Sumatera Utara	,\
    5590	:	22312	Sibuntuon	Balige	Kab.	Toba Samosir	Sumatera Utara	,\
    5591	:	22312	Silalahi Pagar Batu	Balige	Kab.	Toba Samosir	Sumatera Utara	,\
    5592	:	22312	Tambunan Sunge	Balige	Kab.	Toba Samosir	Sumatera Utara	,\
    5593	:	22457	Marbun	Bakti Raja	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    5594	:	22457	Marbun Tonga Marbun Dolok	Bakti Raja	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    5595	:	22457	Simamora	Bakti Raja	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    5596	:	22457	Simangulampe	Bakti Raja	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    5597	:	22457	Sinambela	Bakti Raja	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    5598	:	22457	Siunong-Unong Julu	Bakti Raja	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    5599	:	22457	Tipang	Bakti Raja	Kab.	Humbang Hasundutan	Sumatera Utara	,\
    5600	:	20613	Bandar Sakti	Bajenis	Kota	Tebing Tinggi	Sumatera Utara	,\
    5601	:	20611	Berohol	Bajenis	Kota	Tebing Tinggi	Sumatera Utara	,\
    5602	:	20612	Bulian	Bajenis	Kota	Tebing Tinggi	Sumatera Utara	,\
    5603	:	20621	Durian	Bajenis	Kota	Tebing Tinggi	Sumatera Utara	,\
    5604	:	20621	Pelita	Bajenis	Kota	Tebing Tinggi	Sumatera Utara	,\
    5605	:	20612	Pinang Mancung	Bajenis	Kota	Tebing Tinggi	Sumatera Utara	,\
    5606	:	20612	Teluk Karang	Bajenis	Kota	Tebing Tinggi	Sumatera Utara	,\
    5607	:	20774	Batu Jongjong	Bahorok	Kab.	Langkat	Sumatera Utara	,\
    5608	:	20774	Empus	Bahorok	Kab.	Langkat	Sumatera Utara	,\
    5609	:	20774	Lau Damak	Bahorok	Kab.	Langkat	Sumatera Utara	,\
    5610	:	20774	Musam Pembangunan	Bahorok	Kab.	Langkat	Sumatera Utara	,\
    5611	:	20774	Pekan Bahorok	Bahorok	Kab.	Langkat	Sumatera Utara	,\
    5612	:	20774	Perkebunan Bukit Lawang	Bahorok	Kab.	Langkat	Sumatera Utara	,\
    5613	:	20774	Perkebunan Bungara	Bahorok	Kab.	Langkat	Sumatera Utara	,\
    5614	:	20774	Perkebunan Pulau Rambung	Bahorok	Kab.	Langkat	Sumatera Utara	,\
    5615	:	20774	Perkebunan Sei Musam	Bahorok	Kab.	Langkat	Sumatera Utara	,\
    5616	:	20774	Perkebunan Turangi	Bahorok	Kab.	Langkat	Sumatera Utara	,\
    5617	:	20774	Sampe Raya	Bahorok	Kab.	Langkat	Sumatera Utara	,\
    5618	:	20774	Sei Musam Kendit	Bahorok	Kab.	Langkat	Sumatera Utara	,\
    5619	:	20774	Sematar	Bahorok	Kab.	Langkat	Sumatera Utara	,\
    5620	:	20774	Simpang Pulau Rambung	Bahorok	Kab.	Langkat	Sumatera Utara	,\
    5621	:	20774	Suka Rakyat (Sukarayat)	Bahorok	Kab.	Langkat	Sumatera Utara	,\
    5622	:	20774	Tanjung Lenggang	Bahorok	Kab.	Langkat	Sumatera Utara	,\
    5623	:	20774	Timbang Jaya	Bahorok	Kab.	Langkat	Sumatera Utara	,\
    5624	:	20774	Timbang Lawan	Bahorok	Kab.	Langkat	Sumatera Utara	,\
    5625	:	20774	Ujung Bandar	Bahorok	Kab.	Langkat	Sumatera Utara	,\
    5626	:	22654	Aek Horsik	Badiri	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5627	:	22654	Gunung Kelambu	Badiri	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5628	:	22654	Hutabalang	Badiri	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5629	:	22654	Jago Jago	Badiri	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5630	:	22654	Kebun Pisang	Badiri	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5631	:	22654	Lopian	Badiri	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5632	:	22654	Lubuk Ampolu	Badiri	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5633	:	22654	Pagaran Honas	Badiri	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5634	:	22654	Sitardas	Badiri	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5635	:	20857	Brandan Barat	Babalan	Kab.	Langkat	Sumatera Utara	,\
    5636	:	20857	Brandan Timur	Babalan	Kab.	Langkat	Sumatera Utara	,\
    5637	:	20857	Brandan Timur Baru	Babalan	Kab.	Langkat	Sumatera Utara	,\
    5638	:	20857	Pelawi Selatan	Babalan	Kab.	Langkat	Sumatera Utara	,\
    5639	:	20857	Pelawi Utara	Babalan	Kab.	Langkat	Sumatera Utara	,\
    5640	:	20857	Securai Selatan	Babalan	Kab.	Langkat	Sumatera Utara	,\
    5641	:	20857	Securai Utara	Babalan	Kab.	Langkat	Sumatera Utara	,\
    5642	:	20857	Teluk Meku	Babalan	Kab.	Langkat	Sumatera Utara	,\
    5643	:	22747	Arse	Arse	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5644	:	22747	Arse Hanopan	Arse	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5645	:	22747	Lancat	Arse	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5646	:	22747	Nanggar Jati	Arse	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5647	:	22747	Nanggar Jati Hutapadang	Arse	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5648	:	22747	Natambang Roncitan	Arse	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5649	:	22747	Pardomuan	Arse	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5650	:	22747	Pinagar	Arse	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5651	:	22747	Pinagar	Arse	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5652	:	22747	Sipogu	Arse	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5653	:	22866	Aramo	Aramo	Kab.	Nias Selatan	Sumatera Utara	,\
    5654	:	22866	Bagoa	Aramo	Kab.	Nias Selatan	Sumatera Utara	,\
    5655	:	22866	Baohao	Aramo	Kab.	Nias Selatan	Sumatera Utara	,\
    5656	:	22866	Dao-dao	Aramo	Kab.	Nias Selatan	Sumatera Utara	,\
    5657	:	22866	Hiliadolowa	Aramo	Kab.	Nias Selatan	Sumatera Utara	,\
    5658	:	22866	Hiliamozula / Hiliamauzula	Aramo	Kab.	Nias Selatan	Sumatera Utara	,\
    5659	:	22866	Hilifadolo	Aramo	Kab.	Nias Selatan	Sumatera Utara	,\
    5660	:	22866	Hiligafoa	Aramo	Kab.	Nias Selatan	Sumatera Utara	,\
    5661	:	22866	Hiligumbu	Aramo	Kab.	Nias Selatan	Sumatera Utara	,\
    5662	:	22866	Hilimagiao	Aramo	Kab.	Nias Selatan	Sumatera Utara	,\
    5663	:	22866	Hilimbowo	Aramo	Kab.	Nias Selatan	Sumatera Utara	,\
    5664	:	22866	Hilimezaya	Aramo	Kab.	Nias Selatan	Sumatera Utara	,\
    5665	:	22866	Hilioru dua	Aramo	Kab.	Nias Selatan	Sumatera Utara	,\
    5666	:	22866	Hilisawato	Aramo	Kab.	Nias Selatan	Sumatera Utara	,\
    5667	:	22866	Hilitatao	Aramo	Kab.	Nias Selatan	Sumatera Utara	,\
    5668	:	22866	Hume	Aramo	Kab.	Nias Selatan	Sumatera Utara	,\
    5669	:	22866	Sikhorilafau	Aramo	Kab.	Nias Selatan	Sumatera Utara	,\
    5670	:	22866	Sisobambowo	Aramo	Kab.	Nias Selatan	Sumatera Utara	,\
    5671	:	22733	Batang Tura Sirumambe	Angkola Timur (Padang Sidempuan)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5672	:	22733	Gunung Manungkap	Angkola Timur (Padang Sidempuan)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5673	:	22733	Huraba	Angkola Timur (Padang Sidempuan)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5674	:	22733	Huta Ginjang	Angkola Timur (Padang Sidempuan)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5675	:	22733	Lantosan Rogas	Angkola Timur (Padang Sidempuan)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5676	:	22733	Marisi	Angkola Timur (Padang Sidempuan)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5677	:	22733	Pall Sebelas	Angkola Timur (Padang Sidempuan)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5678	:	22733	Panompuan	Angkola Timur (Padang Sidempuan)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5679	:	22733	Panompuan Jae	Angkola Timur (Padang Sidempuan)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5680	:	22733	Pargarutan Dolok	Angkola Timur (Padang Sidempuan)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5681	:	22733	Pargarutan Huta Baru	Angkola Timur (Padang Sidempuan)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5682	:	22733	Pargarutan Jae	Angkola Timur (Padang Sidempuan)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5683	:	22733	Pargarutan Julu	Angkola Timur (Padang Sidempuan)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5684	:	22733	Pargarutan Tonga	Angkola Timur (Padang Sidempuan)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5685	:	22733	Pasar Pargarutan	Angkola Timur (Padang Sidempuan)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5686	:	22733	Sanggapati	Angkola Timur (Padang Sidempuan)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5687	:	22733	Sijungkang	Angkola Timur (Padang Sidempuan)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5688	:	22733	Simandalu	Angkola Timur (Padang Sidempuan)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5689	:	22733	Siregar Matogu	Angkola Timur (Padang Sidempuan)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5690	:	22733	Sirumambe	Angkola Timur (Padang Sidempuan)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5691	:	22733	Sosopan Pargarutan	Angkola Timur (Padang Sidempuan)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5692	:	22733	Tabusira	Angkola Timur (Padang Sidempuan)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5693	:	22733	Tiang Aras	Angkola Timur (Padang Sidempuan)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5694	:	22732	Aek Natas	Angkola Selatan (Siais)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5695	:	22732	Dolok Gadang / Godang	Angkola Selatan (Siais)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5696	:	22732	Gunung Baringin	Angkola Selatan (Siais)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5697	:	22732	Napa	Angkola Selatan (Siais)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5698	:	22732	Pardomuan	Angkola Selatan (Siais)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5699	:	22732	Perkebunan Simarpinggan	Angkola Selatan (Siais)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5700	:	22732	Pintu Padang	Angkola Selatan (Siais)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5701	:	22732	Siamporik Dolok	Angkola Selatan (Siais)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5702	:	22732	Siamporik Lombang	Angkola Selatan (Siais)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5703	:	22732	Sibongbong	Angkola Selatan (Siais)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5704	:	22732	Sihopur	Angkola Selatan (Siais)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5705	:	22732	Sihuik Huik	Angkola Selatan (Siais)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5706	:	22732	Simarpinggan	Angkola Selatan (Siais)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5707	:	22732	Sinyior	Angkola Selatan (Siais)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5708	:	22732	Situmbaga	Angkola Selatan (Siais)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5709	:	22732	Tandihat	Angkola Selatan (Siais)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5710	:	22732	Tapian Nauli	Angkola Selatan (Siais)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5711	:	22735	Aek Pardomuan	Angkola Sangkunur	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5712	:	22735	Bandar Tarutung	Angkola Sangkunur	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5713	:	22735	Batu Godang	Angkola Sangkunur	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5714	:	22735	Malombu	Angkola Sangkunur	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5715	:	22735	Perkebunan	Angkola Sangkunur	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5716	:	22735	Rianiate	Angkola Sangkunur	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5717	:	22735	Sangkunur	Angkola Sangkunur	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5718	:	22735	Simataniari	Angkola Sangkunur	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5719	:	22735	Simatohir	Angkola Sangkunur	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5720	:	22735	Tindoan Laut	Angkola Sangkunur	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5721	:	22735	Aek Nabara	Angkola Barat (Padang Sidempuan)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5722	:	22735	Lembah Lubuk Manik	Angkola Barat (Padang Sidempuan)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5723	:	22735	Lobu Layan Sigordang	Angkola Barat (Padang Sidempuan)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5724	:	22735	Panobasan	Angkola Barat (Padang Sidempuan)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5725	:	22735	Parsalakan	Angkola Barat (Padang Sidempuan)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5726	:	22735	Sialogo	Angkola Barat (Padang Sidempuan)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5727	:	22735	Sibangkua	Angkola Barat (Padang Sidempuan)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5728	:	22735	Sigumuru	Angkola Barat (Padang Sidempuan)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5729	:	22735	Simatohir / Simatoir	Angkola Barat (Padang Sidempuan)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5730	:	22735	Simatorkis Sisoma	Angkola Barat (Padang Sidempuan)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5731	:	22735	Sisundung	Angkola Barat (Padang Sidempuan)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5732	:	22735	Sitinjak	Angkola Barat (Padang Sidempuan)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5733	:	22735	Siuhom	Angkola Barat (Padang Sidempuan)	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5734	:	22651	Bondar Sihudon I	Andam Dewi	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5735	:	22651	Bondar Sihudon II	Andam Dewi	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5736	:	22651	Ladang Tengah	Andam Dewi	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5737	:	22651	Lobu Tua	Andam Dewi	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5738	:	22651	Pangaribuan	Andam Dewi	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5739	:	22651	Rinabolak	Andam Dewi	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5740	:	22651	Sawah Lamo	Andam Dewi	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5741	:	22651	Sigolang	Andam Dewi	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5742	:	22651	Sijungkang	Andam Dewi	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5743	:	22651	Sirami Ramian	Andam Dewi	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5744	:	22651	Sitiris-Tiris	Andam Dewi	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5745	:	22651	Sogar	Andam Dewi	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5746	:	22651	Sosor Gonting	Andam Dewi	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5747	:	22651	Uratan	Andam Dewi	Kab.	Tapanuli Tengah	Sumatera Utara	,\
    5748	:	22866	Amandraya	Amandraya	Kab.	Nias Selatan	Sumatera Utara	,\
    5749	:	22866	Boholu	Amandraya	Kab.	Nias Selatan	Sumatera Utara	,\
    5750	:	22866	Hilifadolo	Amandraya	Kab.	Nias Selatan	Sumatera Utara	,\
    5751	:	22866	Hilihoru	Amandraya	Kab.	Nias Selatan	Sumatera Utara	,\
    5752	:	22866	Hilimaera	Amandraya	Kab.	Nias Selatan	Sumatera Utara	,\
    5753	:	22866	Hilimbowo	Amandraya	Kab.	Nias Selatan	Sumatera Utara	,\
    5754	:	22866	Hilimbulawa	Amandraya	Kab.	Nias Selatan	Sumatera Utara	,\
    5755	:	22866	Hilindraso	Amandraya	Kab.	Nias Selatan	Sumatera Utara	,\
    5756	:	22866	Hilisalo`o	Amandraya	Kab.	Nias Selatan	Sumatera Utara	,\
    5757	:	22866	Loloabolo	Amandraya	Kab.	Nias Selatan	Sumatera Utara	,\
    5758	:	22866	Lolomoyo	Amandraya	Kab.	Nias Selatan	Sumatera Utara	,\
    5759	:	22866	Lolozaria	Amandraya	Kab.	Nias Selatan	Sumatera Utara	,\
    5760	:	22866	Orahili Eho	Amandraya	Kab.	Nias Selatan	Sumatera Utara	,\
    5761	:	22866	Sifaoro`asi	Amandraya	Kab.	Nias Selatan	Sumatera Utara	,\
    5762	:	22866	Sinar Ino`o	Amandraya	Kab.	Nias Selatan	Sumatera Utara	,\
    5763	:	22866	Sirofi	Amandraya	Kab.	Nias Selatan	Sumatera Utara	,\
    5764	:	22866	Sisarahili	Amandraya	Kab.	Nias Selatan	Sumatera Utara	,\
    5765	:	22866	Sisobahili	Amandraya	Kab.	Nias Selatan	Sumatera Utara	,\
    5766	:	22866	Tuhemberua Amandraya	Amandraya	Kab.	Nias Selatan	Sumatera Utara	,\
    5767	:	22866	Tuindrao	Amandraya	Kab.	Nias Selatan	Sumatera Utara	,\
    5768	:	22866	Tuindrao Satu	Amandraya	Kab.	Nias Selatan	Sumatera Utara	,\
    5769	:	22814	Banua Sibohou III	Alasa Talumuzoi	Kab.	Nias Utara	Sumatera Utara	,\
    5770	:	22814	Harefanaese	Alasa Talumuzoi	Kab.	Nias Utara	Sumatera Utara	,\
    5771	:	22814	Hilimbowo Kare	Alasa Talumuzoi	Kab.	Nias Utara	Sumatera Utara	,\
    5772	:	22814	Hilina A	Alasa Talumuzoi	Kab.	Nias Utara	Sumatera Utara	,\
    5773	:	22814	Laehuwa	Alasa Talumuzoi	Kab.	Nias Utara	Sumatera Utara	,\
    5774	:	22814	Mazingo	Alasa Talumuzoi	Kab.	Nias Utara	Sumatera Utara	,\
    5775	:	22861	Anaoma	Alasa	Kab.	Nias Utara	Sumatera Utara	,\
    5776	:	22861	Banua Sibohou I	Alasa	Kab.	Nias Utara	Sumatera Utara	,\
    5777	:	22861	Banua Sibohou II	Alasa	Kab.	Nias Utara	Sumatera Utara	,\
    5778	:	22861	Bitaya	Alasa	Kab.	Nias Utara	Sumatera Utara	,\
    5779	:	22861	Dahana Alasa	Alasa	Kab.	Nias Utara	Sumatera Utara	,\
    5780	:	22861	Dahana Tugala Oyo	Alasa	Kab.	Nias Utara	Sumatera Utara	,\
    5781	:	22861	Fulolo	Alasa	Kab.	Nias Utara	Sumatera Utara	,\
    5782	:	22861	Hiligawoni	Alasa	Kab.	Nias Utara	Sumatera Utara	,\
    5783	:	22861	Lahemboho	Alasa	Kab.	Nias Utara	Sumatera Utara	,\
    5784	:	22861	Loloana`a	Alasa	Kab.	Nias Utara	Sumatera Utara	,\
    5785	:	22861	Ombolata	Alasa	Kab.	Nias Utara	Sumatera Utara	,\
    5786	:	22861	Ononamolo Alasa	Alasa	Kab.	Nias Utara	Sumatera Utara	,\
    5787	:	22861	Ononamolo Tumula	Alasa	Kab.	Nias Utara	Sumatera Utara	,\
    5788	:	22861	Siwabanua	Alasa	Kab.	Nias Utara	Sumatera Utara	,\
    5789	:	22386	Horsik	Ajibata	Kab.	Toba Samosir	Sumatera Utara	,\
    5790	:	22386	Motung	Ajibata	Kab.	Toba Samosir	Sumatera Utara	,\
    5791	:	22386	Pardamean Ajibata	Ajibata	Kab.	Toba Samosir	Sumatera Utara	,\
    5792	:	22386	Pardamean Sibisa	Ajibata	Kab.	Toba Samosir	Sumatera Utara	,\
    5793	:	22386	Pardomuan Ajibata	Ajibata	Kab.	Toba Samosir	Sumatera Utara	,\
    5794	:	22386	Pardomuan Motung	Ajibata	Kab.	Toba Samosir	Sumatera Utara	,\
    5795	:	22386	Parsaoran Ajibata	Ajibata	Kab.	Toba Samosir	Sumatera Utara	,\
    5796	:	22386	Parsaoran Sibisa	Ajibata	Kab.	Toba Samosir	Sumatera Utara	,\
    5797	:	22386	Sigapiton	Ajibata	Kab.	Toba Samosir	Sumatera Utara	,\
    5798	:	22386	Sirungkungon	Ajibata	Kab.	Toba Samosir	Sumatera Utara	,\
    5799	:	21256	Aras	Air Putih	Kab.	Batu Bara	Sumatera Utara	,\
    5800	:	21256	Indrapura Kota	Air Putih	Kab.	Batu Bara	Sumatera Utara	,\
    5801	:	21256	Indrasakti	Air Putih	Kab.	Batu Bara	Sumatera Utara	,\
    5802	:	21256	Kampung Kelapa	Air Putih	Kab.	Batu Bara	Sumatera Utara	,\
    5803	:	21256	Limau Sundai	Air Putih	Kab.	Batu Bara	Sumatera Utara	,\
    5804	:	21256	Pasar Lapan	Air Putih	Kab.	Batu Bara	Sumatera Utara	,\
    5805	:	21256	Pematang Panjang	Air Putih	Kab.	Batu Bara	Sumatera Utara	,\
    5806	:	21256	Perkotaan	Air Putih	Kab.	Batu Bara	Sumatera Utara	,\
    5807	:	21256	Sipare-Pare	Air Putih	Kab.	Batu Bara	Sumatera Utara	,\
    5808	:	21256	Sukaraja	Air Putih	Kab.	Batu Bara	Sumatera Utara	,\
    5809	:	21256	Tanah Merah	Air Putih	Kab.	Batu Bara	Sumatera Utara	,\
    5810	:	21256	Tanah Rendah	Air Putih	Kab.	Batu Bara	Sumatera Utara	,\
    5811	:	21256	Tanah Tinggi	Air Putih	Kab.	Batu Bara	Sumatera Utara	,\
    5812	:	21256	Tanjung Harapan	Air Putih	Kab.	Batu Bara	Sumatera Utara	,\
    5813	:	21256	Tanjung Kubah	Air Putih	Kab.	Batu Bara	Sumatera Utara	,\
    5814	:	21256	Tanjung Muda	Air Putih	Kab.	Batu Bara	Sumatera Utara	,\
    5815	:	21256	Tanjungmulya	Air Putih	Kab.	Batu Bara	Sumatera Utara	,\
    5816	:	21256	Titi Payung	Air Putih	Kab.	Batu Bara	Sumatera Utara	,\
    5817	:	21263	Air Joman	Air Joman	Kab.	Asahan	Sumatera Utara	,\
    5818	:	21263	Air Joman Baru	Air Joman	Kab.	Asahan	Sumatera Utara	,\
    5819	:	21263	Banjar	Air Joman	Kab.	Asahan	Sumatera Utara	,\
    5820	:	21263	Binjai Serbangan	Air Joman	Kab.	Asahan	Sumatera Utara	,\
    5821	:	21263	Pasar Lembu	Air Joman	Kab.	Asahan	Sumatera Utara	,\
    5822	:	21263	Punggulan	Air Joman	Kab.	Asahan	Sumatera Utara	,\
    5823	:	21263	Subur	Air Joman	Kab.	Asahan	Sumatera Utara	,\
    5824	:	21272	Air Genting	Air Batu	Kab.	Asahan	Sumatera Utara	,\
    5825	:	21272	Air Teluk Hessa	Air Batu	Kab.	Asahan	Sumatera Utara	,\
    5826	:	21272	Danau Sijabut	Air Batu	Kab.	Asahan	Sumatera Utara	,\
    5827	:	21272	Hessa Air Genting	Air Batu	Kab.	Asahan	Sumatera Utara	,\
    5828	:	21272	Hessa Perlompongan	Air Batu	Kab.	Asahan	Sumatera Utara	,\
    5829	:	21272	Perkebunan Air Batu I-II	Air Batu	Kab.	Asahan	Sumatera Utara	,\
    5830	:	21272	Perkebunan Air Batu III-IV	Air Batu	Kab.	Asahan	Sumatera Utara	,\
    5831	:	21272	Perkebunan Pulahan	Air Batu	Kab.	Asahan	Sumatera Utara	,\
    5832	:	21272	Pinanggiripan	Air Batu	Kab.	Asahan	Sumatera Utara	,\
    5833	:	21272	Pulau Pule	Air Batu	Kab.	Asahan	Sumatera Utara	,\
    5834	:	21272	Sei/Sungai Alim Ulu	Air Batu	Kab.	Asahan	Sumatera Utara	,\
    5835	:	21272	Sijabut Teratai	Air Batu	Kab.	Asahan	Sumatera Utara	,\
    5836	:	22857	Afulu	Afulu	Kab.	Nias Utara	Sumatera Utara	,\
    5837	:	22851	Faekhunaa	Afulu	Kab.	Nias Utara	Sumatera Utara	,\
    5838	:	22851	Harewakhe	Afulu	Kab.	Nias Utara	Sumatera Utara	,\
    5839	:	22851	Lauru Fadoro	Afulu	Kab.	Nias Utara	Sumatera Utara	,\
    5840	:	22851	Lauru I Afulu	Afulu	Kab.	Nias Utara	Sumatera Utara	,\
    5841	:	22851	Lauru Lahewa	Afulu	Kab.	Nias Utara	Sumatera Utara	,\
    5842	:	22851	Ombolata Afulu	Afulu	Kab.	Nias Utara	Sumatera Utara	,\
    5843	:	22851	Sifaoroasi	Afulu	Kab.	Nias Utara	Sumatera Utara	,\
    5844	:	22851	Sisobahili	Afulu	Kab.	Nias Utara	Sumatera Utara	,\
    5845	:	21274	Aek Bamban	Aek Songsongan	Kab.	Asahan	Sumatera Utara	,\
    5846	:	21274	Aek Songsongan	Aek Songsongan	Kab.	Asahan	Sumatera Utara	,\
    5847	:	21274	Lobu Rappa	Aek Songsongan	Kab.	Asahan	Sumatera Utara	,\
    5848	:	21274	Marjanji Aceh	Aek Songsongan	Kab.	Asahan	Sumatera Utara	,\
    5849	:	21274	Mekar Marjanji	Aek Songsongan	Kab.	Asahan	Sumatera Utara	,\
    5850	:	21274	Perkebunan Bandar Pulau	Aek Songsongan	Kab.	Asahan	Sumatera Utara	,\
    5851	:	21274	Perkebunan Bandar Selamat	Aek Songsongan	Kab.	Asahan	Sumatera Utara	,\
    5852	:	21274	Situnjak	Aek Songsongan	Kab.	Asahan	Sumatera Utara	,\
    5853	:	21274	Tangga	Aek Songsongan	Kab.	Asahan	Sumatera Utara	,\
    5854	:	21455	Adian Torop	Aek Natas	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    5855	:	21455	Bandar Durian	Aek Natas	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    5856	:	21455	Bandar Durian II	Aek Natas	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    5857	:	21455	Kampung Yaman	Aek Natas	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    5858	:	21455	Pangkalan	Aek Natas	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    5859	:	21455	Perkebunan Aek Pamingke	Aek Natas	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    5860	:	21455	Perkebunan Halim B	Aek Natas	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    5861	:	21455	Poldung	Aek Natas	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    5862	:	21455	Rombisan	Aek Natas	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    5863	:	21455	Sibito	Aek Natas	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    5864	:	21455	Simonis	Aek Natas	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    5865	:	21455	Terang Bulan	Aek Natas	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    5866	:	21455	Ujung Padang	Aek Natas	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    5867	:	22755	Aek Bonban	Aek Nabara Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5868	:	22755	Aek Buaton	Aek Nabara Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5869	:	22755	Aek Nabara Jae	Aek Nabara Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5870	:	22755	Aek Nabara Julu	Aek Nabara Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5871	:	22755	Aek Nabara Tonga	Aek Nabara Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5872	:	22755	Bangkuang	Aek Nabara Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5873	:	22755	Hadungdung Aek Rampa	Aek Nabara Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5874	:	22755	Hadungdung Pintu Padang	Aek Nabara Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5875	:	22755	Huta Bargot	Aek Nabara Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5876	:	22755	Janji Maria	Aek Nabara Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5877	:	22755	Marenu	Aek Nabara Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5878	:	22755	Padang Galugur Julu	Aek Nabara Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5879	:	22755	Padang Galugur Tonga	Aek Nabara Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5880	:	22755	Padang Garugur Jae	Aek Nabara Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5881	:	22755	Paran Julu	Aek Nabara Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5882	:	22755	Paran Tonga An	Aek Nabara Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5883	:	22755	Paya Bahung	Aek Nabara Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5884	:	22755	Sayur Mahincat	Aek Nabara Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5885	:	22755	Sayur Matua	Aek Nabara Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5886	:	22755	Sidokan	Aek Nabara Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5887	:	22755	Sipagabu	Aek Nabara Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5888	:	22755	Tanjung	Aek Nabara Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5889	:	22755	Tanjung Rokan	Aek Nabara Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5890	:	22755	Tobing	Aek Nabara Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5891	:	22755	Tobing Tinggi	Aek Nabara Barumun	Kab.	Padang Lawas	Sumatera Utara	,\
    5892	:	21273	Aek Bange	Aek Ledong	Kab.	Asahan	Sumatera Utara	,\
    5893	:	21273	Aek Korsik	Aek Ledong	Kab.	Asahan	Sumatera Utara	,\
    5894	:	21273	Aek Ledong	Aek Ledong	Kab.	Asahan	Sumatera Utara	,\
    5895	:	21273	Aek Nabuntu	Aek Ledong	Kab.	Asahan	Sumatera Utara	,\
    5896	:	21273	Ledong Barat	Aek Ledong	Kab.	Asahan	Sumatera Utara	,\
    5897	:	21273	Ledong Timur	Aek Ledong	Kab.	Asahan	Sumatera Utara	,\
    5898	:	21273	Padang Sipirok	Aek Ledong	Kab.	Asahan	Sumatera Utara	,\
    5899	:	21455	Aek Korsik	Aek Kuo	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    5900	:	21455	Bandar Selamat	Aek Kuo	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    5901	:	21455	Karang Ayer (Anyar)	Aek Kuo	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    5902	:	21455	Padang Maninjau	Aek Kuo	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    5903	:	21455	Perkebunan Padang Halaban	Aek Kuo	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    5904	:	21455	Perkebunan Panigoran	Aek Kuo	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    5905	:	21455	Purwo Rejo	Aek Kuo	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    5906	:	21455	Sidomulyo	Aek Kuo	Kab.	Labuhan Batu Utara	Sumatera Utara	,\
    5907	:	21273	Aek Loba	Aek Kuasan	Kab.	Asahan	Sumatera Utara	,\
    5908	:	21273	Aek Loba Afdeling I	Aek Kuasan	Kab.	Asahan	Sumatera Utara	,\
    5909	:	21273	Aek Loba Pekan	Aek Kuasan	Kab.	Asahan	Sumatera Utara	,\
    5910	:	21273	Alang Bombon (Bonbon)	Aek Kuasan	Kab.	Asahan	Sumatera Utara	,\
    5911	:	21273	Lobbu Jior (Lobu Jiur)	Aek Kuasan	Kab.	Asahan	Sumatera Utara	,\
    5912	:	21273	Rawa Sari	Aek Kuasan	Kab.	Asahan	Sumatera Utara	,\
    5913	:	21273	Sengon Sari	Aek Kuasan	Kab.	Asahan	Sumatera Utara	,\
    5914	:	22758	Aek Latong	Aek Bilah	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5915	:	22758	Aek Urat	Aek Bilah	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5916	:	22758	Biru	Aek Bilah	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5917	:	22758	Huta Baru	Aek Bilah	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5918	:	22758	Huta Tonga	Aek Bilah	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5919	:	22758	Lobu Tayas	Aek Bilah	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5920	:	22758	Sigolang	Aek Bilah	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5921	:	22758	Sihulambu	Aek Bilah	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5922	:	22758	Silangkitang	Aek Bilah	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5923	:	22758	Tapus Godang	Aek Bilah	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5924	:	22758	Tapus Sipagabu	Aek Bilah	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5925	:	22758	Tolang	Aek Bilah	Kab.	Tapanuli Selatan	Sumatera Utara	,\
    5926	:	22461	Adiankoting	Adian Koting	Kab.	Tapanuli Utara	Sumatera Utara	,\
    5927	:	22461	Banuaji I	Adian Koting	Kab.	Tapanuli Utara	Sumatera Utara	,\
    5928	:	22461	Banuaji II	Adian Koting	Kab.	Tapanuli Utara	Sumatera Utara	,\
    5929	:	22461	Banuaji IV	Adian Koting	Kab.	Tapanuli Utara	Sumatera Utara	,\
    5930	:	22461	Dolok Nauli	Adian Koting	Kab.	Tapanuli Utara	Sumatera Utara	,\
    5931	:	22461	Pagaran Lambung I	Adian Koting	Kab.	Tapanuli Utara	Sumatera Utara	,\
    5932	:	22461	Pagaran Lambung II	Adian Koting	Kab.	Tapanuli Utara	Sumatera Utara	,\
    5933	:	22461	Pagaran Lambung III	Adian Koting	Kab.	Tapanuli Utara	Sumatera Utara	,\
    5934	:	22461	Pagaran Lambung IV	Adian Koting	Kab.	Tapanuli Utara	Sumatera Utara	,\
    5935	:	22461	Pagaran Pisang	Adian Koting	Kab.	Tapanuli Utara	Sumatera Utara	,\
    5936	:	22461	Pansur Batu	Adian Koting	Kab.	Tapanuli Utara	Sumatera Utara	,\
    5937	:	22461	Pardomuan Nauli	Adian Koting	Kab.	Tapanuli Utara	Sumatera Utara	,\
    5938	:	22461	Siantar Nai Pospos	Adian Koting	Kab.	Tapanuli Utara	Sumatera Utara	,\
    5939	:	22461	Sibalanga	Adian Koting	Kab.	Tapanuli Utara	Sumatera Utara"
