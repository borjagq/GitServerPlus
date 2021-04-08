#!/bin/php

<?php

// Require the functions file.
require_once(__DIR__ . '/functions.php');

// Require the classes.
require_once(__DIR__ . '/Repo.php');

// Populate the $_GET variable.
parse_str(getenv('QUERY_STRING'), $_GET);

// Authentication.
auth_control();

// Check that the variable function is set.
if (!isset($_GET['func']))
	die('{"success": false, "msg": "Missing"}');

// Switch through the different options.
switch ($_GET['func']) {

	// Create a new repo.
	case 'create_repo':

		// Get the parameters.
		$team = $_GET['team'];
		$name = $_GET['name'];
		$desc = $_GET['desc'];
		$access = intval($_GET['access']);

		// Get the existing groups.
		$groups = get_groups();
		
		// Check if they are acceptable.
		// Check if the team is not an existing group.
		if (!in_array($team, $groups))
			die('{"success": false, "msg": "Wrong team"}');

		// Check if the name matches the accepted regex.
		if (!preg_match('/[A-Za-z0-9]+/', $name))
			die('{"success": false, "msg": "Wrong name"}');

		// Check if the access is not in the range.
		if ($access < 1 || $access > 3)
			die('{"success": false, "msg": "Wrong access"}');

		// Create the path for the git repo.
		$path = '/git/' . $name . '.git';

		// Check if the file exists.
		if (Repo::testRepo($path))
			die('{"success": false, "msg": "Already exists"}');

		// Create the git repo.
		$git = Repo::initRepo($path);

		// Set the repo's team.
		$git->setTeam($team);

		// Set the repo's description.
		$git->setDesc($desc);

		// Set the repo's access level.
		$git->setAccess($access);
		
		die('{"success": true}');

		break;

	// Return the repo's info.
	case 'delete_repo':

		// Get the parameters.
		$name = $_GET['repo'];

		// Check if the name matches the accepted regex.
		if (!preg_match('/[A-Za-z0-9]+/', $name))
			die('{"success": false, "msg": "Wrong name"}');

		// Create the path for the git repo.
		$path = '/git/' . $name . '.git';

		// Check if the file does not exist.
		if (!Repo::testRepo($path))
			die('{"success": false, "msg": "Not found"}');

		// Create the Repo class.
		$git = new Repo($path);

		// Delete the repo.
		if (!$git->delete())
			die('{"success": false, "msg": "Could not delete"}');

		// Build the return var.
		$ret = array(
			"success"	=> true,
			"return"	=> $ret
		);

		// Echo the result.
		echo json_encode($ret);

		break;
	

	// Return the user groups in the system.
	case 'get_groups':

		// Get the existing groups.
		$groups = get_groups();

		// Build the return var.
		$ret = array(
			"success"	=> true,
			"return"	=> $groups
		);

		// Echo the result.
		echo json_encode($ret);

		break;

	// Return the repo's info.
	case 'get_repo_info':

		// Get the parameters.
		$path = $_GET['repo'];

		// Check if the file does not exist.
		if (!Repo::testRepo($path))
			die('{"success": false, "msg": "Not found"}');

		// Create the Repo class.
		$git = new Repo($path);

		// Get the repo's name.
		$name = $git->getName();

		// Get the repo's team.
		$team = $git->getTeam();

		// Get the repo's description.
		$desc = $git->getDesc();

		// Set the repo's access level.
		$access = $git->getAccess();
		
		// Get the return array.
		$ret = array(
			'name'		=> $name,
			'team'		=> $team,
			'desc'		=> $desc,
			'access'	=> $access
		);

		// Build the return var.
		$ret = array(
			"success"	=> true,
			"return"	=> $ret
		);

		// Echo the result.
		echo json_encode($ret);

		break;

	// Update a repo.
	case 'update_repo':

		// Get the parameters.
		$old_path = $_GET['old_path'];
		$team = $_GET['team'];
		$name = $_GET['name'];
		$desc = $_GET['desc'];
		$access = intval($_GET['access']);

		// Get the existing groups.
		$groups = get_groups();
		
		// Check if they are acceptable.
		// Check if the team is not an existing group.
		if (!in_array($team, $groups))
			die('{"success": false, "msg": "Wrong team"}');

		// Check if the name matches the accepted regex.
		if (!preg_match('/[A-Za-z0-9]+/', $name))
			die('{"success": false, "msg": "Wrong name"}');

		// Check if the access is not in the range.
		if ($access < 1 || $access > 3)
			die('{"success": false, "msg": "Wrong access"}');

		// Check if the file exists.
		if (!Repo::testRepo($old_path))
			die('{"success": false, "msg": "Not found"}');

		// Create the path for the git repo.
		$path = '/git/' . $name . '.git';

		// Create the Repo instance.
		$git = new Repo($old_path);

		// Check if there is a rename to be done.
		if ($path != $old_path) {

			// Check if the file already exists.
			if (Repo::testRepo($path))
				die('{"success": false, "msg": "Already exists"}');

			// Rename the git repo.
			$git = $git->renameRepo($path);

			// Check if it was succesfully renamed.
			if ($git === false)
				die('{"success": false, "msg": "Could not be renamed"}');

		}

		// Set the repo's team.
		$git->setTeam($team);

		// Set the repo's description.
		$git->setDesc($desc);

		// Set the repo's access level.
		$git->setAccess($access);
		
		die('{"success": true}');

		break;

	default:

		die('{"success": false, "msg": "Wrong"}');

}

?>
