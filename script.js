var DEFAULT_ROWS = 10;
var DEFAULT_COLS = 12;
var cellSize;
var rows = DEFAULT_ROWS;
var cols = DEFAULT_COLS;
var clickable = [];
var filledArray = new Array(cols * rows).fill(0);

document.addEventListener('DOMContentLoaded',
    function (event) {
        var canvasElement = gameGrid.getContext("2d");

        document.getElementById("width").value = DEFAULT_COLS;
        document.getElementById("height").value = DEFAULT_ROWS;

        setCanvasSize(DEFAULT_ROWS, DEFAULT_COLS, document.documentElement.clientWidth, document.documentElement.clientHeight);

        var canvasWidth = gameGrid.width;
        var canvasHeight = gameGrid.height;

        cellSize = canvasWidth / DEFAULT_COLS;

        createCanvas(canvasElement);

        gameGrid.addEventListener("click", (evt) => {
            var mousePos = getMousePos(gameGrid, evt);
            
            for(let i = 0; i < clickable.length; i++){
                var cell =  clickable[i];
              
                canvasElement.beginPath();
                canvasElement.rect(cell.rect.x, cell.rect.y, cellSize, cellSize);
                if (canvasElement.isPointInPath(mousePos.x, mousePos.y)){
                    var rect =  cell.rect;
                    canvasElement.beginPath();
                    if (filledArray[i] == 0) {
                        canvasElement.fillStyle = "red";
                        canvasElement.fillRect(rect.x, rect.y, rect.w, rect.h);
                        canvasElement.strokeRect(rect.x, rect.y, rect.w, rect.h);
                        filledArray[i] = 1;
                    }
                    else {
                        canvasElement.clearRect(rect.x, rect.y, rect.w, rect.h);
                        canvasElement.strokeRect(rect.x, rect.y, cellSize, cellSize);
                        filledArray[i] = 0;
                    }
                    break;
                }         
            }
        });
        generate.addEventListener("click", function() {
            grid = new Array(rows);
            for (var i=0; i<rows; i++) { 
                row = new Array(cols);
                for (var j=0; j<cols; j++) {
                    row[j] = filledArray[i * cols + j];
                }
                grid[i] = row;
            }
            var newGrid = getNextGen(grid);
            for (var i=0; i<rows; i++) {
                for (var j=0; j<cols; j++) {
                    filledArray[i * cols + j] = newGrid[i][j];
                }
            }
            fillGrid(filledArray, clickable, canvasElement);
        });
        width.addEventListener("change", function() {
            cols = document.getElementById("width").value;
            filledArray = new Array(cols * rows).fill(0);

            setCanvasSize(rows, cols, document.documentElement.clientWidth, document.documentElement.clientHeight);

            var canvasWidth = gameGrid.width;
            var canvasHeight = gameGrid.height;

            cellSize = canvasWidth / cols;

            clickable = [];

            createCanvas(canvasElement);
        });
        height.addEventListener("change", function() {
            rows = document.getElementById("height").value;
            filledArray = new Array(cols * rows).fill(0);

            setCanvasSize(rows, cols, document.documentElement.clientWidth, document.documentElement.clientHeight);

            var canvasWidth = gameGrid.width;
            var canvasHeight = gameGrid.height;

            cellSize = canvasWidth / cols;

            clickable = [];

            createCanvas(canvasElement);
        })
    }
);

function getMousePos(canvas, evt) {
    var ClientRect = canvas.getBoundingClientRect();
    return { 
        x: Math.round(evt.clientX - ClientRect.left),
        y: Math.round(evt.clientY - ClientRect.top)
    };
}

function fillGrid(filledArray, clickable, ctx) {
    for (var i=0; i<filledArray.length; i++) {
        var rect = clickable[i].rect;
        ctx.beginPath();
        if (filledArray[i] == 1) {
            ctx.fillStyle = "red";
            ctx.fillRect(rect.x, rect.y, rect.w, rect.h);
            ctx.strokeRect(rect.x, rect.y, rect.w, rect.h);
        }
        else {
            ctx.clearRect(rect.x, rect.y, rect.w, rect.h);
            ctx.strokeRect(rect.x, rect.y, rect.w, rect.h);
        }
    }
}

function setCanvasSize(r, c, windowWidth, windowHeight) {
    var usableWidth = 0.95 * windowWidth;
    var usableHeight = 0.8 * windowHeight;
    var cellSize = Math.min(usableWidth / c, usableHeight / r);
    gameGrid.style.width = (cellSize * c).toString() + "px";
    gameGrid.style.height = (cellSize * r).toString() + "px";
    gameGrid.width  = gameGrid.offsetWidth;
    gameGrid.height = gameGrid.offsetHeight;
}

function createCanvas(canvasElement){
    for (var i=0; i<rows; i++){
        for (var j=0; j<cols; j++){
            clickable.push(
                {index: i * cols + j, 
                rect: {
                    x: j * cellSize,
                    y: i * cellSize,
                    w: cellSize,
                    h: cellSize
                }});
        }
    }
    clickable.forEach(cell => {
        canvasElement.beginPath();
        canvasElement.strokeRect(cell.rect.x, cell.rect.y, cellSize, cellSize);
    });
}