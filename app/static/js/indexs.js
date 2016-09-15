$(function() {

$(".file-element").each( function() {
    console.log($(this))

    var hash = "#";
    var formd = "form-";
    var linkd = "link-";
    var dlcount = "dlcount-";
    var id = $('input[name="uniqueid"]', this).val();
    var cid = hash.concat(id);
    var fid = hash.concat(formd.concat(id));
    var lid = hash.concat(linkd.concat(id));
    var dlcid = hash.concat(dlcount.concat(id));

    $(lid).bind('click', function() {
    	setTimeout(function() {
    		$.getJSON('/api/dlcount', {
    		uniqueid: id
			}, function(data) {
				$(dlcid).text(data.response.dl_count);
			})
    	}, 50);

    });

    $(fid).submit(function(e) {
        $.getJSON('/api/delete', {
            uniqueid: id
        },
        function(data) {
            $('#response').text(data.response);
            $('#responseinfo').removeClass('hidden');
            $('#responseinfo').delay(10000).addClass('hidden')
            $(cid).fadeOut(100);
        });
        return false;
    });
}
);

});