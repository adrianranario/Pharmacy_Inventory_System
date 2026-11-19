MANAGER_GROUPS = ('Administrator', 'Pharmacist')


def can_manage_inventory(user):
    """Allow only administrators and pharmacists to manage inventory records."""
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return user.groups.filter(name__in=MANAGER_GROUPS).exists()
