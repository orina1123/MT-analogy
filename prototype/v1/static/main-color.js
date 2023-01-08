/*d3.select("input").on("keyup", function(e){
	if(e.which === 13) {
		e.preventDefault();
		d3.select("#query-button").click();	
	}
});*/

d3.select("#query-button").on("click", 
	function(){ 
		//console.log("click"); 
		var srcSelect = d3.select("#src-select").node();
		var src = srcSelect.options[srcSelect.selectedIndex].value;
		var srcName = srcSelect.options[srcSelect.selectedIndex].text;
		var tgtSelect = d3.select("#tgt-select").node();
		var tgt = tgtSelect.options[tgtSelect.selectedIndex].value;
		var tgtName = tgtSelect.options[tgtSelect.selectedIndex].text;
		var word = d3.select("#query-word-input").node().value;
		console.log(src, tgt, word);

		/*** clear elements & hide ***/
		d3.select("#src-list").selectAll("*").remove();
		d3.select("#tgt-list").selectAll("*").remove();
		d3.select("#cross-list").selectAll("*").remove();
		d3.select("#src-result-card").classed("invisible", true);
		d3.select("#tgt-result-card").classed("invisible", true);
		d3.select("#cross-result-card").classed("invisible", true);
		//TODO loading spinner

		//d3.json("http://localhost:5000/psy2eng_fixation.json")
		//d3.json("/query/psy/eng/examples")
		d3.json("/query/" + src + "/" + tgt + "/" + word)
			.then(function(response){
				console.log(response);

				/* *_[s] most similar to word_[s] */
				d3.select("#word-in-src").text(response["word"]);
				d3.select("#src-community").text(srcName);

				var srcLi = d3.select("#src-list").selectAll("li")
					.data(response['src_sim'])
					.enter()
					.append("li")
					.classed("list-group-item m-1", true);
					/*.style("background-color", function(d){ 
						var sim = +d[1];
						var colorStr = d3.interpolateReds(sim); 
						return colorStr.replace("rgb", "rgba").replace(")", ", " + (sim*0.8) + ")");
					});*/

				srcLi.append("span")
					.classed("badge text-bg-success", true)
					.text(function(d){ return d[0]; });
				/*
				srcLi.append("span")
					.classed("mx-3 px-2", true)
					.classed("text-bg-light", true)
					.text(function(d){ return d[1].toFixed(4); });
				*/
				srcLi.append("div").classed("progress my-1", true).style("width", "50%")/*.style("display", "inline-block").style("float", "right")*/
					.append("div").classed("progress-bar", true).attr("role", "progressbar")
					.style("width", d => d[1]*100 + "%")
					.style("aria-valuenow", d => d[1]*100).style("aria-valuemin", "0").style("aria-valuemax", "100")
					.style("background-color", d => d3.interpolateReds(+d[1]).replace("rgb", "rgba").replace(")", ", 0.7"));

				d3.select("#src-result-card").classed("invisible", false);

				/* *_[t] most similar to word_[t] */
				d3.select("#word-in-tgt").text(response["word"]);
				d3.select("#tgt-community").text(tgtName);

				var tgtLi = d3.select("#tgt-list").selectAll("li")
					.data(response['tgt_sim'])
					.enter()
					.append("li")
					.classed("list-group-item m-1", true);
					/*.style("background-color", function(d){ 
						var colorStr = d3.interpolateReds(+d[1]); 
						return colorStr.replace("rgb", "rgba").replace(")", ", 0.6)");
					});*/
				tgtLi.append("span")
					.classed("badge text-bg-primary", true)
					.text(function(d){ return d[0]; });
				/*
				tgtLi.append("span")
					.classed("mx-3 px-2", true)
					.classed("text-bg-light", true)
					.text(function(d){ return d[1].toFixed(4); });
				*/
				tgtLi.append("div").classed("progress my-1", true).style("width", "50%")/*.style("display", "inline-block").style("float", "right")*/
					.append("div").classed("progress-bar", true).attr("role", "progressbar")
					.style("width", d => d[1]*100 + "%")
					.style("aria-valuenow", d => d[1]*100).style("aria-valuemin", "0").style("aria-valuemax", "100")
					.style("background-color", d => d3.interpolateReds(+d[1]).replace("rgb", "rgba").replace(")", ", 0.7"));

				d3.select("#tgt-result-card").classed("invisible", false);

				/* *_[t] most similar to word_[s] */
				d3.select("#word-in-cross").text(response["word"]);
				d3.select("#tgt-community-cross").text(tgtName);

				var xLi = d3.select("#cross-list").selectAll("li")
					.data(response['cross_sim'])
					.enter()
					.append("li")
					.classed("list-group-item m-1", true);
					/*.style("background-color", function(d){ 
						var colorStr = d3.interpolateReds(+d[1]); 
						return colorStr.replace("rgb", "rgba").replace(")", ", 0.6)");
					});*/
				xLi.append("span")
					.classed("badge text-bg-primary", true)
					.text(function(d){ return d[0]; });
				/*
				xLi.append("span")
					.classed("mx-3 px-2", true)
					.classed("text-bg-light", true)
					.text(function(d){ return d[1].toFixed(4); });
				*/
				xLi.append("div").classed("progress my-1", true).style("width", "50%")/*.style("display", "inline-block").style("float", "right")*/
					.append("div").classed("progress-bar", true).attr("role", "progressbar")
					.style("width", d => d[1]*100 + "%")
					.style("aria-valuenow", d => d[1]*100).style("aria-valuemin", "0").style("aria-valuemax", "100")
					.style("background-color", d => d3.interpolateReds(+d[1]).replace("rgb", "rgba").replace(")", ", 0.7"));

				/* self similarity & rank */
				d3.select("#self-src-word-span").text(response["word"])
				d3.select("#self-tgt-word-span").text(response["word"])
				d3.select("#self-rank-span").text((+response["self_rank"])+1)
				/*
				d3.select("#self-sim-span").text(response["self_sim"].toFixed(4))
				*/

				d3.select("#cross-result-card").classed("invisible", false);
			});
	});