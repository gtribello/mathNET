'use strict'

var myplot = new plotter();

function addGraphFunctionsToApi( interpreter, scope ){
    // Add an API function for updating the graph when there is new data
    var wrapper = function(x,y) {
      x = x ? x.toString() : '';
      y = y ? y.toString() : '';
      return interpreter.createPrimitive(myplot.addDataToGraph(x,y));
    };
    interpreter.setProperty(scope, 'addDataToGraph', interpreter.createNativeFunction(wrapper));
}

function plotter(){
    this.data = [];

    this.options_ = {
      //curveType: 'function',
      width: 400, height: 400,
      chartArea: {left: '10%', width: '85%', height: '85%'}
    };

    this.addDataToGraph = function( x, y ) {
      // Add data to the array containing the data
      this.data.push([x, y]); 
      // And plot the data
      this.plotGraph('graph','scatter');
    };

    this.plotGraph = function(div_id,gtype) {
      // Create the data table from the stored data.
      var data = google.visualization.arrayToDataTable(this.data);
      // Create and draw the visualization, passing in the data and options.
      if( gtype=='scatter' ){
         new google.visualization.ScatterChart(document.getElementById(div_id)).draw(data, this.options_);
      } else if( gtype=='column' ){
         new google.visualization.ColumnChart(document.getElementById(div_id)).draw(data, this.options_);
      } else if( gtype=='line' ){
         new google.visualization.LineChart(document.getElementById(div_id)).draw(data, this.options_);
      }
    };
}

// Define a custom block to add data to the graph
Blockly.Blocks["draw_point"] = {
  // take input and plot it on y
  init: function() {
    this.jsonInit({
      "message0": "plot point at x = %1",
      "args0": [
        {
          "type": "input_value",     
          "name": "X"
        }
      ],
      "message1": " and y = %1",
      "args1": [
        {
         "type": "input_value",     
         "name": "Y"
        }
      ],
      "inputsInline": true,
      "nextStatement": null,
      "previousStatement": null,
      "colour": Blockly.Blocks.variables.HUE,
      "tooltip": Blockly.Msg.VARIABLES_SET_TOOLTIP,
      "helpUrl": Blockly.Msg.VARIABLES_SET_HELPURL
    });
  } 
};

Blockly.JavaScript['draw_point'] = function(block) {
  var x = Blockly.JavaScript.valueToCode(block, 'X', Blockly.JavaScript.ORDER_ATOMIC) || '0';
  var y = Blockly.JavaScript.valueToCode(block, 'Y', Blockly.JavaScript.ORDER_ATOMIC) || '0';
  var code = 'addDataToGraph(' + x + ', ' + y + ');\n';
  return code; 
};

Blockly.Python['draw_point'] = function(block) {
  var x = Blockly.Python.valueToCode(block, 'X', Blockly.Python.ORDER_ATOMIC) || '0';
  var y = Blockly.Python.valueToCode(block, 'Y', Blockly.Python.ORDER_ATOMIC) || '0';
  var code = 'addDataToGraph(' + x + ', ' + y + ')\n';
  return code;
};
