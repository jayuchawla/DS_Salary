var body = document.getElementsByTagName('body')[0];
var data = [];
var regressionLineContext = null;

function setup() {
    var canvas = document.createElement('canvas');
    canvas.id = 'canvas';
    canvas.width = 400;
    canvas.height = 400;
    canvas.style.zIndex = 8;
    canvas.style.position = 'absolute';
    canvas.style.border = '1px solid black';
    canvas.style.backgroundColor = 'rgb(40,40,40)';
    canvas.style.margin = '10px';
    body.appendChild(canvas);
    return canvas;
}

function markPoint(event, canvas) {
    var rect = canvas.getBoundingClientRect();
    // console.log(event);
    var x = event.clientX - rect.left; 
    var y = event.clientY - rect.top;
    data.push([x,y]);
    // console.log(point);
    drawCoordinatesAndRegressionLine(canvas);
}

function linearRegression() {
    var xsum = 0;
    var ysum = 0;
    for(var i = 0; i<data.length; i++) {
        xsum += data[i][0];
        ysum += data[i][1];
    }
    var xmean = xsum / data.length;
    var ymean = ysum / data.length;

    var numerator = 0;
    var denominator = 0;
    for(var i = 0; i<data.length; i++) {
        numerator += ((data[i][0] - xmean) * (data[i][1] - ymean));
        denominator += ((data[i][0] - xmean) * (data[i][0] - xmean));
    }
    
    var b1 = numerator / denominator;
    var b0 = ymean - b1*xmean;
    return [b0,b1];
}

function drawCoordinatesAndRegressionLine(canvas) {
    if(regressionLineContext) {
        regressionLineContext.clearRect(0, 0, canvas.width, canvas.height);
    }
    for(var i = 0; i<data.length; i++) {
        var context = canvas.getContext('2d');
        // console.log(context);
        context.fillStyle = '#ffffff';
        context.beginPath();
        context.arc(data[i][0], data[i][1], 3, 0, Math.PI*2, true);
        context.fill();    
    }
    if(data.length > 1) {
        var params = linearRegression();
        regressionLineContext = drawRegressionLine(params[0], params[1], canvas);    
    }
    return;
}

function drawRegressionLine(b0, b1, canvas) {
    var x1 = 0;
    var y1 = b1*x1 + b0;
    var x2 = canvas.width;
    var y2 = b1*x2 + b0;

    var context = canvas.getContext('2d');
    context.strokeStyle = '#87ceeb';
    context.lineWidth = 1;
    context.beginPath();
    context.moveTo(x1,y1);
    context.lineTo(x2,y2);
    context.stroke();
    return context;
}

var canvas = setup();
// console.log(canvas);
canvas.addEventListener('click', (event) => markPoint(event, canvas));