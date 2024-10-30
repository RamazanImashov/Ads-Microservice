VERSATILEIMAGEFIELD_SETTINGS = {
    'cache_length': 2592000,  # 30 дней
    'cache_name': 'versatileimagefield_cache',
    'jpeg_resize_quality': 70,
    'sized_directory_name': '__sized__',
    'filtered_directory_name': '__filtered__',
    'placeholder_directory_name': '__placeholder__',
    'create_images_on_demand': False,
    'image_key_post_processor': None,
    'progressive_jpeg': False
}

VERSATILEIMAGEFIELD_RENDITION_KEY_SETS = {
    'car_images': [
        ('webp_medium', 'thumbnail__400x400__webp'),
        ('webp_small', 'thumbnail__200x200__webp')
    ]
}