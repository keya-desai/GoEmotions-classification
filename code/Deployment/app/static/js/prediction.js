function addText(){

    sentence = d3.select("#sentence").property("value")



    checkOne = d3.select("#one").property("checked")

    if(checkOne){

        d3.json('get_prediction/' + sentence +'/' + 3, function(error, idx){

        const d = {'1' : "Positive", '2' : "Negative", '0' : "Neutral"}
        console.log(d[idx])
        emotion = d[idx]
        
        var text = textContainer1.selectAll("text").data(dummyData)
        text.enter()
            .append("text")
            .merge(text)
            .attr("x", function(d) { return 15; })
            .attr("y", function(d) { return 20; })
            .html(emotion)
            .attr("font-family", "sans-serif")
            .attr("font-size", "20px")
            .attr("fill", "black");  

        });
    }

    checkTwo = d3.select("#two").property("checked")

    if(checkTwo){

        d3.json('get_prediction/' + sentence +'/' + 6, function(error, idx){

        const d = {'0' : "Joy", '1' : "Neutral", '2' : "Anger", 
                '3': "Surprise", '4' : "Sadness", '5' : "Fear"}
        console.log(d[idx])
        emotion = d[idx]
        
        var text = textContainer1.selectAll("text").data(dummyData)
        text.enter()
            .append("text")
            .merge(text)
            .attr("x", function(d) { return 15; })
            .attr("y", function(d) { return 20; })
            .html(emotion)
            .attr("font-family", "sans-serif")
            .attr("font-size", "20px")
            .attr("fill", "black");  

        });
    }

    checkThree = d3.select("#three").property("checked")

    if(checkThree){

        d3.json('get_prediction/' + sentence +'/' + 15, function(error, idx){

        const d = {'0' : 'Admiration/ Desire', '1' : 'Disapproval/ Disgust/ Disappointment/ Embarrasement', '2' : "Anger/ Annoyance", 
                '3': "Excitement/ Amusement", '4' : "Love/ Caring", '5' : "Approval", '6' : "Gratitude", '7' : "Curiosity", 
                '8' : "Sadness/ Grief/ Remorse", '9' : "Joy/ Pride/ Relief", '10' : "Optimism", '11' : "Confusion", '12' : "Realization", 
                '13' : "Surprise", '14' : "Fear/ Nervousness"}
        console.log(d[idx])
        emotion = d[idx]
        
        var text = textContainer1.selectAll("text").data(dummyData)
        text.enter()
            .append("text")
            .merge(text)
            .attr("x", function(d) { return 15; })
            .attr("y", function(d) { return 20; })
            .html(emotion)
            .attr("font-family", "sans-serif")
            .attr("font-size", "20px")
            .attr("fill", "black");  

        });
    }

    

}

var dummyData = "dummy"
var width_text = d3.select('#text1').node().getBoundingClientRect().width,
    height_text = d3.select('#text1').node().getBoundingClientRect().height;
    textContainer1 = d3.select("#text1")
                        .append("svg")
                        .attr("width", width_text)
                        .attr("height", height_text);

function updateText(){
    textContainer1.selectAll("text").exit().remove();
    addText()
}

var checkbox = d3.select("#submit")
                .on("click", updateText);
console.log("In prediction.js")
