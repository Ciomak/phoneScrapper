from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import re


# mgsm_terminals
# mgsm_terminals_stage

engine = create_engine('postgresql+psycopg2://kamilc:rexmil@localhost:5432/terminals', echo=True)
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)


class TerminalStage(Base):
    __tablename__ = 'mgsm_stage'

    id = Column(Integer, primary_key=True, autoincrement=True)
    terminal_id = Column(Integer)
    url = Column(String(500))
    terminal_name = Column(String(250))
    attribute_section = Column(String(250))
    attribute_name = Column(String(250))
    attribute_value = Column(String(10000))

    def __init__(self, url, terminal_id, bs):
        self.url = url
        self.terminal_id = terminal_id
        self.bs = bs

    def setTerminalName(self):
        pass

    def setTerminalSection(self):
        pass

    def setAttributeName(self):
        pass

    def setAttributeValue(self):
        pass


class Terminal(Base):
    __tablename__ = 'mgsm'

    terminal_id = Column(Integer, primary_key=True, autoincrement=False)
    url = Column(String(500))
    terminal_vendor = Column(String(50))
    terminal_name = Column(String(250))
    alter_names = Column(String(500))
    lte_standard = Column(Boolean)
    terminal_height = Column(Float)
    terminal_width = Column(Float)
    terminal_tick = Column(Float)
    terminal_weight = Column(Float)
    main_screen_colors = Column(Float)
    main_screen_size = Column(Float)
    main_screen_res_x = Column(Integer)
    main_screen_res_y = Column(Integer)
    main_screen_ppi = Column(Integer)
    main_screen_ratio = Column(Float)
    max_time_call = Column(Float)
    max_time_stand_by = Column(Float)
    battery = Column(Integer)
    fast_charge = Column(Boolean)
    induction_charge = Column(Boolean)
    internal_memory = Column(String(50))
    ram_memory = Column(String(50))
    os = Column(String(50))
    processor_cores = Column(Integer)
    processor_gpu = Column(String(100))
    processor_speed = Column(Float)
    touch_screen = Column(Boolean)
    dual_sim = Column(Boolean)
    release_date = Column(String(25))
    rear_first_camera_matrix = Column(Integer)
    rear_first_camera_optical_zoom = Column(Boolean)
    rear_first_camera_digital_zoom = Column(Boolean)
    rear_first_camera_flash = Column(Boolean)
    rear_second_camera_matrix = Column(Integer)
    rear_second_camera_optical_zoom = Column(Boolean)
    rear_second_camera_digital_zoom = Column(Boolean)
    rear_second_camera_mlash = Column(Boolean)
    rear_third_camera_matrix = Column(Integer)
    rear_third_camera_optical_zoom = Column(Boolean)
    rear_third_camera_digital_zoom = Column(Boolean)
    rear_third_camera_flash = Column(Boolean)
    rear_fourth_camera_matrix = Column(Integer)
    rear_fourth_camera_optical_zoom = Column(Boolean)
    rear_fourth_camera_digital_zoom = Column(Boolean)
    rear_fourth_camera_flash = Column(Boolean)
    front_first_camera_matrix = Column(Integer)
    front_first_camera_optical_zoom = Column(Boolean)
    front_first_camera_digital_zoom = Column(Boolean)
    front_first_camera_flash = Column(Boolean)
    finger_print_scanner = Column(Boolean)
    bluetooth = Column(Boolean)
    wifi = Column(Boolean)
    wifi24 = Column(Boolean)
    wifi50 = Column(Boolean)
    nfc = Column(Boolean)
    user_score = Column(Float)
    user_design_score = Column(Float)
    user_capabilities_score = Column(Float)
    scores = Column(Integer)
    visits = Column(Integer)
    phone_jack = Column(Boolean)
    phone_kind = Column(String(50))

    def __init__(self, url, terminal_id, bs):
        self.url = url
        self.terminal_id = terminal_id
        self.bs = bs
        self.initClass()

    def initClass(self):
        self.setMainScreen()
        self.setTerminalVendor()

    def setMainScreen(self):
        value = self.parseCat('Wyświetlacz')

        ratio = re.compile('(?P<ratio>\d{1,2}[,.]\d{1,2})%')
        ppi = re.compile('(?P<ppi>\d{2,4}).ppi')
        colors = re.compile('(?P<num>\d{2,3})(?P<sep>[kM])')
        res = re.compile('(?P<x>\d{2,4}).x.(?P<y>\d{2,4}).px')
        size = re.compile('(?P<size>\d{1,2}[,.]\d{1,2})"')

        if value:
            if re.search(ratio, value.text):
                try:
                    self.main_screen_ratio = float(re.search(ratio, value.text).group('ratio'))
                except:
                    self.main_screen_ratio = None
            
            if re.search(ppi, value.text):
                try:
                    self.main_screen_ppi = int(re.search(ppi, value.text).group('ppi'))
                except:
                    self.main_screen_ppi = None
            
            if re.search(colors, value.text):
                try:
                    if re.search(colors, value.text).group('sep') == 'k':
                        self.main_screen_colors = float(int(re.search(colors, value.text).group('num')/1000))
                    else:
                        self.main_screen_colors = float(re.search(colors, value.text).group('num'))
                except:
                    self.main_screen_colors = None
            
            if re.search(res, value.text):
                try:
                    self.main_screen_res_x = int(re.search(res, value.text).group('x'))
                    self.main_screen_res_y = int(re.search(res, value.text).group('y'))
                except:
                    self.main_screen_res_x = None
                    self.main_screen_res_y = None
            
            if re.search(size, value.text):
                try:
                    self.main_screen_size = float(re.search(size, value.text).group('size'))
                except:
                    self.main_screen_size = None
        else:
            self.main_screen_colors = None
            self.main_screen_ppi = None
            self.main_screen_ratio = None
            self.main_screen_res_x = None
            self.main_screen_res_y = None
            self.main_screen_size = None

    def setTerminalVendor(self):
        try:
            self.terminal_vendor = self.terminal_name.split(' ')[0]
        except:
            self.terminal_vendor = None

    def setTerminalName(self):
        try:
            self.terminal_name = ' '.join(self.bs.find('div', {'id': 'PhoneModelName'}).find('h1').text.strip().split(' ')[:-2])
        except:
            self.terminal_name = None

    def setAlterNames(self):
        value = self.parseCat('Inne nazwy tego telefonu')
        if value:
            self.alter_names = value.text.strip()
        else:
            self.alter_names = value

    def setLteStandard(self):
        value = self.parseCat('Standard LTE')
        if value:
            if len(value.text.strip()) > 0:
                self.lte_standard = True
            else:
                try:
                    img = value.find('span')
                    if 'cross' in img['class']:
                        self.lte_standard = False
                    elif 'tick' in img['class']:
                        self.lte_standard = True
                    elif 'question' in img['class']:
                        self.lte_standard = None
                except:  # noqa E722
                    self.lte_standard = None
        else:
            self.lte_standard = None

    def setPhoneKind(self):
        value = self.parseCat('Rodzaj')

        if value:
            if len(value.text.strip()) > 0:
                self.phone_kind = value.text.strip()
            else:
                self.phone_kind = None
        else:
            self.phone_kind = None

    def setTerminalDims(self):
        value = self.parseCat('Wymiary')

        if value:
            dims = re.compile('(?P<height>\d{,4}.\d{,2}).x.(?P<width>\d{,4}.\d{,2}).x.(?P<tick>\d{,4}.\d{,2}).mm')
            try:
                res = re.search(dims, value.text)
                self.terminal_height = float(res.group('height'))
                self.terminal_width = float(res.group('width'))
                self.terminal_tick = float(res.group('tick'))
            except:
                self.terminal_height = None
                self.terminal_width = None
                self.terminal_tick = None

    def setTerminalWeight(self):
        value = self.parseCat('Waga')
        if value:
            try:
                self.terminal_weight = float(value.text.strip().split(' ')[0])
            except:  # noqa E722
                self.terminal_weight = None
        else:
            self.terminal_weight = None

    def setBattery(self):
        value = self.parseCat('Standardowa bateria')
        if value:
            try:
                self.battery = int(re.search(re.compile('\d+'), value.text).group(0))
            except:  # noqa E722
                self.battery = None
        else:
            self.battery = None

    def setFastCharge(self):
        value = self.parseCat('Szybkie ładowanie')
        if value:
            if len(value.text.strip()) > 0:
                self.fast_charge = True
            else:
                try:
                    img = value.find('span')
                    if 'cross' in img['class']:
                        self.fast_charge = False
                    elif 'tick' in img['class']:
                        self.fast_charge = True
                    elif 'question' in img['class']:
                        self.fast_charge = None
                except:  # noqa E722
                    self.fast_charge = None
        else:
            self.fast_charge = None

    def setInductionCharge(self):
        value = self.parseCat('Ładowanie indukcyjne')
        if value:
            if len(value.text.strip()) > 0:
                self.induction_charge = True
            else:
                try:
                    img = value.find('span')
                    if 'cross' in img['class']:
                        self.induction_charge = False
                    elif 'tick' in img['class']:
                        self.induction_charge = True
                    elif 'question' in img['class']:
                        self.induction_charge = None
                except:  # noqa E722
                    self.induction_charge = None
        else:
            self.induction_charge = None

    def setInternalMemory(self):
        value = self.parseCat('Pamięć wbudowana')
        if value:
            try:
                self.internal_memory = value.text.strip()
            except:  # noqa E722
                self.internal_memory = None
        else:
            self.internal_memory = None

    def setRamMemory(self):
        value = self.parseCat('Pamięć RAM')
        if value:
            try:
                self.ram_memory = value.text.strip()
            except:  # noqa E722
                self.ram_memory = None
        else:
            self.ram_memory = None

    def setOs(self):
        value = self.parseCat('System operacyjny')
        if value:
            try:
                self.os = value.text.strip()
            except:  # noqa E722
                self.os = None
        else:
            self.os = None

    def setProcessor(self):
        value = self.parseCat('Procesor')
        
        if value:
            for descendant in value.descendants:
                if str(descendant).startswith('Zegar procesora'):
                    try:
                        self.processor_speed = float(str(descendant).split(':')[-1].split()[0])
                    except:  # noqa E722
                        self.processor_speed = None

                if str(descendant).startswith('Liczba rdzeni'):
                    try:
                        self.processor_cores = int(str(descendant).split(':')[-1].split()[0])
                    except:  # noqa E722
                        self.processor_cores = None

        else:
            self.processor_cores = None
            self.processor_speed = None

    def setTouchScreen(self):
        value = self.parseCat('Ekran dotykowy')
        if value:
            if len(value.text.strip()) > 0:
                self.touch_screen = value.text.strip()
            else:
                try:
                    img = value.find('span')
                    if 'cross' in img['class']:
                        self.touch_screen = False
                    elif 'tick' in img['class']:
                        self.touch_screen = True
                    elif 'question' in img['class']:
                        self.touch_screen = None
                except:  # noqa E722
                    self.touch_screen = None
        else:
            self.touch_screen = None

    def setDualSim(self):
        value = self.parseCat('(DualSIM)')
        if value:
            if len(value.text.strip()) > 0:
                self.dual_sim = True
            else:
                try:
                    img = value.find('span')
                    if 'cross' in img['class']:
                        self.dual_sim = False
                    elif 'tick' in img['class']:
                        self.dual_sim = True
                    elif 'question' in img['class']:
                        self.dual_sim = None
                except:  # noqa E722
                    self.dual_sim = None
        else:
            self.dual_sim = None

    def setReleaseDate(self):
        dictq = {'I': 'Q1', 'II': 'Q2', 'III': 'Q3', 'IV': 'Q4'}
        value = self.parseCat('Wprowadzony na rynek')
        if value:
            if len(value.text.strip()) > 0:
                periods = value.text.strip().split(' ')
                year = re.search(re.compile('\d{4}'), value.text.strip()).group(0)  # noqa W605
                period = str(year) + dictq.get(periods[0])
                self.release_date = period
            else:
                try:
                    img = value.find('span')
                    if 'cross' in img['class']:
                        self.release_date = None
                    elif 'tick' in img['class']:
                        self.release_date = None
                    elif 'question' in img['class']:
                        self.release_date = None
                except:  # noqa E722
                    self.dual_sim = None
        else:
            self.dual_sim = None

    def setRearCamera(self):
        value = self.bs.find_all('div', {'class': 'foto-enumerate'})

        if value:
            for v in value:
                if v.find_previous('h2', {'class': 'phone_card__panel-header-title'}).text == 'APARAT FOTOGRAFICZNY - TYŁ':
                    if v.text == 'Pierwszy aparat':
                        for d in v.find_next('ul').descendats:
                            print(d)
                        self.rear_first_camera_matrix = None
                        self.rear_first_camera_flash = None
                        self.rear_first_camera_digital_zoom = None
                        self.rear_first_camera_optical_zoom = None
                    elif v.text == 'Drugi aparat':
                        for d in v.find_next('ul').descendats:
                            print(d)
                        self.rear_second_camera_matrix = None
                        self.rear_second_camera_flash = None
                        self.rear_second_camera_digital_zoom = None
                        self.rear_second_camera_optical_zoom = None
                    elif v.text == 'Trzeci aparat':
                        for d in v.find_next('ul').descendats:
                            print(d)
                        self.rear_third_camera_matrix = None
                        self.rear_third_camera_flash = None
                        self.rear_third_camera_digital_zoom = None
                        self.rear_third_camera_optical_zoom = None
                    elif v.text == 'Czwarty aparat':
                        for d in v.find_next('ul').descendats:
                            print(d)
                        self.rear_fourth_camera_matrix = None
                        self.rear_fourth_camera_flash = None
                        self.rear_fourth_camera_digital_zoom = None
                        self.rear_fourth_camera_optical_zoom = None

    def setFrontCamera(self):
        value = self.bs.find_all('div', {'class': 'foto-enumerate'})

        if value:
            for v in value:
                if v.find_previous('h2', {'class': 'phone_card__panel-header-title'}).text == 'APARAT FOTOGRAFICZNY - PRZÓD':
                    if v.text == 'Pierwszy aparat':
                        for d in v.find_next('ul').descendats:
                            print(d)
                        self.front_first_camera_matrix = None
                        self.front_first_camera_flash = None
                        self.front_first_camera_digital_zoom = None
                        self.front_first_camera_optical_zoom = None
                    elif v.text == 'Drugi aparat':
                        pass
                        # for d in v.find_next('ul').descendats:
                        #     print(d)
                        # self.rear_second_camera_matrix = None
                        # self.rear_second_camera_flash = None
                        # self.rear_second_camera_digital_zoom = None
                        # self.rear_second_camera_optical_zoom = None
                    elif v.text == 'Trzeci aparat':
                        pass
                        # for d in v.find_next('ul').descendats:
                        #     print(d)
                        # self.rear_third_camera_matrix = None
                        # self.rear_third_camera_flash = None
                        # self.rear_third_camera_digital_zoom = None
                        # self.rear_third_camera_optical_zoom = None
                    elif v.text == 'Czwarty aparat':
                        pass
                        # for d in v.find_next('ul').descendats:
                        #     print(d)
                        # self.rear_fourth_camera_matrix = None
                        # self.rear_fourth_camera_flash = None
                        # self.rear_fourth_camera_digital_zoom = None
                        # self.rear_fourth_camera_optical_zoom = None

    def setFingerPrintScanner(self):
        value = self.parseCat('Czytnik linii papilarnych')
        if value:
            try:
                img = value.find('span')
                if 'cross' in img['class']:
                    self.finger_print_scanner = False
                elif 'tick' in img['class']:
                    self.finger_print_scanner = True
                elif 'question' in img['class']:
                    self.finger_print_scanner = None
            except:  # noqa E722
                self.finger_print_scanner = None
        else:
            self.finger_print_scanner = None

    def setBluetooth(self):
        value = self.parseCat('Bluetooth')
        if value:
            try:
                img = value.find('span')
                if 'cross' in img['class']:
                    self.bluetooth = False
                elif 'tick' in img['class']:
                    self.bluetooth = True
                elif 'question' in img['class']:
                    self.bluetooth = None
            except:  # noqa E722
                self.bluetooth = None
        else:
            self.bluetooth = None

    def setWifi(self):
        value = self.parseCat('WiFi')
        if value:
            try:
                img = value.find('span')
                if 'cross' in img['class']:
                    self.wifi = False
                elif 'tick' in img['class']:
                    self.wifi = True
                elif 'question' in img['class']:
                    self.wifi = None
            except:  # noqa E722
                self.wifi = None
        else:
            self.wifi = None

    def setWifi24(self):
        value = self.parseCat('Częstotliwości WiFi')
        if value:
            if re.search(re.compile('2.4'), value.text.strip()):
                self.wifi24 = True
            else:
                self.wifi24 = False
        else:
            self.wifi24 = None

    def setWifi50(self):
        value = self.parseCat('Częstotliwości WiFi')
        if value:
            if re.search(re.compile('5'), value.text.strip()):
                self.wifi50 = True
            else:
                self.wifi50 = False
        else:
            self.wifi50 = None

    def setNfc(self):
        value = self.parseCat('NFC')
        if value:
            if len(value.text.strip()) > 0:
                self.nfc = True
            else:
                try:
                    img = value.find('span')
                    if 'cross' in img['class']:
                        self.nfc = False
                    elif 'tick' in img['class']:
                        self.nfc = True
                    elif 'question' in img['class']:
                        self.nfc = None
                except:  # noqa E722
                    self.nfc = None
        else:
            self.nfc = None

    def setUserScore(self):
        value = self.bs.find('div', {'PDVA-header'})

        if value:
            try:
                self.user_score = float(value.text.strip().split()[-1].replace(',', '.'))
            except:  # noqa E722
                self.user_score = None
        else:
            self.user_score = None

    def setUserDesignScore(self):
        value = self.bs.find_all('div', {'class': 'vote-text'})

        if value:
            for score in value:
                sp = score.text.split()
                if sp[0] == 'Design':
                    try:
                        self.user_design_score = float(sp[1].strip().replace(',', '.'))
                    except:  # noqa E722
                        self.user_design_score = None
        else:
            self.user_design_score = None

    def setUserCapabilitiesScore(self):
        value = self.bs.find_all('div', {'class': 'vote-text'})

        if value:
            for score in value:
                sp = score.text.split()
                if sp[0] == 'Możliwości':
                    try:
                        self.user_capabilities_score = float(sp[1].strip().replace(',', '.'))
                    except:  # noqa E722
                        self.user_capabilities_score = None
        else:
            self.user_capabilities_score = None

    def setScores(self):
        value = self.bs.find('div', {'class': 'AddedInfo'})

        if value:
            for v in value.text.split('|'):
                if re.search(re.compile('Ocen'), v):
                    try:
                        self.scores = int(re.search(re.compile('\d+'), v).group(0))
                    except:  # noqa E722
                        self.scores = None
                    break
                else:
                    self.scores = None
        else:
            self.scores = None

    def setVisits(self):
        value = self.bs.find('div', {'class': 'AddedInfo'})

        if value:
            for v in value.text.split('|'):
                if re.search(re.compile('Wizyt'), v):
                    try:
                        self.visits = int(re.search(re.compile('\d+'), v).group(0))
                    except:  # noqa E722
                        self.visits = None
                    break
                else:
                    self.visits = None
        else:
            self.visits = None

    def setPhoneJack(self):
        value = self.parseCat('Audio Jack')
        if value:
            if len(value.text.strip()) > 0:
                self.phone_jack = True
            else:
                try:
                    img = value.find('span')
                    if 'cross' in img['class']:
                        self.phone_jack = False
                    elif 'tick' in img['class']:
                        self.phone_jack = True
                    elif 'question' in img['class']:
                        self.phone_jack = None
                except:  # noqa E722
                    self.phone_jack = None
        else:
            self.phone_jack = None

    def parseCat(self, category):
        category = self.bs.find_all(string=re.compile(category, re.IGNORECASE))
        if category:
            parents = [x.parent for x in category]
            for parent in parents:
                for sibling in parent.find_next_siblings():
                    if 'phoneCategoryValue' in sibling['class']:
                        return sibling

        return None


def createTables():
    Base.metadata.create_all()

def dropTables():
    Base.metadata.drop_all()