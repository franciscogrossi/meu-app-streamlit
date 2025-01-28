import os
import streamlit as st
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# ==================================================
# DICIONÁRIO DE IDs DO FBREF (cole exatamente o seu)
# ==================================================
TIMES_JOGADORES_ID = {
    "Arsenal": {
        "William Saliba": "972aeb2a",
        "Gabriel Magalhães": "67ac5bb8",
        "Kai Havertz": "fed7cb61",
        "Thomas Partey": "529f49ab",
        "Jurriën Timber": "41034650",
        "Declan Rice": "1c7012b8",
        "Gabriel Martinelli": "48a5a5d6",
        "Leandro Trossard": "38ceb24a",
        "Martin Odegaard": "79300479",
        "Riccardo Calafiori": "aded8e6f",
        "Ben White": "35e413f1",
        "Mikel Merino": "d080ed5e",
        "Gabriel Jesus": "b66315ae",
        "Jorginho": "45db685d",
        "Myles Lewis-Skelly": "5dff6c28",
        "Jakub Kiwior": "dc3e663e",
        "Ethan Nwaneri": "7f94982c",
        "Oleksandr Zinchenko": "51cf8561"
    },
    "Aston Villa": {
        "Youri Tielemans": "56f7a928",
        "Morgan Rogers": "2e5915f1",
        "Pau Torres": "532e1e4f",
        "Ezri Konsa": "0313a347",
        "Lucas Digne": "1b84dbe1",
        "Ollie Watkins": "aed3a70f",
        "John McGinn": "90f91999",
        "Matty Cash": "2389cdc2",
        "Leon Bailey": "3a233281",
        "Amadou Onana": "828657ff",
        "Diego Carlos": "b4a014b1",
        "Boubacar Kamara": "cc77354e",
        "Jacob Ramsey": "1544f145",
        "Jhon Durán": "414184f7",
        "Ross Barkley": "3a24769f",
        "Lamare Bogarde": "bca5c4a7",
        "Jaden Philogene Bidace": "19f4d211",
        "Ian Maatsen": "cab9634e",
        "Tyrone Mings": "8397a50c",
        "Kosta Nedeljković": "c70be9cf",
        "Emi Buendía": "66b76d44",
        "Robin Olsen": "e7ee38c3"
    },
    "Bournemouth": {
        "Illia Zabarnyi": "88968486",
        "Milos Kerkez": "0ad53bdc",
        "Antoine Semenyo": "efd2ec23",
        "Lewis Cook": "2afc7272",
        "Ryan Christie": "26ce2263",
        "Evanilson": "6f3cc2fe",
        "Justin Kluivert": "4c3a6744",
        "Marcus Tavernier": "5c0da4a4",
        "Adam Smith": "20b104bc",
        "Marcos Senesi": "35141f4c",
        "Dean Huijsen": "87278bce",
        "Dango Ouattara": "2f9e4435",
        "Tyler Adams": "2b09d998",
        "Julian Araujo": "8f4541c2",
        "David Brooks": "dc4cae05",
        "James Hill": "69942fb3",
        "Enes Ünal": "f8eca1b6",
        "Alex Scott": "104d0bb8",
        "Luis Sinisterra": "8e16dd48",
        "Philip Billing": "d328a254"
    },
    "Brentford": {
        "Nathan Collins": "a8c19eb8",
        "Bryan Mbeumo": "6afaebf2",
        "Keane Lewis-Potter": "41f08ac8",
        "Mikkel Damsgaard": "215f3907",
        "Christian Norgaard": "df0a4c90",
        "Vitaly Janelt": "8449d35e",
        "Yoane Wissa": "2500cef9",
        "Ethan Pinnock": "e541326e",
        "Sepp van den Berg": "7bf9400b",
        "Kevin Schade": "52afb588",
        "Mads Roerslev": "57c94db2",
        "Kristoffer Ajer": "a8c0acb7",
        "Mathias Jensen": "0f134faf",
        "Yehor Yarmoliuk": "907a5d7c",
        "Fabio Carvalho": "966e28d0",
        "Ben Mee": "8df7a2fb",
        "Thiago": "dc45ac24",
        "Edmond-Paris Maghoma": "8a3ddcd2",
        "Yunus Emre Konak": "e02b5b36"
    },
    "Brighton": {
        "Kaoru Mitoma": "74618572",
        "Jan Paul van Hecke": "4fd08daa",
        "Carlos Baleba": "a1390d2f",
        "Lewis Dunk": "282f75f3",
        "Joel Veltman": "dad4b285",
        "Pervis Estupiñán": "d38fdf53",
        "Danny Welbeck": "ce5143da",
        "Georginio Rutter": "c64c01fc",
        "João Pedro": "e8832875",
        "Yasin Ayari": "f173303a",
        "Jack Hinshelwood": "e98211e7",
        "Igor Júlio": "a4e85758",
        "Yankuba Minteh": "c3cf087d",
        "Simon Adingra": "4dcec659",
        "Ferdi Kadioglu": "66c52a77",
        "Mats Wieffer": "4876c9ab",
        "Matt O'Riley": "fb495bb8",
        "Tariq Lamptey": "f4e433d4",
        "Brajan Gruda": "ae9b998d",
        "James Milner": "2f90f6b8",
        "Julio Enciso": "9cfbad36",
        "Evan Ferguson": "4596da74",
        "Adam Webster": "c40b6180",
        "Billy Gilmour": "df10e27c",
        "Jakub Moder": "f230bc30",
        "Jeremy Sarmiento": "ac0d576d",
        "Solly March": "bb5fbd2b"
    },
    "Chelsea": {
        "Moisés Caicedo": "16264a81",
        "Cole Palmer": "dc7f8a28",
        "Levi Colwill": "700783e7",
        "Nicolas Jackson": "9c36ed83",
        "Marc Cucurella": "1daec722",
        "Enzo Fernández": "5ff4ab71",
        "Noni Madueke": "bf34eebd",
        "Malo Gusto": "d56b9520",
        "Wesley Fofana": "132a82f1",
        "Jadon Sancho": "dbf053da",
        "Pedro Neto": "7ba2eaa9",
        "Roméo Lavia": "ecad9aa5",
        "Tosin Adarabioyo": "c81d773d",
        "Axel Disasi": "ad82197c",
        "Christopher Nkunku": "7c56da38",
        "João Félix": "8aafd64f",
        "Reece James": "1265a93a",
        "Benoît Badiashile": "06df8256",
        "Joshua Acheampong": "b7e62e1d",
        "Renato Veiga": "fc8fcbd1",
        "Mykhailo Mudryk": "049a888d",
        "Kiernan Dewsbury-Hall": "5c74c0f5",
        "Marc Guiu": "d3d774cc"
    },
    "Crystal Palace": {
        "Tyrick Mitchell": "5cbd1eb0",
        "Marc Guéhi": "d0706b27",
        "Daniel Muñoz": "778ef829",
        "Jean-Philippe Mateta": "50e6dc35",
        "Maxence Lacroix": "277c49ed",
        "Eberechi Eze": "ae4fc6a4",
        "Ismaila Sarr": "bfdb33aa",
        "Will Hughes": "a0666d3e",
        "Jefferson Lerma": "9b5ce51a",
        "Trevoh Chalobah": "5515376c",
        "Daichi Kamada": "15b287da",
        "Chris Richards": "0a3d6d2b",
        "Adam Wharton": "4b542852",
        "Eddie Nketiah": "a53649b7",
        "Cheick Doucouré": "ce4f40c7",
        "Nathaniel Clyne": "0442183b",
        "Justin Devenny": "6c2b66fc",
        "Odsonne Édouard": "0562b7f1",
        "Joachim Andersen": "e34fc66d",
        "Chadi Riad": "b3b9b8b8",
        "Jeffrey Schlupp": "3312f911",
        "Jordan Ayew": "da052c14"
    },
    "Everton": {
        "James Tarkowski": "15ea812b",
        "Iliman Ndiaye": "5ed97752",
        "Vitaliy Mykolenko": "30d4a2e5",
        "Idrissa Gana Gueye": "72c812f3",
        "Dominic Calvert-Lewin": "59e6e5bf",
        "Ashley Young": "be927d03",
        "Abdoulaye Doucouré": "02b29014",
        "Dwight McNeil": "fc15fb84",
        "Orel Mangala": "a572e291",
        "Jack Harrison": "aa849a12",
        "Jarrad Branthwaite": "c1949191",
        "Michael Keane": "c5b7c315",
        "Jesper Lindstrom": "37dc1a48",
        "Tim Iroegbunam": "84c5ceea",
        "James Garner": "4e015693",
        "Séamus Coleman": "0420d84f",
        "Armando Broja": "97220da2",
        "Beto": "ed5c0319",
        "Roman Dixon": "6fba4dba",
        "Nathan Patterson": "230f0471",
        "Harrison Armstrong": "de59e609",
        "Jake O'Brien": "25f2ef01"
    },
    "Fulham": {
        "Antonee Robinson": "289601e6",
        "Alex Iwobi": "6ca5ec4b",
        "Calvin Bassey": "a36524bf",
        "Raúl Jiménez": "b561db50",
        "Andreas Pereira": "6639e500",
        "Kenny Tete": "77d7c96f",
        "Saša Lukić": "c6e8cf1f",
        "Emile Smith Rowe": "17695062",
        "Issa Diop": "a712ca2b",
        "Joachim Andersen": "e34fc66d",
        "Adama Traoré": "9a28eba4",
        "Sander Berge": "d0b6129f",
        "Harry Wilson": "c6dc9ecd",
        "Timothy Castagne": "197640fd",
        "Rodrigo Muniz": "a755db8c",
        "Reiss Nelson": "c5bdb6e3",
        "Tom Cairney": "a8748947",
        "Jorge Cuenca": "0abc51f2",
        "Joshua King": "86109b3b",
        "Harrison Reed": "803ae100",
        "Martial Godo": "e0eea46f",
        "Ryan Sessegnon": "6aa3e78b",
        "Carlos Vinícius": "8b529245",
        "Jay Stansfield": "b2626673",
        "Samuel Amissah": "2835bfe1"
    },
    "Ipswich Town": {
        "Leif Davis": "8574c61f",
        "Sam Morsy": "a23c0949",
        "Omari Hutchinson": "bd9553e6",
        "Liam Delap": "dd897ee7",
        "Dara O'Shea": "1d042188",
        "Sammie Szmodics": "39944392",
        "Jacob Greaves": "1f169636",
        "Jens Cajuste": "928a4a61",
        "Wes Burns": "b3fe23c6",
        "Cameron Burgess": "da61ca98",
        "Axel Tuanzebe": "2baec6ce",
        "Kalvin Phillips": "4f565d77",
        "Ben Johnson": "9319781b",
        "Luke Woolfenden": "e28e9bec",
        "Conor Chaplin": "4ec55b87",
        "Jack Clarke": "e16932d8",
        "Harry Clarke": "a64f2573",
        "Chiedozie Ogbene": "788c0277",
        "Nathan Broadhead": "43309491",
        "Massimo Luongo": "967ac6e1",
        "Jack Taylor": "48eed8d5",
        "George Hirst": "78e87179",
        "Ali Al Hamadi": "8450467d",
        "Marcus Harness": "90e9ca3d",
        "George Edmundson": "46ff3923",
        "Conor Townsend": "4dc4f138"
    },
    "Leicester City": {
        "James Justin": "fb614c44",
        "Jamie Vardy": "45963054",
        "Victor Bernth Kristiansen": "505486d6",
        "Wilfred Ndidi": "6b47c5db",
        "Wout Faes": "9c221d14",
        "Harry Winks": "2f7acede",
        "Stephy Mavididi": "30144daa",
        "Facundo Buonanotte": "468a7a91",
        "Jannik Vestergaard": "1900032e",
        "Bilal El Khannouss": "f7042636",
        "Boubakary Soumaré": "ae59b359",
        "Jordan Ayew": "da052c14",
        "Caleb Okoli": "8ec109e6",
        "Conor Coady": "2928dca2",
        "Oliver Skipp": "6250083a",
        "Abdul Fatawu Issahaku": "bceda5ff",
        "Kasey McAteer": "b2c66859",
        "Bobby Reid": "0f7533cd",
        "Luke Thomas": "fc027d02",
        "Ricardo Pereira": "75a72a99",
        "Patson Daka": "ca45605e",
        "Danny Ward": "d3ce0e89",
        "Hamza Choudhury": "7d2d3329",
        "Odsonne Édouard": "0562b7f1",
        "Will Alves": "39ef5a7b"
    },
    "Liverpool": {
        "Virgil van Dijk": "e06683ca",
        "Mohamed Salah": "e342ad68",
        "Ryan Gravenberch": "b8e740fb",
        "Trent Alexander-Arnold": "cd1acf9d",
        "Andrew Robertson": "2e4f5f03",
        "Alexis Mac Allister": "83d074ff",
        "Luis Díaz": "4a1a9578",
        "Dominik Szoboszlai": "934e1968",
        "Ibrahima Konaté": "5ed9b537",
        "Cody Gakpo": "1971591f",
        "Curtis Jones": "4fb9c88f",
        "Darwin Núñez": "4d77b365",
        "Diogo Jota": "178ae8f8",
        "Joe Gomez": "7a11550b",
        "Kostas Tsimikas": "f315ca93",
        "Jarell Quansah": "4125cb98",
        "Conor Bradley": "bbd67769",
        "Wataru Endo": "c149016b",
        "Harvey Elliott": "b9e1436c",
        "Federico Chiesa": "b0f7e36c",
        "Vitezslav Jaros": "12bb4d6a"
    },
    "Manchester City": {
        "Erling Haaland": "1f44ac21",
        "Joško Gvardiol": "5ad50391",
        "Bernardo Silva": "3eb22ec9",
        "Manuel Akanji": "89ac64a6",
        "Rico Lewis": "b57e066e",
        "Mateo Kovačić": "79c0821a",
        "İlkay Gündoğan": "819b3158",
        "Sávio": "fe6e7156",
        "Phil Foden": "ed1e53f3",
        "Rúben Dias": "31c69ef1",
        "Kevin De Bruyne": "e46012d4",
        "Kyle Walker": "86dd77d1",
        "Jeremy Doku": "fffea3e5",
        "Matheus Nunes": "e6af02e0",
        "Nathan Aké": "eaeca114",
        "Jack Grealish": "b0b4fd3e",
        "John Stones": "5eecec3d",
        "Rodri": "6434f10d"
    },
    "Manchester Utd": {
        "Diogo Dalot": "d9565625",
        "Bruno Fernandes": "507c7bdf",
        "Noussair Mazraoui": "b74277a0",
        "Lisandro Martínez": "bac46a10",
        "Matthijs de Ligt": "d6e53a3a",
        "Amad Diallo": "9dc96f10",
        "Kobbie Mainoo": "c6220452",
        "Marcus Rashford": "a1d5bd30",
        "Rasmus Højlund": "491a433d",
        "Alejandro Garnacho": "7aa8adfe",
        "Casemiro": "4d224fe8",
        "Harry Maguire": "d8931174",
        "Manuel Ugarte": "c9817014",
        "Joshua Zirkzee": "028e70b9",
        "Christian Eriksen": "980522ec",
        "Mason Mount": "9674002f",
        "Jonny Evans": "f8fcd2a5",
        "Leny Yoro": "6763f716",
        "Tyrell Malacia": "6b6c793c",
        "Antony": "99127249",
        "Luke Shaw": "9c94165b",
        "Victor Lindelöf": "f5deef4c"
    },
    "Newcastle Utd": {
        "Bruno Guimarães": "82518f62",
        "Dan Burn": "b2d31e83",
        "Joelinton": "c17bfb65",
        "Anthony Gordon": "2bd83368",
        "Alexander Isak": "8e92be30",
        "Lewis Hall": "da011f18",
        "Fabian Schär": "c8aa95da",
        "Valentino Livramento": "afed6722",
        "Jacob Murphy": "de112b84",
        "Sandro Tonali": "0db169ae",
        "Sean Longstaff": "a2b105e0",
        "Harvey Barnes": "3ea50f67",
        "Joe Willock": "a3b03921",
        "Kieran Trippier": "21512407",
        "Lloyd Kelly": "f31def1e",
        "Emil Krafth": "77cf6852",
        "Sven Botman": "ccce7025",
        "Miguel Almirón": "862a1c15",
        "Callum Wilson": "c596fcb0",
        "William Osula": "7b355808",
        "Lewis Miley": "2c6835e5",
        "Matt Targett": "e514ab62"
    },
    "Nott'ham Forest": {
        "Ola Aina": "246d153b",
        "Nikola Milenković": "bee704fc",
        "Murillo": "1704b0b8",
        "Chris Wood": "4e9a0555",
        "Callum Hudson-Odoi": "15f3ec41",
        "Morgan Gibbs-White": "32f60ed8",
        "Elliot Anderson": "de31038e",
        "Anthony Elanga": "2fba6108",
        "Ryan Yates": "c1fe2a48",
        "Neco Williams": "dd323728",
        "Nicolás Domínguez": "20b3a502",
        "Álex Moreno": "16e9d0ea",
        "James Ward-Prowse": "3515d404",
        "Jota Silva": "4d77e622",
        "Ibrahim Sangaré": "bced0375",
        "Morato": "0f41e2ee",
        "Taiwo Awoniyi": "e5478b87",
        "Ramón Sosa": "2d3417a1",
        "Willy Boly": "a4ac4b8f",
        "Danilo": "a816dbfb",
        "Harry Toffolo": "a105d46a",
        "Eric da Silva Moreira": "0a4f579a"
    },
    "Southampton": {
        "Kyle Walker-Peters": "984a5a64",
        "Taylor Harwood-Bellis": "47327321",
        "Jan Bednarek": "4115ce4e",
        "Mateus Fernandes": "ef491564",
        "Flynn Downes": "69fdb896",
        "Tyler Dibling": "bdcc89ae",
        "Adam Armstrong": "68c720b5",
        "Joe Aribo": "328f7d51",
        "Yukinari Sugawara": "580bcd18",
        "Jack Stephens": "6adbc307",
        "Cameron Archer": "05e8ca6d",
        "Ryan Manning": "847b53eb",
        "Nathan Wood-Gordon": "4ccf2d5b",
        "Lesley Ugochukwu": "1df4a109",
        "James Bree": "c07b7c5c",
        "Adam Lallana": "99813635",
        "Ben Brereton": "57827369",
        "Paul Onuachu": "c06d1086",
        "Ryan Fraser": "d56543a0",
        "William Smallbone": "5e105217",
        "Kamaldeen Sulemana": "a62f8bf1",
        "Charlie Taylor": "cc2d7ad5"
    },
    "Tottenham": {
        "Dejan Kulusevski": "df3cda47",
        "Pedro Porro": "27d0a506",
        "Dominic Solanke": "e77dc3b2",
        "Destiny Udogie": "7cd520e8",
        "Brennan Johnson": "0cd31129",
        "Son Heung-min": "92e7e919",
        "James Maddison": "ee38d9c5",
        "Pape Matar Sarr": "feb5d972",
        "Radu Drăgușin": "620922ed",
        "Cristian Romero": "a3d94a58",
        "Yves Bissouma": "6c203af0",
        "Micky van de Ven": "8fe2a392",
        "Rodrigo Bentancur": "3b8674e6",
        "Archie Gray": "f58515f5",
        "Djed Spence": "9bc9a519",
        "Timo Werner": "49fe9070",
        "Lucas Bergvall": "a109e5c8",
        "Ben Davies": "44781702",
        "Wilson Odobert": "35516eac",
        "Mikey Moore": "00953a9d",
        "Richarlison": "fa031b34",
        "Sergio Reguilón": "3353737a"
    },
    "West Ham": {
        "Max Kilman": "d0f72bf1",
        "Aaron Wan-Bissaka": "9e525177",
        "Jarrod Bowen": "79c84d1c",
        "Emerson Palmieri": "e0bc6fdc",
        "Lucas Paquetá": "9b6f7fd5",
        "Tomáš Souček": "6613c819",
        "Mohammed Kudus": "b62878a5",
        "Konstantinos Mavropanos": "00963611",
        "Guido Rodríguez": "34e393f2",
        "Edson Álvarez": "8b3ab7ad",
        "Michail Antonio": "ac05f970",
        "Carlos Soler": "fed17f5a",
        "Jean-Clair Todibo": "88f130ed",
        "Crysencio Summerville": "df04eb4b",
        "Vladimír Coufal": "fdf3cb77",
        "Niclas Füllkrug": "4f16405e",
        "Danny Ings": "07802f7f",
        "Andy Irving": "b1be9fc0",
        "Aaron Cresswell": "4f974391",
        "Oliver Scarles": "242e5e6d",
        "Luis Guilherme": "b7672d43"
    },
    "Wolves": {
        "Rayan Aït-Nouri": "9b398aea",
        "Jørgen Strand Larsen": "f553b2b3",
        "João Gomes": "8b57ad2c",
        "Matheus Cunha": "dc62b55d",
        "Nélson Semedo": "d04b94db",
        "Mario Lemina": "2b471f99",
        "Toti Gomes": "f0caab96",
        "André": "ec604e2c",
        "Santiago Bueno": "edc98fac",
        "Craig Dawson": "3e9e06cb",
        "Matt Doherty": "d557d734",
        "Jean-Ricner Bellegarde": "10f0fdd3",
        "Rodrigo Gomes": "8dcf77c0",
        "Gonçalo Guedes": "e6bc67d7",
        "Hwang Hee-chan": "169fd162",
        "Yerson Mosquera": "1e159d70",
        "Tommy Doyle": "5526deb1",
        "Pablo Sarabia": "9744ff80",
        "Carlos Forbs": "8a310070"
    },
}

# ==================================================
# CONFIG DE ESTATÍSTICAS (versão em inglês)
# ==================================================
# - "Finalizações": subpath vazio e coluna "Sh"
# - "Faltas Cometidas": subpath "misc" e coluna "Fls"
STATS_CONFIG = {
    "Finalizações": {
        "subpath": "",
        "colunas_necessarias": {"Date", "Squad", "Opponent", "Venue", "Sh", "Min", "Comp"},
        "nome_coluna_fbref": "Sh",
        "nome_coluna_final": "Finalizacoes",
    },
    "Faltas Cometidas": {
        "subpath": "misc",
        "colunas_necessarias": {"Date", "Squad", "Opponent", "Venue", "Fls", "Min", "Comp"},
        "nome_coluna_fbref": "Fls",
        "nome_coluna_final": "Faltas",
    },
}

# --------------------------------------------------
# FUNÇÃO DE RASPAGEM (COM CACHE) - SELENIUM
# --------------------------------------------------
@st.cache_data(ttl=600, show_spinner=False)
def scrape_fbref(slug, nome_jogador, subpath, colunas_necessarias, nome_coluna_fbref, nome_coluna_final):
    if subpath:
        url = f"https://fbref.com/en/players/{slug}/matchlogs/2024-2025/{subpath}/{nome_jogador}-Match-Logs"
    else:
        url = f"https://fbref.com/en/players/{slug}/matchlogs/2024-2025/{nome_jogador}-Match-Logs"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    if os.path.exists('/usr/bin/chromium'):
        chrome_options.binary_location = '/usr/bin/chromium'

    service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    time.sleep(4)

    try:
        show_unused_button = driver.find_element(By.PARTIAL_LINK_TEXT, "Show matches as unused substitute")
        show_unused_button.click()
        time.sleep(2)
    except:
        pass

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    all_dfs = pd.read_html(str(soup))
    lista_validas = []
    for df_temp in all_dfs:
        if isinstance(df_temp.columns, pd.MultiIndex):
            df_temp.columns = df_temp.columns.droplevel(0)
        if colunas_necessarias.issubset(df_temp.columns):
            lista_validas.append(df_temp)

    if not lista_validas:
        return pd.DataFrame()

    df = pd.concat(lista_validas, ignore_index=True)
    invalid = ["Date", "Opponent", "Venue", "Performance", "None"]
    df = df[~df["Date"].isin(invalid)]

    colunas_para_manter = ["Date", "Comp", "Squad", "Opponent", "Venue", "Min"]
    if nome_coluna_fbref not in colunas_para_manter:
        colunas_para_manter.append(nome_coluna_fbref)
    df = df[colunas_para_manter]

    renomes = {
        "Date": "Data",
        "Comp": "Competicao",
        "Squad": "Equipe",
        "Opponent": "Adversario",
        "Venue": "CasaFora",
        "Min": "Minutos",
        nome_coluna_fbref: nome_coluna_final
    }
    df.rename(columns=renomes, inplace=True)

    return df

# --------------------------------------------------
# CARREGAR CSV OFFLINE (OPCIONAL)
# --------------------------------------------------
def load_offline_data(csv_path: str) -> pd.DataFrame:
    if not os.path.exists(csv_path):
        return pd.DataFrame()
    return pd.read_csv(csv_path)

# --------------------------------------------------
# CSS PERSONALIZADO - SEM .container
# --------------------------------------------------
PAGE_CSS = """
<style>
html, body, [class*="css"] {
    font-size: 16px; /* Ajuste como preferir */
    font-family: "Open Sans", sans-serif;
    background-color: #f9f9f9;
}

/* Manter h1 grande em comparação ao resto */
h1 {
    font-size: 2em; /* Ajuste como preferir p/ destacar */
    margin: 0.3em 0 0.2em 0; 
    color: #2B2B2B;
}

h2, h3 {
    color: #2B2B2B;
}

hr {
    margin: 2rem 0;
}

/* Tabela Personalizada */
.custom-table {
    border-collapse: collapse;
    width: 100%;
    margin: 1rem 0;
}
.custom-table th {
    background-color: #f5f5f5;
    font-weight: bold;
}
.custom-table, .custom-table th, .custom-table td {
    border: 1px solid #ccc;
    padding: 8px;
    text-align: center;
}
.custom-table tbody tr:hover {
    background-color: #f0f0f0;
}

/* Responsivo */
@media only screen and (max-width: 768px) {
    html, body, [class*="css"] {
        font-size: 12px; 
    }
    .custom-table td, .custom-table th {
        padding: 6px !important;
        font-size: 12px;
    }
}
@media only screen and (max-width: 480px) {
    html, body, [class*="css"] {
        font-size: 11px;
    }
    .custom-table td, .custom-table th {
        padding: 4px !important;
        font-size: 10px;
    }
}

/* Remove Streamlit's default menu and footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""

st.set_page_config(page_title="Análise - Premier League", layout="wide")
st.markdown(PAGE_CSS, unsafe_allow_html=True)

# --------------------------------------------------
# TÍTULO (SEM Beta, SEM SUBTÍTULO)
# --------------------------------------------------
st.markdown("<h1>Análise - Premier League</h1>", unsafe_allow_html=True)

# --------------------------------------------------
# APP PRINCIPAL
# --------------------------------------------------
if "df_jogos" not in st.session_state:
    st.session_state["df_jogos"] = pd.DataFrame()
if "estatistica_selecionada" not in st.session_state:
    st.session_state["estatistica_selecionada"] = ""

col1, col2, col3, col4 = st.columns([3, 3, 2, 1])
with col1:
    time_selecionado = st.selectbox("Selecione o Time", list(TIMES_JOGADORES_ID.keys()))
with col2:
    jogador = st.selectbox("Selecione o Jogador", list(TIMES_JOGADORES_ID[time_selecionado].keys()))
with col3:
    estatistica = st.selectbox("Estatística", list(STATS_CONFIG.keys()))
with col4:
    num_jogos = st.slider("Jogos Analisados", 1, 30, 10)

usar_offline = st.checkbox("Usar Dados Offline (CSV)?", value=False)

if st.button("Analisar"):
    st.session_state["estatistica_selecionada"] = estatistica

    config = STATS_CONFIG[estatistica]
    slug = TIMES_JOGADORES_ID[time_selecionado][jogador]
    nome_para_url = jogador.replace(" ", "-")

    with st.spinner("⚽ Buscando informações do jogador..."):
        if usar_offline:
            csv_name = f"dados_offline_{time_selecionado}_{jogador}_{estatistica}.csv"
            csv_name = csv_name.replace(" ", "_")
            df = load_offline_data(csv_name)
        else:
            df = scrape_fbref(
                slug=slug,
                nome_jogador=nome_para_url,
                subpath=config["subpath"],
                colunas_necessarias=config["colunas_necessarias"],
                nome_coluna_fbref=config["nome_coluna_fbref"],
                nome_coluna_final=config["nome_coluna_final"],
            )

    if df.empty:
        st.error("Nenhum dado encontrado (DF vazio).")
        st.session_state["df_jogos"] = pd.DataFrame()
    else:
        # Filtra somente Premier League
        df = df[df["Competicao"] == "Premier League"]

        # Remove jogadores sem minutos
        df["Minutos"] = pd.to_numeric(df["Minutos"], errors="coerce").fillna(0).astype(int)
        df = df[df["Minutos"] != 0]

        # Converte a estatística principal
        nome_coluna_principal = config["nome_coluna_final"]
        df[nome_coluna_principal] = (
            pd.to_numeric(df[nome_coluna_principal], errors="coerce")
            .fillna(0)
            .astype(int)
        )

        # Ordena datas desc
        df["Data"] = pd.to_datetime(df["Data"])
        df.sort_values("Data", ascending=False, inplace=True)
        df.reset_index(drop=True, inplace=True)

        # Pega só os últimos N jogos
        df = df.head(num_jogos)
        df.index = df.index + 1

        # Converte data e local
        df["Data"] = df["Data"].dt.strftime("%d/%m/%y")
        df["CasaFora"] = df["CasaFora"].replace({
            "Home": "Casa",
            "Away": "Fora",
            "Neutral": "Neutro"
        })

        # Se ainda existir a coluna Equipe, remove
        if "Equipe" in df.columns:
            df.drop(columns=["Equipe"], inplace=True)

        st.session_state["df_jogos"] = df

# --------------------------------------------------
# EXIBIÇÃO DOS RESULTADOS
# --------------------------------------------------
df_jogos = st.session_state["df_jogos"]
estatistica_escolhida = st.session_state["estatistica_selecionada"]

if not df_jogos.empty:
    st.markdown("<hr>", unsafe_allow_html=True)
    filtro_local = st.radio("Filtrar Jogos (Casa ou Fora)?", ["Todos", "Casa", "Fora"], index=0)
    df_filtrado = df_jogos.copy()
    if filtro_local != "Todos":
        df_filtrado = df_filtrado[df_filtrado["CasaFora"] == filtro_local]

    if df_filtrado.empty:
        st.warning("Nenhum jogo encontrado neste filtro.")
    else:
        df_filtrado.reset_index(drop=True, inplace=True)
        df_filtrado.index = df_filtrado.index + 1

        # Mostra a tabela
        tabela_html = df_filtrado.to_html(classes="custom-table", index=True, border=0, justify="center")
        st.markdown(tabela_html, unsafe_allow_html=True)

        if estatistica_escolhida:
            nome_coluna_principal = STATS_CONFIG[estatistica_escolhida]["nome_coluna_final"]
        else:
            nome_coluna_principal = "Valor"

        media_valor = df_filtrado[nome_coluna_principal].mean()
        st.markdown(
            f"<p><strong>Média de {estatistica_escolhida} (Filtro):</strong> {media_valor:.2f}</p>",
            unsafe_allow_html=True
        )

        # Tabela Over
        over_lines = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5]
        total_jogos = len(df_filtrado)
        resultados = []
        for line in over_lines:
            count = sum(df_filtrado[nome_coluna_principal] > line)
            prob = count / total_jogos if total_jogos else 0
            odd_justa = f"{(1/prob):.2f}" if prob > 0 else "∞"
            resultados.append({
                "Linha Over": f"Mais de {line}",
                "Jogos Over": count,
                "Probabilidade": f"{prob:.2%}",
                "Odd Justa": odd_justa
            })

        df_overs = pd.DataFrame(resultados)
        overs_html = df_overs.to_html(classes="custom-table", index=False, border=0, justify="center")
        st.markdown(f"<h4>Estatísticas de Over - {estatistica_escolhida}</h4>", unsafe_allow_html=True)
        st.markdown(overs_html, unsafe_allow_html=True)
