from edc_navbar import NavbarItem, site_navbars, Navbar


motheo = Navbar(name='motheo_call_manager')

motheo.append_item(
    NavbarItem(name='call_manager',
               label='Call Manager',
               fa_icon='fa-phone-square',
               url_name='call_manager_listboard_url'))

site_navbars.register(motheo)
