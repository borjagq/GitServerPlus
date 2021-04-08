<?php

/**
 * Repo is a class for managing Git repositories.
 * 
 * Repo is a class that allows us to retrieve information from a git
 * repository as well as updating such information.
 * 
 * @package GitServerPlus
 * @author Borja García Quiroga
 * @version $Revision: 2.0.0$
 * @access public
 */
class Repo extends SplFileInfo {

	/**
	 * Create a new repo.
	 * 
	 * Creates a new Git repository and returns the Repo class.
	 * 
	 * @since 1.1.0
	 * 
	 * @param string $path Path of the new git repo.
	 * @return Repo
	 */
	static public function initRepo($path) {

		// Test if it is a repo.
		if (Repo::testRepo($path))
			return false;

		// Create the git repo.
		shell_exec("git init --bare $path");

		// Create the Repo class.
		$git = new Repo($path);

		return $git;

	}

	/**
	 * Test git repo.
	 * 
	 * Test if a directory is a git repository.
	 * 
	 * @param string $path Path of the new git repo.
	 * @return bool
	 */
	static public function testRepo($path) {

		// Check if the file does not exist.
		if (!file_exists($path))
			return false;

		// Execute the git command to test the directory.
		$ret = shell_exec("git --git-dir ${path} rev-parse");

		// If $ts is empty.
		if ($ret == "" || $ret == "\n")
			return true;

		return false;

	}

	/**
	 * Constructor.
	 *
	 * Constructor of the Repo instance from a DirectoryIterator instance.
	 *
	 * @since 1.0.0
	 *
	 * @param DirectoryIterator|string $di DirectoryIterator of the git repo directory or path.
	 */
	public function __construct($dir) {

		// Check if the parameter is a DirectoryIterator.
		if (is_a($dir, 'DirectoryIterator')) {
			
			// Get the path of the repo.
			$dir = $dir->getPathname();
		
		}
		
		// Call the SplFileInfo standard constructor.
		parent::__construct($dir);

	}

	/**
	 * Get the repo's access level.
	 *
	 * Returns the access level of the repository based on the permissions.
	 *
	 * @since 1.0.0
	 *
	 * @return string Repository's description.
	 */
	public function getAccess() {
		
		// Get the path of the repo.
		$path = $this->getPathname();

		// Get the permissions.
		$perms = fileperms($path);

		// Group.
		$info .= (($perms & 0x0020) ? 'r' : '-');
		$info .= (($perms & 0x0010) ? 'w' : '-');

		// World.
		$info .= (($perms & 0x0004) ? 'r' : '-');
		$info .= (($perms & 0x0002) ? 'w' : '-');

		// Switch through the options.
		switch ($info) {

			case 'rwrw':
				$access = 1;
				break;

			case 'rwr-':
				$access = 2;
				break;

			case 'rw--':
				$access = 3;
				break;

		}

		// Return the label.
		return $access;

	}

	/**
	 * Get the repo's description.
	 *
	 * Returns the description of the repository.
	 *
	 * @since 1.0.0
	 *
	 * @return string Repository's description.
	 */
	public function getDesc() {
		
		// Get the path of the repo.
		$path = $this->getPathname();

		// Return the content of the description.
		return file_get_contents($path . '/description');

	}

	/**
	 * Get the last update.
	 * 
	 * Get the date of the last update as a convenient string.
	 * 
	 * @since 1.0.0
	 * 
	 * @return string Repository's last update.
	 */
	public function getLastUpdate() {

		// Get the path of the repo.
		$path = $this->getPathname();

		// Execute the log command to retrieve the last commit.
		$ts = shell_exec("git --git-dir ${path} log -1 --format=%ct");

		// If $ts is empty.
		if ($ts == "" || $ts == "\n")
			return get_ui_string("No se ha actualizado nunca");

		// Convert the timestamp to an integer.
		$ts = intval($ts);

		// Get the current timestamp.
		$now = time();

		// Get the difference.
		$diff = $now - $ts;

		// If it was less than a minute ago.
		if ($diff < 60)
			return get_ui_string("Actualizado ahora mismo");
		
		// Convert this seconds difference to minutes.
		$diff = bgq_intdiv($diff, 60);
		
		// If it was a matter of minutes.
		if ($diff < 60)
			return get_ui_string("Actualizado hace %d minutos", array($diff));

		// Convert this minutes difference to hours.
		$diff = bgq_intdiv($diff, 60);
		
		// If it was a matter of hours.
		if ($diff < 24)
			return get_ui_string("Actualizado hace %d horas", array($diff));

		// Convert this hours difference to days.
		$diff = bgq_intdiv($diff, 24);
		
		// If it was a matter of days.
		if ($diff < 7)
			return get_ui_string("Actualizado hace %d días", array($diff));

		// Convert this days difference to weeks.
		$diff_2 = bgq_intdiv($diff, 7);
		
		// If it was a matter of 1 or 2 weeks.
		if ($diff_2 == 1)
			return get_ui_string("Actualizado hace %d semana", array($diff));

		// If it was a matter of 1 or 2 weeks.
		if ($diff_2 == 2)
			return get_ui_string("Actualizado hace %d semanas", array($diff));

		// Convert this days difference to years.
		$diff = bgq_intdiv($diff, 365);

		// Check if one year went by or not.
		if ($diff < 1) {

			// Get the date format.
			$format = get_ui_string("%e de %B");

		} else {

			// Get the date format, including the year.
			$format = get_ui_string("%e de %B de %G");

		}

		// Get the date.
		$date = trim(strftime($format, $ts));

		// Return the string indicating the date.
		return get_ui_string("Actualizado el %s", array($date));

	}

	/**
	 * Get the repo's name.
	 *
	 * Returns the name of the repository file.
	 *
	 * @since 1.0.0
	 *
	 * @return string Repository name.
	 */
	public function getName() {
		
		// Return the name excluding the extension.
		return $this->getBasename('.' . $this->getExtension());

	}

	/**
	 * Get the commit count.
	 * 
	 * Get the total number of commits in the repository.
	 * 
	 * @since 1.0.0
	 * 
	 * @return int Commit count.
	 */
	public function getNumCommits() {

		// Get the path of the repo.
		$path = $this->getPathname();

		// Execute the log command to retrieve the commit count.
		$count = shell_exec("git --git-dir ${path} rev-list --all --count");

		// Return it as an integer.
		return intval($count);

	}

	/**
	 * Get the branch count.
	 * 
	 * Get the total number of branches in the repository.
	 * 
	 * @since 1.0.0
	 * 
	 * @return int Branch count.
	 */
	public function getNumBranches() {

		// Get the path of the repo.
		$path = $this->getPathname();

		// Execute the log command to retrieve the branch count.
		$count = shell_exec("git --git-dir ${path} branch --all | wc -l");

		// Return it as an integer.
		return intval($count);

	}

	/**
	 * Get the repo's team.
	 *
	 * Returns the name of the repository's owning group (team).
	 *
	 * @since 1.0.0
	 *
	 * @return string Repository owning group's name.
	 */
	public function getTeam() {
		
		// Get the path of the repo.
		$path = $this->getPathname();

		// Return the group name.
		return posix_getgrgid(filegroup($path))['name'];

	}

	/**
	 * Set the repo's access level.
	 *
	 * Sets the permissions of the repository based on the acces level.
	 *
	 * @since 1.0.0
	 *
	 * @param int Access level.
	 */
	public function setAccess($access) {
		
		// Get the path of the repo.
		$path = $this->getPathname();

		// Switch through the options.
		switch ($access) {

			// Public.
			case 1:
				shell_exec("chmod -R u=rwx,g=rwx,o=rw $path");
				break;

			// Protected.
			case 2:
				shell_exec("chmod -R u=rwx,g=rwx,o=r $path");
				break;

			case 3:
				shell_exec("chmod -R u=rwx,g=rwx,o= $path");
				break;

		}

	}

	/**
	 * Set the repo's description.
	 *
	 * Sets the description of the repository.
	 *
	 * @since 1.0.0
	 *
	 * @param string Repository's description.
	 */
	public function setDesc($desc) {
		
		// Get the path of the repo.
		$path = $this->getPathname();

		// Store the content of the description.
		file_put_contents($path . '/description', $desc);

	}

	/**
	 * Set the repo's team.
	 *
	 * Sets the team (group) which owns the repository.
	 *
	 * @since 1.0.0
	 *
	 * @param string Repository's owning group's name.
	 */
	public function setTeam($team) {
		
		// Get the path of the repo.
		$path = $this->getPathname();

		// Set the group.
		shell_exec("chgrp -R $team $path");

	}

	/**
	 * Delete git repo.
	 * 
	 * Delete the git repo and all its files.
	 * 
	 * @return bool
	 */
	public function delete() {

		// Get the path of the repo.
		$path = $this->getPathname();

		// Execute the command.
		$status = shell_exec("rm -rf $path 2>&1; echo $?");

		// If $status is empty.
		if ($ret == "" || $ret == "\n")
			return true;

		// Otherwise, it didn't work.
		return false;

	}

	/**
	 * Rename git repo.
	 * 
	 * Rename the git repo and return the new Repo.
	 * 
	 * @param string $new_path New path to the repo.
	 * @return Repo
	 */
	public function renameRepo($new_path) {

		// Check if the new path is equal to the current one.
		if ($this->getPathname() == $new_path)
			return false;

		// Check if the current file is already a repository.
		if (Repo::testRepo($new_path))
			return false;

		// Rename the repo.
		if (!rename($this->getPathname(), $new_path))
			return false;

		// Create and renew the new Repo instance.
		return new Repo($new_path);

	}
	
}

?>