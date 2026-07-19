from django.core.management.base import BaseCommand
from api.models import District, Taluka, Village, Office, Service
import random
import string

class Command(BaseCommand):
    help = 'Seeds the database with all 33 districts of Gujarat, their talukas, villages, offices, and services.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Checking database status...')
        
        # If already fully seeded, skip to save time and prevent token deletion
        if Service.objects.count() >= 20:
            self.stdout.write(self.style.SUCCESS('Database already has all services and offices seeded. Skipping seeding.'))
            return

        self.stdout.write('Clearing incomplete/sample location data...')
        Office.objects.all().delete()
        Village.objects.all().delete()
        Taluka.objects.all().delete()
        District.objects.all().delete()

        # All 33 Districts and their Talukas of Gujarat
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

        # Real Village lists mapping ( Ahmedabad, Surat, Rajkot )
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
                "Chorasi": ["Abhva", "Asarma", "Bhanodra", "Bharthana Kosad", "Bhatha", "Bhatia", "Bhatlai", "Bhatpor", "Bhesan", "Bhimpor", "Bhimrad", "Bonand", "Budia", "Chichi", "Chorasi", "Dakhkhanvada", "Damka", "Deladva", "Devadh", "Dumas", "Eklera", "Gaviyar", "Hajira", "Ichchhapor", "Jiav", "Kachholi", "Kansad", "Kapletha", "Karadva", "Kavas", "Khajod", "Kosad", "Kumbharia", "Lajpor", "Magdalla", "Mora", "Okha", "Pali", "Pardi Kanade", "Popda", "Rundh", "Sabargam", "Samrod", "Saniya Hemad", "Sarsana", "Sultanabad", "Talangpor", "Umber", "Vanz", "Variav", "Vedchha"],
                "Kamrej": ["Abrama", "Alura", "Amboli", "Antroli", "Bharda", "Dhatva", "Digas", "Dungra", "Ghaludi", "Horp", "Kholwad", "Kosmada", "Laskana", "Navagam", "Pasodara", "Pardi", "Sevni", "Valak", "Vav", "Velanja"],
                "Olpad": ["Achharan", "Admor", "Ambheta", "Andhi", "Anita", "Ariana", "Asnad", "Atodara", "Balkas", "Barbodhan", "Bhadol", "Bhagwa", "Bhandut", "Dandi", "Delad", "Erthan", "Gola", "Hathisa", "Isanpur", "Jafarabad", "Kadvad", "Kanora", "Karanj", "Kawas", "Kim", "Kudsad", "Olpad", "Orma", "Sayan", "Sherdi", "Sithan", "Takarma", "Talad", "Ten", "Umra", "Vadoli", "Vaswari", "Veluk"]
            },
            "Rajkot": {
                "Rajkot": ["Anandpar", "Badpar", "Bamanbore", "Bedla", "Bhayasar", "Chikhla", "Dhandhni", "Gadhka", "Gavridad", "Gunda", "Halenda", "Haripar", "Hodthali", "Jasani", "Jiyana", "Kalipat", "Kankot", "Kasturbadham", "Kathrota", "Khambha", "Kherdi", "Khokhadad", "Kuvadva", "Lampasari", "Lapasari", "Loddha", "Lothada", "Mahi", "Mahika", "Maliyshan", "Mavdi", "Metoda", "Mota Mava", "Munjka", "Nagalpar", "Nakrawadi", "Navagam", "Parevala", "Pipalia", "Rafala", "Ramnagar", "Ronki", "Samadhiyala", "Sanosara", "Sar", "Sardhar", "Satda", "Sayper", "Sokhada", "Thebachda", "Thorala", "Vadali", "Vajdi", "Vankvad"],
                "Gondal": ["Ambardi", "Anida", "Bandra", "Betavad", "Bhandaria", "Bharudi", "Bhojpara", "Biliyala", "Charnida", "Chora", "Daddhar", "Dali", "Derdi", "Devcharadi", "Devla", "Dhadva", "Dhudasiya", "Garamali", "Ghoghavadar", "Gomto", "Gondal", "Gundala", "Hadmatala", "Hajivadar", "Jamvadi", "Kamandal", "Kantoli", "Karmal Kotda", "Keshavala", "Kolithad", "Limbadiya", "Lunivav", "Mahikantharia", "Mandlikpur", "Masitala", "Meta Khambhaliya", "Moti Khilori", "Moviya", "Nagadka", "Nana Mandava", "Padvala", "Paneli", "Patidad", "Patiyali", "Pipaliya", "Ribda", "Sogthi", "Sultanpur", "Trakuda", "Umvada", "Vasavad", "Veji", "Vinivadar", "Vorakotda"]
            }
        }

        self.stdout.write("Seeding all 33 districts and locations...")

        for idx, (dist_name, talukas) in enumerate(gujarat_data.items()):
            # Generate unique codes to prevent database constraint collisions
            rto_code = f"{idx+1:02d}"
            code = f"GJ{rto_code}"
            
            district, _ = District.objects.get_or_create(
                name=dist_name,
                defaults={"code": code, "rto_code": rto_code}
            )

            # Create 1 default RTO Office for every District
            Office.objects.get_or_create(
                office_name=f"{dist_name} RTO Office",
                office_code=f"RTO-{dist_name[:3].upper()}-{rto_code}",
                office_type="RTO",
                district=district,
                defaults={"address": f"RTO Compound, {dist_name} City"}
            )

            for tal_name in talukas:
                taluka, _ = Taluka.objects.get_or_create(name=tal_name, district=district)

                # Always create a Mamlatdar Office for every Taluka (Urban/General)
                Office.objects.get_or_create(
                    office_name=f"Mamlatdar Office {tal_name}",
                    office_code=f"MAM-{tal_name[:3].upper()}-{random_code()}",
                    office_type="URBAN",
                    district=district,
                    taluka=taluka,
                    defaults={"address": f"Taluka Seva Sadan, {tal_name}"}
                )

                # Identify if this Taluka matches an Urban City Center
                is_city_center = "City" in tal_name or tal_name == dist_name or tal_name in ["Adajan", "Athwa", "Katargam", "Limbayat", "Udhna", "Varachha", "Rander"]
                
                if is_city_center:
                    # Create Urban Office (Civic Center)
                    Office.objects.get_or_create(
                        office_name=f"{tal_name} Civic Center",
                        office_code=f"OFF-{tal_name[:3].upper()}-{random_code()}",
                        office_type="URBAN",
                        district=district,
                        taluka=taluka,
                        defaults={"address": f"Municipal Office, {tal_name}"}
                    )

                # Check if we have real village listings for this Taluka
                has_real_villages = dist_name in village_data and tal_name in village_data[dist_name]
                villages_to_create = village_data[dist_name][tal_name] if has_real_villages else [f"{tal_name} Village A", f"{tal_name} Village B"]

                for v_name in villages_to_create:
                    village, _ = Village.objects.get_or_create(name=v_name, taluka=taluka)
                    
                    # Create Rural Office (Gram Panchayat)
                    Office.objects.get_or_create(
                        office_name=f"Gram Panchayat {v_name}",
                        office_code=f"GP-{v_name[:3].upper()}-{random_code()}",
                        office_type="RURAL",
                        district=district,
                        taluka=taluka,
                        village=village,
                        defaults={"address": f"Panchayat Bhavan, {v_name}"}
                    )

        self.stdout.write(f"Districts seeded: {District.objects.count()}")
        self.stdout.write(f"Talukas seeded: {Taluka.objects.count()}")
        self.stdout.write(f"Villages seeded: {Village.objects.count()}")
        self.stdout.write(f"Offices seeded: {Office.objects.count()}")

        # Seed services (Rural, Urban, RTO)
        services_data = [
            # URBAN
            {"name": "Income Certificate", "office_type": "URBAN", "avg_time_minutes": 15},
            {"name": "Caste Certificate", "office_type": "URBAN", "avg_time_minutes": 15},
            {"name": "Domicile Certificate", "office_type": "URBAN", "avg_time_minutes": 20},
            {"name": "Non-Creamylayer Certificate", "office_type": "URBAN", "avg_time_minutes": 20},
            {"name": "Character Certificate", "office_type": "URBAN", "avg_time_minutes": 10},
            {"name": "Property Tax Payment", "office_type": "URBAN", "avg_time_minutes": 10},
            {"name": "Professional Tax Registration", "office_type": "URBAN", "avg_time_minutes": 25},
            {"name": "Shop & Establishment License", "office_type": "URBAN", "avg_time_minutes": 30},
            {"name": "Birth/Death Certificate", "office_type": "URBAN", "avg_time_minutes": 15},
            {"name": "Marriage Registration", "office_type": "URBAN", "avg_time_minutes": 45},

            # RURAL
            {"name": "Income Certificate", "office_type": "RURAL", "avg_time_minutes": 15},
            {"name": "Caste Certificate", "office_type": "RURAL", "avg_time_minutes": 20},
            {"name": "Non-Creamylayer Certificate", "office_type": "RURAL", "avg_time_minutes": 20},
            {"name": "Domicile Certificate", "office_type": "RURAL", "avg_time_minutes": 15},
            {"name": "Character Certificate", "office_type": "RURAL", "avg_time_minutes": 10},

            # RTO
            {"name": "Learner License", "office_type": "RTO", "avg_time_minutes": 30},
            {"name": "Driving License Test", "office_type": "RTO", "avg_time_minutes": 60},
            {"name": "Vehicle Registration", "office_type": "RTO", "avg_time_minutes": 45},
            {"name": "Fitness Certificate", "office_type": "RTO", "avg_time_minutes": 40},
            {"name": "Transfer of Ownership", "office_type": "RTO", "avg_time_minutes": 30},
        ]
        
        for s_data in services_data:
            srv, created = Service.objects.get_or_create(
                name=s_data["name"],
                office_type=s_data["office_type"],
                defaults={"avg_time_minutes": s_data["avg_time_minutes"]}
            )
            if created:
                self.stdout.write(f"Created Service: {srv.name} ({srv.office_type})")

        self.stdout.write(self.style.SUCCESS('Successfully seeded all Gujarat location data and services!'))

def random_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
