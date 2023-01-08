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

		d3.json("/query-ctx/" + src + "/" + tgt + "/" + word)
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
						var sim = +d['sim'];
						var colorStr = d3.interpolateReds(sim); 
						return colorStr.replace("rgb", "rgba").replace(")", ", " + (sim*0.8) + ")");
					});*/

				srcLi.append("span")
					.classed("badge text-bg-success", true)
					.text(function(d){ return d['word']; });
				/*
				srcLi.append("span")
					.classed("mx-3 px-2", true)
					.classed("text-bg-light", true)
					.text(function(d){ return d['sim'].toFixed(4); });
				*/
				srcLi.append("ul").selectAll("li")
					.data(function(d){ 
						var d_ctx = d['ctx'];
						d_ctx.forEach(function(ctx){
							ctx['sim_word'] = d['word'];
						});
						return d_ctx;
					})
					.enter()
					.append("li")
					.append("span")
					.html(function(d){
						var w = d['sim_word'];
						return d['sent'].split(w).join("<mark>" + w + "</mark>");
					});//FIXME better word matching

				d3.select("#src-result-card").classed("invisible", false);

				/* *_[t] most similar to word_[t] */
				d3.select("#word-in-tgt").text(response["word"])
				d3.select("#tgt-community").text(tgtName);

				var tgtLi = d3.select("#tgt-list").selectAll("li")
					.data(response['tgt_sim'])
					.enter()
					.append("li")
					.classed("list-group-item m-1", true);
					/*.style("background-color", function(d){ 
						var colorStr = d3.interpolateReds(+d['sim']); 
						return colorStr.replace("rgb", "rgba").replace(")", ", 0.6)");
					});*/
				tgtLi.append("span")
					.classed("badge text-bg-primary", true)
					.text(function(d){ return d['word']; });
				/*
				tgtLi.append("span")
					.classed("mx-3 px-2", true)
					.classed("text-bg-light", true)
					.text(function(d){ return d['sim'].toFixed(4); });
				*/
				tgtLi.append("ul").selectAll("li")
					.data(function(d){ 
						var d_ctx = d['ctx'];
						d_ctx.forEach(function(ctx){
							ctx['sim_word'] = d['word'];
						});
						return d_ctx;
					})
					.enter()
					.append("li")
					.append("span")
					.html(function(d){
						var w = d['sim_word'];
						return d['sent'].split(w).join("<mark>" + w + "</mark>");
					});

				d3.select("#tgt-result-card").classed("invisible", false);

				/* *_[t] most similar to word_[s] */
				d3.select("#word-in-cross").text(response["word"])
				d3.select("#tgt-community-cross").text(tgtName);

				var xLi = d3.select("#cross-list").selectAll("li")
					.data(response['cross_sim'])
					.enter()
					.append("li")
					.classed("list-group-item m-1", true);
					/*.style("background-color", function(d){ 
						var colorStr = d3.interpolateReds(+d['sim']); 
						return colorStr.replace("rgb", "rgba").replace(")", ", 0.6)");
					});*/
				xLi.append("span")
					.classed("badge text-bg-primary", true)
					.text(function(d){ return d['word']; });
				/*
				xLi.append("span")
					.classed("mx-3 px-2", true)
					.classed("text-bg-light", true)
					.text(function(d){ return d['sim'].toFixed(4); });
				*/
				xLi.append("ul").selectAll("li")
					.data(function(d){ 
						var d_ctx = d['ctx'];
						d_ctx.forEach(function(ctx){
							ctx['sim_word'] = d['word'];
						});
						return d_ctx;
					})
					.enter()
					.append("li")
					.append("span")
					.html(function(d){
						var w = d['sim_word'];
						return d['sent'].split(w).join("<mark>" + w + "</mark>");
					});

				/* self similarity & rank */
				d3.select("#self-src-word-span").text(response["word"])
				d3.select("#self-tgt-word-span").text(response["word"])
				d3.select("#self-rank-span").text((+response["self_rank"])+1)
				d3.select("#self-sim-span").text(response["self_sim"].toFixed(4))

				d3.select("#cross-result-card").classed("invisible", false);
			});
	});