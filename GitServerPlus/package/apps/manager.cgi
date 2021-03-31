#!/bin/php

<?php

// Include the functions file.
require_once(__DIR__ . '/functions.php');

// Get the auth message.
$auth_msg = shell_exec('/usr/syno/synoman/webman/login.cgi');

// Parse the HTTP response.
$auth_msg = http_parse_response($auth_msg)['Content'];

// Parse the JSON response.
$auth_msg = json_decode($auth_msg);

// Check if the user is logged in.
if (!$auth_msg->success) {

	// Set the forbidden header status.
	http_response_code(403);
	die();

}

?>
<html>
	<head>
		<title>Git Repo Manager</title>
		<style>

		

		</style>
	</head>
	<body>
		<?php

		// Create a Git directory iterator.
		$git_dir = new DirectoryIterator('/git');

		// Iterate through the files and dirs in the git repo.
		foreach ($git_dir as $repo) {

			// If the file is a dot directory, skip it.
			if ($repo->isDot())
				continue;
			
			// If it does not have the properties of a git repo, skip it.
			if ($repo->getExtension() != 'git' || $repo->isFile())
				continue;

			// Get the repo team.
			$team = posix_getgrgid(filegroup($repo->getPathname()))['name'];

			echo $team . ' - ' . $repo->getFilename() . "<br>";

		}

		?>
	</body>
</html>
