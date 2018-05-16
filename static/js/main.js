jQuery(document).ready(function ($) {
	$("tbody>tr").click(function () {
		window.location = $(this).data("href");
	});

	$("#add").click(function () {
		$(".opac, .spinner").show();
		$.post("/api/tokens/", {contract: $("#contract").val()})
			.fail(function () {
				$(".opac, .spinner").hide();
			})
			.done(function (data) {
				$(".opac, .spinner").hide();
			});

	});
	var ctx = document.getElementById("myChart");
	var scatterChart = new Chart(ctx, {
		type: 'scatter',
		data: {
			datasets: [{
				label: 'Scatter Dataset',
				data: [{
					x: -10,
					y: 0
				}, {
					x: 0,
					y: 10
				}, {
					x: 10,
					y: 5
				}]
			}]
		},
		options: {
			scales: {
				xAxes: [{
					type: 'linear',
					position: 'bottom'
				}]
			}
		}
	});
});


