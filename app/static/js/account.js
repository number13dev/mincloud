$(function() {

var other_form = function(e) {
		var toSentData = $("form").serialize();

		$.post('/_account', toSentData, function(data) {
				$('#response').text(data.response);
				$('#responseinfo').removeClass('hidden');
				$('#responseinfo').delay(10000).fadeOut(300);
				$('#newuserform')[0].reset();
				$('input[name=username]').focus().select();
			});
		return false;
};

$('#newuserform').submit(other_form);

});