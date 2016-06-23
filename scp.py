import os
import sublime, sublime_plugin

class ScpCommand(sublime_plugin.WindowCommand):
	def _get_cmd(self):
		settings = self.window.project_data()['settings']['scp']
		filepath = self.window.active_view().file_name()
		project_path = self.window.extract_variables()['folder']
		external_path = os.path.join(settings['bind_dir'], filepath[len(project_path)+1:])

		return 'scp -P %d %s %s@%s:%s' % (
			settings['port'],
			filepath,
			settings['username'],
			settings['domain'],
			external_path,
		)

	def run(self):
		project_path = self.window.extract_variables()['folder']
		settings = self.window.project_data()['settings']['scp']
		view = self.window.active_view()
		filepath = view.file_name()
		view.run_command("save")
		if filepath.startswith(project_path):
			cmd = self._get_cmd()
			print(cmd)
			err = os.system(cmd)
			if err:
				print("Error: ", err)
				view.set_status("Scp", "Error scp: " + str(err))
				# self.window.status_message("Error scp: " + str(err))
			else:
				view.set_status("Scp", "Ok: send to " + settings['domain'])
				# self.window.status_message("Ok: send to " + settings['domain'])
