from .messages import success_message, info_message, warning_message
from .directory import Directory
from .file import CommonFile
import sys
import os
from io import TextIOWrapper
from ..utils.regexps import (
    JS_URL_REGEXP, CSS_URL_REGEXP, HTML_LINK_TAG_REGEXP,
    HTML_SCRIPT_TAG_REGEXP, HTML_NOSCRIPT_TAG_REGEXP, HTML_DIVROOT_TAG_REGEXP
)


class Builder:

    def __init__(self, path_map: dict[str, Directory]):
        self.DJANGO_ROOT_PATH = path_map['django_root_path']
        self.REACT_ROOT_PATH = path_map['react_root_path']
        self.DJANGO_APP_PATH = path_map['django_app_path']
        self.REACT_APP_PATH = path_map['react_app_path']

        self.DJANGO_APP_NAME = self.DJANGO_APP_PATH.dir_name

        self.REACT_BUILD_DIR = self.REACT_APP_PATH / 'build'
        self.REACT_STATIC_FILES = self.REACT_BUILD_DIR / 'static'
        self.REACT_MEDIA_PATHS = [
            self.REACT_STATIC_FILES / 'media',
            self.REACT_BUILD_DIR
        ]

        self.DJANGO_STATIC_FILES = self.DJANGO_APP_PATH / 'static' \
            / self.DJANGO_APP_NAME

        self.DJANGO_MEDIA_URL = 'media/react-media'
        self.DJANGO_MEDIA_PATH = self.DJANGO_ROOT_PATH / 'data' / 'web' \
            / 'media' / 'react-media'

    def run(self):
        self.build_react_app()
        self.copy_static_files()
        self.copy_media_files()
        self.copy_html_files()
        success_message('all proccess is completed!')
        info_message('Github: diasEric04\n\n')

    def build_react_app(self):
        info_message('build react app...')
        system = sys.platform

        cmd = f'cd {self.REACT_APP_PATH.str_path} ; npm run build'

        if system == 'win32':
            cmd = f'cd {self.REACT_APP_PATH.str_path} & npm run build'

        os.system(cmd)
        success_message('build completed!')

    def copy_static_files(self):
        info_message('copying ALL static files...')
        self.REACT_STATIC_FILES.self_walk(
            func_dirs=self.static_copy_dirs,
            func_files=self.static_copy_files
        )
        success_message('all static files are copied!')

    def copy_media_files(self):
        info_message('copying ALL media files...')
        for dir in self.REACT_MEDIA_PATHS:
            dir.self_list_dir(
                func_files=self.media_copy_files
            )
        success_message('all media files are copied!')

    def copy_html_files(self):
        info_message('copying html files...')
        self.REACT_BUILD_DIR.self_list_dir(
            func_files=self.html_copy_files
        )
        success_message('all html files are copied!')
    # secondary methods

    def static_copy_dirs(self, root, dir: str):
        if dir != 'media':
            new_dir = self.DJANGO_STATIC_FILES / dir
            warning_message(f'copying dir "{dir}/"')
            new_dir.remove_all()
            os.makedirs(new_dir.str_path, exist_ok=True)

    def static_copy_files(self, root, file):
        if os.path.basename(root) == "media":
            return
        original_file = CommonFile(root, file)
        new_dir = Directory(os.path.join(
            root.replace(
                self.REACT_STATIC_FILES.str_path,
                self.DJANGO_STATIC_FILES.str_path
            )
        ))

        warning_message(f'copying file "{file}"...')
        new_file = original_file.self_copy(new_dir)

        if new_file.extesion == '.js':
            warning_message(
                f'adjusting text of js file "{file}"'
            )
            self.rewrite_js(new_file)

        elif new_file.extesion in ['.scss', '.sass', '.css']:
            warning_message(
                f'adjusting text of stylesheet file "{file}"'
            )
            self.rewrite_stylesheet(new_file)

    def rewrite_js(self, new_file: CommonFile):
        new_js_file_text = ''

        def func_read(file: TextIOWrapper):
            nonlocal new_js_file_text
            js_text = file.read()
            new_js_file_text = JS_URL_REGEXP.sub(
                 r'"media/react-media/\2"', js_text
            )

        def func_write(file: TextIOWrapper):
            nonlocal new_js_file_text
            file.write(new_js_file_text)

        new_file.update_text(
            func_read=func_read,
            func_write=func_write
        )

    def rewrite_stylesheet(self, new_file: CommonFile):
        new_stylesheet_text = ''

        def func_read(file: TextIOWrapper):
            nonlocal new_stylesheet_text
            stytesheet_text = file.read()
            new_stylesheet_text = CSS_URL_REGEXP.sub(
                 r'url(/media/react-media/\2)', stytesheet_text
            )

        def func_write(file: TextIOWrapper):
            nonlocal new_stylesheet_text
            file.write(new_stylesheet_text)

        new_file.update_text(
            func_read=func_read,
            func_write=func_write
        )

    def media_copy_files(self, item):
        # item ja é um file valido
        item = CommonFile(item)
        if item.extesion != '.html':
            warning_message(f'copying media file "{item.file_name}"')
            item.self_copy(self.DJANGO_MEDIA_PATH)

    def html_copy_files(self, item):
        item = CommonFile(item)

        if item.extesion == '.html':
            warning_message(f'copying html file "{item.file_name}"')
            DJANGO_APP_TEMPLATE_PATH = self.DJANGO_APP_PATH / 'templates' \
                / self.DJANGO_APP_NAME / 'pages'
            new_item = item.self_copy(DJANGO_APP_TEMPLATE_PATH)

            new_html_text = ''

            def func_read(file: TextIOWrapper):
                nonlocal new_html_text
                html_text = file.read()

                link_tags = HTML_LINK_TAG_REGEXP.findall(html_text)
                script_tags = HTML_SCRIPT_TAG_REGEXP.findall(html_text)
                noscript_tags = HTML_NOSCRIPT_TAG_REGEXP.findall(html_text)
                divroot = HTML_DIVROOT_TAG_REGEXP.findall(html_text)

                app_name = self.DJANGO_APP_NAME

                link_tags = [
                    HTML_LINK_TAG_REGEXP.sub(
                        r'\2'+self.set_django_tag(app_name+r'\4')+r'\5',
                        link_tag) + '\n'
                    for link_tag, _, _, _, _ in link_tags
                ]

                script_tags = [
                    HTML_SCRIPT_TAG_REGEXP.sub(
                        r'\2'+self.set_django_tag(app_name+r'\4')+r'\5',
                        script_tag) + '\n'
                    for script_tag, _, _, _, _ in script_tags
                ]

                new_html_text = (
                    f"{{% extends '{app_name}/base.html' %}}\n"
                    '{% load static %}\n\n'

                    '{% block additional_links %}\n'
                    f"\t{''.join(script_tags)}"
                    f"\t{''.join(link_tags)}"
                    '{% endblock additional_links %}\n\n\n'


                    '{% block content %}\n'
                    f"\t{''.join(noscript_tags)}\n"
                    f"\t{''.join(divroot)}\n"
                    '{% endblock content %}\n'
                )

            def func_write(file: TextIOWrapper):
                nonlocal new_html_text
                file.write(new_html_text)

            new_item.update_text(
                func_read=func_read,
                func_write=func_write
            )

    @staticmethod
    def set_django_tag(str):
        return f"{{% static '{str}' %}}"
