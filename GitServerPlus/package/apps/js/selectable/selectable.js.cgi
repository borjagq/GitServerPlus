#!/bin/php

<?php

// Require the functions file.
require_once(__DIR__ . '/../../functions.php');

// Authentication.
auth_control();

?>

// Create a custom select.
$.fn.selectable = function(name, values, selected, required=false) {

	// Create a new element.
	var inner = '<table class="selectable">' +
		'<thead>' +
			'<tr>' +
				'<th>' +
					'<label><input type="checkbox" /><span>' + selected + '</span></label>' +
				'</th>' +
			'</tr>' +
		'</thead>' +
		'<tbody>';

	required = (required) ? ' required' : '';
	
	// Iterate through the values in values.
	values.forEach(elm => {

		// Check if this one is checked or not.
		var sel_this = (elm == selected) ? ' checked' : '';

		// Append it to inner.
		inner += '<tr>' +
			'<td>' +
				'<label>' +
					'<input type="radio" name="' + name + '" value="' + elm + '"' + sel_this + required + ' />' +
					'<span>' + elm + '</span>' +
				'</label>' +
			'</td>' +
		'</tr>';
		
	});
	
	// Close it.
	inner += '</tbody></table>';

	// Put it int the element.
	this.html(inner);
		
};

// Close open selectables on any foreign click.
$(document).on('click', 'body', function(e) {

	// Mark the checkbox as closed.
	$('.selectable.visible input[type=checkbox]').prop('checked', false);

	// Remove the visible class.
	$('.selectable.visible').removeClass('visible');

});

// Avoid active closures from prompting double-events.
$(document).on('click', '.selectable.visible', function(e) {

	e.stopPropagation();

});

// Open / close the selectable.
$(document).on('change', '.selectable input[type=checkbox]', function(e) {

	// Check if it visible or not.
	if ($(this).prop('checked')) {

		// Make it visible.
		$(this).parents('.selectable').addClass('visible');

	} else {

		// Make it invisible.
		$(this).parents('.selectable').removeClass('visible');

	}

});

// Change the selected option.
$(document).on('change', '.selectable input[type=radio]', function(e) {

	// Set the top label's content with the selected value.
	$(this).parents('.selectable').find('thead label > span').text($(this).val());

	// Mark the checkbox as closed.
	$(this).parents('.selectable').find('input[type=checkbox]').prop('checked', false);

	// Remove the visible class.
	$(this).parents('.selectable').removeClass('visible');

});
