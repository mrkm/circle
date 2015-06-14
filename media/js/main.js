function alert(level, message){
    var element = $('#alert');
    element.html("");
    $("<div/>", {"class":"flash-"+level, text:message}).appendTo(element);
    element.show();
    setTimeout(function(){return $('#alert').fadeOut()}, 5000);
}
