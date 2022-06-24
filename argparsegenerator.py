#!/usr/bin/env python3

"""
    Gathers the functions and generates argpase based on them.
"""

import argparse
import inspect

class ArgparseGenerator:

    def __init__(self) -> None:

        global_parser = argparse.ArgumentParser(add_help=False)
        global_parser.add_argument('--debug', default=False, required=False, action='store_true', dest="debug", help='debug flag')

        parser_tree = {}

        method_list = [method for method in dir(self) if not method.startswith('_')]

        parser_tree[None] = {
            '_parser': argparse.ArgumentParser(),
            '_subparser': None
        }

        for method_name in method_list:
            parts = []
            parent = None
            depth = 0
            for method_part in method_name.split('_'):
                parts.append(method_part)
                current_part = '_'.join(parts)
                if current_part not in parser_tree:
                    if not parser_tree[parent]['_subparser']:
                        parser_tree[parent]['_subparser'] = parser_tree[parent]['_parser'].add_subparsers(dest=f'method_part_{depth}')
                    help_string = None
                    try:
                        help_string = getattr(self, current_part).__doc__
                    except: pass
                    parser_tree[current_part] = {
                        '_parser': parser_tree[parent]['_subparser'].add_parser(method_part, help=help_string, parents=[global_parser]),
                        '_subparser': None
                    }
                parent = current_part
                depth += 1

            method_ref = getattr(self, method_name)

            signature = inspect.signature(method_ref)
            for arg_name, arg_value in signature.parameters.items():
                parser_tree[parent]['_parser'].add_argument(
                    f'--{arg_name}',
                    default=(arg_value.default if arg_value.default is not inspect.Parameter.empty else None),
                    required=(arg_value.default is inspect.Parameter.empty),
                )
                parser_tree[parent]['_method'] = method_ref

        parsed_args = parser_tree[None]['_parser'].parse_args()

        recovered_parts = []
        recovered_index = 0
        try:
            while True:
                found_method_part = parsed_args.__getattribute__(f'method_part_{recovered_index}')
                if found_method_part is None:
                    break
                recovered_parts.append(found_method_part)
                recovered_index += 1
        except AttributeError:
            pass

        if recovered_parts:
            recovered_method_name = '_'.join(recovered_parts)
            try:
                recovered_method = getattr(self, recovered_method_name)
                fas = inspect.getfullargspec(recovered_method)
                new_args = {}
                for arg in fas.args[1:]:
                    new_args[arg] = parsed_args.__dict__[arg]
                if parser_tree[recovered_method_name]['_subparser'] is not None:
                    parser_tree[recovered_method_name]['_parser'].print_help()
                else:
                    recovered_method(**new_args)
            except AttributeError:
                parser_tree[recovered_method_name]['_parser'].print_help()
        else:
            parser_tree[None]['_parser'].print_help()

    
    def files(self): """Manage files""" # Just used for documentation at this level, not needed as a function really.

    def files_upload(self, destination: str, auth_credentials: str='just an example'):
        """
        Uploads to destination and authenticates with auth_credentials
        """
        print(f'Uploading to "{destination}"')
        print('Done')

    def files_download(self, destination: str, auth_credentials: str='just an example'):
        """
        Downloads from destination and authenticates with auth_credentials
        """
        print(f'Downloading from "{destination}"')
        print('Done')

    def users(self): """Manage users""" # Just used for documentation at this level, not needed as a function really.

    def users_delete(self, username: str):
        """
        Creates a user.
        """
        print(f'Deleting user "{username}"')

    def users_create(self, username: str):
        """
        Deletes a user.
        """
        print(f'Creating user "{username}"')


if __name__ == '__main__':
    ArgparseGenerator()
