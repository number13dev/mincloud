
var csrftoken = $('meta[name=csrf-token]').attr('content');

var apiurls = {
	api_publiclink_create: '/api/publiclink/create',
	api_publiclink_unpublish: '/api/publiclink/unpublish',
	api_publiclink_publish: '/api/publiclink/publish',
	api_file_delete: '/api/delete',
	api_dlcount: '/api/dlcount'
};

var fileelementfun =  function() {

		//todo needs improvements this is such a waste xD - but works for now
		var id = $('input[name="uniqueid"]', this).val();

		var hash = "#";
		var formd = "delete-";
		var linkd = "link-";

		//public links stuff
		var pubbutton = "pubbutton-";
		var unpub = "unpub-";
		var pubd = "pub-";
		var crpub = "crpub-";
		var unpubid = hash.concat(unpub.concat(id));
		var pubid = hash.concat(pubd.concat(id));
		var createpubid = hash.concat(crpub.concat(id));
		var pubbuttonid = hash.concat(pubbutton.concat(id));


		//to toggle the dropdown
		var dropd = "dropdown-";
		var dropdid = hash.concat(dropd.concat(id));

		var cid = hash.concat(id); //complete row
		var deleteid = hash.concat(formd.concat(id));
		var linkid = hash.concat(linkd.concat(id));

		//for the download count
		var dlcount = "dlcount-";
		var dlcountid = hash.concat(dlcount.concat(id));

		var toSentData = {csrf_token: csrftoken, uniqueid: id}

		//todo change dropdown menu based on action
		//Make Public
		var create_public = function(e) {
			  $.getJSON('/api/publiclink/create', toSentData, function(data) {
				var linkresponse = "<p>" +
					  data.response +
					  "</p>" +
					  "<div class=\"input-group\">" +
					  "<input id=\"#pubresponse\" type=\"text\" class=\"form-control\" value=" +
					  data.url +
					  ">" +
					  "<div class=\"input-group-btn\">" +
					  "<button type=\"button\" data-clipboard-target=\"#pubresponse\" class=\"btn\">"+
					  "<i class=\"fa fa-clipboard fa-fw\"></i>"  +
					  "</button>" +
					  "</div>" +
					  "</div>";
				$('#response').html(linkresponse);
				$(dropdid).dropdown('toggle');
				$('#responseinfo').removeClass('hidden');
				$('#responseinfo').delay(20000).fadeOut(300);
				$(pubbuttonid).html(data.button);
			  });
			  return false;
		};

		//Unpublish
		var unpublish = function(e) {
			$.getJSON('/api/publiclink/unpublish', toSentData, function(data) {
				$('#response').text(data.response);
				$('#responseinfo').removeClass('hidden');
				$('#responseinfo').delay(1000).fadeOut(300);
				$(dropdid).dropdown('toggle');
				$(pubbuttonid).html(data.button);
			});
			return false;
		};

		//Publish
		var publish = function(e) {
			$.getJSON('/api/publiclink/publish', toSentData, function(data) {
				$('#response').text(data.response);
				$('#responseinfo').removeClass('hidden');
				$('#responseinfo').delay(10000).fadeOut(300);
				$(dropdid).dropdown('toggle');
				$(pubbuttonid).html(data.button);
			});
			return false;
		};

		//Delete
		var deletefun = function(e) {
				$.getJSON('/api/delete', toSentData,
				function(data) {
					$('#response').text(data.response);
					$('#responseinfo').removeClass('hidden');
					$('#responseinfo').delay(10000).addClass('hidden')
					$(dropdid).dropdown('toggle');
					$(cid).fadeOut(500);
				});
				return false;
			};

		//gets the DownloadCount after a given time
		var dlcountfun = function() {
			setTimeout(function() {
				$.getJSON('/api/dlcount', toSentData, function(data) {
					$(dlcountid).text(data.response.dl_count);
				});
			}, 50);
		};

		//Requests a Public URL
		$(createpubid).bind('click', create_public);

		//Unpublishs a Public URL
		$(unpubid).bind('click', unpublish);

		//Publishes a Public URL
		$(pubid).bind('click', publish);

		//Deletes a File from the Server
		$(deleteid).bind('click', deletefun);

		//Requests the Download count, shortly after a download has been made
		$(linkid).bind('click', dlcountfun);

};

$(function() {
	$(".file-element").each(fileelementfun);
});
