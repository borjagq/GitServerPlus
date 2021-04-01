<?php

/**
 * Example_Class is a sample class for demonstrating PHPDoc
 * 
 * Repo is a class that allows us to retrieve information from a git
 * repository as well as updating such information.
 * 
 * @package GitServerPlus
 * @author Borja García Quiroga
 * @version $Revision: 1.0.0$
 * @access public
 */
class Repo {

	/**
	 * Git repository DirectoryIterator.
	 *
	 * @since 1.0.0
	 * @var DirectoryIterator $git_dir
	 */
	private $git_dir;

	/**
	 * Constructor.
	 *
	 * Constructor of the Repo instance from a DirectoryIterator instance.
	 *
	 * @since 1.0.0
	 *
	 * @param DirectoryIterator $di DirectoryIterator of the git repo directory.
	 */
	function __construct($di) {
		
		// Set the $git_dir property.
		$this->git_dir = clone $di;

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
		$path = $this->git_dir->getPathname();

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
		$path = $this->git_dir->getPathname();

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
		$path = $this->git_dir->getPathname();

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
		return $this->git_dir->getBasename('.' . $this->git_dir->getExtension());

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
		$path = $this->git_dir->getPathname();

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
		$path = $this->git_dir->getPathname();

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
		$path = $this->git_dir->getPathname();

		// Return the group name.
		return posix_getgrgid(filegroup($path))['name'];

	}
	
}

?>