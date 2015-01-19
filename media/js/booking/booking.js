function checkDate($, url, date, hour, length, location){
    $.ajax({
	url: url,
	responseType: 'text/html',
	type: 'POST',
	data: {"date":date, "hour":hour, "length":length ,"location":location, },
	response: {},
	success: function(response, isSuccess) {
	    if (response == "true"){
		$("#booking-submit").removeAttr("disabled");
	    }else{
		$("#booking-submit").attr("disabled", "disabled");
	    }
	}
    });
}
