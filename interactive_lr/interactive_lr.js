var body = document.getElementsByTagName('body')[0];
var data = [];
var b0=0, b1=1;
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

function drawCoordinatesAndRegressionLine(canvas) {
    b0=0;
    b1=0;
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
        // linearRegression();
        gradientDescent();
        // console.log(params);
        regressionLineContext = drawRegressionLine(canvas);    
    }
    return;
}

// Why Gradient Descent ? : The formula for b1 and b0 looks very simple, even computationally, because it only works for **univariate case**, i.e. when you have only one variable. In the multivariate case, when you have many variables, the formulae is slightly more complicated on paper and requires much more calculations when you implement it in software
// gradientDescent starts with assuming values for slopes and constant and then tweak these values based on errors in actual and predicted (using guess)
function gradientDescent() {
    var learningRate = 0.02;
    for(var i = 0; i<data.length; i++) {
        var x = data[i][0];
        var y = data[i][1];
        
        var guess = b1*x + b0;
        console.log("y: ", y, "guess: ", guess);
        // why not square error ? cuz we are required to tune b1 and b0 according to positive and negative errors
        var error = y - guess;
        // console.log(error);
        b1 = b1 + error*(x/canvas.width)*learningRate;
        b0 = b0 + error*learningRate;
    }
}

// b1 = sum((xi-xmean)*(yi-ymean)) / sum((xi-xmean)*(xi-xmean))
// b0 = ymean - b1*xmean
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
    
    b1 = numerator / denominator;
    b0 = ymean - b1*xmean;
}

function drawRegressionLine(canvas) {
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