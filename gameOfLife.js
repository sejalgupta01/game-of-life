function mod(n, m) {
    return ((n % m) + m) % m;
}

function printGrid(grid){
    var row ="";
    for (var i=0; i<gridBreadth; i++){
        for (var j=0; j<gridLength; j++){
            row += grid[i][j] + " ";
        }
        row += "\n";
    }
    console.log(row);
}

function getNextGen(grid){
    newGrid = JSON.parse(JSON.stringify(grid));
    for (var i=0; i<gridBreadth; i++){
        for (var j=0; j<gridLength; j++){
            var neighbours = grid[mod(i-1, gridBreadth)][mod(j-1, gridLength)] + grid[mod(i-1, gridBreadth)][mod(j+1, gridLength)];
            neighbours += grid[mod(i+1, gridBreadth)][mod(j-1, gridLength)] + grid[mod(i+1, gridBreadth)][mod(j+1, gridLength)];
            neighbours += grid[i][mod(j-1, gridLength)] + grid[i][mod(j+1, gridLength)];
            neighbours += grid[mod(i-1, gridBreadth)][j] + grid[mod(i+1, gridBreadth)][j];
            if (neighbours < 2){
                newGrid[i][j] = 0;
            }
            else if (neighbours > 3) {
                newGrid[i][j] = 0;
            }
            else if (neighbours == 3) {
                newGrid[i][j] = 1;
            }
        }
    }
    return newGrid;
}

var gridLength = 5;
var gridBreadth = 5;
var grid = [[1,0,1,1,0], [0,0,0,1,1], [1,1,1,0,0], [0,0,0,0,1], [0,0,0,0,0]];
var numberOfGens = 5;

printGrid(grid);

for(var i=0; i<numberOfGens; i++){
    grid = getNextGen(grid);
    printGrid(grid);
}