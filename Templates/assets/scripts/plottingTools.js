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
    // Add an API function for drawing the graph based on a table
    var wrapper = function(x,y) {
      x = x ? x.toString() : '';
      y = y ? y.toString() : '';
      return interpreter.createPrimitive(myplot.drawScatterGraphFromTable(x,y));
    };
    interpreter.setProperty(scope, 'drawBarGraphFromTable', interpreter.createNativeFunction(wrapper));
    // Add an API function for drawing the graph based on a table
    var wrapper = function(x,y) {
      x = x ? x.toString() : '';
      y = y ? y.toString() : '';
      return interpreter.createPrimitive(myplot.drawBarGraphFromTable(x,y));
    };
    interpreter.setProperty(scope, 'drawBarGraphFromTable', interpreter.createNativeFunction(wrapper));
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

    this.drawScatterGraphFromTable = function( x, y ) {
      var xnums = x.split(','); var ynums = y.split(',');
      // Check that the lengths of the input vectors are the same
      if( xnums.length!=ynums.length ){ alert("mismatch between number of items in x and y input lists"); return; }
      // Make sure the data table is empty
      this.data.length = 0; this.data.unshift(['x', 'y'], [0, 0]);
      // Add all data to data table 
      for(var i=0; i<xnums.length; i++ ){ this.data.push([xnums[i], ynums[i]]); } 
      // And plot the data
      this.plotGraph('graph','scatter'); 
    };

    this.drawBarGraphFromTable = function( x, y ) {
      var xnums = x.split(','); var ynums = y.split(',');
      // Check that the lengths of the input vectors are the same
      if( xnums.length!=ynums.length ){ alert("mismatch between number of items in x and y input lists"); return; }
      // Make sure the data table is empty
      this.data.length = 0; this.data.unshift(['x', 'y'], [0, 0]);
      // Add all data to data table 
      for(var i=0; i<xnums.length; i++ ){ this.data.push([xnums[i], ynums[i]]); }
      // And plot the data
      this.plotGraph('graph','column');
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

// Define a custom block to draw a graph based on a table
Blockly.Blocks["draw_list"] = {
  // take input and plot it on y
  init: function() {
    this.jsonInit({
      "message0": "plot table with x = %1",
      "args0": [
        {
          "type": "input_value",
          "name": "X",
          "check": "Array"
        }
      ],
      "message1": " and y = %1",
      "args1": [
        {
         "type": "input_value",
         "name": "Y",
         "check": "Array"
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

Blockly.JavaScript['draw_list'] = function(block) {
  var x = Blockly.JavaScript.valueToCode(block, 'X', Blockly.JavaScript.ORDER_ATOMIC) || '0';
  var y = Blockly.JavaScript.valueToCode(block, 'Y', Blockly.JavaScript.ORDER_ATOMIC) || '0';
  var code = 'drawScatterGraphFromTable(' + x + ', ' + y + ');\n';
  return code;
};

Blockly.Python['draw_list'] = function(block) {
  var x = Blockly.Python.valueToCode(block, 'X', Blockly.Python.ORDER_ATOMIC) || '0';
  var y = Blockly.Python.valueToCode(block, 'Y', Blockly.Python.ORDER_ATOMIC) || '0';
  var code = 'matplotlib.pyplot.plot(' + x + ', ' + y + ')\nmatplotlib.pyplot.show()';
  return code;
};

// Define a custom block to draw a bar chart based on a table
Blockly.Blocks["draw_bar_chart"] = {
  // take input and plot it on y
  init: function() {
    this.jsonInit({
      "message0": "plot bar chart with x = %1",
      "args0": [
        {
          "type": "input_value",
          "name": "X",
          "check": "Array"
        }
      ],
      "message1": " and y = %1",
      "args1": [
        {
         "type": "input_value",
         "name": "Y",
         "check": "Array"
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

Blockly.JavaScript['draw_bar_chart'] = function(block) {
  var x = Blockly.JavaScript.valueToCode(block, 'X', Blockly.JavaScript.ORDER_ATOMIC) || '0';
  var y = Blockly.JavaScript.valueToCode(block, 'Y', Blockly.JavaScript.ORDER_ATOMIC) || '0';
  var code = 'drawBarGraphFromTable(' + x + ', ' + y + ');\n';
  return code;
};

Blockly.Python['draw_bar_chart'] = function(block) {
  var x = Blockly.Python.valueToCode(block, 'X', Blockly.Python.ORDER_ATOMIC) || '0';
  var y = Blockly.Python.valueToCode(block, 'Y', Blockly.Python.ORDER_ATOMIC) || '0';
  var code = 'matplotlib.pyplot.bar(' + x + ', ' + y + ', 0.4 )\nmatplotlib.pyplot.show()';
  return code;
};
