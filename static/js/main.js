jQuery(document).ready(function ($) {
	$("tbody>tr").click(function () {
		window.location = $(this).data("href");
	});

	$("#add").click(function () {
		$(".opac, .spinner").show();
		$.post("/api/tokens/", {address: $("#contract").val()})
			.fail(function () {
				$(".opac, .spinner").hide();
				$("#contract").addClass("is-invalid");
				$("#error").show();
			})
			.done(function (data) {
				$(".opac, .spinner").hide();
				$("#contract").addClass("is-valid");
				$("#error").hide();
				window.location.reload(false);
				/*var markup = "<tr data-href='/token/" + data.address + "'>";
				markup+= "<td></td>"
				markup+= "<td>"+data.name+"</td>"
				markup+= "<td>"+data.address+"</td>"
				markup+= "<td>Нет</td>"
				markup += "</tr>"
				$("#tokens tbody").append(markup)*/
			});

	});

	var ctx = $("#myChart");
	$("#update_volume").click(function () {

		$.get("/api/update_volumes/" + ctx.attr("data-pk") + "/").done(function (data) {

		});

	});
	function unpack(rows, key) {
		return rows.map(function (row) {
			return row[key];
		});
	}


	var row;
	if (ctx) {
		$.get("/api/volumes/" + ctx.attr("data-pk") + "/").done(function (data) {
			var data = [
				{
					x: unpack(data, 'date'),
					y: unpack(data, 'volume'),
					type: 'scatter'
				}
			];

			Plotly.plot(document.getElementById("myChart"), data);
		});
	}

});


