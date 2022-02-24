from os.path import basename, splitext


def get_filename_ext(filepath):
    base_name = basename(filepath)
    name, ext = splitext(base_name)
    return name, ext

def upload_product_file(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.id}-{instance.title}{ext}"
    return f"products/{final_name}"

def upload_blog_file(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.id}-{instance.title}{ext}"
    return f"blogs/{final_name}"

def upload_user_file(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.id}-{instance.username}{ext}"
    return f"users/{final_name}"
