<?php

/**
 * Parses a HTTP response.
 *
 * Receives a string containing a HTTP response formed by headers and a message.
 *  * 
 * @param string $response
 * @return array
 */
function http_parse_response($response) {

	// Init the return value.
	$ret_val = array();

	// Separate the fields in the response.
	$fields = explode("\r\n", preg_replace('/\x0D\x0A[\x09\x20]+/', ' ', $response));

	// Get the very last field and store it.
	$ret_val['Content'] = $fields[count($fields) - 1];

	// Delete the last field that we set as content;
	unset($fields[count($fields) - 1]);

	// Iterate through the fields.
	foreach ($fields as $field) {

		// Do not process empty fields.
		if (empty($field)) {
			continue;
		}

		// Match the header pattern.
		if (preg_match('/([^:]+): (.+)/m', $field, $match)) {

			// Replace pattern by strtoupper.
			$match[1] = preg_replace('/(?<=^|[\x09\x20\x2D])./e', 'strtoupper("\0")', strtolower(trim($match[1])));

			// Check if that header has been already set in the return array.
			if (isset($ret_val[$match[1]])) {

				// If this header is not an array.
				if (!is_array($ret_val[$match[1]])) {

					// Transform it into one (array).
					$ret_val[$match[1]] = array($ret_val[$match[1]]);

				}

				// Append the new header.
				$ret_val[$match[1]][] = trim($match[2]);

			} else {

				// Store the header.
				$ret_val[$match[1]] = trim($match[2]);

			}

		} else {

			// If this no-header-like contains HTTP.
			if (preg_match('/HTTP\//', $field)) {

				// Following HTTP standards which are space-separated
				preg_match('/(.*?) (.*?) (.*)/', $field, $matches);

				// Store the HTTP values.
				$ret_val['HTTP']['version'] = $matches[1];
				$ret_val['HTTP']['code'] = $matches[2];
				$ret_val['HTTP']['reason'] = $matches[3];

			} else {

				// Store the content.
				$ret_val['Content'][] = $field;

			}

		}

	}

	return $ret_val;

}

?>