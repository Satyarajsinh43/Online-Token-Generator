import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'token_generator.settings')
django.setup()

from api.models import Department, Service, Counter, Token, District, Taluka, Village, Office

def seed():
    print("Seeding data...")

    # Data Structure: District -> [Talukas]
    gujarat_data = {
        "Ahmedabad": ["Ahmedabad City", "Bavla", "Daskroi", "Detroj-Rampura", "Dhandhuka", "Dholera", "Dholka", "Mandal", "Sanand", "Viramgam"],
        "Amreli": ["Amreli", "Babra", "Bagasara", "Dhari", "Jafrabad", "Khambha", "Lathi", "Lilia", "Mahuva", "Rajula", "Savarkundla", "Vadia"],
        "Anand": ["Anand", "Anklav", "Borsad", "Khambhat", "Petlad", "Sojitra", "Tarapur", "Umreth"],
        "Aravalli": ["Bayad", "Bhiloda", "Dhansura", "Malpur", "Modasa", "Megraj"],
        "Banaskantha": ["Amirgadh", "Bhabhar", "Danta", "Dantiwada", "Deesa", "Deodar", "Kankrej", "Lakhani", "Palanpur", "Tharad", "Vadgam", "Vav"],
        "Bharuch": ["Amod", "Ankleshwar", "Bharuch", "Hansot", "Jambusar", "Jhagadia", "Netrang", "Vagra", "Valia"],
        "Bhavnagar": ["Bhavnagar", "Gariyadhar", "Ghogha", "Jesar", "Mahuva", "Palitana", "Sihor", "Talaja", "Umrala", "Vallabhipur"],
        "Botad": ["Botad", "Barwala", "Gadhada", "Ranpur"],
        "Chhota Udaipur": ["Bodeli", "Chhota Udaipur", "Jetpur Pavi", "Kavant", "Naswadi", "Sankheda"],
        "Dahod": ["Dahod", "Fatepura", "Garbad", "Limkheda", "Jhalod", "Randhikpur", "Singvad", "Devgadh Baria"],
        "Dang": ["Ahwa", "Subir", "Waghai"],
        "Devbhoomi Dwarka": ["Bhanvad", "Dwarka", "Kalyanpur", "Khambhalia"],
        "Gandhinagar": ["Gandhinagar", "Kalol", "Mansa", "Dehgam"],
        "Gir Somnath": ["Gir Gadhada", "Kodinar", "Sutrapada", "Talala", "Una", "Veraval"],
        "Jamnagar": ["Dhrol", "Jamnagar", "Jodiya", "Kalavad", "Lalpur", "Jamjodhpur"],
        "Junagadh": ["Bhesan", "Junagadh City", "Junagadh Rural", "Keshod", "Malia", "Manavadar", "Mangrol", "Mendarda", "Vanthali", "Visavadar"],
        "Kheda": ["Galteshwar", "Kheda", "Mahudha", "Matar", "Nadiad", "Kapadvanj", "Kathlal", "Thasra", "Vaso"],
        "Kutch": ["Abdasa", "Anjar", "Bhachau", "Bhuj", "Gandhidham", "Lakhpat", "Mandvi", "Mundra", "Nakhatrana", "Rapar"],
        "Mahisagar": ["Balasinor", "Kadana", "Khanpur", "Lunawada", "Santrampur", "Virpur"],
        "Mehsana": ["Becharaji", "Kadi", "Kheralu", "Mehsana", "Patan", "Satlasana", "Unjha", "Vadnagar", "Vijapur", "Visnagar"],
        "Morbi": ["Halvad", "Maliya", "Morbi", "Tankara", "Wankaner"],
        "Narmada": ["Dediyapada", "Garudeshwar", "Nandod", "Sagbara", "Tilakwada"],
        "Navsari": ["Chikhli", "Gandevi", "Jalalpore", "Navsari", "Vansda", "Ganasda"],
        "Panchmahal": ["Goghamba", "Halol", "Jambughoda", "Kalol", "Lunawada", "Godhra", "Shehra"],
        "Patan": ["Chanasma", "Harij", "Patan", "Radhanpur", "Sankheshwar", "Sami", "Sidhpur", "Vagdod", "Becharaji"],
        "Porbandar": ["Porbandar", "Ranavav", "Kutiyana"],
        "Rajkot": ["Dhoraji", "Gondal", "Jamkandorna", "Jasdan", "Jetpur", "Kotda Sangani", "Lodhika", "Paddhari", "Rajkot", "Upleta", "Vinchhiya"],
        "Sabarkantha": ["Himatnagar", "Idar", "Khedbrahma", "Poshina", "Prantij", "Talod", "Vadali", "Vijaynagar"],
        "Surat": ["Bardoli", "Choryasi", "Kamrej", "Mahuv", "Mandvi", "Mangrol", "Olpad", "Palasana", "Palsana", "Umarpada"],
        "Surendranagar": ["Chotila", "Dasada", "Dhrangadhra", "Lakhtar", "Limbdi", "Muli", "Sayla", "Thangadh", "Wadhwan"],
        "Tapi": ["Mahuva", "Nizar", "Songadh", "Uchhal", "Valod", "Vyara"],
        "Vadodara": ["Dabhoi", "Karjan", "Padra", "Savli", "Sinor", "Vadodara (Rural)", "Vaghodia"],
        "Valsad": ["Dharampur", "Kaprada", "Pardi", "Umbergaon", "Valsad", "Vapi"]
    }

    if District.objects.count() > 0:
        print("Database already has location data. Skipping seeding.")
        return
    
    print("Populating location data...")
    
    # Data Structure: District -> { Taluka -> [Villages] }
    # We populate real data where found, otherwise leave empty or add generic logic later.
    village_data = {
        "Ahmedabad": {
            "Ahmedabad City": ["Maninagar", "Navrangpura", "Paldi", "Thaltej", "Gota", "Vastrapur", "Bodakdev", "Chandkheda", "Naroda", "Odhav", "Vatva"],
            "Daskroi": ["Aslali", "Badodara", "Bakrol Bujrang", "Barejadi", "Bharkunda", "Bhat", "Bhavda", "Bhuval", "Bhuvaldi", "Bibipur", "Chandial", "Chavlaj", "Chosar", "Devdi", "Dhamatvan", "Gamdi", "Gatrad", "Geratnagar", "Geratpur", "Giramtha", "Govindada", "Harnivav", "Hathijan", "Hirapur", "Huka", "Istolabad", "Jetalpur", "Kaniyel", "Kasindra", "Khodiyar", "Kubadthal", "Kuha", "Lalpur", "Lapkaman", "Lilapur", "Mahijda", "Memadpur", "Miroli", "Muthiya", "Navapura", "Navarangpura", "Naz", "Ode", "Paldi Kankaj", "Pardhol", "Pasunj", "Ranodara", "Ropda", "Timba", "Undrel", "Vadod", "Vahelal", "Vanch", "Vasai", "Visalpur", "Zanu"],
            "Sanand": ["Anadej", "Aniyali", "Bakrana", "Bhavanpur", "Bol", "Changodar", "Charal", "Chekhla", "Chharodi", "Daduka", "Daran", "Dodar", "Fangdi", "Garodiya", "Godhavi", "Goraj", "Govinda", "Hirapur", "Iyava", "Juda", "Juwal", "Kalana", "Kaneti", "Khicha", "Khoda", "Khoraj", "Kodaliya", "Kolat", "Kundal", "Kunvar", "Lekhamba", "Lodariyal", "Makhiyav", "Mankol", "Matoda", "Melasana", "Modasar", "Moraiya", "Moti Devti", "Nani Devti", "Naranpura", "Navapura", "Nidhrad", "Palwada", "Pipan", "Rampura", "Rethal", "Rupavati", "Sanand (Rural)", "Sanathal", "Sari", "Shela", "Shiyawada", "Soyla", "Tajpur", "Telav", "Upardal", "Vanaliya", "Vasna Chacharavadi", "Vasna Iyava", "Vasodara", "Vinchhiya", "Virochannagar", "Zamp", "Zolapur"],
            "Bavla": ["Adroda", "Amipura", "Bagodara", "Baldana", "Bhamsara", "Bhayla", "Chhabasar", "Chiyada", "Dahegamda", "Devadthal", "Devdholera", "Dhanwada", "Dhedhal", "Dhingda", "Dumali", "Durgi", "Gangad", "Gundanapara", "Hasannagar", "Juval Rupavati", "Kaliveji", "Kalyangadh", "Kanotar", "Kavitha", "Kavla", "Kerala", "Kesaradi", "Kochariya", "Lagdana", "Memar", "Meni", "Metal", "Mithapur", "Nanodara", "Rajoda", "Ranesar", "Rasam", "Rohika", "Rupal", "Sakodara", "Saljada", "Sankod", "Sarala", "Shiyal", "Vasna Dhedhal", "Vasna Nanodara", "Zekda"],
            "Dholka": ["Ambaliyara", "Ambareli", "Ambethi", "Anandpura", "Andhari", "Arnej", "Badarkha", "Begva", "Bhetawada", "Bholad", "Bhumli", "Bhurkhi", "Chaloda", "Chandisar", "Dadusar", "Dholi", "Dholka", "Ganesar", "Ganol", "Girand", "Gundi", "Ingoli", "Jakhda", "Jalalpur Godhaneshvar", "Jalalpur Vazifa", "Javaraj", "Kadipur", "Kaliyapura", "Kalyanpur", "Kariyana", "Kauka", "Kesargadh", "Khanpur", "Kharanti", "Khatripur", "Koth", "Lana", "Loliya", "Moti Boru", "Mujpur", "Nani Boru", "Nesda", "Paldi", "Pisawada", "Rajpur", "Rampur", "Rampura", "Ranoda", "Raypur", "Rupgadh", "Sahij", "Samani", "Saragvala", "Sarandi", "Saroda", "Sathal", "Shekhdi", "Shiyawada", "Simej", "Sindhraj", "Transad", "Uteliya", "Valthera", "Varna", "Vasna Keliya", "Vataman", "Vautha", "Vejalka", "Virdi", "Virpur"],
            "Viramgam": ["Asalgam", "Bhadana", "Bhavda", "Bhojva", "Chanothiya", "Chuninapura", "Dalsana", "Dediyasan", "Devpura", "Dhakdi", "Dumana", "Ghoda", "Goraiya", "Hansalpur Sereshvar", "Jakhwada", "Jaksi", "Jalampura", "Jetapur", "Juna Padar", "Kadipur", "Kaliyana", "Kalyanpur", "Kamijla", "Kankaravadi", "Kanpura", "Karakathal", "Karangadh", "Kariyana", "Kayla", "Khengariya", "Khudad", "Kokata", "Kumarkhan", "Limbad", "Liya", "Melaj", "Memadpura", "Moti Kishol", "Moti Kumad", "Nadiyana", "Nani Kishol", "Nani Kumad", "Nilki", "Ogan", "Rahemalpur", "Rangpur", "Rupavati", "Sabalpura", "Sachana", "Sarsavadi", "Shahpur", "Shivpura", "Sokali", "Thori Mubarak", "Thori Thambha", "Thori Vadgas", "Thuleta", "Ukhalod", "Vadgas", "Valana", "Vani", "Vansva", "Vanthal", "Vasan", "Vasveliya", "Vekariya", "Viramgam", "Zezara"]
        },
        "Surat": {
            "Surat City": ["Adajan", "Athwa", "Katargam", "Limbayat", "Udhna", "Varachha", "Rander"],
            "Chorasi": ["Abhva", "Asarma", "Bhanodra", "Bharthana Kosad", "Bhatha", "Bhatia", "Bhatlai", "Bhatpor", "Bhesan", "Bhimpor", "Bhimrad", "Bonand", "Budia", "Chichi", "Chorasi", "Dakhkhanvada", "Damka", "Deladva", "Devadh", "Dumas", "Eklera", "Gabheni", "Gaviyar", "Goja", "Hajira", "Ichchhapor", "Jiav", "Kachholi", "Kansad", "Kapletha", "Karadva", "Kavas", "Khajod", "Khambhasla", "Kharvasa", "Kosad", "Kumbharia", "Lajpor", "Magdalla", "Malgama", "Mohni", "Mora", "Okha", "Pali", "Pardi Kanade", "Popda", "Rajgari", "Ravla", "Rundh", "Sabargam", "Samrod", "Saniya Hemad", "Saniya Kanade", "Saroli", "Sarsana", "Sonari", "Sultanabad", "Sunvali", "Talangpor", "Timbarva", "Umber", "Vansva", "Vanta", "Vanz", "Variav", "Vedchha"],
            "Kamrej": ["Abrama", "Alura", "Amboli", "Antroli", "Bharda", "Dhatva", "Digas", "Dungra", "Ghaludi", "Horp", "Kholwad", "Kosmada", "Laskana", "Navagam", "Pasodara", "Pardi", "Sevni", "Valak", "Vav", "Velanja"],
            "Olpad": ["Achharan", "Admor", "Ambheta", "Andhi", "Anita", "Ariana", "Asnad", "Atodara", "Balkas", "Barbodhan", "Bhadol", "Bhagwa", "Bhandut", "Dandi", "Delad", "Erthan", "Gola", "Hathisa", "Isanpur", "Jafarabad", "Kadvad", "Kanora", "Karanj", "Kawas", "Kim", "Kudsad", "Lavachha", "Mahamadpore", "Masma", "Mindhi", "Mirjapor", "Mor", "Mulad", "Narkhadi", "Olpad", "Orma", "Paria", "Pinjarat", "Sayan", "Sherdi", "Sithan", "Sondla", "Syadla", "Takarma", "Talad", "Ten", "Thothb", "Umra", "Vadoli", "Vaswari", "Veluk"]
        },
        "Rajkot": {
            "Rajkot": ["Anandpar", "Badpar", "Bamanbore", "Bedla", "Bhayasar", "Chikhla", "Dhandhni", "Gadhka", "Gavridad", "Gunda", "Halenda", "Haripar", "Hodthali", "Jasani", "Jiyana", "Kalipat", "Kankot", "Kasturbadham", "Kathrota", "Khambha", "Kherdi", "Khokhadad", "Kuvadva", "Lampasari", "Lapasari", "Loddha", "Lothada", "Mahi", "Mahika", "Maliyshan", "Mavdi", "Metoda", "Mota Mava", "Munjka", "Nagalpar", "Nakrawadi", "Navagam", "Parevala", "Pipalia", "Rafala", "Ramnagar", "Ronki", "Samadhiyala", "Sanosara", "Sar", "Sardhar", "Satda", "Sayper", "Sokhada", "Thebachda", "Thorala", "Vadali", "Vajdi", "Vankvad"],
            "Gondal": ["Ambardi", "Anida", "Bandra", "Betavad", "Bhandaria", "Bharudi", "Bhojpara", "Biliyala", "Charnida", "Chora", "Daddhar", "Dali", "Derdi", "Devcharadi", "Devla", "Dhadva", "Dhudasiya", "Garamali", "Ghoghavadar", "Gomto", "Gondal", "Gundala", "Hadmatala", "Hajivadar", "Jamvadi", "Kamandal", "Kantoli", "Karmal Kotda", "Keshavala", "Kolithad", "Limbadiya", "Lunivav", "Mahikantharia", "Mandlikpur", "Masitala", "Meta Khambhaliya", "Moti Khilori", "Moviya", "Nagadka", "Nana Mandava", "Padvala", "Paneli", "Patidad", "Patiyali", "Pipaliya", "Ribda", "Sogthi", "Sultanpur", "Trakuda", "Umvada", "Vasavad", "Veji", "Vinivadar", "Vorakotda"]
        }
    }

    # 1. Create Districts and Talukas
    for i, (dist_name, talukas) in enumerate(gujarat_data.items()):
        code = f"{i+1:02d}" 
        
        dist, _ = District.objects.get_or_create(name=dist_name, defaults={"code": code})
        
        for tal_name in talukas:
            tal, _ = Taluka.objects.get_or_create(name=tal_name, district=dist)

            # Check if we have village data for this District -> Taluka
            if dist_name in village_data and tal_name in village_data[dist_name]:
                real_villages = village_data[dist_name][tal_name]
                for v_name in real_villages:
                     v, _ = Village.objects.get_or_create(name=v_name, taluka=tal)
                     # Create a default office for each real village (e.g., Gram Panchayat)
                     Office.objects.get_or_create(name=f"Gram Panchayat {v_name}", village=v, address=f"Main Road, {v_name}")
            else:
                 # Default generic villages if no real data
                 pass

    print(f"Districts: {District.objects.count()}")
    print(f"Talukas: {Taluka.objects.count()}")
    print(f"Villages: {Village.objects.count()}")
    print(f"Offices: {Office.objects.count()}")

    # 5. Create Departments
    dept_revenue, _ = Department.objects.get_or_create(name="Revenue Department", description="Land and Revenue related")
    dept_panchayat, _ = Department.objects.get_or_create(name="Panchayat Department", description="Rural development")
    dept_transport, _ = Department.objects.get_or_create(name="Transport Department", description="RTO related")

    print(f"Departments: {Department.objects.count()}")

    # 6. Create Services
    # Revenue Services
    srv_income, _ = Service.objects.get_or_create(name="Income Certificate", department=dept_revenue, prefix="INC")
    srv_caste, _ = Service.objects.get_or_create(name="Caste Certificate", department=dept_revenue, prefix="CST")
    srv_domicile, _ = Service.objects.get_or_create(name="Domicile Certificate", department=dept_revenue, prefix="DOM")
    
    # Transport Services
    srv_license, _ = Service.objects.get_or_create(name="Driving License", department=dept_transport, prefix="DL")
    srv_vehicle, _ = Service.objects.get_or_create(name="Vehicle Registration", department=dept_transport, prefix="VR")

    print(f"Services: {Service.objects.count()}")

    # 7. Create Counters (Generic setup for now)
    cnt_1, _ = Counter.objects.get_or_create(name="Counter 1", department=dept_revenue)
    cnt_2, _ = Counter.objects.get_or_create(name="Counter 2", department=dept_transport)

    print("Database seeded successfully!")

if __name__ == '__main__':
    seed()
