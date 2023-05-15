def remove_suffix_if_present(domain_name):
    base, sep, suffix = domain_name.rpartition('.')
    return base if sep == '.' and suffix.isdigit() else domain_name
