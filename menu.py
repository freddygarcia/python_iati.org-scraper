import sys
import collections
import readline

import click

import report
import downloader
import activities_filter

def set_completer(values):

    def completer(text, state):
        options = [
            v for v in values
            if v.lower().startswith(text.lower())
        ]

        try:
            return options[state]
        except IndexError:
            return None

    readline.set_completer(completer)
    readline.set_completer_delims('')
    readline.parse_and_bind("tab: complete")

def unset_completer():
    readline.set_completer()

class Menu():

    @staticmethod
    def pick(selected_filter, choice):
        result = dict(
            ('d', x) for x, y in selected_filter.items()
            if choice == y
        ).get('d')

        return result

    @staticmethod
    def format_display(filter_name):
        capitalized = filter_name[0].upper() + filter_name[1:]
        clean_chars = (capitalized
                            .replace('-', ' ')
                            .replace('__', ' ')
                            .replace('gt', '(greater than) ')
                            .replace('lt', '(less than) ')
                        )
        justified = clean_chars.ljust(30)
        return justified

    def __init__(self):
        self.reset_selected_filters()
        self.choices = dict(enumerate(activities_filter.filters.keys(), 1))

    def reset_selected_filters(self):
        self.selected_filters = collections.defaultdict(list)

    def show_menu(self):
        # clear screen
        click.clear()

        click.echo('IATI.org API downloader\n')

        for i, item in enumerate(activities_filter.filters.keys()):
            # capitalize first letter, padd padding
            formatted = Menu.format_display(item)
            # add current selections
            selected = self.selected_filters.get(item, '')
            # display text option
            click.echo(f' [{str(i + 1).rjust(2)}] {formatted} {selected} ',)

        # display extra options
        click.echo(' [77] Go')
        click.echo(' [88] Reset')
        click.echo(' [99] Bye')

    def select_choice(self):
        choice = click.prompt('> ', type=int)
        menu_choice = self.choices.get(choice)

        if choice == 77:
            click.echo('\nDownloading file...')
            f_content = downloader.retrieve_file(self.selected_filters)

            click.echo('Generating excel...')
            f_path = report.save(f_content)

            click.echo(f'File saved in ./{f_path}')
            click.prompt('Press Enter to continue...', default='', prompt_suffix='')
            return
        if choice == 88:
            if click.confirm('Sure want to reset?'):
                self.reset_selected_filters()
        elif choice == 99:
            if click.confirm('Sure want to exit?'):
                sys.exit(0)
        else:
            self.select_filter(menu_choice)

    def select_filter(self, menu_choice):
        selected_filter = activities_filter.filters.get(menu_choice)

        # add autocompletion
        if menu_choice not in activities_filter.no_autocomplete:
            set_completer(selected_filter.values())

        # read input choice
        choice = input(f"({menu_choice}) > ")
        if menu_choice not in activities_filter.no_autocomplete:
            # pick a filter by given choice
            result = Menu.pick(selected_filter, choice)
        else:
            # keep same value
            result = choice
        # check if result has some value
        valid_choice = result is not None

        if valid_choice:
            # avoid multiple values in dates
            if menu_choice in activities_filter.no_autocomplete:
                self.selected_filters[menu_choice] = [result]
            # avoid adding same values
            elif result not in self.selected_filters[menu_choice]:
                self.selected_filters[menu_choice].append(result)
        else:
            click.echo('Invalid choice')

        if click.confirm('Do you want to add more?'):
            self.select_filter(menu_choice)

    def loop(self):
        while True:
            self.show_menu()
            self.select_choice()
