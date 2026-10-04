"""Adresy, kolejność materiałów i drobne teksty interfejsu, których nie ma w plikach Word."""

SITE = 'https://grupoervoy.com'
LANGS = ['pl', 'es', 'en']
DEFAULT = 'pl'            # polski pod adresem głównym, pozostałe języki w podkatalogach
X_DEFAULT = 'en'          # hreflang x-default: angielski dla użytkowników spoza PL/ES/EN (np. producenci z Niemiec czy Włoch)
PREFIX = {'pl': '', 'es': 'es/', 'en': 'en/'}
HTML_LANG = {'pl': 'pl', 'es': 'es-MX', 'en': 'en'}
# hreflang z regionem: polski dla Polski, hiszpański dla Meksyku, angielski dla wszystkich (x-default też EN)
HREFLANG = {'pl': 'pl-PL', 'es': 'es-MX', 'en': 'en'}
OG_LOCALE = {'pl': 'pl_PL', 'es': 'es_MX', 'en': 'en_US'}

# klucz strony -> ścieżka w każdym języku (bez prefiksu języka)
ROUTES = {
    'home':      {'pl': '', 'es': '', 'en': ''},
    'uslugi':    {'pl': 'uslugi/', 'es': 'servicios/', 'en': 'services/'},
    'u1':        {'pl': 'uslugi/badanie-rynku/', 'es': 'servicios/estudio-de-mercado/', 'en': 'services/market-research/'},
    'u2':        {'pl': 'uslugi/przygotowanie-produktu/', 'es': 'servicios/preparacion-de-producto/', 'en': 'services/product-compliance/'},
    'u3':        {'pl': 'uslugi/reprezentacja/', 'es': 'servicios/representacion/', 'en': 'services/representation/'},
    'u4':        {'pl': 'uslugi/import-i-logistyka/', 'es': 'servicios/importacion-y-logistica/', 'en': 'services/import-and-logistics/'},
    'u5':        {'pl': 'uslugi/dystrybutorzy/', 'es': 'servicios/distribuidores/', 'en': 'services/distributors/'},
    'u6':        {'pl': 'uslugi/targi-i-promocja/', 'es': 'servicios/ferias-y-promocion/', 'en': 'services/trade-shows/'},
    'proces':    {'pl': 'jak-pracujemy/', 'es': 'como-trabajamos/', 'en': 'how-we-work/'},
    'wiedza':    {'pl': 'baza-wiedzy/', 'es': 'conocimiento/', 'en': 'knowledge/'},
    'wiedza.akt': {'pl': 'baza-wiedzy/aktualnosci/', 'es': 'conocimiento/novedades/', 'en': 'knowledge/updates/'},
    'wiedza.zas': {'pl': 'baza-wiedzy/zasoby/', 'es': 'conocimiento/recursos/', 'en': 'knowledge/resources/'},
    'art.1':     {'pl': 'baza-wiedzy/pierwsze-kroki/', 'es': 'conocimiento/primeros-pasos/', 'en': 'knowledge/first-steps/'},
    'art.2':     {'pl': 'baza-wiedzy/normy-nom/', 'es': 'conocimiento/normas-nom/', 'en': 'knowledge/nom-standards/'},
    'art.3':     {'pl': 'baza-wiedzy/kod-taryfowy/', 'es': 'conocimiento/fraccion-arancelaria/', 'en': 'knowledge/tariff-code/'},
    'art.4':     {'pl': 'baza-wiedzy/importer/', 'es': 'conocimiento/importador/', 'en': 'knowledge/importer/'},
    'art.5':     {'pl': 'baza-wiedzy/pochodzenie-i-clo/', 'es': 'conocimiento/origen-y-aranceles/', 'en': 'knowledge/origin-and-duties/'},
    'art.6':     {'pl': 'baza-wiedzy/etykieta-zywnosci/', 'es': 'conocimiento/etiquetado-de-alimentos/', 'en': 'knowledge/food-labelling/'},
    'art.7':     {'pl': 'baza-wiedzy/posiadacz-certyfikatu-nom/', 'es': 'conocimiento/titular-del-certificado-nom/', 'en': 'knowledge/nom-certificate-holder/'},
    'akt.1':     {'pl': 'baza-wiedzy/zmiany-celne-2026/', 'es': 'conocimiento/reforma-aduanera-2026/', 'en': 'knowledge/customs-reform-2026/'},
    'zas.targi': {'pl': 'baza-wiedzy/targi/', 'es': 'conocimiento/ferias/', 'en': 'knowledge/trade-shows/'},
    'zas.slownik': {'pl': 'baza-wiedzy/slownik/', 'es': 'conocimiento/glosario/', 'en': 'knowledge/glossary/'},
    'marki':     {'pl': 'nasze-marki/', 'es': 'nuestras-marcas/', 'en': 'our-brands/'},
    'onas':      {'pl': 'o-nas/', 'es': 'nosotros/', 'en': 'about/'},
    'kontakt':   {'pl': 'kontakt/', 'es': 'contacto/', 'en': 'contact/'},
    'polityka':  {'pl': 'polityka-prywatnosci/', 'es': 'aviso-de-privacidad/', 'en': 'privacy/'},
}

ARTICLES = ['art.1', 'art.2', 'art.3', 'art.4', 'art.5', 'art.6', 'art.7']
UPDATES = ['akt.1']
RESOURCES = ['zas.targi', 'zas.slownik']
SERVICES = ['u1', 'u2', 'u3', 'u4', 'u5', 'u6']

WHATSAPP = {'pl': 'kontakt.osoba1', 'es': 'kontakt.osoba2', 'en': 'kontakt.osoba2'}

UI = {
    'pl': {
        'skip': 'Przejdź do treści', 'menu': 'Menu', 'nav': 'Nawigacja główna', 'langs': 'Wybór języka',
        'lang_names': {'pl': 'Polski', 'es': 'Español', 'en': 'English'},
        'home': 'Strona główna', 'tabs': 'Działy bazy wiedzy', 'more': 'Czytaj dalej',
        'fairs_cols': ['Termin', 'Targi', 'Branża', 'Dla kogo'], 'fairs_industry': 'Branża', 'fairs_city': 'Miasto',
        'all': 'Wszystkie', 'rec': 'Polecamy', 'new_tab': 'otwiera się w nowej karcie',
        'count': ['Pokazujemy {n} imprezę.', 'Pokazujemy {n} imprezy.', 'Pokazujemy {n} imprez.'],
        'fairs_empty': 'Brak targów dla wybranych filtrów. Wybierz inną branżę albo miasto.',
        'gl_search': 'Szukaj w słowniku', 'gl_placeholder': 'np. pedimento, NOM, importer', 'gl_empty': 'Nie znaleźliśmy takiego hasła.',
        'foot_services': 'Usługi', 'foot_company': 'Firma', 'foot_contact': 'Kontakt',
        'privacy_pending': 'Polityka prywatności jest w przygotowaniu i pojawi się tu wkrótce. Jeśli masz pytania o to, jak przetwarzamy dane, napisz na info@grupoervoy.com.',
        'privacy_h1': 'Polityka prywatności',
        'call': 'Zadzwoń', 'write': 'Napisz e-mail', 'whatsapp': 'Napisz na WhatsApp', 'address': 'Adres',
        'updated': 'Aktualizacja:',
        'facts': [('Monterrey', 'Siedziba spółki w stanie Nuevo León'), ('Meksyk i Polska', 'Zespół po obu stronach Atlantyku'), ('3 języki', 'Hiszpański, angielski i polski'), ('2 własne marki', 'Simple Made Blinds Mexico i Polaca Foods')],
    },
    'es': {
        'skip': 'Ir al contenido', 'menu': 'Menú', 'nav': 'Navegación principal', 'langs': 'Idioma',
        'lang_names': {'pl': 'Polski', 'es': 'Español', 'en': 'English'},
        'home': 'Inicio', 'tabs': 'Secciones', 'more': 'Leer más',
        'fairs_cols': ['Fecha', 'Feria', 'Industria', 'Para quién'], 'fairs_industry': 'Industria', 'fairs_city': 'Ciudad',
        'all': 'Todas', 'rec': 'Recomendada', 'new_tab': 'se abre en una pestaña nueva',
        'count': ['Mostramos {n} feria.', 'Mostramos {n} ferias.', 'Mostramos {n} ferias.'],
        'fairs_empty': 'No hay ferias con estos filtros. Pruebe con otra industria o ciudad.',
        'gl_search': 'Buscar en el glosario', 'gl_placeholder': 'p. ej. pedimento, NOM, importador', 'gl_empty': 'No encontramos ese término.',
        'foot_services': 'Servicios', 'foot_company': 'Empresa', 'foot_contact': 'Contacto',
        'privacy_pending': 'Estamos preparando nuestro aviso de privacidad y lo publicaremos aquí en breve. Si tiene dudas sobre el tratamiento de sus datos, escríbanos a info@grupoervoy.com.',
        'privacy_h1': 'Aviso de privacidad',
        'call': 'Llamar', 'write': 'Enviar correo', 'whatsapp': 'Escribir por WhatsApp', 'address': 'Dirección',
        'updated': 'Actualizado:',
        'facts': [('Monterrey', 'Sede de la empresa en Nuevo León'), ('México y Polonia', 'Equipo a ambos lados del Atlántico'), ('3 idiomas', 'Español, inglés y polaco'), ('2 marcas propias', 'Simple Made Blinds Mexico y Polaca Foods')],
    },
    'en': {
        'skip': 'Skip to content', 'menu': 'Menu', 'nav': 'Main navigation', 'langs': 'Language',
        'lang_names': {'pl': 'Polski', 'es': 'Español', 'en': 'English'},
        'home': 'Home', 'tabs': 'Sections', 'more': 'Read more',
        'fairs_cols': ['Dates', 'Trade show', 'Industry', 'Who it is for'], 'fairs_industry': 'Industry', 'fairs_city': 'City',
        'all': 'All', 'rec': 'Recommended', 'new_tab': 'opens in a new tab',
        'count': ['Showing {n} trade show.', 'Showing {n} trade shows.', 'Showing {n} trade shows.'],
        'fairs_empty': 'No trade shows match these filters. Try another industry or city.',
        'gl_search': 'Search the glossary', 'gl_placeholder': 'e.g. pedimento, NOM, importer', 'gl_empty': 'We could not find that term.',
        'foot_services': 'Services', 'foot_company': 'Company', 'foot_contact': 'Contact',
        'privacy_pending': 'Our privacy notice is being prepared and will be published here shortly. If you have questions about how we handle personal data, write to info@grupoervoy.com.',
        'privacy_h1': 'Privacy notice',
        'call': 'Call', 'write': 'Send an email', 'whatsapp': 'Message on WhatsApp', 'address': 'Address',
        'updated': 'Updated:',
        'facts': [('Monterrey', 'Head office in Nuevo León'), ('Mexico and Poland', 'A team on both sides of the Atlantic'), ('3 languages', 'Spanish, English and Polish'), ('2 own brands', 'Simple Made Blinds Mexico and Polaca Foods')],
    },
}
