def config_keys_help_text():
    return (
        'possible config keys:\n\n'
        '"django_root_path", the root dir of django (./ = '
        '(not recomended) root of this project)\n'

        '"react_root_path", the root dir of react (./ = '
        '(not recomended) root of this project)\n'

        '"django_app_path", the root dir of django app which rdw will '
        ' copy all builded files and dirs of react app'
        '( ./ = (not recomended) the root dir of "django_root_path"). '
        'IMPORTANT: requires the same value django root path bellow/above'
        ' (can use "$django_root_path/[app_path]", $[key] acts like a "'
        'placeholder")\n'

        '"react_app_path", the root dir of react app which rdw will '
        ' watch to build all files and dirs'
        '( ./ = (not recomended) the root dir of "react_root_path"). '
        'IMPORTANT: requires the same value react root path bellow/above'
        ' (can use "$react_root_path/[app_path]", $[key] acts like a "'
        'placeholder")\n'
    )
