from rolepermissions.roles import AbstractUserRole


class admin(AbstractUserRole):
    available_permissions = {
        'is_admin'      : True,
        'is_staff'      : True,
        'is_active'     : True,
        'is_superadmin' : True,
    }
    
class user(AbstractUserRole):
    available_permissions = {
        'is_admin'      : False,
        'is_staff'      : False,
        'is_active'     : True,
        'is_superadmin' : False,
    }