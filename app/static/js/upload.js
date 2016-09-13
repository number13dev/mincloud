$(function () {

    var csrftoken = $('meta[name=csrf-token]').attr('content');

    $('#fileupload').fileupload({
        dataType: 'json',
        formData: {'csrf_token': csrftoken},
        add: function(e, data) {
            data.submit();
        },
        dropZone: $('#dropzone'),
        done: function (e, data) {
            $.each(data.result.files, function (index, file) {
                $("#files-table").find('tbody')
                    .append($('<tr>')
                    .append($('<td>')
                        .append($('<a>')
                        .attr('href', file.url)
                        .text(file.name)
                        )
                    )
                    .append($('<td>')
                        .text(file.error
                        )
                    )
                );
            });
		    setTimeout(function() {
				$('#progress .progress-bar').css('width',0);
			}, 1500);
        },
        progressall: function (e, data) {
            var progress = parseInt(data.loaded / data.total * 100, 10);
            $('#progress .progress-bar').css(
                'width',
                progress + '%'
            );
        }
    }).prop('disabled', !$.support.fileInput)
        .parent().addClass($.support.fileInput ? undefined : 'disabled');
});
