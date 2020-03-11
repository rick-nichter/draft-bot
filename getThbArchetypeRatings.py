import requests, json
from bs4 import BeautifulSoup

wTableLocation = "https://draftsim.com/wp-admin/admin-ajax.php?" + \
	"action=wp_ajax_ninja_tables_public_action&table_id=2128&" + \
	"target_action=get-all-data&default_sorting=old_first"
uTableLocation = "https://draftsim.com/wp-admin/admin-ajax.php?" + \
	"action=wp_ajax_ninja_tables_public_action&table_id=2130&" + \
	"target_action=get-all-data&default_sorting=old_first"
bTableLocation = "https://draftsim.com/wp-admin/admin-ajax.php?" + \
	"action=wp_ajax_ninja_tables_public_action&table_id=2124&" + \
	"target_action=get-all-data&default_sorting=old_first"
rTableLocation = "https://draftsim.com/wp-admin/admin-ajax.php?" + \
	"action=wp_ajax_ninja_tables_public_action&table_id=2131&" + \
	"target_action=get-all-data&default_sorting=old_first"

wTable = requests.get(wTableLocation).json()
uTable = requests.get(uTableLocation).json()
bTable = requests.get(bTableLocation).json()
rTable = requests.get(rTableLocation).json()

