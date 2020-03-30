"""
@name     Surround
@package  sublime_plugin
@author   Elliot Marsden

Change or delete characters surrounding a selection.
"""
# pylint: disable=too-few-public-methods

import re

import sublime  # pylint: disable=import-error
import sublime_plugin  # pylint: disable=import-error

TAG_REGEX = r"<([\S]+)([^>]*)>"

def settings():
    return sublime.load_settings("Surround.sublime-settings")

def pair_from_char(surround_char, pairs):
    return pairs.get(surround_char, [(surround_char), surround_char])

def search_patterns_for_surround(surround_char):
    surround_pair = taggify_for_search(
        pair_from_char(
            surround_char,
            settings()["pairs_for_search"],
        )
    )
    return dict(
        open=surround_pair[0],
        close=surround_pair[1],
        flags=sublime.LITERAL if len(surround_pair[0]) <= 1 else 0
    )

def pair_replacement_char(surround_char):
    return taggify_for_replacement(
        pair_from_char(
            surround_char,
            settings()["pairs_for_replace"],
        )
    )

def taggify_for_replacement(surround_pair):
    matches = re.search(TAG_REGEX, surround_pair[0])
    if matches:
        return [surround_pair[0], "</" + matches.group(1) + ">"]
    return surround_pair

def taggify_for_search(surround_pair):
    matches = re.search(TAG_REGEX, surround_pair[0])
    if matches:
        attrs = matches.group(2)
        if len(attrs) == 0:
            attrs = r"([\s]+[^>]*)?"
        open_tag = str("<" + matches.group(1) + attrs + ">")
        close_tag = str("</" + matches.group(1) + ">")
        return [open_tag, close_tag]
    return surround_pair

# Commands to orchestrate input.

class SurroundAddWithPromptCommand(sublime_plugin.WindowCommand):
    """ Surround the selection with something. """

    def run(self):
        self.window.show_input_panel(
            "Surround with:",
            "",
            lambda s: self.window.active_view().run_command(
                "surround_add",
                dict(surround_char=s)
            ),
            None,
            None,
        )

class SurroundChangeWithPromptCommand(sublime_plugin.WindowCommand):
    """ Change the selection's surroundings. """

    def run(self):
        def match_callback(match):
            self.window.show_input_panel(
                "Replace with:",
                "",
                lambda r: self.window.active_view().run_command(
                    "surround_change",
                    dict(match=match, replacement=r)
                ),
                None,
                None,
            )

        self.window.show_input_panel(
            "Match:",
            "",
            match_callback,
            None,
            None,
        )

class SurroundDeleteWithPromptCommand(sublime_plugin.WindowCommand):
    """ Delete something surrounding something. """

    def run(self):
        self.window.show_input_panel(
            "Delete:",
            "",
            lambda m: self.window.active_view().run_command(
                "surround_change",
                dict(match=m, replacement='')
            ),
            None,
            None,
        )

# Commands to do the actual edits.

class SurroundAddCommand(sublime_plugin.TextCommand):
    """ Surround the selection with something """

    def run(self, edit, surround_char):
        surround_pair = pair_replacement_char(surround_char)

        for region in reversed(self.view.sel()):
            self.view.insert(edit, region.end(), surround_pair[1])
            self.view.insert(edit, region.begin(), surround_pair[0])

class SurroundChangeCommand(sublime_plugin.TextCommand):
    """ Change the selection's surroundings. """

    def run(self, edit, match, replacement):
        search = search_patterns_for_surround(match)
        replacement_pair = pair_replacement_char(replacement)

        # Traverse regions backwards so edits don't clobber each other.
        for region in reversed(self.view.sel()):
            end = self.find_end(region.end(), search)
            start = self.find_start(region.begin(), search)
            self.view.replace(edit, end, replacement_pair[1])
            self.view.replace(edit, start, replacement_pair[0])

    def find_start(self, to_pos, search):
        open_matches = self.find_between(0, to_pos, search['open'], search['flags'])
        if not open_matches:
            raise RuntimeError(f"Starting pair not found: {search['open']}")

        prev = open_matches.pop()

        # TODO: I don't think this balancing logic is correct.
        # Balance pairs.
        nr_closers = len(
            self.find_between(prev.end(), to_pos, search['close'], search['flags'])
        )
        return prev if nr_closers % 2 == 0 else self.find_start(prev.begin(), search)

    def find_end(self, from_pos, search):
        nxt = self.view.find(search['close'], from_pos, search['flags'])
        if nxt is None:
            raise RuntimeError(f"Ending pair not found: {search['close']}")

        # Balance pairs.
        nr_openers = len(
            self.find_between(from_pos, nxt.begin(), search['open'], search['flags'])
        )
        return nxt if nr_openers % 2 == 0 else self.find_end(nxt.end(), search)

    def find_between(self, from_pos, to_pos, to_find, flags):
        # TODO: Seems inefficient, better API calls?
        return [
            find for find in self.view.find_all(to_find, flags)
            if find.end() <= to_pos
            and find.begin() >= from_pos
        ]
