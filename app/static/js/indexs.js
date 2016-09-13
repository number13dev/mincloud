$(function() {
console.log("entry...");

$(".file-element").each( function() {
    console.log($(this))

    var hash = "#";
    var formd = "form-";
    var id = $('input[name="uniqueid"]', this).val();
    var cid = hash.concat(id);
    var codo = formd.concat(id);
    var fid = hash.concat(codo);

    console.log("variables: fid:"+fid+" id:"+id);

    $(fid).submit(function(e) {
        console.log("other form xD tohide:" + cid);
        $.getJSON('/delete', {
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