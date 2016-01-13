import sublime, sublime_plugin

class MoveByParagraphCommand(sublime_plugin.TextCommand):
    def run(self, edit, extend = False, forward = True):
        self.view.run_command("move_to", {"to": "hardbol", "extend": extend}) # to mimic TextPad's behaviour
        pt = self.view.sel()[0].b
        if forward:
            rg = self.view.find("\n\s*\n", pt)
            new_pt = rg.b if rg else self.view.size()
        else:
            # couldn't find "find previous" command
            rgs = self.view.find_all("\n[\s]*\n")
            new_pt = 0
            for rg in rgs:
                if rg.b < pt:
                    new_pt = rg.b
        new_pt_visible = self.view.visible_region().contains(new_pt)
        #
        # obviously inefficient way of doing it (couldn't find amount for move command)
        # becomes slow for veeeeery long paragraphs
        self.view.run_command("move", {"by": "lines", "forward": forward, "extend": extend})
        while (self.view.sel()[0].b < new_pt) == forward and self.view.sel()[0].b != pt:
            pt = self.view.sel()[0].b
            self.view.run_command("move", {"by": "lines", "forward": forward, "extend": extend})
        while self.view.sel()[0].b != new_pt:
            self.view.run_command("move", {"by": "characters", "forward": self.view.sel()[0].b < new_pt, "extend": extend})
        if not new_pt_visible:
            self.view.show_at_center(new_pt)