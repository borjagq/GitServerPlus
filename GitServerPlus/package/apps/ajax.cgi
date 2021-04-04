#!/bin/php

<?php

// Require the functions file.
require_once(__DIR__ . '/functions.php');

// Require the classes.
require_once(__DIR__ . '/Repo.php');

// Get the auth message.
$auth_msg = shell_exec('/usr/syno/synoman/webman/login.cgi');

// Parse the HTTP response.
$auth_msg = http_parse_response($auth_msg)['Content'];

// Parse the JSON response.
$auth_msg = json_decode($auth_msg);

/*
// Check if the user is logged in.
if (!$auth_msg->success) {

	// Set the forbidden header status.
	http_response_code(403);
	die('{"success": false, "msg": "Forbidden"}');
	die();

}
*/

// Populate the $_GET variable.
parse_str(getenv('QUERY_STRING'), $_GET);

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

		// Create the git repo.
		shell_exec("git init --bare $path");

		// Create the Git repo directory iterator.
		$git_dir = new DirectoryIterator($path);

		// Create the Repo class.
		$git_dir = new Repo($git_dir);

		// Set the repo's team.
		$git_dir->setTeam($team);

		// Set the repo's description.
		$git_dir->setDesc($desc);

		// Set the repo's access level.
		$git_dir->setAccess($access);
		
		die('{"success": true}');

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

	default:

		die('{"success": false, "msg": "Wrong"}');

}

?>
