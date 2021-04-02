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
	die();

}
*/

// Set the language.
setlocale(LC_TIME, 'es_ES', 'es_ES.utf8');

?>
<html>
	<head>
		<meta charset="UTF-8">
		<title>Git Repo Manager</title>
		<link href="/webman/3rdparty/GitServerPlus/styles/fontawesome/css/all.min.css" rel="stylesheet">
		<link href="/webman/3rdparty/GitServerPlus/styles/selectable/selectable.css" rel="stylesheet">
		<style>

			:root {
				--main-text-color: #505A64;
				--background-color: #FFFFFF;
				--gray-color: #C8D2DC;
				--secondary-color: #215FA6;
			}

			* {
				margin: 0;
				padding: 0;
				font-family: verdana,arial,tahoma,helvetica,sans-serif;
				box-sizing: border-box;
			}

			body {
				font-size: 12px;
				padding: 0 10px;
				color: var(--main-text-color);
				width: 100%;
				height: 100%;
    			overflow: hidden;
			}

			.wrapper {
				padding-top: 50px;
				height: 100%;
				overflow-y: scroll;
			}

			nav {
				box-sizing: border-box;
				border-bottom: solid 1px var(--gray-color);
				position: fixed;
				top: 0;
				right: 10px;
				left: 10px;
				width: auto;
				background-color: var(--background-color);
			}

			nav > table {
				width: 100%;
			}

			nav > table > tbody > tr > td {
				padding: 10px 0;
			}

			button {
				width: auto;
				height: 26px;
				margin: 0;
				margin-left: 6px;
				padding: 0 14px;
				font-family: inherit;
				font-size: 12px;
				font-weight: normal;
				vertical-align: top;
				color: var(--main-text-color);
				outline: 0;
				border: solid 1px var(--gray-color);
				border-radius: 3px;
				background-repeat: no-repeat;
				background-image: url('data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiP…dpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbGw9InVybCgjZ3JhZCkiIC8+PC9zdmc+IA==');
				background-size: 100%;
				background-image: -webkit-gradient(linear, 50% 0%, 50% 100%, color-stop(0%, #f5faff),color-stop(100%, #f0f5fa));
				background-image: -moz-linear-gradient(#f5faff,#f0f5fa);
				background-image: -webkit-linear-gradient(#f5faff,#f0f5fa);
				background-image: linear-gradient(#f5faff,#f0f5fa);
				background-color: #F0F5FA;
				cursor: pointer;
				display: inline-block;
				line-height: 26px;
			}

			button.color {
				border: solid 1px var(--secondary-color);
				background-image: linear-gradient(#3D80CC, #2466B2);
				background-color: #2466B2;
				color: var(--background-color);
			}

			button:first-child {
				margin-left: 0;
			}

			button:hover {
				border: solid 1px #B4BEC8;
				background-image: url('data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz4gPHN2ZyB2ZXJzaW9uPSIxLjEiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PGxpbmVhckdyYWRpZW50IGlkPSJncmFkIiBncmFkaWVudFVuaXRzPSJvYmplY3RCb3VuZGluZ0JveCIgeDE9IjAuNSIgeTE9IjAuMCIgeDI9IjAuNSIgeTI9IjEuMCI+PHN0b3Agb2Zmc2V0PSIwJSIgc3RvcC1jb2xvcj0iI2Y1ZmFmZiIvPjxzdG9wIG9mZnNldD0iMTAwJSIgc3RvcC1jb2xvcj0iI2ViZjBmNSIvPjwvbGluZWFyR3JhZGllbnQ+PC9kZWZzPjxyZWN0IHg9IjAiIHk9IjAiIHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbGw9InVybCgjZ3JhZCkiIC8+PC9zdmc+IA==');
				background-size: 100%;
				background-image: -webkit-gradient(linear, 50% 0%, 50% 100%, color-stop(0%, #f5faff),color-stop(100%, #ebf0f5));
				background-image: -moz-linear-gradient(#f5faff,#ebf0f5);
				background-image: -webkit-linear-gradient(#f5faff,#ebf0f5);
				background-image: linear-gradient(#f5faff,#ebf0f5);
				background-color: #EBF0F5;
			}

			button.color:hover {
				border: solid 1px #0E498C;
				background-image: linear-gradient(#337ACC, #125DB2);
				background-color: #125DB2;
			}

			button:active {
				border: solid 1px #B4BEC8;
				background-image: url('data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz4gPHN2ZyB2ZXJzaW9uPSIxLjEiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PGxpbmVhckdyYWRpZW50IGlkPSJncmFkIiBncmFkaWVudFVuaXRzPSJvYmplY3RCb3VuZGluZ0JveCIgeDE9IjAuNSIgeTE9IjAuMCIgeDI9IjAuNSIgeTI9IjEuMCI+PHN0b3Agb2Zmc2V0PSIwJSIgc3RvcC1jb2xvcj0iI2ViZjBmNSIvPjxzdG9wIG9mZnNldD0iMTAwJSIgc3RvcC1jb2xvcj0iI2U2ZWJmMCIvPjwvbGluZWFyR3JhZGllbnQ+PC9kZWZzPjxyZWN0IHg9IjAiIHk9IjAiIHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbGw9InVybCgjZ3JhZCkiIC8+PC9zdmc+IA==');
				background-size: 100%;
				background-image: -webkit-gradient(linear, 50% 0%, 50% 100%, color-stop(0%, #ebf0f5),color-stop(100%, #e6ebf0));
				background-image: -moz-linear-gradient(#ebf0f5,#e6ebf0);
				background-image: -webkit-linear-gradient(#ebf0f5,#e6ebf0);
				background-image: linear-gradient(#ebf0f5,#e6ebf0);
				background-color: #E6EBF0;
			}

			button.color:active {
				border: solid 1px #0E498C;
				background-image: linear-gradient(#266EBF, #1156A6);
				background-color: #1156A6;
			}

			.repos {
				width: 100%;
			}

			.git-repo {
				width: 100%;
				padding: 20px 20px 25px 20px;
				border-top: 1px solid var(--gray-color);
			}

			.git-repo:first-of-type {
				border-top: none;
			}

			.git-repo table {
				width: 100%;
			}

			.git-repo tr td {
				padding: 5px 0;
			}

			.git-repo h2 {
				display: inline-block;
				font-size: 20px;
				font-weight: normal;
				vertical-align: middle;
				color: var(--main-text-color);
			}

			.git-repo h2 > b {
				font-weight: bold;
			}

			.git-repo .access {
				display: inline-block;
				vertical-align: middle;
				color: #4caf50;
				border: 1px solid #4caf50;
				border-radius: 3px;
				font-size: 12px;
				padding: 0px 5px;
				margin-left: 5px;
			}

			.git-repo .access.protected {
				color: #ff9800;
				border-color: #ff9800;
			}

			.git-repo .access.private {
				color: #ff5722;
				border-color: #ff5722;
			}

			.git-repo .desc {
				color: #676767;
				font-size: 14px;

			}

			.git-repo .more-info span {
				font-size: 12px;
			}

			.git-repo .more-info span::before {
				content: "";
				display: inline-block;
				height: 4px;
				width: 4px;
				background-color: var(--main-text-color);
				vertical-align: middle;
				margin: 0 10px;
				border-radius: 100%;
			}

			.git-repo .more-info span:first-of-type::before {
				content: none;
			}

			.pop-up-window-wrapper {
				position: fixed;
				top: 0;
				right: 0;
				bottom: 0;
				left: 0;
			}

			.pop-up-window-wrapper:last-of-type {
				background-color: #ffffff88;
			}

			.pop-up-window-wrapper > .pop-up-window {
				width: 500px;
				height: 368px;
				margin: auto;
				position: absolute;
				top: 0;
				right: 0;
				bottom: 0;
				left: 0;
				background-color: var(--background-color);
				box-shadow: 0px 4px 8px #00000066;
				border: 1px solid var(--gray-color);
				
			}

			.pop-up-window-wrapper > .pop-up-window > .pop-up-container > nav {
				position: static;
				padding: 20px 0 0 0;
				border-bottom: none;
				background: transparent;
			}

			.pop-up-window-wrapper > .pop-up-window nav > table > tbody > tr > td {
				padding: 0;
				text-align: right;
			}

			.pop-up-window-wrapper > .pop-up-window.processing {
				position: absolute;
				top: 0;
				bottom: 0;
				margin: auto;
				width: 100%;
				height: 40px;
				text-align: center;
			}

			.pop-up-window-wrapper > .pop-up-window.processing > span {
				display: inline-block;
				width: auto;
				height: 40px;
				padding: 7px 20px 7px 52px;
				color: var(--main-text-color);
				border: 1px solid var(--gray-color);
				box-shadow: 0 3px 5px #a2a2a2;
				font-size: 16px;
				line-height: 24px;
				background-position: 20px;
				background-image: url(data:image/gif;base64,R0lGODlhGAAYAJECACpYjMjS3P///wAAACH/C05FVFNDQVBFMi4wAwEAAAAh/wtYTVAgRGF0YVhNUDw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNS1jMDIxIDc5LjE1NDkxMSwgMjAxMy8xMC8yOS0xMTo0NzoxNiAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENDIChXaW5kb3dzKSIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDoxMDlCMUQ4QTVGRDcxMUU0ODk3NEVENEQ3MEI2RDMwMyIgeG1wTU06RG9jdW1lbnRJRD0ieG1wLmRpZDoxMDlCMUQ4QjVGRDcxMUU0ODk3NEVENEQ3MEI2RDMwMyI+IDx4bXBNTTpEZXJpdmVkRnJvbSBzdFJlZjppbnN0YW5jZUlEPSJ4bXAuaWlkOjEwOUIxRDg4NUZENzExRTQ4OTc0RUQ0RDcwQjZEMzAzIiBzdFJlZjpkb2N1bWVudElEPSJ4bXAuZGlkOjEwOUIxRDg5NUZENzExRTQ4OTc0RUQ0RDcwQjZEMzAzIi8+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+Af/+/fz7+vn49/b19PPy8fDv7u3s6+rp6Ofm5eTj4uHg397d3Nva2djX1tXU09LR0M/OzczLysnIx8bFxMPCwcC/vr28u7q5uLe2tbSzsrGwr66trKuqqainpqWko6KhoJ+enZybmpmYl5aVlJOSkZCPjo2Mi4qJiIeGhYSDgoGAf359fHt6eXh3dnV0c3JxcG9ubWxramloZ2ZlZGNiYWBfXl1cW1pZWFdWVVRTUlFQT05NTEtKSUhHRkVEQ0JBQD8+PTw7Ojk4NzY1NDMyMTAvLi0sKyopKCcmJSQjIiEgHx4dHBsaGRgXFhUUExIREA8ODQwLCgkIBwYFBAMCAQAAIfkEBQ8AAgAsAAAAABgAGAAAAkiUj6nLnQBjNKFai6Sm92Y9CZ13gOGIlSbAoZ/Zji8Yd/MmosEt1aQDDAoRul3OdSj6UstK0/iMJnVSqXKKvFqpWNnROwyLDwUAIfkEBQ8AAgAsAgACABQACQAAAh2MfyLA3QiVmxDJ+aq5GOi9dN7HYV9QUmTYnalTAAAh+QQFDwACACwNAAIACQAUAAACFIyPqcvtD4+YtFoKst68+w+G4qgVACH5BAUPAAIALAIADQAUAAkAAAIdhH8iwd0IlZsQyfmquTjovXTex2EfUFJk2J2pUwAAOw==);
				background-repeat: no-repeat;
				background-color: var(--background-color);
				border-radius: 2px;
			}

			.pop-up-window-wrapper > .pop-up-window > .pop-up-container {
				padding: 20px;
			}

			.repo-info {
				width 100%;
			}

			.repo-info #field_team > table {
				width: 150px;
			}

			.repo-info td:nth-of-type(2) span {
				display: inline-block;
				width: 20px;
				text-align: center;
				font-weight: bold;
			}

			.repo-info td:nth-of-type(3) {
				width: 100%;
			}

			.pop-up-window input[type=text] {
				width: 100%;
				height: 26px;
				margin: 0;
				padding: 0 14px;
				font-family: inherit;
				font-size: 12px;
				font-weight: normal;
				vertical-align: top;
				color: var(--main-text-color);
				outline: 0;
				border: solid 1px var(--gray-color);
				border-radius: 3px;
				display: inline-block;
			}

			.pop-up-window > .pop-up-container > div > label,
			.pop-up-window > .pop-up-container > .repo-info > tbody > tr > td > label {
				font-size: 12px;
				color: var(--main-text-color);
				margin-bottom: 10px;
				display: inline-block;
			}

			.pop-up-window > .pop-up-container > * {
				margin-bottom: 15px;
			}

			label.required::after {
				content: "*";
				margin-left: 5px;
				color: var(--secondary-color);
				font-weight: bold;
			}

			.pop-up-window ul {
				list-style: none;
			}

			.pop-up-window ul > li {
				margin-top: 10px;
			}

			.pop-up-window label > input[type=radio] {
				display: none;
			}

			.pop-up-window label > input[type=radio] + i {
				display: inline-block;
				height: 15px;
				width: 15px;
				border: 2px solid var(--secondary-color);
				border-radius: 100%;
			}

			.pop-up-window label > input[type=radio]:checked + i {
				border: 6px solid var(--secondary-color);
			}

			.pop-up-window label > input[type=radio] + i + p {
				width: calc(100% - 25px);
				display: inline-block;
				margin-left: 5px;
				vertical-align: top;
			}

			.pop-up-window label > input[type=radio] + i + p > * {
				display: block;
			}

		</style>
		<script src="/webman/3rdparty/GitServerPlus/js/jquery/jquery.js.cgi"></script>
		<script src="/webman/3rdparty/GitServerPlus/js/selectable/selectable.js.cgi"></script>
		<script>

			// Open the dialog to create a new repository.
			function create_new_repo() {
				console.log("Hello, create!");
			}

			// Refresh the page.
			function refresh_page() {
				location.reload();
			}

		</script>
	</head>
	<body>
		<div class="wrapper">
			<nav class="top-menu">
				<table>
					<tbody>
						<tr>
							<td>
								<button onclick="create_new_repo();"><?php echo get_ui_string("Nuevo repositorio"); ?></button>
								<button onclick="refresh_page();"><?php echo get_ui_string("Refrescar"); ?></button>
							</td>
						</tr>
					</tbody>
				</table>
			</nav>
			<div class="repos">
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

					// Create the Repo class.
					$repo = new Repo($repo);

					// Get the repo team.
					$team = $repo->getTeam();

					// Get the repo name.
					$name = $repo->getName();

					// Get the description.
					$desc = $repo->getDesc();

					// Get the access level.
					$access = $repo->getAccess();

					// Get the update indicator.
					$last_update = $repo->getLastUpdate();

					// Get the total number of commits.
					$num_commits = $repo->getNumCommits();

					// Get the total number of branches.
					$num_branches = $repo->getNumBranches();

					// Init the access type names.
					$access_names = array(
						1	=> get_ui_string('Público'),
						2	=> get_ui_string('Protegido'),
						3	=> get_ui_string('Privado')
					);

					// Init the access type classes.
					$access_classes = array(
						1	=> 'public',
						2	=> 'protected',
						3	=> 'private'
					);

					?>
					<div class="git-repo">
						<table>
							<tbody>
								<tr>
									<td>
										<h2><?php echo $team; ?> / <b><?php echo $name; ?></b></h2>
										<span class="access <?php echo $access_classes[$access]; ?>"><?php echo $access_names[$access]; ?></span>
									</td>
								</tr>
								<tr>
									<td style="padding-top: 10px;">
										<span class="desc"><?php echo $desc; ?></span>
									</td>
								</tr>
								<tr class="more-info">
									<td>
										<span class="last-update"><?php echo $last_update; ?></span><!--
										--><span class="num-commits"><i class="fas fa-undo"></i> <?php echo $num_commits; ?> commits</span><!--
										--><span class="num-branches"><i class="fas fa-code-branch"></i> <?php echo $num_branches; ?> branches</span>
									</td>
								</tr>
							</tbody>
						</table>
					</div>
					<?php

				}
				
				?>
			</div>
		</div>
		<div class="pop-up-window-wrapper">
			<div class="pop-up-window">
				<form id="create_new_repo" class="pop-up-container" method="post">
					<table class="repo-info">
						<tbody>
							<tr>
								<td>
									<label class="required" for="field_team"><?php echo get_ui_string("Equipo"); ?></label>
								</td>
								<td></td>
								<td>
									<label class="required" for="field_name"><?php echo get_ui_string("Nombre del repositorio"); ?></label>
								</td>
							</tr>
							<tr>
								<td>
									<div id="field_team"></div>
								</td>
								<td><span>/</span></td>
								<td>
									<input id="field_name" name="name" type="text" required />
								</td>
							</tr>
						</tbody>
					</table>
					<div>
						<label for="field_desc"><?php echo get_ui_string("Descripción"); ?></label>
						<input id="field_desc" name="desc" type="text" />
					</div>
					<div>
						<ul>
							<li>
								<label>
									<input name="access" type="radio" value="1" required />
									<i></i>
									<p>
										<b><?php echo get_ui_string("Público"); ?></b>
										<span><?php echo get_ui_string("Todos los usuarios pueden hacer pull y hacer push."); ?></span>
									</p>
								</label>
							</li>
							<li>
								<label>
									<input name="access" type="radio" value="2" required />
									<i></i>
									<p>
										<b><?php echo get_ui_string("Protegido"); ?></b>
										<span><?php echo get_ui_string("Todos los usuarios pueden hacer pull pero solo los del grupo pueden hacer push."); ?></span>
									</p>
								</label>
							</li>
							<li>
								<label>
									<input name="access" type="radio" value="3" required checked />
									<i></i>
									<p>
										<b><?php echo get_ui_string("Privado"); ?></b>
										<span><?php echo get_ui_string("Solo los usuarios del grupo pueden hacer pull y push."); ?></span>
									</p>
								</label>
							</li>
						</ul>
					</div>
					<nav class="bottom-menu">
						<table>
							<tbody>
								<tr>
									<td>
										<button id="submit" class="color"><?php echo get_ui_string("Guardar"); ?></button>
										<button id="close_pop_up"><?php echo get_ui_string("Cancelar"); ?></button>
									</td>
								</tr>
							</tbody>
						</table>
					</nav>
				</form>
			</div>
		</div>
		<script>

			// Create the select.
			$("#field_team").selectable('team', ['value 1', 'value 2', 'value 3', 'vaue 4'], '-- Equipo --', true);

		</script>
		<!--
		<div class="pop-up-window-wrapper">
			<div class="pop-up-window processing">
				<span>Procesando...<span>
			</div>
		</div>
		-->
	</body>
</html>
