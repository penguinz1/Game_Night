jQuery(document).ready(function($){

	$('.autofield').on('keyup change paste', function() {
		$(this).attr('value', $(this).val());
	});

});