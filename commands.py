# This is a sample commands.py.  You can add your own commands here.
#
# Please refer to commands_full.py for all the default commands and a complete
# documentation.  Do NOT add them all here, or you may end up with defunct
# commands when upgrading ranger.

# You always need to import ranger.api.commands here to get the Command class:
from ranger.api.commands import *
from ranger.container.file import File

# A simple command for demonstration purposes follows.
# -----------------------------------------------------------------------------

# You can import any python module as needed.
import os
import subprocess

# Any class that is a subclass of "Command" will be integrated into ranger as a
# command.  Try typing ":my_edit<ENTER>" in ranger!


class my_edit(Command):
    # The so-called doc-string of the class will be visible in the built-in
    # help that is accessible by typing "?c" inside ranger.
    """:my_edit <filename>

    A sample command for demonstration purposes that opens a file in an editor.
    """

    # The execute method is called when you run this command in ranger.
    def execute(self):
        # self.arg(1) is the first (space-separated) argument to the function.
        # This way you can write ":my_edit somefilename<ENTER>".
        if self.arg(1):
            # self.rest(1) contains self.arg(1) and everything that follows
            target_filename = self.rest(1)
        else:
            # self.fm is a ranger.core.filemanager.FileManager object and gives
            # you access to internals of ranger.
            # self.fm.thisfile is a ranger.container.file.File object and is a
            # reference to the currently selected file.
            target_filename = self.fm.thisfile.path

        # This is a generic function to print text in ranger.
        self.fm.notify("Let's edit the file " + target_filename + "!")

        # Using bad=True in fm.notify allows you to print error messages:
        if not os.path.exists(target_filename):
            self.fm.notify("The given file does not exist!", bad=True)
            return

        # This executes a function from ranger.core.acitons, a module with a
        # variety of subroutines that can help you construct commands.
        # Check out the source, or run "pydoc ranger.core.actions" for a list.
        self.fm.edit_file(target_filename)

    # The tab method is called when you press tab, and should return a list of
    # suggestions that the user will tab through.
    # tabnum is 1 for <TAB> and -1 for <S-TAB> by default
    def tab(self, tabnum):
        # This is a generic tab-completion function that iterates through the
        # content of the current directory.
        return self._tab_directory_content()

class termtab(Command):
    """:termtab <directory>
    open a new iterm tab in the specified directory,
    or the current directory if none is specified.
    Does nothing if we're not using iTerm
    """

    def execute(self):
        # If not using iTerm, return
        term_program = os.environ['TERM_PROGRAM']
        if term_program != "iTerm.app":
            self.fm.notify("Error: Not using iTerm!")
            return

        target_dir = None
        # If we've selected a directory:
        if self.arg(1):
            selected = self.rest(1)
            if not os.path.isdir(selected):
                self.fm.notify(selected + " is not a directory!")
                return
            target_dir = selected

        # Otherwise, use the current directory
        else:
            target_dir = self.fm.thisdir.path

        # run the applescript that opens the new tab
        os.system(
            'osascript ~/.config/ranger/scripts/iterm-newtab.scpt ' +
            '"cd \'{}\'"'.format(target_dir) +
            '&> /dev/null'
        )

class new_iterm_tab(Command):
    """:new_iterm_tab <directory>
    Opens ranger in a new iterm tab in the specified directory,
    or the current directory if none is specified.
    Does nothing if we're not using iTerm
    """

    def execute(self):
        # If not using iTerm, return
        term_program = os.environ['TERM_PROGRAM']
        if term_program != "iTerm.app":
            self.fm.notify("Error: Not using iTerm!")
            return

        target_dir = None
        # If we've selected a directory:
        if self.arg(1):
            selected = self.rest(1)
            if not os.path.isdir(selected):
                self.fm.notify(selected + " is not a directory!")
                return
            target_dir = selected

        # Otherwise, use the current directory
        else:
            target_dir = self.fm.thisdir.path

        # run the applescript that opens the new tab
        os.system(
            'osascript ~/.config/ranger/scripts/iterm-newtab.scpt ' +
            '"ranger \'{}\'"'.format(target_dir) +
            '&> /dev/null'
        )


    def tab(self, tabnum):
        return self._tab_directory_content()


class vimtab(Command):
    """:vimtab <filename>
    Opens filename in a new iTerm tab, provided we are running
    iterm. If filename is not specified, use the selected file
    """

    def execute(self):
        # If not using iTerm, return
        term_program = os.environ['TERM_PROGRAM']
        if term_program != "iTerm.app":
            self.fm.notify("Error: Not using iTerm!")
            return

        target_files = []
        # If we've selected a directory:
        if self.arg(1):
            selected = self.rest(1)
            if not os.path.exists(selected):
                self.fm.notify(selected + " is not a valid path!")
                return
            target_files = [selected]

        # Otherwise, use the selected files
        else:
            target_files = [f.path for f in self.fm.thistab.get_selection()]

        # Opening multiple directories at once gets a bit wierd in vim,
        # so just open the first one
        if any(map(os.path.isdir, target_files)):
            target_files = [target_files[0]]

        # run the applescript that opens the new tab
        os.system(
            'osascript ~/.config/ranger/scripts/iterm-newtab.scpt ' +
            '"vim {}"'.format(" ".join(map("'{}'".format, target_files))) +
            '&> /dev/null'
        )



    def tab(self, tabnum):
        return self._tab_directory_content()



class tmux_rtab(Command):
    """:tmux_rtab <directory>
    open ranger in a new tmux tab in the specified directory,
    or the current directory if none is specified.
    do nothing if we're not using tmux
    """

    def execute(self):
        # If not using iTerm, return
        tmux = os.environ['TMUX']
        if tmux == "":
            self.fm.notify("Error: Not using tmux!")
            return

        target_dir = None
        # If we've selected a directory:
        if self.arg(1):
            selected = self.rest(1)
            if not os.path.isdir(selected):
                self.fm.notify(selected + " is not a directory!")
                return
            target_dir = selected

        # Otherwise, use the current directory
        else:
            target_dir = self.fm.thisdir.path

        os.system(
            "tmux -2 new-window 'ranger {0}'".format(target_dir)
        )

    def tab(self, tabnum):
        return self._tab_directory_content()


class tmux_tab(Command):
    """:tmux_tab <directory>
    open a new tmux tab in the specified directory,
    or the current directory if none is specified.
    do nothing if we're not using tmux
    """

    def execute(self):
        # If not using iTerm, return
        tmux = os.environ['TMUX']
        if tmux == "":
            self.fm.notify("Error: Not using tmux!")
            return

        target_dir = None
        # If we've selected a directory:
        if self.arg(1):
            selected = self.rest(1)
            if not os.path.isdir(selected):
                self.fm.notify(selected + " is not a directory!")
                return
            target_dir = selected

        # Otherwise, use the current directory
        else:
            target_dir = self.fm.thisdir.path

        os.system(
            "tmux -2 new-window -c {0}".format(target_dir)
        )

    def tab(self, tabnum):
        return self._tab_directory_content()

